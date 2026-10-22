(function () {
  "use strict";
  var LOCALES = ["en", "it", "de", "es", "fr", "ar"];
  var STORAGE_KEY = "assetflow_landing_locale";
  var cache = {};
  var localeRequest = 0;
  var refreshMarketMatrix = null;
  var refreshFeatureTracks = null;

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
        if (refreshMarketMatrix) refreshMarketMatrix();
        document.documentElement.lang = locale;
        document.documentElement.dir = locale === "ar" ? "rtl" : "ltr";
        localizeDigits(locale);
        if (refreshFeatureTracks) refreshFeatureTracks();
        document.querySelectorAll("[data-blog-index]").forEach(function (link) {
          link.href = "/blog/" + locale + "/";
        });
        document.querySelectorAll("[data-blog-article]").forEach(function (link) {
          link.href =
            "/blog/" + locale + "/" + link.dataset.blogArticle + "/";
        });
        document.querySelectorAll("[data-doc-index]").forEach(function (link) {
          link.href = "/docs/" + locale + "/";
        });
        document.querySelectorAll("[data-doc-article]").forEach(function (link) {
          link.href = "/docs/" + locale + "/" + link.dataset.docArticle + "/";
        });
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
    var hero = document.querySelector(".hero");
    var desktopRail = window.matchMedia("(min-width: 1024px)");
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
      var heroHeight = hero ? hero.offsetHeight : 0;
      var railActive = desktopRail.matches && window.scrollY >= heroHeight - 96;
      var classNames = main.className
        .split(/\s+/)
        .filter(function (name) {
          return name && name !== "is-section-rail-active";
        });
      if (railActive) classNames.push("is-section-rail-active");
      main.className = classNames.join(" ");
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
    window.addEventListener("hashchange", scheduleUpdate);
    window.addEventListener("pageshow", scheduleUpdate);
    if (hero && "IntersectionObserver" in window) {
      var heroObserver = new IntersectionObserver(scheduleUpdate, {
        rootMargin: "-96px 0px 0px 0px",
      });
      heroObserver.observe(hero);
    }
    window.requestAnimationFrame(updateCurrent);
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
    document.querySelectorAll("[data-demo-target]").forEach(function (link) {
      link.addEventListener("click", function (event) {
        if (
          event.defaultPrevented || event.button !== 0 || event.metaKey ||
          event.ctrlKey || event.shiftKey || event.altKey
        ) return;
        var target = tabs.find(function (tab) {
          return tab.dataset.demo === link.dataset.demoTarget;
        });
        if (target) select(target, true);
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
    var table = section.querySelector(".market-matrix");
    var activeButton;
    function select(button) {
      activeButton = button;
      var column = Number(button.dataset.column);
      buttons.forEach(function (other) {
        other.setAttribute("aria-pressed", String(other === button));
      });
      table.querySelectorAll("tr").forEach(function (row) {
        Array.from(row.cells).forEach(function (cell, index) {
          cell.classList.toggle("is-selected", index === column - 1);
          cell.hidden = index !== 0 && index !== column - 1;
        });
      });
      section.dataset.market = button.dataset.market;
      section.querySelector("[data-market-start]").hidden = button.dataset.market !== "home";
      section.querySelector("[data-market-contact]").hidden = button.dataset.market === "home";
      section.querySelector("[data-market-announcement]").textContent =
        button.dataset.productName + " · " + button.querySelector("small").textContent;
    }
    buttons.forEach(function (button) {
      button.addEventListener("click", function () {
        select(button);
      });
    });
    refreshMarketMatrix = function () {
      if (activeButton) select(activeButton);
    };
    section.classList.add("is-interactive");
    table.classList.add("is-focused");
    section.querySelector(".market-options").hidden = false;
    section.querySelector(".market-actions").hidden = false;
    document.getElementById("matrix-scroll").hidden = false;
    section.querySelector(".matrix-region").removeAttribute("tabindex");
    select(buttons[0]);
  }

  function initHeroColor() {
    var header = document.querySelector(".site-header");
    if (!header) return;
    function updateHeaderHeight() {
      document.documentElement.style.setProperty(
        "--site-header-height",
        header.offsetHeight + "px",
      );
    }
    updateHeaderHeight();
    if ("ResizeObserver" in window)
      new ResizeObserver(updateHeaderHeight).observe(header);
    else window.addEventListener("resize", updateHeaderHeight);
  }

  function initFeatureTracks() {
    var refreshers = [];
    document.querySelectorAll(".feature-chapter").forEach(function (chapter) {
      var track = chapter.querySelector(".feature-grid");
      var controls = chapter.querySelector(".feature-controls");
      var previous = controls.querySelector("[data-feature-prev]");
      var next = controls.querySelector("[data-feature-next]");
      function rtl() {
        return document.documentElement.dir === "rtl";
      }
      function update() {
        var bounds = track.getBoundingClientRect();
        var first = track.firstElementChild.getBoundingClientRect();
        var last = track.lastElementChild.getBoundingClientRect();
        controls.hidden = track.scrollWidth <= track.clientWidth + 2;
        previous.disabled = rtl()
          ? first.right <= bounds.right + 5
          : first.left >= bounds.left - 5;
        next.disabled = rtl()
          ? last.left >= bounds.left - 5
          : last.right <= bounds.right + 5;
      }
      function move(direction) {
        var distance = track.firstElementChild.getBoundingClientRect().width
          + parseFloat(getComputedStyle(track).columnGap);
        track.scrollBy({
          left: distance * direction * (rtl() ? -1 : 1),
          behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches
            ? "auto" : "smooth",
        });
      }
      previous.addEventListener("click", function () { move(-1); });
      next.addEventListener("click", function () { move(1); });
      track.addEventListener("scroll", update, { passive: true });
      track.addEventListener("keydown", function (event) {
        if (event.target !== track) return;
        if (event.key === "ArrowRight" || event.key === "ArrowLeft") {
          event.preventDefault();
          move((event.key === "ArrowRight" ? 1 : -1) * (rtl() ? -1 : 1));
        } else if (event.key === "Home" || event.key === "End") {
          event.preventDefault();
          track.scrollTo({
            left: event.key === "Home" ? 0 : track.scrollWidth * (rtl() ? -1 : 1),
            behavior: "auto",
          });
        }
      });
      window.addEventListener("resize", update);
      if ("ResizeObserver" in window) new ResizeObserver(update).observe(track);
      refreshers.push(function () {
        track.scrollTo({left: 0, behavior: "auto"});
        window.requestAnimationFrame(update);
      });
      update();
    });
    refreshFeatureTracks = function () {
      refreshers.forEach(function (refresh) { refresh(); });
    };
  }

  function initEditionContact() {
    var dialog = document.getElementById("edition-contact");
    var form = document.getElementById("edition-contact-form");
    if (!dialog || !form) return;
    var edition = form.elements.edition;
    var status = document.getElementById("contact-status");
    var submit = form.querySelector('[type="submit"]');
    var lastTrigger;
    function open(trigger) {
      lastTrigger = trigger;
      edition.value = trigger.dataset.edition || "";
      status.textContent = "";
      delete status.dataset.i18n;
      status.removeAttribute("data-state");
      dialog.showModal();
      edition.focus();
    }
    document.querySelectorAll("[data-contact-open]").forEach(function (trigger) {
      trigger.addEventListener("click", function () {
        var market = document.querySelector("[data-market-interaction]");
        var selected = market && market.querySelector('[data-market][aria-pressed="true"]');
        if (selected && selected.dataset.market !== "home") {
          trigger.dataset.edition = selected.dataset.market.charAt(0).toUpperCase() + selected.dataset.market.slice(1);
        }
        open(trigger);
      });
    });
    dialog.querySelector("[data-contact-close]").addEventListener("click", function () { dialog.close(); });
    dialog.addEventListener("click", function (event) {
      if (event.target === dialog) dialog.close();
    });
    dialog.addEventListener("close", function () {
      if (lastTrigger) lastTrigger.focus();
    });
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      if (!form.reportValidity()) return;
      submit.disabled = true;
      status.dataset.i18n = "contact.sending";
      status.textContent = "Sending…";
      status.dataset.state = "sending";
      fetch("/api/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          edition: edition.value,
          email: form.elements.email.value.trim(),
          message: form.elements.message.value.trim(),
          website: form.elements.website.value,
        }),
      }).then(function (response) {
        if (!response.ok) throw new Error("send failed");
        status.dataset.i18n = "contact.success";
        status.textContent = "Message sent. We’ll be in touch.";
        status.dataset.state = "success";
        form.reset();
      }).catch(function () {
        status.dataset.i18n = "contact.error";
        status.textContent = "We couldn’t send your message. Please try again.";
        status.dataset.state = "error";
      }).finally(function () { submit.disabled = false; });
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    initPricing();
    initDemo();
    initMarketMatrix();
    initSectionRail();
    initHeroColor();
    initFeatureTracks();
    initEditionContact();
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
