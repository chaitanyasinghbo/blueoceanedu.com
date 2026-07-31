/**
 * Blue Ocean Education - lead sheet endpoint.
 *
 * This file is the source of truth for the code, but it does NOT run from
 * here. It runs in Google Apps Script, bound to the leads spreadsheet, and is
 * published as the Web App the forms post to:
 *
 *   https://script.google.com/macros/s/AKfycbxzYB2CtlMlPP0H9zCeEJAElhuSRWnF5RdyiL75JH_G2PcOn7ExTbxdc6kDev63ssMo8w/exec
 *
 * To edit it: open the leads spreadsheet, Extensions > Apps Script, paste this
 * file over Code.gs, then Deploy > Manage deployments > edit the existing
 * deployment > New version > Deploy. Editing without redeploying a new version
 * changes nothing, which is the usual reason a change appears to do nothing.
 * Keep the deployment set to "Execute as: Me" and "Who has access: Anyone",
 * or the browser post fails silently, because the forms use mode: 'no-cors'
 * and never see the response.
 *
 * Posting pages: start.html, lp/, iblp/. They send different field sets, which
 * is why this script is header-driven rather than a fixed column list. A key
 * it has never seen becomes a new column on the right; a key a page omits
 * leaves that cell blank. Neither case needs a code change here.
 *
 * Not everything that posts here is a lead. `next-steps.html` also carries a
 * newsletter signup, and it is prefilled from the lead the family just
 * submitted, so subscribing is one click on the page they land on after
 * booking. Almost everyone who books does it. Those rows used to append to
 * `Leads` carrying the same name, email, phone, grade and school, which made
 * one family read as two leads. They are routed to their own tab now, by
 * `form_source`, and `Leads` holds submissions of the consultation form only.
 *
 * Routing applies to what arrives after the deployment. Rows already in
 * `Leads` stay where they are and are cleaned up by hand.
 */

var SHEET_NAME = 'Leads';
var NEWSLETTER_SHEET_NAME = 'Newsletter';
var TIME_ZONE = 'Asia/Kolkata';
var TIME_FORMAT = 'dd-MMM-yyyy HH:mm:ss';

/* Written as numbers, not text, so the sheet can sort and filter on them.
   Everything else lands as a string. */
var NUMERIC_COLUMNS = [
  'school_fee_annual_inr',
  'school_ib_fee_inr',
  'school_general_fee_inr',
  'school_fee_match_score'
];

/* Columns in the order they should appear when the sheet is created from
   scratch. Anything posted that is not on this list is appended to the right
   in arrival order, so this is a preference, not a constraint. */
var PREFERRED_ORDER = [
  'timestamp',
  'target_audience',
  'form_source',
  'user_type',
  'first_name',
  'last_name',
  'email',
  'phone',
  'grade',
  'school_city',
  'school_name',
  'school_board',
  'school_fee_annual_inr',
  'school_ib_fee_inr',
  'school_general_fee_inr',
  'school_fee_band',
  'school_fee_basis',
  'school_fee_matched_name',
  'school_fee_match_method',
  'school_fee_match_score',
  'pincode',
  'country_pref_1',
  'country_pref_2',
  'country_pref_3',
  'country_prefs',
  'financial_aid',
  'financial_aid_code',
  'page_url',
  'page_title'
];

/* The newsletter tab. Same idea, fewer columns, because the signup posts what
   it can copy off the stored lead and nothing more. `lead_timestamp` is the
   timestamp of that lead's own row, so a subscription can be tied back to the
   submission it came from without matching on email. */
var NEWSLETTER_ORDER = [
  'timestamp',
  'form_source',
  'first_name',
  'last_name',
  'email',
  'phone',
  'user_type',
  'grade',
  'school_name',
  'financial_aid',
  'lead_timestamp',
  'page_url',
  'page_title'
];

/* Which tab a post lands on, keyed by `form_source`. Anything not named here
   is a lead and goes to `Leads`, so a new landing page needs no entry and a
   page that stops being a lead form needs one line.

   Routing on a value the page sends is deliberate: the alternative is letting
   the post name its own destination, which lets a stray request create tabs. */
var SHEET_ROUTES = {
  newsletter_next_steps: { name: NEWSLETTER_SHEET_NAME, order: NEWSLETTER_ORDER }
};

function routeFor_(formSource) {
  var route = SHEET_ROUTES[String(formSource || '')];
  return route || { name: SHEET_NAME, order: PREFERRED_ORDER };
}

