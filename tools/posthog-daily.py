#!/usr/bin/env python3
"""Yesterday's PostHog numbers, as plain text, for the 8am email.

    export POSTHOG_PERSONAL_API_KEY=phx_...
    python3 tools/posthog-daily.py

The key is a **Personal API key**, not the `phc_` project key in
posthog-init.js. They are different things: the project key is publishable and
can only write events, this one reads the whole project back out. It must never
be committed, never appear in a page, and should be created read-only and
scoped to this project alone.

    PostHog -> your avatar -> Personal API keys -> Create key
    Scopes: read on `query`, `project`. Nothing else is needed.

Options, all optional:

    --date 2026-09-02   report on this day instead of yesterday
    --tz Asia/Kolkata   the timezone "yesterday" and the day boundaries mean
    --json              the raw figures, for a caller that wants to format
                        them itself

    POSTHOG_REGION      us (default) or eu, matching posthog-init.js
    POSTHOG_PROJECT_ID  skips the lookup; resolved from the key if unset

Every query is run independently and a failing one prints as unavailable
rather than taking the report down with it. A morning report that is missing
one line is worth having; a morning with no report is not.
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime, timedelta

try:
    from zoneinfo import ZoneInfo
except ImportError:                                   # Python 3.8 and older
    sys.exit("posthog-daily: needs Python 3.9 or newer for zoneinfo")

HOSTS = {"us": "https://us.posthog.com", "eu": "https://eu.posthog.com"}

TIMEOUT = 60


def die(msg):
    sys.exit("posthog-daily: " + msg)


def api(host, key, path, payload=None):
    url = host.rstrip("/") + path
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(
        url, data=data,
        headers={"Authorization": "Bearer " + key,
                 "Content-Type": "application/json"},
        method="POST" if data else "GET")
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")[:400]
        raise RuntimeError("HTTP %s from %s\n%s" % (e.code, url, body))


def query(host, key, project, sql, params):
    """One HogQL query. Returns a list of rows, each a list of values."""
    result = api(host, key, "/api/projects/%s/query/" % project,
                 {"query": {"kind": "HogQLQuery", "query": sql,
                            "values": params}})
    return result.get("results", [])


# ── The window ───────────────────────────────────────────────────────
# PostHog stores timestamps in UTC, so a "day" is only meaningful once a
# timezone is named. The families and the team are in India, so the default
# is Asia/Kolkata and not whatever the machine running this happens to be set
# to. A report whose day boundary moves with the operator is not comparable
# to yesterday's.

def window(day, tz):
    start = datetime(day.year, day.month, day.day, tzinfo=tz)
    return start, start + timedelta(days=1)


def iso(dt):
    return dt.astimezone(ZoneInfo("UTC")).strftime("%Y-%m-%dT%H:%M:%S")


# ── The questions ────────────────────────────────────────────────────
# Each is a name, the HogQL, and how many rows to show. `{start}` and `{end}`
# are HogQL placeholders bound from `values`, not string interpolation, so
# nothing here can be injected into.

TOTALS = """
SELECT
  countIf(event = '$pageview')                     AS pageviews,
  uniq(person_id)                                  AS visitors,
  uniq($session_id)                                AS sessions,
  countIf(event = 'lead_submitted')                AS leads,
  countIf(event = 'booking_completed')             AS bookings,
  countIf(event = '$rageclick')                    AS rageclicks
FROM events
WHERE timestamp >= {start} AND timestamp < {end}
"""

TOP_PAGES = """
SELECT concat(properties.$host, properties.$pathname) AS page,
       count()          AS views,
       uniq(person_id)  AS visitors
FROM events
WHERE event = '$pageview' AND timestamp >= {start} AND timestamp < {end}
GROUP BY page ORDER BY views DESC LIMIT 10
"""

REFERRERS = """
SELECT coalesce(nullIf(properties.$referring_domain, ''), '(direct)') AS source,
       uniq(person_id) AS visitors
FROM events
WHERE event = '$pageview' AND timestamp >= {start} AND timestamp < {end}
GROUP BY source ORDER BY visitors DESC LIMIT 8
"""

CAMPAIGNS = """
SELECT coalesce(nullIf(properties.utm_source, ''), '(none)')   AS utm_source,
       coalesce(nullIf(properties.utm_campaign, ''), '(none)') AS campaign,
       uniq(person_id) AS visitors
FROM events
WHERE event = '$pageview' AND timestamp >= {start} AND timestamp < {end}
  AND properties.utm_source != ''
GROUP BY utm_source, campaign ORDER BY visitors DESC LIMIT 8
"""

LEADS_BY_SOURCE = """
SELECT coalesce(nullIf(properties.lead_source, ''), 'unknown') AS form,
       countIf(event = 'lead_submitted')    AS leads,
       countIf(event = 'booking_completed') AS bookings
FROM events
WHERE event IN ('lead_submitted', 'booking_completed')
  AND timestamp >= {start} AND timestamp < {end}
GROUP BY form ORDER BY leads DESC
"""

# lp-v2 alone. The distribution of reasons is what says which condition is
# killing the most leads, and therefore what to change in the ad.
QUALIFICATION = """
SELECT event,
       coalesce(nullIf(properties.lead_reason, ''), '(none)') AS reason,
       count() AS n
FROM events
WHERE event IN ('target_lead', 'non_target_lead')
  AND timestamp >= {start} AND timestamp < {end}
