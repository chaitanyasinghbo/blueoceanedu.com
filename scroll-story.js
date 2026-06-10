(function () {
  function clamp(value, min, max) {
    return Math.max(min, Math.min(max, value));
  }

  function initVerticalScrollStory(options) {
    const settings = Object.assign({
      rowSelector: "[data-scroll-story-row]",
      copySelector: "[data-scroll-story-copy]",
      visualSelector: "[data-scroll-story-visual]",
      classTarget: document.body,
      readyClass: "scroll-story-ready",
      propertyPrefix: "scroll-story",
      mediaQuery: "(min-width: 981px) and (prefers-reduced-motion: no-preference)",
      viewportAnchor: 0.52,
      travel: 0.72,
      minCopyOpacity: 0.28,
      minVisualOpacity: 0.4,
      copyTranslate: 42,
      visualTranslate: 86,
      minVisualScale: 0.955
    }, options || {});

    const rows = Array.from(document.querySelectorAll(settings.rowSelector));
    const motionQuery = window.matchMedia(settings.mediaQuery);
    let frame = null;

    if (!rows.length) {
      return {
        update: function () {},
        destroy: function () {}
      };
    }

    const property = function (name) {
      return "--" + settings.propertyPrefix + "-" + name;
    };

    const setStatic = function () {
      settings.classTarget.classList.remove(settings.readyClass);
      rows.forEach(function (row) {
        row.style.removeProperty(property("copy-opacity"));
        row.style.removeProperty(property("visual-opacity"));
        row.style.removeProperty(property("copy-y"));
        row.style.removeProperty(property("visual-y"));
        row.style.removeProperty(property("visual-scale"));
      });
    };

    const update = function () {
      frame = null;

      if (!motionQuery.matches) {
        setStatic();
        return;
      }

      settings.classTarget.classList.add(settings.readyClass);
      const anchor = window.innerHeight * settings.viewportAnchor;
      const travel = Math.max(window.innerHeight * settings.travel, 1);

      rows.forEach(function (row) {
        const rect = row.getBoundingClientRect();
        const center = rect.top + rect.height * 0.5;
        const distance = clamp((center - anchor) / travel, -1, 1);
        const focus = Math.max(0, 1 - Math.abs(distance));
        const eased = 1 - Math.pow(1 - focus, 3);

        row.style.setProperty(property("copy-opacity"), String(settings.minCopyOpacity + eased * (1 - settings.minCopyOpacity)));
        row.style.setProperty(property("visual-opacity"), String(settings.minVisualOpacity + eased * (1 - settings.minVisualOpacity)));
        row.style.setProperty(property("copy-y"), Math.round(distance * settings.copyTranslate) + "px");
        row.style.setProperty(property("visual-y"), Math.round(distance * settings.visualTranslate) + "px");
        row.style.setProperty(property("visual-scale"), String(settings.minVisualScale + eased * (1 - settings.minVisualScale)));
      });
    };

    const requestUpdate = function () {
      if (frame === null) {
        frame = window.requestAnimationFrame(update);
      }
    };

    const onMotionChange = function () {
      requestUpdate();
    };

    update();
    window.addEventListener("scroll", requestUpdate, { passive: true });
    window.addEventListener("resize", requestUpdate);

    if (motionQuery.addEventListener) {
      motionQuery.addEventListener("change", onMotionChange);
    } else {
      motionQuery.addListener(onMotionChange);
    }

    return {
      update: update,
      destroy: function () {
        window.removeEventListener("scroll", requestUpdate);
        window.removeEventListener("resize", requestUpdate);

        if (motionQuery.removeEventListener) {
          motionQuery.removeEventListener("change", onMotionChange);
        } else {
          motionQuery.removeListener(onMotionChange);
        }

        if (frame !== null) {
          window.cancelAnimationFrame(frame);
          frame = null;
        }

        setStatic();
      }
    };
  }

  window.BlueOceanScrollStory = {
    initVerticalScrollStory: initVerticalScrollStory
  };
})();
