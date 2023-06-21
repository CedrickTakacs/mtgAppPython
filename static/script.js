document.addEventListener("DOMContentLoaded", function() {
    var searchForm = document.getElementById("search-form");
    searchForm.addEventListener("submit", function(event) {
        event.preventDefault();
        var searchQuery = document.getElementById("search-query").value;
        fetch("/", {
            method: "POST",
            body: JSON.stringify({ search_query: searchQuery }),
            headers: {
                "Content-Type": "application/json",
            }
        }).then(function(response) {
            return response.text();
        }).then(function(html) {
            document.getElementById("card-container").innerHTML = html;
        });
    });
});
