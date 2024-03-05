// Listen for the 'DOMContentLoaded' event to ensure the DOM is fully loaded before running the script.
document.addEventListener("DOMContentLoaded", function () {

    // Defines a function to toggle the visibility of the search form.
    const toggleSearchForm = function () {
        // Retrieves the search form container element by its ID.
        const searchFormContainer = document.getElementById("searchFormContainer");
        // Retrieves the button element that toggles the search form visibility by its ID.
        const toggleButton = document.getElementById("toggleSearchButton");

        // Checks if the search form is currently not displayed.
        if (searchFormContainer.style.display === "none") {
            // Makes the search form visible.
            searchFormContainer.style.display = "block";
            // Updates the toggle button text to offer hiding the search options.
            toggleButton.textContent = "Hide Search Options";
        } else {
            // Hides the search form if it is currently visible.
            searchFormContainer.style.display = "none";
            // Updates the toggle button text to offer showing the search options.
            toggleButton.textContent = "Show Search Options";
        }
    }

    // Retrieves the button element that toggles the search form visibility by its ID.
    const toggleButton = document.getElementById("toggleSearchButton");

    // Checks if the toggle button exists to avoid errors in case it's not present in the DOM.
    if (toggleButton) {
        // Adds an event listener to the toggle button to call the toggleSearchForm function when clicked.
        toggleButton.addEventListener('click', toggleSearchForm);
    }
});


// Listen for the 'DOMContentLoaded' event to ensure the DOM is fully loaded before running the script.
document.addEventListener("DOMContentLoaded", function () {
    // Retrieves the search form element by its ID.
    const searchForm = document.getElementById('searchForm');

    // Checks if the search form exists to avoid errors in case it's not present in the DOM.
    if (searchForm) {
        // Adds an event listener to handle the form submission.
        searchForm.addEventListener('submit', function (e) {
            // Initializes a flag to keep track of whether all fields are empty.
            let allEmpty = true;
            // Selects all input fields except those of type "hidden", and all select elements within the form.
            searchForm.querySelectorAll('input:not([type="hidden"]), select').forEach(function (input) {
                // Trims the value of the input field and checks if it is not empty.
                if (input.value.trim() !== '') {
                    // If any field is not empty, sets the flag to false.
                    allEmpty = false;
                }
            });
            // If all fields are empty, prevents the form from being submitted.
            if (allEmpty) {
                e.preventDefault();
            }
        });
    }
});


// Listen for the 'DOMContentLoaded' event to ensure the DOM is fully loaded before running the script.
document.addEventListener("DOMContentLoaded", function () {
    // Retrieves the modal, image, and selector elements by their IDs or class names.
    const modal = document.getElementById("chartModal");
    const img = document.getElementById("chartImage");
    const selector = document.getElementById("chartSelector");
    const span = document.getElementsByClassName("close")[0];

    // Checks if the chart selector exists to avoid errors in case it's not present in the DOM.
    if (selector) {
        // Adds an event listener to handle the change event on the selector.
        selector.addEventListener('change', function () {
            // Retrieves the selected chart value.
            const chartValue = selector.value;
            // Switches based on the selected chart value to update the image source.
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
                    img.src = '';
            }
            // Displays the modal by changing its style to 'block'.
            modal.style.display = "block";
        });
    }

    // Checks if the close button (span) exists.
    if (span) {
        // Adds an onclick event listener to the close button to hide the modal.
        span.onclick = function () {
            if (modal) {
                modal.style.display = "none";
            }
        };
    }

    // Adds an onclick event listener to the window to close the modal when clicking outside of it.
    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
});


