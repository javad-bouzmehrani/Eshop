/* ========== TABS ========== */
function switchTab(index) {
  const tabs = document.querySelectorAll(".tab-btn");
  const panes = document.querySelectorAll(".tab-pane");

  tabs.forEach((tab, i) => {
    tab.classList.toggle("is-active", i === index);
  });

  panes.forEach((pane, i) => {
    pane.classList.toggle("is-active", i === index);
  });
}

/* ========== IMAGE GALLERY========== */
function switchImage(button) {
  document.querySelectorAll(".thumb-btn").forEach((btn) => {
    btn.classList.remove("is-active");
  });
  button.classList.add("is-active");

  const newSrc = button.dataset.src;
  if (!newSrc) return;
  setMainImage(newSrc);
}

/* ========== GALLERY MODAL ========== */
function openGalleryModal(event) {
  if (event) event.preventDefault();
  const modal = document.getElementById("gallery-modal");
  if (!modal) return;
  modal.classList.add("is-open");
  document.body.style.overflow = "hidden";
}

function closeGalleryModal() {
  const modal = document.getElementById("gallery-modal");
  if (!modal) return;
  modal.classList.remove("is-open");
  document.body.style.overflow = "";
}

function pickGalleryImage(src) {
  setMainImage(src);
  closeGalleryModal();
}

function setMainImage(src) {
  const mainImg = document.getElementById("main-product-img");
  if (!mainImg || !src) return;

  mainImg.style.opacity = "0.4";
  setTimeout(() => {
    mainImg.src = src;
    mainImg.style.opacity = "1";
  }, 150);
}

document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") closeGalleryModal();
});
/* ========== COLOR ========== */
function selectColor(button, name) {
  document.querySelectorAll(".color-btn").forEach((btn) => {
    btn.classList.remove("is-active");
  });

  button.classList.add("is-active");

  const selectedColorName = document.getElementById("selected-color-name");

  if (selectedColorName) {
    selectedColorName.textContent = name;
  }
}

/* ========== CAPACITY ========== */
function selectCapacity(button) {
  document.querySelectorAll(".capacity-btn").forEach((btn) => {
    btn.classList.remove("is-active");
  });

  button.classList.add("is-active");
}

/* ========== QUANTITY ========== */
let qty = 1;

function toPersianNumber(number) {
  const persianDigits = ["۰", "۱", "۲", "۳", "۴", "۵", "۶", "۷", "۸", "۹"];

  return String(number).replace(/\d/g, (digit) => persianDigits[Number(digit)]);
}

function changeQty(delta) {
  const input = document.getElementById("quantity-display");
  if (!input) return;

  let current = parseInt(input.value, 10) || 1;
  current = Math.max(1, Math.min(5, current + delta));
  input.value = current;
}

/* ========== FAVORITE ========== */
let isFavorite = false;

function toggleFavorite() {
  isFavorite = !isFavorite;

  const favoriteButton = document.getElementById("btn-favorite");
  const favoriteIcon = document.getElementById("fav-icon");

  if (!favoriteButton || !favoriteIcon) return;

  favoriteButton.classList.toggle("is-fav", isFavorite);

  favoriteIcon.style.fill = isFavorite ? "currentColor" : "none";
  favoriteIcon.style.stroke = "currentColor";
}

/* ========== SHARE ========== */
function shareProduct() {
  if (navigator.share) {
    navigator
      .share({
        title: "سامسونگ Galaxy S24 Ultra در بازار آنلاین",
        url: window.location.href,
      })
      .catch(() => {});
  } else {
    alert("لینک کالا با موفقیت کپی شد!");
  }
}

/* ========== ADD TO CART (AJAX + Login check) ========== */
document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("add-to-cart-form");
  if (form) form.addEventListener("submit", addToCartFeedback);
});

async function addToCartFeedback(event) {
  event.preventDefault();

  const form = event.currentTarget;
  const button = document.getElementById("btn-add-cart");
  if (!button) return;

  const textElement = button.querySelector("span");
  const originalText = textElement.textContent;

  button.disabled = true;
  button.classList.remove("is-success");
  textElement.textContent = "در حال افزودن...";

  try {
    const response = await fetch(form.action, {
      method: "POST",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": form.querySelector("[name=csrfmiddlewaretoken]").value,
      },
      body: new FormData(form),
      credentials: "same-origin",
    });

    const data = await response.json();

    if (response.status === 401 && data.login_required) {
      window.location.href = data.redirect || "/auth";
      return;
    }

    if (!response.ok || !data.ok) {
      throw new Error("request failed");
    }

    /* ---- موفق ---- */
    button.classList.add("is-success");
    textElement.textContent = "✓ به سبد اضافه شد";

    const cartBadge = document.querySelector(".cart-count");
    if (cartBadge && data.cart_count != null) {
      cartBadge.textContent = data.cart_count;
    }

    setTimeout(() => {
      button.classList.remove("is-success");
      textElement.textContent = originalText;
      button.disabled = false;
    }, 2000);

  } catch (err) {
    button.classList.remove("is-success");
    textElement.textContent = "خطا! دوباره تلاش کنید";
    setTimeout(() => {
      textElement.textContent = originalText;
      button.disabled = false;
    }, 2000);
  }
}
/* ========== RELATED SLIDER ========== */
function scrollRelated(direction) {
  const slider = document.getElementById("related-slider");

  if (!slider) return;

  slider.scrollBy({
    left: direction * 280,
    behavior: "smooth",
  });
}

/* ========== REVIEW MODAL ========== */
function openReviewModal() {
  switchTab(1);
  alert("فرم ثبت دیدگاه باز شد.");
}