function doPost(e) {
  /* One writer at a time. Two forms submitting in the same second otherwise
     read the same last row and one overwrites the other. */
  var lock = LockService.getScriptLock();
  lock.waitLock(30000);
  try {
    var data = (e && e.parameter) ? e.parameter : {};
    var route = routeFor_(data.form_source);
    var sheet = getSheet_(route.name, route.order);
    var headers = getHeaders_(sheet, route.order);

    /* Any key we have not seen becomes a column. */
    var fresh = [];
    for (var key in data) {
      if (headers.indexOf(key) === -1) fresh.push(key);
    }
    if (fresh.length) {
      sheet.getRange(1, headers.length + 1, 1, fresh.length).setValues([fresh]);
      headers = headers.concat(fresh);
      styleHeader_(sheet, headers.length);
      if (fresh.indexOf('timestamp') !== -1) formatTimestampColumn_(sheet, headers);
    }

    var row = headers.map(function (header) {
      if (header === 'timestamp') return data.timestamp ? new Date(data.timestamp) : new Date();
      if (NUMERIC_COLUMNS.indexOf(header) !== -1) {
        return data[header] ? Number(data[header]) : '';
      }
      return data[header] !== undefined ? data[header] : '';
    });

    sheet.appendRow(row);
    return json_({ ok: true });
  } catch (err) {
    return json_({ ok: false, error: String(err) });
  } finally {
    lock.releaseLock();
  }
}

/* ── The booking is no longer this script's business ────────────────
   It used to be. The scheduler was a Google appointment schedule, a
   cross-origin iframe that publishes no event, so the page could not see a
   booking happen inside it and this script answered `?booked=<email>` from
   the calendar while the page polled it.

   The site books through Calendly now, and Calendly posts a message to the
   page the moment a slot is taken, so the booking is observed where it
   happens. The calendar lookup, the JSONP reply it needed and the Calendar
   scope they pulled in are all gone with it.

   Nothing needs redeploying for that. A deployment still carrying the old
   code simply answers a question the site has stopped asking. */

function doGet() {
  return json_({ ok: true, service: 'Blue Ocean lead sheet' });
}

function getSheet_(name, order) {
  name = name || SHEET_NAME;
  order = order || PREFERRED_ORDER;
  var book = SpreadsheetApp.getActiveSpreadsheet();

  /* The forms send a UTC instant, which is the right thing to send. What makes
     a row read as IST is the spreadsheet's own timezone, so it is pinned here
     rather than left on whatever the sheet was created with. Checked before
     it is set, because an unconditional write on every submission is an API
     call for nothing. */
  if (book.getSpreadsheetTimeZone() !== TIME_ZONE) {
    book.setSpreadsheetTimeZone(TIME_ZONE);
  }

  var sheet = book.getSheetByName(name);
  if (!sheet) {
    sheet = book.insertSheet(name);
    sheet.getRange(1, 1, 1, order.length).setValues([order]);
    styleHeader_(sheet, order.length);
    formatTimestampColumn_(sheet, order);
  }
  return sheet;
}

/* The timestamp column stays a real date value, not a preformatted string, so
   the sheet can sort and filter on it. The format is display only. */
function formatTimestampColumn_(sheet, headers) {
  var index = headers.indexOf('timestamp');
  if (index === -1) return;
  sheet.getRange(2, index + 1, Math.max(sheet.getMaxRows() - 1, 1), 1)
       .setNumberFormat(TIME_FORMAT);
}

function getHeaders_(sheet, order) {
  order = order || PREFERRED_ORDER;
  if (sheet.getLastColumn() === 0) {
    sheet.getRange(1, 1, 1, order.length).setValues([order]);
    styleHeader_(sheet, order.length);
    return order.slice();
  }
  return sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0].map(String);
}

function styleHeader_(sheet, width) {
  sheet.getRange(1, 1, 1, width).setFontWeight('bold');
  sheet.setFrozenRows(1);
}

/**
 * Run once, by hand, from the Apps Script editor after pasting this file over
 * an older version of the script. It pins the timezone to IST, formats the
 * timestamp column, and adds the columns the three-step form introduced to a
 * sheet that already holds rows. It never touches the data underneath, and it
 * is safe to run twice.
 */
function setUpSheet() {
  var sheet = getSheet_();
  var headers = getHeaders_(sheet);
  var missing = PREFERRED_ORDER.filter(function (name) {
    return headers.indexOf(name) === -1;
  });
  if (missing.length) {
    sheet.getRange(1, headers.length + 1, 1, missing.length).setValues([missing]);
    headers = headers.concat(missing);
    styleHeader_(sheet, headers.length);
  }
  formatTimestampColumn_(sheet, headers);
}

function json_(payload) {
  return ContentService
    .createTextOutput(JSON.stringify(payload))
    .setMimeType(ContentService.MimeType.JSON);
}
