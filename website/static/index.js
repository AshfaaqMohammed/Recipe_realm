function performSearch() {
    var query = document.getElementsByName("query")[0].value;
    var resultsContainer = document.getElementById("searchResultsContainer");
    var AllResultsContainer = document.getElementById("searchAllResultsContainer");

    fetch(`/search?query=${query}`)
        .then(response => response.json())
        .then(results => {
            resultsContainer.innerHTML = generateResultsHTML(results);
        })
        .catch(error => console.error("Error:", error));

    fetch(`/search_all?query=${query}`)
        .then(response => response.json())
        .then(allResults => {
            AllResultsContainer.innerHTML = generateAllResultsHTML(allResults);
        })
        .catch(error => console.error("Error:", error));
}


function generateResultsHTML(results) {
    if (results.length > 0) {
        var html = '<div class="row">';
        results.forEach(recipe => {
            console.log(recipe)
            html += `<div class="col-md-4 category__link">
                        <a href="${recipe.url}" class="text-center">
                        <div class="shadow">
                            <img src="${recipe.img_url}" alt="image" loading="lazy" class="category__img">
                        </div>
                        <div class="pt-1">
                            ${recipe.name}
                        </div>
                        </a>
                    </div>`;
        });
        html += '</div>';
        return html;
    } else {
        return '<h1 style="text-align: center;">No results found.</h1>';
    }
}

function generateAllResultsHTML(allResults) {
    if (allResults.length > 0) {
        var html = '<div class="row">'; 
        allResults.forEach(recipe => {
            html += `<div class="col-md-4 category__link">
                        <a href="${recipe.url}" class="text-center">
                        <div class="shadow">
                            <img src="${recipe.img_url}" alt="image" loading="lazy" class="category__img">
                        </div>
                        <div class="pt-1">
                            ${recipe.name}
                        </div>
                        </a>
                    </div>`;
        });
        html += '</div>';
        return html;
    } else {
        return '<h1 style="text-align: center;">No results found.</h1>';
    }
}
