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
            const html = results.slice(0, 12).map(result => {
                const item = result.item;
                const section = item.section ? item.section.charAt(0).toUpperCase() + item.section.slice(1) : 'General';
                
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
                    <a href="${item.url}" class="db pa3 no-underline search-result-item">
                        <div class="flex items-center justify-between mb1">
                            <div class="neon-cyan fw6 f5">${title}</div>
                            <span class="badge ml2">${section}</span>
                        </div>
                        <div class="f7 silver truncate o-70">${item.description || 'View details...'}</div>
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
