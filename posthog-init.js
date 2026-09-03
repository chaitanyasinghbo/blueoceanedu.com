/* PostHog, loaded and configured in one place.

   The key, the region and every capture option are here and nowhere else.
   Every page carries the same two lines inside its @analytics block: a three
   line stub that queues, and a deferred tag for this file. So changing the
   key, the region, or whether session replay runs is one edit to one file,
   not an edit to eleven heads and four generated ones.

   Copies of this file live in lp/, iblp/ and lp-v2/ because those folders are
   served self-contained. tools/build-landing-pages.py copies it into the first
   two and fails the build if the lp-v2 copy has drifted; do not edit any copy.

   ── Why a stub rather than PostHog's own snippet ──────────────────
   PostHog ships a minified loader that stubs `window.posthog` and replays
   whatever was called before the library arrives. We do the same job in three
   readable lines instead, for one reason: the stub has to run SYNCHRONOUSLY
   and this file must not. An inline script at the foot of the body runs before
   any deferred script, and next-steps.html fires the booking from exactly
   there, so a deferred `BOPostHog` would be undefined at the moment the one
   event that matters most is sent. The stub is inline and costs nothing; the
   library is deferred and blocks no render.

   ── Before this collects anything ─────────────────────────────────
   1. Create a free project at posthog.com and copy the Project API key.
   2. Put it in PROJECT_KEY below, and set REGION to match the cloud you
      picked. Until then this file loads, does nothing, and asks Posthog for
      nothing at all.
   3. If you chose EU, change the preconnect in every page's resource hints
      from us-assets to eu-assets. It is a hint, so a wrong one costs a little
      speed rather than any data.
   4. Session replay is a project setting as well as a client option. Both
      have to be on. Turn it on under Settings, Session replay.                */

(function () {
  'use strict';

  /* ── The two things you edit ──────────────────────────────────── */

  /* The Project API key, `phc_` followed by 43 characters. It is a publishable
     key: it is meant to sit in client-side source and can only write events.
     The Personal API key that reads data back out is a different key and must
     never appear in this file. */
  var PROJECT_KEY = '';

  /* 'us' or 'eu'. This is fixed when the PostHog project is created and
     cannot be changed afterwards without moving the project. */
  var REGION = 'us';

  /* ── Everything below follows from those two ──────────────────── */

  /* `lib` is a whole URL rather than a host plus a path. Written the other
     way, the path half is a quoted string ending in .js, which is exactly what
     tools/find-unused.py counts as a reference to a file in this repository,
     and it then reports that file missing every time anybody runs it. */
  var HOSTS = {
    us: { api: 'https://us.i.posthog.com',
          lib: 'https://us-assets.i.posthog.com/static/array.js' },
    eu: { api: 'https://eu.i.posthog.com',
          lib: 'https://eu-assets.i.posthog.com/static/array.js' }
  };

  var host = HOSTS[REGION] || HOSTS.us;

  var OPTIONS = {
    api_host: host.api,

    /* A person profile per identified family, not per anonymous visitor.
       Anonymous events still carry a distinct_id and still build funnels;
       what this avoids is a person record for every bot that loads the home
       page, which is what makes the person table useless to read. */
    person_profiles: 'identified_only',

    /* The reason to run PostHog next to GA4 at all: clicks, form interactions
       and rage clicks captured without anyone deciding in advance that they
       were worth capturing. */
    autocapture: true,
    rageclick: true,

    /* Multi-page site, so one pageview per document load is correct, and
       pageleave is what makes time-on-page and bounce mean anything. */
    capture_pageview: true,
    capture_pageleave: true,

    /* The site is served from blueoceanedu.com, lp.blueoceanedu.com and
       iblp.blueoceanedu.com. Without this a family who lands on an ad page
       and then reads the main site is two people. */
    cross_subdomain_cookie: true,

    /* Session replay, which is the point of this over GA4: watching where a
       family stalls in the form beats guessing from a drop-off number. */
    disable_session_recording: false,
    session_recording: {
      /* Every input is replaced with asterisks in the recording. This is
         PostHog's default and it is restated here because it is the whole
         basis on which replay is acceptable on a page that collects a child's
         name, a parent's phone number and a school. Do not set it false. */
      maskAllInputs: true,

      /* Anything that renders a family's own words back at them gets masked
         too. Nothing carries this attribute yet; it is here so that the way
         to hide an element from a recording is to mark it up, rather than to
         come back and edit this file. */
      maskTextSelector: '[data-ph-mask]'
    }
  };

  /* The stub the @analytics block defined. If this file somehow loads without
     it, make one, so nothing below has to test for it. */
  var bo = window.BOPostHog = window.BOPostHog || { _q: [] };

  function noop() {}

  /* No key yet: leave the stub in place as a sink that drops calls, and touch
     the network not at all. This is the state the file ships in. */
  if (PROJECT_KEY.indexOf('phc_') !== 0) {
    bo._q = [];
    bo.capture = noop;
    bo.identify = noop;
    return;
  }

  function send(method, args) {
    var ph = window.posthog;
    if (ph && typeof ph[method] === 'function') ph[method].apply(ph, args);
  }

  function ready() {
    var queued = bo._q || [];

    /* Swap the queueing stub for direct calls before draining, so a capture
       made from inside a drained call cannot land back in the queue. */
    bo._q = [];
    bo.capture = function () { send('capture', [].slice.call(arguments)); };
    bo.identify = function () { send('identify', [].slice.call(arguments)); };

    for (var i = 0; i < queued.length; i++) send(queued[i][0], queued[i][1]);
  }

  var script = document.createElement('script');
  script.src = host.lib;
  script.async = true;

  script.onload = function () {
    if (!window.posthog || typeof window.posthog.init !== 'function') return;
    window.posthog.init(PROJECT_KEY, OPTIONS);
    ready();
  };

  /* Blocked by an extension, a network, or a content blocker. The queue is
     dropped and every call after this is a no-op. Analytics is always what
     gives way; nothing on the page may depend on this having worked. */
  script.onerror = function () {
    bo._q = [];
    bo.capture = noop;
    bo.identify = noop;
  };

  document.head.appendChild(script);
})();
