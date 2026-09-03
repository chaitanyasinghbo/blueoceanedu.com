# The morning analytics email

What the scheduled cloud agent does every morning. The routine's own prompt is
three lines and points here, so the procedure is version-controlled rather than
buried in a scheduler field. The one thing that is **not** here is the PostHog
Personal API key, which the routine carries, because this repository is public.

Work through these in order.

## 1. The key

The routine's prompt carries the Personal API key. If it is still the literal
placeholder text, PostHog has not been set up yet.

**Send no email.** Stop, and say in the final message that the key is still a
placeholder. Do not hunt for the key elsewhere, do not substitute another data
source, and do not send an email with no numbers in it. A daily email that says
nothing is how a daily email stops being read.

## 2. Run the report

From the repository root:

```
POSTHOG_PERSONAL_API_KEY='<the key from the prompt>' \
POSTHOG_REGION=us \
python3 tools/posthog-daily.py
```

The script covers the previous calendar day in `Asia/Kolkata`, the day boundary
this business runs on. **Do not pass `--date` or `--tz`.**

If `us` gives an authentication error, try `eu` once before calling it a
failure. The project lives on one cloud or the other and the key only works
against its own.

If the script exits non-zero, do not send a formatted report. Send one short
email to `admissions@blueoceanedu.com`, subject `Blue Ocean analytics: report
failed`, with the error text in the body. A failure that is visible gets fixed;
a silent one does not.

## 3. Send it

Gmail. To `admissions@blueoceanedu.com`. Subject `Blue Ocean analytics, <the
date the report names>`.

Body: the script's output **verbatim and unchanged**, then two or three
sentences of your own reading noting only what actually stands out. A metric
well off its seven-day average, a jump in rage clicks, a form taking leads but
producing no bookings, a campaign whose traffic is not converting.

If nothing stands out, say so in one line. Do not manufacture significance out
of a quiet day, and do not restate figures the reader can already see directly
above.

## What not to do

Do not edit any file in this repository, do not commit, do not open a pull
request. The email and the final message are the only outputs.
