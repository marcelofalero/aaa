(function () {
  const initTable = function (wrapper) {
    if (wrapper.dataset.jsInitialized) return;
    wrapper.dataset.jsInitialized = "true";

    const table = wrapper.querySelector('.interactive-table');
    if (!table) return;

    const filterInput = wrapper.querySelector('.table-filter-input');
    const rows = table.querySelectorAll('.data-row');
    const separators = table.querySelectorAll('.table-separator');

    // Click handling
    table.addEventListener('click', function (e) {
      const row = e.target.closest('.data-row');
      if (e.target.tagName === 'A' || !row) return;

      const targetId = row.getAttribute('data-target');
      const targetRow = document.getElementById(targetId);

      if (targetRow) {
        const isVisible = targetRow.style.display === 'table-row';

        const allDescRows = table.querySelectorAll('.description-row');
        allDescRows.forEach(r => r.style.display = 'none');

        const allDataRows = table.querySelectorAll('.data-row');
        allDataRows.forEach(r => r.classList.remove('active-row'));

        if (!isVisible) {
          targetRow.style.display = 'table-row';
          row.classList.add('active-row');
        }
      }
    });

    // Filter handling
    if (filterInput) {
      filterInput.addEventListener('input', function () {
        const query = this.value.toLowerCase().trim();
        rows.forEach(row => {
          const text = row.textContent.toLowerCase();
          const targetId = row.getAttribute('data-target');
          const descRow = document.getElementById(targetId);

          if (text.includes(query)) {
            row.style.display = 'table-row';
          } else {
            row.style.display = 'none';
            if (descRow) descRow.style.display = 'none';
            row.classList.remove('active-row');
          }
        });

        separators.forEach(sep => {
          let next = sep.nextElementSibling;
          let hasVisible = false;
          while (next && !next.classList.contains('table-separator')) {
            if (next.classList.contains('data-row') && next.style.display !== 'none') {
              hasVisible = true;
              break;
            }
            next = next.nextElementSibling;
          }
          sep.style.display = hasVisible ? 'table-row' : 'none';
        });
      });
    }
  };

  const bindAllTables = () => {
    document.querySelectorAll('.table-wrapper').forEach(initTable);
  };

  // Run immediately, in case script was deferred or loaded after DOM
  bindAllTables();

  // Run on DOMContentLoaded, in case script was in head
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bindAllTables);
  }
})();
