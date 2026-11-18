(function () {
  'use strict';

  const toastHost = document.getElementById('toastHost');

  /* ---------- نمایش پیام ---------- */
  function showToast(message, type) {
    if (!toastHost) return;

    const toast = document.createElement('div');
    toast.className = 'toast toast--' + (type || 'info');
    toast.textContent = message;
    toastHost.appendChild(toast);

    requestAnimationFrame(function () {
      toast.classList.add('is-visible');
    });

    setTimeout(function () {
      toast.classList.remove('is-visible');
      setTimeout(function () {
        toast.remove();
      }, 220);
    }, 2800);
  }

  /* ---------- پیام‌های data-toast ---------- */
  document.addEventListener('click', function (event) {
    const toastEl = event.target.closest('[data-toast]');
    if (!toastEl) return;

    const href = toastEl.getAttribute('href');
    if (!href || href === '#') {
      event.preventDefault();
    }

    showToast(
      toastEl.getAttribute('data-toast'),
      toastEl.getAttribute('data-toast-type') || 'info'
    );
  });

  /* ---------- مدیریت آواتار ---------- */
  const avatarImg = document.getElementById('avatarImg');
  const avatarFileInput = document.getElementById('avatarFileInput');
  const avatarEditBtn = document.getElementById('avatarEditBtn');
  const avatarUploadBtn = document.getElementById('avatarUploadBtn');
  const avatarDeleteBtn = document.getElementById('avatarDeleteBtn');

  const defaultAvatarHTML = avatarImg ? avatarImg.innerHTML : '';

  function openFilePicker() {
    if (avatarFileInput) avatarFileInput.click();
  }

  if (avatarEditBtn) avatarEditBtn.addEventListener('click', openFilePicker);
  if (avatarUploadBtn) avatarUploadBtn.addEventListener('click', openFilePicker);

  if (avatarFileInput) {
    avatarFileInput.addEventListener('change', function () {
      const file = avatarFileInput.files && avatarFileInput.files[0];
      if (!file) return;

      if (!file.type.startsWith('image/')) {
        showToast('لطفاً فقط فایل تصویری انتخاب کنید.', 'error');
        avatarFileInput.value = '';
        return;
      }

      if (file.size > 2 * 1024 * 1024) {
        showToast('حجم تصویر نباید بیشتر از ۲ مگابایت باشد.', 'error');
        avatarFileInput.value = '';
        return;
      }

      const reader = new FileReader();

      reader.onload = function (event) {
        avatarImg.innerHTML =
          '<img src="' + event.target.result + '" alt="تصویر پروفایل کاربر">';
        showToast('تصویر پروفایل با موفقیت بارگذاری شد.', 'success');
      };

      reader.onerror = function () {
        showToast('خواندن تصویر ناموفق بود.', 'error');
      };

      reader.readAsDataURL(file);
      avatarFileInput.value = '';
    });
  }

  if (avatarDeleteBtn) {
    avatarDeleteBtn.addEventListener('click', function () {
      if (avatarImg) {
        avatarImg.innerHTML = defaultAvatarHTML;
        showToast('تصویر پروفایل حذف شد.', 'info');
      }
    });
  }

  /* ---------- قالب‌بندی شماره شبا ---------- */
  const shebaInput = document.getElementById('sheba');

  if (shebaInput) {
    shebaInput.addEventListener('input', function () {
      const digits = shebaInput.value.replace(/\D/g, '').slice(0, 24);
      let formatted = '';

      for (let i = 0; i < digits.length; i++) {
        if (i > 0 && i % 4 === 0) formatted += ' ';
        formatted += digits[i];
      }

      shebaInput.value = formatted;
    });
  }
})();