(function () {
  "use strict";

  var SUPPORTED_LOCALES = ["en", "it", "de", "es", "fr", "ar"];
  var RTL_LOCALES = ["ar"];
  var DEFAULT_LOCALE = "en";
  var STORAGE_KEY = "assetflow_landing_locale";

  var cache = {};

  function getInitialLocale() {
    try {
      var stored = window.localStorage.getItem(STORAGE_KEY);
      if (stored && SUPPORTED_LOCALES.indexOf(stored) !== -1) {
        return stored;
      }
    } catch (e) {
      /* localStorage unavailable, ignore */
    }

    var nav = (navigator.language || navigator.userLanguage || "en").slice(0, 2).toLowerCase();
    if (SUPPORTED_LOCALES.indexOf(nav) !== -1) {
      return nav;
    }
    return DEFAULT_LOCALE;
  }

  function getByPath(obj, path) {
    return path.split(".").reduce(function (acc, key) {
      return acc && typeof acc === "object" ? acc[key] : undefined;
    }, obj);
  }

  function applyTranslations(dict) {
    var nodes = document.querySelectorAll("[data-i18n]");
    nodes.forEach(function (node) {
      var key = node.getAttribute("data-i18n");
      var value = getByPath(dict, key);
      if (typeof value === "string") {
        node.textContent = value;
      }
    });
  }

  function setDocumentDirection(locale) {
    var isRtl = RTL_LOCALES.indexOf(locale) !== -1;
    document.documentElement.setAttribute("lang", locale);
    document.documentElement.setAttribute("dir", isRtl ? "rtl" : "ltr");
  }

  function syncPickers(locale) {
    var pickers = document.querySelectorAll("#lang-picker, #lang-picker-2");
    pickers.forEach(function (picker) {
      picker.value = locale;
    });
  }

  function loadLocale(locale) {
    if (cache[locale]) {
      return Promise.resolve(cache[locale]);
    }
    return fetch("locales/" + locale + ".json")
      .then(function (res) {
        if (!res.ok) {
          throw new Error("Failed to load locale: " + locale);
        }
        return res.json();
      })
      .then(function (dict) {
        cache[locale] = dict;
        return dict;
      });
  }

  function setLocale(locale) {
    if (SUPPORTED_LOCALES.indexOf(locale) === -1) {
      locale = DEFAULT_LOCALE;
    }
    loadLocale(locale)
      .then(function (dict) {
        applyTranslations(dict);
        setDocumentDirection(locale);
        syncPickers(locale);
        try {
          window.localStorage.setItem(STORAGE_KEY, locale);
        } catch (e) {
          /* ignore storage failures */
        }
      })
      .catch(function () {
        if (locale !== DEFAULT_LOCALE) {
          setLocale(DEFAULT_LOCALE);
        }
      });
  }

  function initPricingToggle() {
    var buttons = document.querySelectorAll(".toggle-btn");
    var monthlyEls = document.querySelectorAll(".price-monthly");
    var annualEls = document.querySelectorAll(".price-annual");

    buttons.forEach(function (button) {
      button.addEventListener("click", function () {
        var period = button.getAttribute("data-period");
        buttons.forEach(function (b) {
          b.classList.toggle("is-active", b === button);
          b.setAttribute("aria-pressed", b === button ? "true" : "false");
        });
        var showAnnual = period === "annual";
        monthlyEls.forEach(function (el) {
          el.classList.toggle("is-hidden", showAnnual);
        });
        annualEls.forEach(function (el) {
          el.classList.toggle("is-hidden", !showAnnual);
        });
      });
    });
  }

  function initLanguagePickers() {
    var pickers = document.querySelectorAll("#lang-picker, #lang-picker-2");
    pickers.forEach(function (picker) {
      picker.addEventListener("change", function (event) {
        setLocale(event.target.value);
      });
    });
  }

  function initFooterYear() {
    var yearEl = document.getElementById("year");
    if (yearEl) {
      yearEl.textContent = String(new Date().getFullYear());
    }
  }

  function initScrollReveal() {
    var targets = document.querySelectorAll(".reveal");
    if (!targets.length) {
      return;
    }
    if (!("IntersectionObserver" in window)) {
      targets.forEach(function (el) {
        el.classList.add("is-visible");
      });
      return;
    }
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );
    targets.forEach(function (el) {
      observer.observe(el);
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    initPricingToggle();
    initLanguagePickers();
    initFooterYear();
    initScrollReveal();
    setLocale(getInitialLocale());
  });
})();
