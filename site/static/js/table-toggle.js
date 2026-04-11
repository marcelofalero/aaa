(function () {
  const initTable = function (wrapper) {
    if (wrapper.dataset.jsInitialized) return;
    wrapper.dataset.jsInitialized = "true";

    const table = wrapper.querySelector('.interactive-table');
    if (!table) return;

    const filterInput = wrapper.querySelector('.table-filter-input');
    const separators = table.querySelectorAll('.table-separator');

    // Accordion Toggle logic
    const setGroupState = (sep, isExpanded) => {
      const chevron = sep.querySelector('.chevron');
      sep.setAttribute('data-expanded', isExpanded ? 'true' : 'false');
      if (chevron) chevron.textContent = isExpanded ? '▼' : '▶';

      let next = sep.nextElementSibling;
      while (next && !next.classList.contains('table-separator')) {
        if (!isExpanded) {
          next.style.display = 'none';
          if (next.classList.contains('data-row')) next.classList.remove('active-row');
          if (next.classList.contains('description-row')) next.style.display = 'none';
        } else {
          if (next.classList.contains('data-row')) {
            next.style.display = 'table-row';
          }
        }
        next = next.nextElementSibling;
      }
    };

    // Initial State based on data-expanded
    separators.forEach(sep => {
      const isExpanded = sep.getAttribute('data-expanded') === 'true';
      setGroupState(sep, isExpanded);
    });

    // Click handling
    table.addEventListener('click', function (e) {
      // 1. Accordion Toggle
      const sep = e.target.closest('.accordion-toggle');
      if (sep) {
        const isExpanded = sep.getAttribute('data-expanded') === 'true';
        setGroupState(sep, !isExpanded);
        return;
      }

      // 2. Data Row Description Toggle
      const row = e.target.closest('.data-row');
      if (e.target.tagName === 'A' || !row) return;

      const targetId = row.getAttribute('data-target');
      const targetRow = document.getElementById(targetId);

      if (targetRow) {
        const isVisible = targetRow.style.display === 'table-row';

        // Collapse all descriptions in this table
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
        const rows = table.querySelectorAll('.data-row');

        if (query === '') {
          // Restore accordion state
          separators.forEach(sep => {
            const isExpanded = sep.getAttribute('data-expanded') === 'true';
            setGroupState(sep, isExpanded);
            sep.style.display = 'table-row';
          });
          return;
        }

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
          // Temporarily show matches regardless of accordion state during filter
          if (hasVisible) {
            const chevron = sep.querySelector('.chevron');
            if (chevron) chevron.textContent = '▼';
          }
        });
      });
    }
  };

  const bindAllTables = () => {
    document.querySelectorAll('.table-wrapper').forEach(initTable);
    // Handle Hash Deep-Linking
    const expandFromHash = () => {
      const hash = decodeURIComponent(window.location.hash.substring(1));
      if (!hash) return;

      const targetRow = document.getElementById(hash);
      if (targetRow && targetRow.classList.contains('data-row')) {
        // Find preceding separator
        let prev = targetRow.previousElementSibling;
        while (prev && !prev.classList.contains('table-separator')) {
          prev = prev.previousElementSibling;
        }
        if (prev) {
          setGroupState(prev, true);
        }

        // Expand description
        const targetId = targetRow.getAttribute('data-target');
        const descRow = document.getElementById(targetId);
        if (descRow) {
          descRow.style.display = 'table-row';
          targetRow.classList.add('active-row');
          
          // Scroll to row
          setTimeout(() => {
            targetRow.scrollIntoView({ behavior: 'smooth', block: 'center' });
          }, 100);
        }
      }
    };

    // Run on load
    expandFromHash();

    // Run on hash change (for subsequent searches)
    window.addEventListener('hashchange', expandFromHash);
  };

  // Run immediately, in case script was deferred or loaded after DOM
  bindAllTables();

  // Run on DOMContentLoaded, in case script was in head
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bindAllTables);
  }
})();
