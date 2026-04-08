(function() {
    let fuse;
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');

    if (!searchInput || !searchResults) return;

    // Fetch index
    fetch('/index.json')
        .then(response => response.json())
        .then(data => {
            const options = {
                keys: ['title', 'description', 'content', 'section'],
                threshold: 0.4,
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
        displayResults(results);
    });

    function displayResults(results) {
        if (results.length === 0) {
            searchResults.innerHTML = '<div class="pa3 silver">No results found.</div>';
        } else {
            const html = results.slice(0, 10).map(result => {
                const item = result.item;
                return `
                    <a href="${item.url}" class="db pa3 no-underline hover-bg-neon-cyan-20 border-b border-white-10">
                        <div class="neon-cyan fw6 mb1">${item.title}</div>
                        <div class="f7 silver truncate">${item.description}</div>
                    </a>
                `;
            }).join('');
            searchResults.innerHTML = html;
        }
        searchResults.classList.remove('hidden');
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
})();
