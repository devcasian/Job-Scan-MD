document.addEventListener('DOMContentLoaded', function() {
    const searchForm = document.getElementById('searchForm');
    const searchButton = document.getElementById('searchButton');
    const loadingIndicator = document.getElementById('loadingIndicator');

    searchForm.addEventListener('submit', function(e) {
        e.preventDefault();
        searchButton.disabled = true;
        loadingIndicator.style.display = 'block';
        
        this.submit();
    });
});
