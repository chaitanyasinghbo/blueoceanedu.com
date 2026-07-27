/* Lead and booking events, in one place.

   Three pages fire these: start.html, the landing hero on lp/ and iblp/, and
   next-steps.html. Keeping the code here rather than inline in each of them is
   the difference between one conversion definition and three that drift.

   The funnel has two steps and each fires its own event:

     submit  ->  Lead              fired in place, on the page with the form
     book    ->  Schedule          fired on next-steps.html, after the booking

   The Lead fires in place rather than on a redirect because the scheduler
   appears in the card on submit, and a family that fills the form and then
   never picks a slot is still a lead. Waiting for a distinct URL to count it
   would silently drop every one of those.

   Copies of this file live in lp/ and iblp/ because those folders are served
   self-contained. tools/build-landing-pages.py copies it; do not edit those.  */

window.BOEvents = (function () {
  'use strict';

  var LEAD_KEY = 'blueOceanLead';

  function save(payload) {
    try {
      sessionStorage.setItem(LEAD_KEY, JSON.stringify(payload));
    } catch (err) {
      /* Private mode with storage denied. The lead is already posted to the
         sheet by this point, so nothing is lost but the personalisation and
         the booking event on the next page. */
      console.warn('Unable to save lead details:', err);
    }
  }

  function read() {
    try {
      var raw = sessionStorage.getItem(LEAD_KEY);
      return raw ? JSON.parse(raw) : null;
    } catch (err) {
      console.warn('Unable to read saved lead details:', err);
      return null;
    }
  }

  /* One event per lead per step.

     Keyed to the lead's own timestamp, so a refresh, a back-and-forward or a
     second tab cannot count the same step twice, while a genuine second
     submission carries a new timestamp and still counts.

     If storage is denied the event fires anyway. Counting a lead twice is the
     cheaper failure of the two. */
  function once(step, lead) {
    if (!lead || !lead.timestamp) return false;
    var key = 'boCounted:' + step + ':' + lead.timestamp;
    try {
      if (sessionStorage.getItem(key)) return false;
      sessionStorage.setItem(key, '1');
    } catch (err) {}
    return true;
  }

  /* fbq gets an eventID so a server-side Conversions API event for the same
     step of the same lead can be deduplicated against this one later. */
  function fire(step, metaEvent, dataLayerEvent, lead) {
    if (!once(step, lead)) return;

    if (typeof fbq === 'function') {
      fbq('track', metaEvent, {
        content_name: lead.form_source || 'unknown',
        content_category: lead.grade || ''
      }, { eventID: step + '-' + lead.timestamp });
    }

    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({
      event: dataLayerEvent,
      lead_source: lead.form_source || 'unknown',
      lead_grade: lead.grade || '',
      lead_target: lead.target_audience || ''
    });
  }

  /* ── The scheduler ────────────────────────────────
     Calendly, mounted into the form card once the form is submitted.

     This used to be a Google appointment schedule, which is a cross-origin
     iframe that publishes nothing. The booking was invisible from the page,
     so the only way to know was to ask the calendar for it afterwards from
     Apps Script and poll that answer. Calendly posts `calendly.event_scheduled`
     to this window the instant a slot is taken, so a booking is now something
     the page observes rather than something it infers. The poll, the JSONP
     helper and the calendar lookup behind them are all gone.

     The scheduler is mounted on submit rather than written into the markup
     for two reasons: nothing at all is fetched from Calendly for a family
     that never gets past the form, and by the time it does mount we know
     their name and address, so it opens with both already filled in.

     The button under the scheduler stays. It costs one line and it is what
     covers a family whose booking message never reaches us — a blocked
     third-party frame, an extension, a Calendly change. Nothing may stand
     between a family and the next page. */

  /* `hide_gdpr_banner=1` is load-bearing, not a preference.

     Calendly renders a OneTrust cookie banner inside its own iframe at
     `position: fixed; z-index: 2147483645`. On a desktop frame it is a small
     card in the bottom-left corner and misses the calendar. In a phone-width
     frame it becomes a 300x328 floating panel over the bottom half of the
     month grid, and every date with slots in it sits underneath. A family on
     a phone taps a date and nothing happens, because the tap lands on
     `#onetrust-policy-text`.

     It is worse than an ordinary overlay because it is fixed to the bottom of
     the *iframe*, and the iframe is taller than the phone. The thing blocking
     the taps is below the fold, so there is nothing to dismiss and no way to
     tell that anything is in the way. Measured: with the banner the date
     button hit-tests to the banner, without it the button hit-tests to
     itself. Do not drop this parameter. */
  var CALENDLY_URL = 'https://calendly.com/operations-blueoceanedu/meet-with-blue-ocean-education'
    + '?background_color=e5ded3&text_color=13171b&primary_color=e0600e'
    + '&hide_gdpr_banner=1';
  var CALENDLY_SCRIPT = 'https://assets.calendly.com/assets/external/widget.js';
  var CALENDLY_TIMEOUT_MS = 6000;

  /* Below this, a page_height report is a document that has not rendered yet
     rather than a height. Calendly sends `26px` and then `2px` before it
     sends the real figure. */
  var MIN_CREDIBLE_HEIGHT = 320;

  var calendlyWaiters = [];
  var calendlyAsked = false;
  var calendlySettled = false;

  /* Fetches widget.js once and calls back with whether it arrived.

     It is loaded here rather than from a script tag on the page so that a
     visitor who reads the page and leaves never touches Calendly at all. */
  function loadCalendly(done) {
    if (window.Calendly) return done(true);
    if (calendlySettled) return done(false);

    calendlyWaiters.push(done);
    if (calendlyAsked) return;
    calendlyAsked = true;

    var script = document.createElement('script');
    script.src = CALENDLY_SCRIPT;
    script.async = true;
    script.onerror = function () { settle(); };
    document.head.appendChild(script);

    /* onload fires before Calendly finishes defining itself often enough to
       be worth polling for the object rather than trusting the event. */
    var startedAt = new Date().getTime();
    var timer = setInterval(function () {
      if (window.Calendly) return settle();
      if (new Date().getTime() - startedAt > CALENDLY_TIMEOUT_MS) settle();
    }, 100);

    function settle() {
      clearInterval(timer);
      calendlySettled = true;
      var ok = !!window.Calendly;
      var waiting = calendlyWaiters;
      calendlyWaiters = [];
      waiting.forEach(function (fn) { fn(ok); });
    }
  }

  /* Calendly speaks to the page through window messages. Two matter:
     the booking itself, and the height its own content needs — the second is
     the only way to size the frame for a screen we cannot measure, and
     without it the family scrolls inside a box that is scrolling the page. */
  function listen(mount, onBooked) {
    /* The floor is the height the stylesheet opened the frame at, measured
       before anything is written to it: 700px on a desktop, 900px on a phone.

       A fixed floor was worse than none. It was 560px, which is under both
       CSS openings, so the first junk report shrank every frame it touched
       and a phone lost 340px of scheduler for the five seconds until the real
       height arrived. The frame clips its overflow and the iframe is
       height:100%, so a frame left short is a scheduler whose dates and
       confirm button are below the cut with no way to scroll to them. */
    var floor = mount ? Math.round(mount.getBoundingClientRect().height) : 0;
    if (!(floor > 0)) floor = MIN_CREDIBLE_HEIGHT;

    function handler(event) {
      if (!event || String(event.origin).indexOf('calendly.com') === -1) return;
      var data = event.data;
      if (!data || typeof data.event !== 'string') return;
      if (data.event.indexOf('calendly.') !== 0) return;

      if (data.event === 'calendly.page_height') {
        var height = parseInt(String((data.payload && data.payload.height) || ''), 10);
        if (height >= MIN_CREDIBLE_HEIGHT && mount) {
          mount.style.height = Math.max(height, floor) + 'px';
        }
        return;
      }

      if (data.event === 'calendly.event_scheduled') {
        window.removeEventListener('message', handler);
        if (typeof onBooked === 'function') onBooked(data.payload || {});
      }
    }

    window.addEventListener('message', handler);
  }

  /* The plain-iframe path, used when widget.js does not arrive.

     embed_domain and embed_type are what make Calendly post its messages to
     the parent window, so the booking is still detected on this path. */
  function embedFallback(mount, url, name, email) {
    var src = url + (url.indexOf('?') === -1 ? '?' : '&')
      + 'embed_domain=' + encodeURIComponent(window.location.hostname)
      + '&embed_type=Inline'
      + (name ? '&name=' + encodeURIComponent(name) : '')
      + (email ? '&email=' + encodeURIComponent(email) : '');

    var frame = document.createElement('iframe');
    frame.src = src;
    frame.title = 'Book a call with Blue Ocean Education';
    frame.setAttribute('frameborder', '0');
    mount.appendChild(frame);
  }

  function mountCalendly(options) {
    var mount = options && options.mount;
    if (!mount) return;

    var lead = (options && options.lead) || {};
    var onBooked = options && options.onBooked;
    var url = (options && options.url)
      || mount.getAttribute('data-calendly-url')
      || CALENDLY_URL;

    var name = [lead.first_name, lead.last_name]
      .filter(Boolean).join(' ').trim();
    var email = lead.email || '';

    listen(mount, onBooked);

    loadCalendly(function (ready) {
      /* Clears the placeholder the markup carries while this loads. */
      mount.innerHTML = '';

      if (ready && typeof window.Calendly.initInlineWidget === 'function') {
        window.Calendly.initInlineWidget({
          url: url,
          parentElement: mount,
          prefill: { name: name, email: email },
          /* The lead row and the Calendly booking are two records of the same
             family. These are what let them be matched later. */
          utm: {
            utmSource: lead.form_source || 'website',
            utmMedium: 'inline_embed',
            utmCampaign: lead.target_audience || ''
          }
        });
        return;
      }

      embedFallback(mount, url, name, email);
    });
  }

  return {
    saveLead: save,
    readLead: read,
    mountCalendly: mountCalendly,

    /* The form was submitted. Fires on the page that holds the form. */
    lead: function (payload) {
      save(payload);
      fire('lead', 'Lead', 'LEAD_SUBMITTED', payload);
    },

    /* A slot was booked. Fires on next-steps.html, which is reached either
       by Calendly telling the page a slot was taken or by the button under
       the scheduler. Both mean the same thing. */
    booked: function (lead) {
      fire('booked', 'Schedule', 'BOOKING_COMPLETED', lead);
    }
  };
})();
