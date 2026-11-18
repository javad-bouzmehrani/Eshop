(function () {
  "use strict";

  /* =====================================================
     Switch Between Login / Register Tabs
     ===================================================== */
  function switchAuthTab(target) {
    var tabLogin = document.getElementById("tab-login");
    var tabRegister = document.getElementById("tab-register");
    var secLogin = document.getElementById("section-login");
    var secRegister = document.getElementById("section-register");

    if (!tabLogin || !tabRegister || !secLogin || !secRegister) return;

    var showLogin = target === "login";

    secLogin.classList.toggle("hidden", !showLogin);
    secRegister.classList.toggle("hidden", showLogin);

    tabLogin.classList.toggle("active", showLogin);
    tabRegister.classList.toggle("active", !showLogin);

    tabLogin.setAttribute("aria-selected", showLogin ? "true" : "false");
    tabRegister.setAttribute("aria-selected", showLogin ? "false" : "true");
  }

  /* =====================================================
     Toggle Password Visibility
     ===================================================== */
  function togglePasswordVisibility(inputId, btn) {
    if (!inputId || !btn) return;

    var input = document.getElementById(inputId);
    if (!input) return;

    var icon = btn.querySelector(".material-symbols-outlined");

    if (input.type === "password") {
      input.type = "text";
      if (icon) icon.textContent = "visibility_off";
      btn.setAttribute("aria-label", "مخفی کردن رمز عبور");
    } else {
      input.type = "password";
      if (icon) icon.textContent = "visibility";
      btn.setAttribute("aria-label", "نمایش رمز عبور");
    }
  }

  /* =====================================================
     EVENT BINDINGS
     ===================================================== */
  document.addEventListener("DOMContentLoaded", function () {
    var tabLogin = document.getElementById("tab-login");
    var tabRegister = document.getElementById("tab-register");

    if (tabLogin) {
      tabLogin.addEventListener("click", function () {
        switchAuthTab("login");
      });
      tabLogin.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          switchAuthTab("login");
        }
      });
    }

    if (tabRegister) {
      tabRegister.addEventListener("click", function () {
        switchAuthTab("register");
      });
      tabRegister.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") {
          e.preventDefault();
          switchAuthTab("register");
        }
      });
    }

    var toggleBtns = document.querySelectorAll("[data-toggle-pass]");
    toggleBtns.forEach(function (btn) {
      btn.addEventListener("click", function () {
        var targetId = this.getAttribute("data-toggle-pass");
        togglePasswordVisibility(targetId, this);
      });
    });
  });
})();