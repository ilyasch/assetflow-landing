(function () {
  "use strict";
  var LOCALES = ["en", "it", "de", "es", "fr", "ar"];
  var STORAGE_KEY = "assetflow_landing_locale";
  var cache = {};
  var localeRequest = 0;
  var refreshMarketSpotlight = null;
  var refreshHowCarousel = null;

  function initialLocale() {
    var requested = new URLSearchParams(window.location.search).get("lang");
    if (LOCALES.indexOf(requested) !== -1) return requested;
    try {
      var stored = localStorage.getItem(STORAGE_KEY);
      if (LOCALES.indexOf(stored) !== -1) return stored;
    } catch (e) {
      /* Locale still works without storage. */
    }
    var language = (navigator.language || "en").slice(0, 2).toLowerCase();
    return LOCALES.indexOf(language) === -1 ? "en" : language;
  }

  function valueAt(dict, key) {
    return key.split(".").reduce(function (value, part) {
      return value && typeof value === "object" ? value[part] : undefined;
    }, dict);
  }

  function translate(dict) {
    document.querySelectorAll("[data-i18n]").forEach(function (node) {
      var value = valueAt(dict, node.dataset.i18n);
      if (typeof value === "string") node.textContent = value;
    });
    document.querySelectorAll("[data-i18n-aria]").forEach(function (node) {
      var value = valueAt(dict, node.dataset.i18nAria);
      if (typeof value === "string") node.setAttribute("aria-label", value);
    });
  }

  function localizeDigits(locale) {
    var digits = "0123456789",
      arabic = "٠١٢٣٤٥٦٧٨٩";
    var from = locale === "ar" ? digits : arabic;
    var to = locale === "ar" ? arabic : digits;
    var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    var node;
    while ((node = walker.nextNode())) {
      node.nodeValue = node.nodeValue.replace(/[0-9٠-٩]/g, function (digit) {
        var index = from.indexOf(digit);
        return index < 0 ? digit : to.charAt(index);
      });
    }
  }

  function loadLocale(locale) {
    if (cache[locale]) return Promise.resolve(cache[locale]);
    return fetch("/locales/" + locale + ".json")
      .then(function (response) {
        if (!response.ok) throw new Error("Locale unavailable");
        return response.json();
      })
      .then(function (dict) {
        cache[locale] = dict;
        return dict;
      });
  }

  function setLocale(locale) {
    if (LOCALES.indexOf(locale) === -1) locale = "en";
    var request = ++localeRequest;
    return loadLocale(locale)
      .then(function (dict) {
        if (request !== localeRequest) return;
        translate(dict);
        if (refreshMarketSpotlight) refreshMarketSpotlight();
        document.documentElement.lang = locale;
        document.documentElement.dir = locale === "ar" ? "rtl" : "ltr";
        localizeDigits(locale);
        document.querySelectorAll("[data-blog-index]").forEach(function (link) {
          link.href = "/blog/" + locale + "/";
        });
        document.querySelectorAll("[data-blog-article]").forEach(function (link) {
          link.href =
            "/blog/" + locale + "/" + link.dataset.blogArticle + "/";
        });
        if (refreshHowCarousel) refreshHowCarousel();
        document.getElementById("lang-picker").value = locale;
        if (dict.seo) {
          document.title = dict.seo.title;
          [
            "description",
            "og:description",
            "twitter:description",
            "og:title",
            "twitter:title",
          ].forEach(function (key) {
            var meta = document.querySelector(
              'meta[name="' + key + '"], meta[property="' + key + '"]',
            );
            if (meta)
              meta.content =
                key.indexOf("title") !== -1
                  ? dict.seo.title
                  : dict.seo.description;
          });
        }
        try {
          localStorage.setItem(STORAGE_KEY, locale);
        } catch (e) {
          /* Optional persistence. */
        }
      })
      .catch(function () {
        if (request !== localeRequest) return;
        if (locale !== "en") return setLocale("en");
        // The complete English fallback is already present in the document.
        document.getElementById("lang-picker").value =
          document.documentElement.lang;
      });
  }

  function initPricing() {
    document.querySelector(".pricing").classList.add("is-interactive");
    var buttons = document.querySelectorAll("[data-period]");
    buttons.forEach(function (button) {
      button.setAttribute(
        "aria-pressed",
        button.dataset.period === "monthly" ? "true" : "false",
      );
      button.addEventListener("click", function () {
        var annual = button.dataset.period === "annual";
        buttons.forEach(function (other) {
          other.classList.toggle("is-active", other === button);
          other.setAttribute(
            "aria-pressed",
            other === button ? "true" : "false",
          );
        });
        document.querySelectorAll(".price-monthly").forEach(function (node) {
          node.classList.toggle("is-hidden", annual);
        });
        document.querySelectorAll(".price-annual").forEach(function (node) {
          node.classList.toggle("is-hidden", !annual);
        });
      });
    });
  }

  function initSectionRail() {
    var links = Array.from(document.querySelectorAll("[data-section-link]"));
    var main = document.getElementById("main");
    var header = document.querySelector(".site-header");
    var desktopRail = window.matchMedia("(min-width: 1200px)");
    var sections = links
      .map(function (link) {
        return document.querySelector(link.getAttribute("href"));
      })
      .filter(Boolean);
    if (!links.length) return;
    var updateCurrent = function () {
      var anchor = window.innerHeight * 0.36;
      var currentSection = sections[0];
      sections.forEach(function (section) {
        if (section.getBoundingClientRect().top <= anchor)
          currentSection = section;
      });
      var current = "#" + currentSection.id;
      links.forEach(function (link) {
        if (link.getAttribute("href") === current)
          link.setAttribute("aria-current", "location");
        else link.removeAttribute("aria-current");
      });
      var nextSectionTop = sections[0].getBoundingClientRect().top;
      var headerBottom = header.getBoundingClientRect().bottom;
      main.classList.toggle(
        "is-section-rail-active",
        desktopRail.matches && nextSectionTop <= headerBottom + 8,
      );
    };
    var scheduled = false;
    function scheduleUpdate() {
      if (scheduled) return;
      scheduled = true;
      window.requestAnimationFrame(function () {
        scheduled = false;
        updateCurrent();
      });
    }
    window.addEventListener("scroll", scheduleUpdate, { passive: true });
    window.addEventListener("resize", scheduleUpdate);
    updateCurrent();
  }

  function initHowCarousel() {
    var carousels = Array.from(document.querySelectorAll("[data-feature-carousel]"));
    if (!carousels.length) return;
    var refreshers = [];
    carousels.forEach(function (carousel) {
      var slides = Array.from(carousel.querySelectorAll("[data-feature-slide]"));
      var controls = carousel.querySelector("[data-feature-controls]");
      var previous = carousel.querySelector("[data-feature-previous]");
      var next = carousel.querySelector("[data-feature-next]");
      var status = carousel.querySelector("[data-feature-status]");
      if (slides.length < 2 || !controls || !previous || !next || !status) return;
      var activeIndex = 0;
      function updateStatus() {
        var locale = document.documentElement.lang || "en";
        var format = new Intl.NumberFormat(locale, { minimumIntegerDigits: 2 });
        status.textContent = format.format(activeIndex + 1) + " / " + format.format(slides.length);
      }
      function select(index) {
        var oldIndex = activeIndex;
        activeIndex = (index + slides.length) % slides.length;
        slides.forEach(function (slide) {
          var selected = slideIndex === activeIndex;
          slide.hidden = !selected;
          slide.classList.remove("is-entering", "is-forward", "is-backward");
          if (selected && oldIndex !== activeIndex) {
            slide.classList.add("is-entering", activeIndex > oldIndex ? "is-forward" : "is-backward");
            slide.addEventListener("animationend", function cleanup() {
              slide.classList.remove("is-entering", "is-forward", "is-backward");
            }, { once: true });
          }
        });
        updateStatus();
      }
      previous.addEventListener("click", function () { select(activeIndex - 1); });
      next.addEventListener("click", function () { select(activeIndex + 1); });
      controls.hidden = false;
      carousel.classList.add("is-interactive");
      select(0);
      refreshers.push(updateStatus);
    });
    refreshHowCarousel = function () { refreshers.forEach(function (refresh) { refresh(); }); };
  }

  function initDemo() {
    var demo = document.querySelector(".ownership-demo");
    var tabs = Array.from(demo.querySelectorAll("[data-demo]"));
    var panels = demo.querySelectorAll(".demo-panel");
    var tablist = demo.querySelector(".demo-tabs");
    tablist.setAttribute("role", "tablist");
    tablist.dataset.i18nAria = "site.demoTitle";
    tablist.setAttribute(
      "aria-label",
      document.querySelector('[data-i18n="site.demoTitle"]').textContent,
    );
    function select(tab, focus) {
      tabs.forEach(function (other) {
        var active = other === tab;
        other.setAttribute("aria-selected", String(active));
        other.tabIndex = active ? 0 : -1;
      });
      panels.forEach(function (panel) {
        panel.hidden = panel.id !== "demo-" + tab.dataset.demo;
      });
      demo.querySelectorAll("[data-demo-context]").forEach(function (context) {
        context.hidden = context.dataset.demoContext !== tab.dataset.demo;
      });
      if (focus) tab.focus();
    }
    tabs.forEach(function (tab, index) {
      tab.setAttribute("role", "tab");
      tab.addEventListener("click", function () {
        select(tab, false);
      });
      tab.addEventListener("keydown", function (event) {
        var vertical = getComputedStyle(tablist).flexDirection === "column";
        tablist.setAttribute(
          "aria-orientation",
          vertical ? "vertical" : "horizontal",
        );
        var previous = vertical
          ? "ArrowUp"
          : document.documentElement.dir === "rtl"
            ? "ArrowRight"
            : "ArrowLeft";
        var next = vertical
          ? "ArrowDown"
          : document.documentElement.dir === "rtl"
            ? "ArrowLeft"
            : "ArrowRight";
        var target;
        if (event.key === previous)
          target = (index + tabs.length - 1) % tabs.length;
        else if (event.key === next) target = (index + 1) % tabs.length;
        else if (event.key === "Home") target = 0;
        else if (event.key === "End") target = tabs.length - 1;
        else return;
        event.preventDefault();
        select(tabs[target], true);
      });
    });
    panels.forEach(function (panel) {
      panel.setAttribute("role", "tabpanel");
      panel.tabIndex = 0;
    });
    var orientation = window.matchMedia("(max-width: 620px)");
    function syncOrientation() {
      tablist.setAttribute(
        "aria-orientation",
        orientation.matches ? "horizontal" : "vertical",
      );
    }
    syncOrientation();
    orientation.addEventListener("change", syncOrientation);
    demo.classList.add("is-interactive");
    select(tabs[0], false);
    var review = demo.querySelector(".demo-review");
    var detail = demo.querySelector(".review-detail");
    var confirm = demo.querySelector(".demo-confirm");
    var reset = demo.querySelector(".demo-reset");
    var status = demo.querySelector(".confirmation");
    var badge = demo.querySelector(".status-pill");
    function currentText(key) {
      return (
        valueAt(cache[document.documentElement.lang] || cache.en || {}, key) ||
        {
          "site.confirmation":
            "Example task confirmed. No real reminder was created.",
          "site.confirmed": "Confirmed in this example",
          "site.draft": "Suggested task · review first",
        }[key]
      );
    }
    review.addEventListener("click", function () {
      review.hidden = true;
      detail.hidden = false;
      confirm.focus();
    });
    confirm.addEventListener("click", function () {
      detail.hidden = true;
      status.dataset.i18n = "site.confirmation";
      status.textContent = currentText("site.confirmation");
      badge.dataset.i18n = "site.confirmed";
      badge.textContent = currentText("site.confirmed");
      reset.hidden = false;
      reset.focus();
    });
    reset.addEventListener("click", function () {
      delete status.dataset.i18n;
      status.textContent = "";
      badge.dataset.i18n = "site.draft";
      badge.textContent = currentText("site.draft");
      detail.hidden = true;
      reset.hidden = true;
      review.hidden = false;
      review.focus();
    });
  }

  function initMarketMatrix() {
    var section = document.querySelector("[data-market-interaction]");
    if (!section) return;
    var buttons = Array.from(section.querySelectorAll("[data-market]"));
    var table = document.querySelector(".market-matrix");
    var activeButton;
    function select(button, scroll) {
      activeButton = button;
      var column = Number(button.dataset.column);
      buttons.forEach(function (other) {
        other.setAttribute("aria-pressed", String(other === button));
      });
      table.querySelectorAll("tr").forEach(function (row) {
        Array.from(row.cells).forEach(function (cell, index) {
          cell.classList.toggle("is-selected", index === column - 1);
        });
      });
      section.querySelector("[data-market-title]").textContent =
        button.querySelector("span").textContent;
      section.querySelector("[data-market-status]").textContent =
        button.querySelector("small").textContent;
      section.querySelectorAll("[data-market-value]").forEach(function (value) {
        var row = table.tBodies[0].rows[Number(value.dataset.marketValue) - 1];
        value.textContent = row.cells[column - 1].textContent.trim();
      });
      if (scroll && window.matchMedia("(max-width: 1014px)").matches) {
        var cell = table.tHead.rows[0].cells[column - 1];
        cell.scrollIntoView({
          block: "nearest",
          inline: "center",
          behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches
            ? "auto"
            : "smooth",
        });
      }
    }
    buttons.forEach(function (button) {
      button.addEventListener("click", function () {
        select(button, true);
      });
    });
    refreshMarketSpotlight = function () {
      if (activeButton) select(activeButton, false);
    };
    section.classList.add("is-interactive");
    select(buttons[0], false);
  }

  document.addEventListener("DOMContentLoaded", function () {
    initPricing();
    initDemo();
    initHowCarousel();
    initMarketMatrix();
    initSectionRail();
    document
      .getElementById("lang-picker")
      .addEventListener("change", function (event) {
        setLocale(event.target.value);
      });
    document.getElementById("year").textContent = String(
      new Date().getFullYear(),
    );
    var menu = document.querySelector(".mobile-menu");
    menu.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        menu.open = false;
      });
    });
    menu.addEventListener("keydown", function (event) {
      if (event.key === "Escape") {
        menu.open = false;
        menu.querySelector("summary").focus();
      }
    });
    document.addEventListener("click", function (event) {
      if (!menu.contains(event.target)) menu.open = false;
    });
    setLocale(initialLocale());
  });
})();
