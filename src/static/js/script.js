document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM fully loaded and parsed");

    function toggleSearchForm() {
        var searchFormContainer = document.getElementById("searchFormContainer");
        var toggleButton = document.getElementById("toggleSearchButton");

        if (searchFormContainer.style.display === "none") {
            searchFormContainer.style.display = "block";
            toggleButton.textContent = "Hide Search Options";
        } else {
            searchFormContainer.style.display = "none";
            toggleButton.textContent = "Show Search Options";
        }
    }

    // Ensure the toggleSearchForm function is defined above this line
    var toggleButton = document.getElementById("toggleSearchButton");
    if (toggleButton) {
        toggleButton.addEventListener('click', toggleSearchForm);
        console.log("Event listener attached");
    } else {
        console.log("Toggle button not found");
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const searchForm = document.getElementById('searchForm');

    searchForm.addEventListener('submit', function (e) {
        let allEmpty = true;
        // Check all input and select elements except CSRF tokens
        searchForm.querySelectorAll('input:not([type="hidden"]), select').forEach(function (input) {
            if (input.value.trim() !== '') {
                allEmpty = false;
            }
        });

        // If all fields are empty, prevent the form from submitting
        if (allEmpty) {
            e.preventDefault();
        }
    });
});

document.addEventListener("DOMContentLoaded", function () {
    var modal = document.getElementById("chartModal");
    var img = document.getElementById("chartImage");
    var selector = document.getElementById("chartSelector");
    var span = document.getElementsByClassName("close")[0];

    selector.addEventListener('change', function () {
        var chartValue = selector.value;
        switch (chartValue) {
            case 'popularIngredients':
                img.src = popularIngredientsChart;
                break;
            case 'recipeDifficultyDistribution':
                img.src = recipeDifficultyDistributionChart;
                break;
            case 'cookingTimeByDifficulty':
                img.src = cookingTimeByDifficultyChart;
                break;
            default:
                img.src = ''; // default or error image
        }
        modal.style.display = "block";
    });

    span.onclick = function () {
        modal.style.display = "none";
    }

    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
});