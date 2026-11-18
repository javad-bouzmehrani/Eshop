(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {

    /* =====================================================
       View Switcher: Grid / List
       ===================================================== */
    var gridBtn = document.getElementById('view-grid');
    var listBtn = document.getElementById('view-list');
    var productContainer = document.getElementById('product-grid');

    if (gridBtn && listBtn && productContainer) {
      gridBtn.addEventListener('click', function () {
        gridBtn.classList.add('active');
        listBtn.classList.remove('active');
        productContainer.classList.remove('list-view');
      });

      listBtn.addEventListener('click', function () {
        listBtn.classList.add('active');
        gridBtn.classList.remove('active');
        productContainer.classList.add('list-view');
      });
    }

    /* =====================================================
       Reset Filters
       ===================================================== */
    var resetBtn = document.getElementById('reset-filters');
    if (resetBtn) {
      resetBtn.addEventListener('click', function () {
        // Uncheck all checkboxes
        var checkboxes = document.querySelectorAll('.cbx, .toggle-card input[type="checkbox"]');
        checkboxes.forEach(function (cb) { cb.checked = false; });

        // Reset range slider
        var range = document.querySelector('.range-input');
        if (range) range.value = range.min;

        // Clear brand search
        var brandSearch = document.querySelector('.brand-search-input');
        if (brandSearch) brandSearch.value = '';

        // Deselect color swatches
        var swatches = document.querySelectorAll('.swatch.selected');
        swatches.forEach(function (s) { s.classList.remove('selected'); });
      });
    }

    /* =====================================================
       Color Swatch Selection
       ===================================================== */
    var swatches = document.querySelectorAll('.swatch');
    swatches.forEach(function (swatch) {
      swatch.addEventListener('click', function () {
        // Toggle: only one selected at a time
        swatches.forEach(function (s) { s.classList.remove('selected'); });
        this.classList.add('selected');
      });
    });

    /* =====================================================
       Sort Buttons
       ===================================================== */
    var sortBtns = document.querySelectorAll('.sort-btn');
    sortBtns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        sortBtns.forEach(function (b) { b.classList.remove('active'); });
        this.classList.add('active');
      });
    });

  });

})();