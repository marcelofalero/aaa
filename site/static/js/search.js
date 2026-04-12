window.addEventListener('DOMContentLoaded', () => {
    let fuse;
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');

    if (!searchInput || !searchResults) return;

    // Hotkey for search
    document.addEventListener('keydown', (e) => {
        if (e.key === '/' && document.activeElement !== searchInput) {
            e.preventDefault();
            searchInput.focus();
        }
    });

    // Fetch index
    const lang = document.documentElement.lang || 'en';
    const indexPath = lang.startsWith('es') ? '/es/index.json' : '/index.json';

    fetch(indexPath)
        .then(response => response.json())
        .then(data => {
            const options = {
                keys: ['title', 'description', 'content', 'section'],
                threshold: 0.3,
                includeMatches: true
            };
            fuse = new Fuse(data, options);
        })
        .catch(err => {
            console.error('Error loading search index:', err);
        });

    searchInput.addEventListener('input', () => {
        const query = searchInput.value;
        if (!fuse || query.length < 2) {
            searchResults.innerHTML = '';
            searchResults.classList.add('hidden');
            return;
        }

        const results = fuse.search(query);
        displayResults(results, lang);
    });

    function displayResults(results, lang) {
        if (results.length === 0) {
            const noMatchesMsg = lang.startsWith('es') ? 'No se encontraron coincidencias.' : 'No matches found in library.';
            searchResults.innerHTML = `<div class="pa3 silver f6 italic">${noMatchesMsg}</div>`;
        } else {
            const html = results.slice(0, 8).map(result => {
                const item = result.item;
                const sectionRaw = item.section || 'General';
                const section = sectionRaw.charAt(0).toUpperCase() + sectionRaw.slice(1);
                
                // Icon mapping
                let icon = '📄'; // Default
                if (sectionRaw.includes('equipment')) icon = '🛠️';
                if (sectionRaw.includes('weapon')) icon = '⚔️';
                if (sectionRaw.includes('skill')) icon = '🎯';
                if (sectionRaw.includes('rules')) icon = '📖';
                if (sectionRaw.includes('species')) icon = '👥';
                if (sectionRaw.includes('profession')) icon = '👷';
                if (sectionRaw.includes('cybernetics')) icon = '🦾';

                // Simple highlighting logic
                let title = item.title;
                if (result.matches) {
                    result.matches.forEach(match => {
                        if (match.key === 'title') {
                            title = highlightText(title, match.indices);
                        }
                    });
                }

                return `
                    <a href="${item.url}" class="pa2 no-underline search-result-item flex items-center" style="display: flex !important; align-items: center !important; text-decoration: none !important;">
                        <span class="mr3 f5 flex-shrink-0" style="width: 24px; text-align: center; display: inline-block;" title="${section}">${icon}</span>
                        <span class="neon-cyan fw6 f7 truncate flex-auto" style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${title}</span>
                    </a>
                `;
            }).join('');
            searchResults.innerHTML = html;
        }
        searchResults.classList.remove('hidden');
    }

    function highlightText(text, indices) {
        let result = '';
        let lastIndex = 0;
        
        // Sort indices to ensure we process them in order
        const sortedIndices = [...indices].sort((a, b) => a[0] - b[0]);
        
        sortedIndices.forEach(([start, end]) => {
            result += text.substring(lastIndex, start);
            result += `<span class="search-highlight">${text.substring(start, end + 1)}</span>`;
            lastIndex = end + 1;
        });
        
        result += text.substring(lastIndex);
        return result;
    }

    // Close results when clicking outside
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.search-container')) {
            searchResults.classList.add('hidden');
        }
    });

    // Re-show results when clicking input
    searchInput.addEventListener('click', () => {
        if (searchResults.innerHTML !== '') {
            searchResults.classList.remove('hidden');
        }
    });
});
