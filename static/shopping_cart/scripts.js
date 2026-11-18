(function () {
  "use strict";

  var PERSIAN_DIGITS = ["۰", "۱", "۲", "۳", "۴", "۵", "۶", "۷", "۸", "۹"];

  function toPersian(num) {
    return String(num).replace(/\d/g, function (d) {
      return PERSIAN_DIGITS[Number(d)];
    });
  }

  function formatPrice(n) {
    var s = Math.round(n).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    return toPersian(s);
  }

  function showToast(msg) {
    var toast = document.getElementById("toast");
    var text = document.getElementById("toast-text");
    if (!toast || !text) return;
    text.textContent = msg;
    toast.classList.add("show");
    clearTimeout(showToast._t);
    showToast._t = setTimeout(function () {
      toast.classList.remove("show");
    }, 2200);
  }

  function getItems() {
    return Array.prototype.slice.call(
      document.querySelectorAll("#items-list .item-card")
    );
  }

  function getQty(card) {
    var el = card.querySelector(".qty-value");
    if (!el) return 1;
    var raw = el.textContent.trim();
    var western = raw.replace(/[۰-۹]/g, function (d) {
      return String("۰۱۲۳۴۵۶۷۸۹".indexOf(d));
    });
    var n = parseInt(western, 10);
    return isNaN(n) || n < 1 ? 1 : n;
  }

  function setQty(card, qty) {
    var el = card.querySelector(".qty-value");
    if (el) el.textContent = toPersian(qty);
    var minusBtn = card.querySelector('[data-action="minus"] .material-symbols-outlined');
    if (minusBtn) {
      minusBtn.textContent = qty <= 1 ? "delete" : "remove";
    }
  }

  function recalc() {
    var items = getItems();
    var count = 0;
    var subtotal = 0;
    var discount = 0;

    items.forEach(function (card) {
      var qty = getQty(card);
      var price = Number(card.getAttribute("data-price")) || 0;
      var old = Number(card.getAttribute("data-old")) || price;
      count += qty;
      subtotal += old * qty;
      discount += (old - price) * qty;
    });

    var total = subtotal - discount;

    var el;
    el = document.getElementById("calc-count");
    if (el) el.textContent = toPersian(count);

    el = document.getElementById("calc-subtotal");
    if (el) el.textContent = formatPrice(subtotal) + " تومان";

    el = document.getElementById("calc-discount");
    if (el) el.textContent = formatPrice(discount) + "- تومان";

    el = document.getElementById("calc-total");
    if (el) el.textContent = formatPrice(total);

    el = document.getElementById("calc-points");
    if (el) el.textContent = "+" + toPersian(Math.floor(total / 1000000) * 2) + " امتیاز";

    el = document.getElementById("items-count-badge");
    if (el) el.textContent = toPersian(count) + " مورد";

    el = document.getElementById("step-item-count");
    if (el) el.textContent = toPersian(count) + " کالا";

    el = document.getElementById("header-cart-count");
    if (el) el.textContent = toPersian(count);

    // Free shipping progress (threshold 500000)
    var FREE_THRESHOLD = 500000;
    var remain = Math.max(0, FREE_THRESHOLD - total);
    var pct = Math.min(100, (total / FREE_THRESHOLD) * 100);

    el = document.getElementById("free-ship-remain");
    if (el) {
      if (remain <= 0) {
        el.textContent = "۰ تومان";
      } else {
        el.textContent = formatPrice(remain) + " تومان";
      }
    }

    el = document.getElementById("ship-progress");
    if (el) el.style.width = pct + "%";
  }

  function removeItem(card) {
    card.style.transition = "opacity 0.25s ease, transform 0.25s ease";
    card.style.opacity = "0";
    card.style.transform = "translateX(20px)";
    setTimeout(function () {
      card.remove();
      recalc();
      showToast("کالا از سبد حذف شد");
      if (getItems().length === 0) {
        var list = document.getElementById("items-list");
        if (list) {
          list.innerHTML =
            '<p style="text-align:center;padding:2rem;color:var(--outline)">سبد خرید شما خالی است.</p>';
        }
      }
    }, 250);
  }

  // Event delegation on items list
  var list = document.getElementById("items-list");
  if (list) {
    list.addEventListener("click", function (e) {
      var btn = e.target.closest("[data-action]");
      if (!btn) return;
      var card = btn.closest(".item-card");
      if (!card) return;
      var action = btn.getAttribute("data-action");
      var qty = getQty(card);

      if (action === "plus") {
        if (qty < 10) {
          setQty(card, qty + 1);
          recalc();
        }
      } else if (action === "minus") {
        if (qty <= 1) {
          removeItem(card);
        } else {
          setQty(card, qty - 1);
          recalc();
        }
      } else if (action === "remove") {
        removeItem(card);
      } else if (action === "save") {
        removeItem(card);
        var saved = document.getElementById("saved-count");
        if (saved) {
          var n = parseInt(
            saved.textContent.replace(/[۰-۹]/g, function (d) {
              return String("۰۱۲۳۴۵۶۷۸۹".indexOf(d));
            }),
            10
          );
          if (isNaN(n)) n = 0;
          saved.textContent = toPersian(n + 1);
        }
        showToast("کالا برای بعد ذخیره شد");
      }
    });
  }

  // Clear all
  var clearBtn = document.getElementById("btn-clear-all");
  if (clearBtn) {
    clearBtn.addEventListener("click", function () {
      var items = getItems();
      if (!items.length) {
        showToast("سبد خرید خالی است");
        return;
      }
      items.forEach(function (card) {
        card.remove();
      });
      var listEl = document.getElementById("items-list");
      if (listEl) {
        listEl.innerHTML =
          '<p style="text-align:center;padding:2rem;color:var(--outline)">سبد خرید شما خالی است.</p>';
      }
      recalc();
      showToast("تمام اقلام حذف شدند");
    });
  }

  // Promo code
  var promoBtn = document.getElementById("btn-apply-promo");
  if (promoBtn) {
    promoBtn.addEventListener("click", function () {
      var input = document.getElementById("promo-code");
      var code = input ? input.value.trim() : "";
      if (!code) {
        showToast("کد تخفیف را وارد کنید");
        return;
      }
      showToast("کد «" + code + "» اعمال شد");
    });
  }

  // Checkout
  var checkoutBtn = document.getElementById("btn-checkout");
  if (checkoutBtn) {
    checkoutBtn.addEventListener("click", function () {
      if (getItems().length === 0) {
        showToast("سبد خرید خالی است");
        return;
      }
      showToast("در حال انتقال به مرحله ارسال...");
    });
  }

  // Saved list
  var viewSaved = document.getElementById("btn-view-saved");
  if (viewSaved) {
    viewSaved.addEventListener("click", function () {
      showToast("لیست خرید بعدی باز شد");
    });
  }

  // Newsletter
  var newsForm = document.getElementById("news-form");
  if (newsForm) {
    newsForm.addEventListener("submit", function (e) {
      e.preventDefault();
      showToast("عضویت در خبرنامه ثبت شد");
      newsForm.reset();
    });
  }

  // Initial calc
  recalc();
})();
