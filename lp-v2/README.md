# lp-v2, the qualifying landing page

A dedicated landing page for Meta prospecting. It is **not** built by
`tools/build-landing-pages.py` and deliberately sits outside that pipeline,
because `lp/` and `iblp/` are "index.html with a different hero" and the whole
point of this page is that it is not the homepage.

Serve it at its own path or hostname. `next-steps.html` here is a copy of the
site one with the pixel patch described below.

## What is different from `lp/`, and why

| Change | Reason |
|---|---|
| **Student role removed.** The form opens with a required "I am the parent or legal guardian" checkbox. | `lp/` defaults the role button to **Student**. The ad copy also spoke to students. Together they were the largest source of unusable leads. |
| **Filter questions first, contact details last.** Grade and board on step 1, school on step 2, name, email and phone on step 3. | A family that does not fit drops out before a `Lead` event is paid for, and progressive disclosure raises completion on the ones that do fit. |
| **Price stated above the fold and again lower down.** | The cheapest quality filter available. Set `PRICE_FROM` in the page script. |
| **Criteria stated above the fold.** Grades 8 to 11, named boards. | Filters better than any targeting setting in Ads Manager. |
| **6x claim and the acceptance-rate table removed.** | One digit off Crimson's headline claim, and every row of the table is exactly 6.0x the published general rate, meaning it was derived rather than counted. Do not reinstate without the underlying application and admit counts. |
| **Right-fit block moved high**, with a cost line added. | It was the strongest writing on the site and it sat near the bottom. |
| **No navigation, no outbound links** except the privacy policy. | One page, one action. |
| **Self-contained and light.** 176 KB first load against roughly 1 MB before. | Pages under 1.5 seconds convert far better, and 65% of the traffic is a phone on mobile data. |
| **Scholarship reframed as an outcome**, not as a reason to click. | The old ad offered a ₹1 Cr scholarship, which recruits families who need funding rather than families who can pay. |

## The two files this page shares with the site

`lead-events.js` and `posthog-init.js` are copies of the root files, because
this folder is served self-contained. They are the two that carry the
conversion and the analytics config, so `tools/build-landing-pages.py` **fails**
if either has drifted from the root, even though it does not build this page:

```
cp lead-events.js posthog-init.js lp-v2/
```

The page also fires `target_lead` or `non_target_lead` into PostHog with
`lead_reason` on it, alongside the Meta `TargetLead` above. The distribution of
reasons is the number this page exists to move, and it is easier to read there
than in the sheet.

## The qualification rule

Runs at submit, in `qualify()`. Five tests, all decidable from fields already
on the form. It writes two new columns to the sheet and Apps Script creates
them automatically.

| Column | Value |
|---|---|
| `target_v2` | `Target` or `Non-target` |
| `target_reason` | `pass`, `not_parent`, `grade_out_of_range`, `school_not_on_list`, `school_fee_below_floor`, `aid_dependent` |

`target_reason` is written on passes too. The distribution of failure reasons
tells you which condition is killing the most leads, and therefore what to fix
in the ad next.

The existing `target_audience` column is still written, with the original rule
unchanged (US in the first two country choices, school on the fee list, fee at
or above ₹5L), so the history stays comparable. It does not test for parent,
grade or aid dependence, which is why `target_v2` is stricter.

## Routing, and the switch you may want to flip

```js
var OFFER_CALENDAR_TO_NON_TARGET = false;
```

At `false`, a family the rule marks Non-target does not see the calendar. They
get the resource path instead. **This is a business decision, not a technical
one.** It means `Schedule` only ever fires for a qualified family, which is what
turns it into a clean optimisation event, and it will cut total bookings.

Set it to `true` to let everyone book and use the flag for measurement only.

`Lead` fires for **every** submission either way. Never suppress it. Meta needs
both counts to work out a rate.

## Events

| Event | Fires | Carries |
|---|---|---|
| `PageView` | on load | standard |
| `Lead` | every submission | `eventID: lead-<timestamp>`, advanced matching |
| `TargetLead` (custom) | qualified only | `eventID: targetlead-<timestamp>` |
| `Schedule` | `next-steps.html`, after Calendly confirms | `eventID: booked-<timestamp>`, advanced matching |

**Advanced matching** is set with `fbq('init', ..., {em, ph, fn, ln, zp})`
immediately before the events fire, and again on `next-steps.html` from the
stored lead. That second one is the fix for `Schedule` sitting at 6.1 out of 10
on match quality while `Lead` scores 8.3.

