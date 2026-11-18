(function () {
  "use strict";

  const toastHost = document.getElementById("toastHost");

  /* ---------- نمایش پیام ---------- */
  function showToast(message, type) {
    if (!toastHost) return;

    const toast = document.createElement("div");
    toast.className = "toast toast--" + (type || "info");
    toast.textContent = message;
    toastHost.appendChild(toast);

    requestAnimationFrame(function () {
      toast.classList.add("is-visible");
    });

    setTimeout(function () {
      toast.classList.remove("is-visible");
      setTimeout(function () {
        toast.remove();
      }, 220);
    }, 2800);
  }

  /* ---------- کپی متن ---------- */
  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text);
    }

    return new Promise(function (resolve, reject) {
      const textarea = document.createElement("textarea");
      textarea.value = text;
      textarea.style.position = "fixed";
      textarea.style.opacity = "0";
      document.body.appendChild(textarea);
      textarea.select();

      try {
        document.execCommand("copy");
        resolve();
      } catch (error) {
        reject(error);
      } finally {
        textarea.remove();
      }
    });
  }

  /* ---------- کلیک‌های عمومی ---------- */
  document.addEventListener("click", function (event) {
    /* کپی مقدار */
    const copyEl = event.target.closest("[data-copy]");
    if (copyEl) {
      event.preventDefault();
      const value =
        copyEl.getAttribute("data-copy") || copyEl.textContent.trim();

      copyText(value)
        .then(function () {
          showToast("کپی شد: " + value, "success");
        })
        .catch(function () {
          showToast("کپی انجام نشد.", "error");
        });

      return;
    }

    /* فعال‌کردن آیتم منوی کناری */
    const navItem = event.target.closest(".nav-item");
    if (navItem) {
      document.querySelectorAll(".nav-item").forEach(function (item) {
        item.classList.remove("nav-item--active");
        item.removeAttribute("aria-current");
      });

      navItem.classList.add("nav-item--active");
      navItem.setAttribute("aria-current", "page");
    }

    /* پیام‌های data-toast */
    const toastEl = event.target.closest("[data-toast]");
    if (toastEl) {
      event.preventDefault();
      showToast(
        toastEl.getAttribute("data-toast"),
        toastEl.getAttribute("data-toast-type") || "info",
      );
    }
  });

  /* ---------- تغییر تصویر پروفایل ---------- */
  const avatarBtn = document.getElementById("avatarBtn");
  const avatarInput = document.getElementById("avatarInput");
  const avatarBox = document.getElementById("avatarBox");

  if (avatarBtn && avatarInput && avatarBox) {
    avatarBtn.addEventListener("click", function (event) {
      event.stopPropagation();
      avatarInput.click();
    });

    avatarInput.addEventListener("change", function () {
      const file = avatarInput.files && avatarInput.files[0];
      if (!file) return;

      if (!file.type.startsWith("image/")) {
        showToast("لطفاً فقط فایل تصویری انتخاب کنید.", "error");
        avatarInput.value = "";
        return;
      }

      if (file.size > 2 * 1024 * 1024) {
        showToast("حجم تصویر نباید بیشتر از ۲ مگابایت باشد.", "error");
        avatarInput.value = "";
        return;
      }

      const reader = new FileReader();

      reader.onload = function (event) {
        avatarBox.innerHTML =
          '<img src="' + event.target.result + '" alt="تصویر پروفایل کاربر">';
        showToast("تصویر پروفایل با موفقیت تغییر کرد.", "success");
      };

      reader.onerror = function () {
        showToast("خواندن تصویر ناموفق بود.", "error");
      };

      reader.readAsDataURL(file);
    });
  }
})();