// Listen for the 'DOMContentLoaded' event to ensure the DOM is fully loaded before running the script.
document.addEventListener('DOMContentLoaded', function () {
    // Retrieves the hamburger menu and navigation items elements by their IDs.
    const hamburger = document.getElementById('hamburger');
    const navItems = document.getElementById('navItems');


    if (hamburger) {
        // Adds a click event listener to the hamburger menu.
        hamburger.addEventListener('click', function () {
            // Toggles the 'active' class on the navigation items, showing or hiding the mobile menu.
            navItems.classList.toggle('active');

            // Checks if the navigation items are currently active (visible).
            if (navItems.classList.contains('active')) {
                // Changes the hamburger menu to a close icon when the menu is active.
                hamburger.innerHTML = '&times;';
            } else {
                // Reverts the hamburger menu icon when the menu is not active.
                hamburger.innerHTML = '&#9776;';
            }
        });
    }


    // Defines a function to close the mobile menu.
    function closeMenu() {
        // Checks if the navigation items are currently active.
        if (navItems.classList.contains('active')) {
            // Removes the 'active' class, hiding the mobile menu, and reverts the hamburger icon.
            navItems.classList.remove('active');
            hamburger.innerHTML = '&#9776;';
        }
    }

    // Adds a click event listener to each navigation item link and button to close the menu upon interaction.
    document.querySelectorAll('.nav-items a, .nav-items button').forEach(function (item) {
        item.addEventListener('click', closeMenu);
    });

    // Retrieves the chart selector element by its ID.
    const chartSelector = document.getElementById('chartSelector');

    // Checks if the chart selector exists to avoid errors in case it's not present in the DOM.
    if (chartSelector) {
        // Adds a change event listener to the chart selector to close the mobile menu when a selection is made.
        chartSelector.addEventListener('change', function () {
            closeMenu();
        });
    }
});


// Listen for the 'DOMContentLoaded' event to ensure the DOM is fully loaded before running the script.
document.addEventListener('DOMContentLoaded', function () {
    // Retrieves the form element for adding a recipe by its ID.
    const addRecipeForm = document.getElementById('addRecipeForm');

    // Checks if the form exists to prevent errors if it's not present.
    if (addRecipeForm) {
        // Retrieves the URL for posting the form data from a data attribute on the form.
        const postUrl = addRecipeForm.getAttribute('data-post-url');

        // Adds an event listener to handle the form submission.
        addRecipeForm.addEventListener('submit', function (e) {
            // Prevents the default form submission mechanism to handle the submission via JavaScript.
            e.preventDefault();

            // Creates a new FormData object, capturing the form's current values.
            const formData = new FormData(addRecipeForm);

            // Executes a fetch request to submit the form data to the server.
            fetch(postUrl, {
                method: 'POST', // Specifies the request method.
                body: formData, // Attaches the form data as the request body.
                headers: {
                    // Includes a CSRF token in the request headers for security purposes.
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                },
                credentials: 'same-origin' // Ensures cookies are sent with the request if the URL is on the same origin.
            })
                .then(response => response.json()) // Parses the JSON response from the server.
                .then(data => {

                    // Checks if the server responded with a success status.
                    if (data.status === 'success') {
                        // Closes the recipe modal by hiding it.
                        document.getElementById('addRecipeModal').style.display = 'none';
                        // Reloads the page to reflect any changes made by the form submission.
                        window.location.reload();
                    }
                })
                .catch(error => console.error('Error:', error)); // Logs any errors that occur during the fetch request.
        });
    }
});

// Listen for the 'DOMContentLoaded' event to ensure the DOM is fully loaded before running the script.
document.addEventListener('DOMContentLoaded', function () {
    // Retrieves the button to add a recipe and the modal for adding a recipe by their IDs.
    const addRecipeButton = document.getElementById('addRecipeButton');
    const addRecipeModal = document.getElementById('addRecipeModal');

    // Retrieves the close (X) button within the addRecipeModal if the modal exists.
    const closeModalSpan = addRecipeModal ? addRecipeModal.querySelector('.close') : null;

    // Defines a function to display the add recipe modal.
    function openAddRecipeModal() {
        if (addRecipeModal) {
            addRecipeModal.style.display = 'block';
        }
    }

    // Defines a function to hide the add recipe modal.
    function closeAddRecipeModal() {
        if (addRecipeModal) {
            addRecipeModal.style.display = 'none';
        }
    }

    // Adds an event listener to the addRecipeButton to open the modal when clicked.
    if (addRecipeButton) {
        addRecipeButton.addEventListener('click', openAddRecipeModal);
    }

    // Adds an event listener to the closeModalSpan to close the modal when clicked.
    if (closeModalSpan) {
        closeModalSpan.addEventListener('click', closeAddRecipeModal);
    }

    // Adds an event listener to the window to close the modal when clicking outside of it.
    window.addEventListener('click', function (event) {
        if (event.target == addRecipeModal) {
            closeAddRecipeModal();
        }
    });
});


