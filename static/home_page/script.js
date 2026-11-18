(function () {
  "use strict";

  /* =====================================================
     Persian Countdown Timer
     ===================================================== */
  var persianDigits = ["۰", "۱", "۲", "۳", "۴", "۵", "۶", "۷", "۸", "۹"];

  function toPersianNumber(n) {
    return String(n)
      .padStart(2, "0")
      .split("")
      .map(function (d) {
        return persianDigits[parseInt(d, 10)] || d;
      })
      .join("");
  }

  var totalSeconds = 8 * 3600 + 44 * 60 + 19; // 08:44:19
  var hoursEl = document.getElementById("hours-val");
  var minEl = document.getElementById("minutes-val");
  var secEl = document.getElementById("seconds-val");

  if (hoursEl && minEl && secEl) {
    setInterval(function () {
      if (totalSeconds > 0) {
        totalSeconds--;
        var h = Math.floor(totalSeconds / 3600);
        var m = Math.floor((totalSeconds % 3600) / 60);
        var s = totalSeconds % 60;
        hoursEl.textContent = toPersianNumber(h);
        minEl.textContent = toPersianNumber(m);
        secEl.textContent = toPersianNumber(s);
      }
    }, 1000);
  }

  /* =====================================================
     Bestseller Tabs
     ===================================================== */
  var tabs = document.querySelectorAll(".bestseller-tab");
  tabs.forEach(function (tab) {
    tab.addEventListener("click", function () {
      tabs.forEach(function (t) {
        t.classList.remove("active");
      });
      this.classList.add("active");
    });
  });
})();
