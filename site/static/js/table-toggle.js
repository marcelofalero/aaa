document.addEventListener('DOMContentLoaded', function() {
  const tables = document.querySelectorAll('.interactive-table');

  tables.forEach(table => {
    // Use a named function for the event listener for clarity
    function handleRowClick(e) {
      // Don't do anything if the click was on a link
      if (e.target.tagName === 'A') {
        return;
      }

      const row = e.target.closest('.data-row');
      if (!row) {
        return;
      }

      const targetId = row.getAttribute('data-target');
      const targetRow = document.getElementById(targetId);

      if (!targetRow) {
        return;
      }

      // Check if the clicked row is already active
      const isAlreadyActive = row.classList.contains('active-row');

      // First, close all description rows and deactivate all data rows
      const allDescRows = table.querySelectorAll('.description-row');
      const allDataRows = table.querySelectorAll('.data-row');

      allDescRows.forEach(r => {
        r.style.display = 'none';
      });
      allDataRows.forEach(r => {
        r.classList.remove('active-row');
      });

      // If the clicked row was not already active, open its description
      if (!isAlreadyActive) {
        targetRow.style.display = 'table-row';
        row.classList.add('active-row');
      }
    }

    table.addEventListener('click', handleRowClick);
  });
});