`fbclid`, `_fbc` and `_fbp` are read on load, written to the sheet, and sent
unhashed. Without them Meta matches roughly a third of leads to real accounts.

## Before this goes live

1. **Set `PRICE_FROM`.** The page ships with `[SET PRICE]` on purpose.
2. **Decide `OFFER_CALENDAR_TO_NON_TARGET`.**
3. **Fix the duplicate events.** Meta is receiving two near-identical streams:
   Lead 207 from the browser and 205 from a server source, Schedule 152 and 151.
   Nothing in this repository sends server-side events, so a Conversions API
   integration exists somewhere outside it, most likely set up in Events Manager.
   Find it and make it send the same `event_id` this page sets, or turn it off.
   Until then every conversion count is roughly double the truth.
4. **Create the custom conversion** on the `TargetLead` custom event in Events
   Manager. Do not optimise for it yet. At the current rate it fires about three
   times a week and Meta needs roughly 25 to 50.
5. **Have a lawyer read the consent block** at the foot of step 3.
6. **Test on a real phone on mobile data**, including that the Calendly frame
   opens and that a Non-target submission cannot reach the calendar.

---

## Build log, 27 August 2026

Rendered in headless Chrome and iterated until the checks below passed.

### Bugs found by looking at it, and fixed

| Bug | Cause | Fix |
|---|---|---|
| **The form was completely dead.** No handler on the page was attached. | `BO.cityList()` threw. `school-fees.js` exports `cities()` and `inCity()`, not `cityList()`/`schoolsInCity()`. The throw killed the whole `DOMContentLoaded` handler. | Correct method names, per-method fallbacks so a partial object cannot throw, and the whole init wrapped in `try` so the form still takes a lead if anything above it fails. |
| Every school resolved to `[object Object]` and so every lead scored `school_not_on_list`. | `inCity()` returns records, not strings. | Use `rec.name` for the option value. |
| The card heading rendered near-white on white. | The card sits inside `.hero`, which sets `color: var(--on-navy)`, and the heading had no colour of its own. | Explicit `color` on `.card` and its headings. |
| The university logos were invisible. | They are white artwork and the wall was on a cream ground. | The wall is now navy, logos inverted to white. |
| The Bhakti outcome card had an empty gap where a photo should be. | A 64px margin hack stood in for a missing portrait. | An initial avatar, and the cards flex so the aid line always sits flush at the bottom. |
| The founder portrait dissolved into the cream section. | The source photo has a white studio background. | Cropped 160px of headroom off the source, and the image now sits in an explicit white card with a border. |
| Suspected mobile overflow. | Not real. Headless Chrome has a 500px minimum viewport, so a 390px screenshot was cropped rather than overflowing. | Verified `scrollWidth === clientWidth`. |

### Functional tests

Five cases driven through all three steps with `fetch` stubbed, so nothing reached the live sheet or Meta.

| Case | Result |
|---|---|
| Parent, Grade 9, IB, listed school (fee ₹5,72,749), no aid needed | `target_v2=Target`, `reason=pass`, calendar shown, `Lead` **and** `TargetLead` fired |
| Parent box unticked | Blocked at step 1 with the error shown, no submission |
| Grade 12 | `reason=grade_out_of_range`, no calendar, `Lead` only |
| Needs 100% aid | `reason=aid_dependent`, no calendar, `Lead` only |
| School not on the fee list | `reason=school_not_on_list`, no calendar, `Lead` only |

`Lead` fires in every case that submits. `TargetLead` fires only on a pass. The calendar appears only on a pass.

**Worth knowing:** in the Grade 12 and needs-aid cases the old `target_audience` column still reads **Target** while `target_v2` reads Non-target. The original rule does not test grade or aid dependence, so the existing count of target leads includes families that fail those two tests.

### Final state

- No JavaScript errors on load.
- 30 cities load from `school-fees.js`, schools populate on city change.
- No horizontal overflow at any width.
- 182 KB critical first load. 500 KB including all below-fold images, which are lazy.
- Price line falls back to a true, softer sentence while `PRICE_FROM` is empty, so the page is shippable before that decision is made and sharper after it.

### Still worth adding

A parent testimonial. There are portraits in `parent-voices/` but no quotes I could verify, and inventing one for a named person is not something to ship. Get one real quote and it belongs directly under the outcomes section.
