document.addEventListener('DOMContentLoaded', function () {
    const searchForm = document.getElementById('search-form');
    searchForm.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent form submission

        const searchQuery = document.getElementById('search-query').value.trim();
        if (searchQuery !== '') {
            fetch('/',
                {
                    method: 'POST',
                    body: new URLSearchParams({
                        'search_query': searchQuery
                    })
                })
                .then(response => response.text())
                .then(data => {
                    const cardContainer = document.getElementById('card-container');
                    cardContainer.innerHTML = data;
                    searchForm.reset(); // Reset the form input field
                })
                .catch(error => console.error('Error:', error));
        }
    });
});