GROUP BY event, reason ORDER BY n DESC
"""

SECTIONS = [
    ("Top pages",            TOP_PAGES,        ("page", "views", "visitors")),
    ("Where they came from", REFERRERS,        ("source", "visitors")),
    ("Campaigns",            CAMPAIGNS,        ("utm_source", "campaign", "visitors")),
    ("Forms",                LEADS_BY_SOURCE,  ("form", "leads", "bookings")),
    ("lp-v2 qualification",  QUALIFICATION,    ("event", "reason", "count")),
]


def safe(fn, default=None):
    """Run one query. A failure costs its own section and nothing else."""
    try:
        return fn(), None
    except Exception as err:                          # noqa: BLE001
        return default, str(err).strip().splitlines()[0]


def rate(numerator, denominator):
    if not denominator:
        return "n/a"
    return "%.1f%%" % (100.0 * numerator / denominator)


def delta(today, baseline):
    """Yesterday against the average of the seven days before it."""
    if baseline is None:
        return ""
    if not baseline:
        return "  (no traffic in the prior week)"
    change = 100.0 * (today - baseline) / baseline
    arrow = "up" if change >= 0 else "down"
    return "  (%s %.0f%% on the 7-day average of %.0f)" % (arrow, abs(change), baseline)


def table(rows, headers):
    if not rows:
        return ["  nothing recorded"]
    widths = [max(len(str(h)), max(len(str(r[i])) for r in rows))
              for i, h in enumerate(headers)]
    out = ["  " + "  ".join(str(h).ljust(widths[i]) for i, h in enumerate(headers))]
    out.append("  " + "  ".join("-" * w for w in widths))
    for r in rows:
        out.append("  " + "  ".join(str(v).ljust(widths[i]) for i, v in enumerate(r)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", help="YYYY-MM-DD, default yesterday")
    ap.add_argument("--tz", default=os.environ.get("POSTHOG_REPORT_TZ",
                                                   "Asia/Kolkata"))
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    key = os.environ.get("POSTHOG_PERSONAL_API_KEY", "").strip()
    if not key:
        die("POSTHOG_PERSONAL_API_KEY is not set. See the top of this file "
            "for which key it wants and how to make one.")

    region = os.environ.get("POSTHOG_REGION", "us").strip().lower()
    host = HOSTS.get(region)
    if not host:
        die("POSTHOG_REGION must be us or eu, got %r" % region)

    try:
        tz = ZoneInfo(args.tz)
    except Exception:
        die("unknown timezone %r" % args.tz)

    if args.date:
        try:
            day = datetime.strptime(args.date, "%Y-%m-%d").date()
        except ValueError:
            die("--date wants YYYY-MM-DD, got %r" % args.date)
    else:
        day = (datetime.now(tz) - timedelta(days=1)).date()

    project = os.environ.get("POSTHOG_PROJECT_ID", "").strip()
    if not project:
        try:
            project = str(api(host, key, "/api/projects/@current/")["id"])
        except Exception as err:                      # noqa: BLE001
            die("could not resolve the project from the key: %s" % err)

    start, end = window(day, tz)
    prior_start = start - timedelta(days=7)
    bounds = {"start": iso(start), "end": iso(end)}
    prior = {"start": iso(prior_start), "end": iso(start)}

    totals, totals_err = safe(
        lambda: query(host, key, project, TOTALS, bounds)[0])
    week, _ = safe(lambda: query(host, key, project, TOTALS, prior)[0])

    if totals_err:
        die("the totals query failed, so there is no report to send: %s"
            % totals_err)

    names = ["pageviews", "visitors", "sessions", "leads", "bookings",
             "rageclicks"]
    now = dict(zip(names, totals))
    avg = {k: (v / 7.0) for k, v in zip(names, week)} if week else {}

    sections = []
    for title, sql, headers in SECTIONS:
        rows, err = safe(lambda sql=sql: query(host, key, project, sql, bounds), [])
        sections.append((title, headers, rows, err))

    if args.json:
        print(json.dumps({
            "date": str(day), "timezone": args.tz, "project": project,
            "totals": now, "prior_week_daily_average": avg,
            "sections": {t: [list(r) for r in rows]
                         for t, _, rows, _ in sections},
        }, indent=2))
        return

    line = []
    line.append("Blue Ocean, %s (%s)" % (day.strftime("%A %-d %B %Y"), args.tz))
    line.append("=" * len(line[0]))
    line.append("")
    line.append("  visitors    %-6d%s" % (now["visitors"],
                                          delta(now["visitors"], avg.get("visitors"))))
    line.append("  pageviews   %-6d%s" % (now["pageviews"],
                                          delta(now["pageviews"], avg.get("pageviews"))))
    line.append("  sessions    %-6d" % now["sessions"])
    line.append("")
    line.append("  leads       %-6d%s" % (now["leads"],
                                          delta(now["leads"], avg.get("leads"))))
    line.append("  bookings    %-6d%s" % (now["bookings"],
                                          delta(now["bookings"], avg.get("bookings"))))
    line.append("")
    line.append("  visitor to lead     %s" % rate(now["leads"], now["visitors"]))
    line.append("  lead to booking     %s" % rate(now["bookings"], now["leads"]))
    line.append("  rage clicks         %d" % now["rageclicks"])

    for title, headers, rows, err in sections:
        line.append("")
        line.append(title)
        line.append("-" * len(title))
        if err:
            line.append("  unavailable: %s" % err)
        else:
            line.extend(table(rows, headers))

    line.append("")
    line.append("Session replays: %s/project/%s/replay" % (host, project))
    print("\n".join(line))


if __name__ == "__main__":
    main()