// Listen for the 'DOMContentLoaded' event to ensure the DOM is fully loaded before running the script.
document.addEventListener('DOMContentLoaded', function () {
    // Retrieves the button to update a recipe by its ID.
    const updateButton = document.getElementById('updateRecipeButton');

    // Checks if the update button exists to prevent errors in case it's not present.
    if (updateButton) {
        // Retrieves the modal for updating a recipe and the close button within it by their selectors.
        const updateModal = document.getElementById('updateRecipeModal');
        const closeUpdateModal = document.querySelector('#updateRecipeModal .close');

        // Adds an event listener to the updateButton to open the update modal when clicked.
        updateButton.addEventListener('click', () => {
            if (updateModal) {
                updateModal.style.display = 'block';
            }
        });

        // Adds an event listener to the close button within the update modal to close it when clicked.
        if (closeUpdateModal) {
            closeUpdateModal.addEventListener('click', () => {
                if (updateModal) {
                    updateModal.style.display = 'none';
                }
            });
        }

        // Adds an event listener to the window to close the update modal when clicking outside of it.
        window.addEventListener('click', (event) => {
            if (event.target == updateModal) {
                updateModal.style.display = 'none';
            }
        });
    }
});


// Listen for the 'DOMContentLoaded' event to ensure the DOM is fully loaded before running the script.
document.addEventListener('DOMContentLoaded', function () {
    // Function to get CSRF token from the cookies, necessary for POST requests
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Checks if the current cookie is the one we're looking for.
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break; // Found the cookie, exit the loop.
                }
            }
        }
        return cookieValue; // Return the found cookie value or null if not found.
    }

    // Retrieve relevant DOM elements for the delete functionality.
    const deleteButton = document.getElementById('deleteRecipeButton');
    const deleteModal = document.getElementById('deleteRecipeModal');
    const closeDeleteModal = document.getElementById('closeDeleteModal');
    const confirmDeleteButton = document.getElementById('confirmDeleteButton');
    const deleteConfirmationInput = document.getElementById('deleteConfirmationInput');

    // Display the delete modal when the delete button is clicked.
    if (deleteButton) {
        deleteButton.addEventListener('click', function () {
            deleteModal.style.display = 'block';
        });
    }

    // Close the delete modal when the close button is clicked.
    if (closeDeleteModal) {
        closeDeleteModal.addEventListener('click', function () {
            deleteModal.style.display = 'none';
        });
    }

    // Close the delete modal when clicking outside of it.
    if (deleteModal) {
        window.addEventListener('click', function (event) {
            if (event.target == deleteModal) {
                deleteModal.style.display = 'none';
            }
        });
    }

    // Confirm deletion when the confirm button is clicked, given the correct confirmation text is entered.
    if (confirmDeleteButton && deleteConfirmationInput) {
        confirmDeleteButton.addEventListener('click', function () {
            const recipeId = deleteButton.dataset.recipeId; // Retrieve the recipe ID from the data-attribute

            if (deleteConfirmationInput.value.trim() === "DELETE RECIPE") {
                // Make a POST request to the server to delete the recipe if the confirmation text is correct
                fetch(`/delete/${recipeId}/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken') // Include CSRF token for security
                    },
                    body: JSON.stringify({
                        'confirmation_text': deleteConfirmationInput.value.trim() // Send confirmation text as JSON
                    }),
                    credentials: 'include' // Ensure credentials such as cookies are included with the request
                })
                    .then(response => response.json()) // Parse the JSON response from the server
                    .then(data => {
                        if (data.status === 'success') {
                            // Notify the user of successful deletion and redirect to the list page
                            alert('Recipe successfully deleted.');
                            window.location.href = "/list/";
                        } else {
                            // Alert the user of an error based on the message from the server
                            alert(`Error: ${data.message}`);
                        }
                    })
                    .catch(error => {
                        // Log and alert the user of any errors that occurred during the fetch operation
                        console.error('Error:', error);
                        alert(`An error occurred: ${error}`);
                    });
            } else {
                // Notify the user to enter the correct confirmation text to proceed with deletion
                alert("You must type 'DELETE RECIPE' to confirm.");
            }
        });
    }
});