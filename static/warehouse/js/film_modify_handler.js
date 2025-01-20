document.addEventListener("DOMContentLoaded", function () {
    // Parse films data from JSON
    const filmsData = JSON.parse(document.getElementById("films-data").textContent);

    const filmSelect = document.getElementById("filmid");
    const filmNameInput = document.getElementById("filmname");
    const filmTypeInput = document.getElementById("filmtype");
    const filmIsoInput = document.getElementById("filmiso");
    const filmDescriptionInput = document.getElementById("description");
    const fileInput = document.getElementById("fileInput");
    const previewImg = document.getElementById("preview");

    // Populate fields when a film is selected
    filmSelect.addEventListener("change", function () {
        const filmId = this.value;
        const selectedFilm = filmsData.find(film => film.id == filmId);

        if (selectedFilm) {
            filmNameInput.value = selectedFilm.film_name || "";
            filmTypeInput.value = selectedFilm.film_type || "";
            filmIsoInput.value = selectedFilm.iso || "";
            filmDescriptionInput.value = selectedFilm.description || "";

            if (selectedFilm.cover_image_url) {
                previewImg.src = selectedFilm.cover_image_url;
                previewImg.style.display = "block";
            } else {
                previewImg.style.display = "none";
            }
        } else {
            filmNameInput.value = "";
            filmTypeInput.value = "";
            filmIsoInput.value = "";
            filmDescriptionInput.value = "";
            previewImg.style.display = "none";
        }
    });

    // Confirm Modify
    const modifyBtn = document.getElementById("modifyBtn");
    modifyBtn.addEventListener("click", function (event) {
        if (!confirm("Are you sure you want to modify this film?")) {
            event.preventDefault();
        }
    });

    // Confirm Delete
    const deleteBtn = document.getElementById("deleteBtn");
    deleteBtn.addEventListener("click", function (event) {
        const filmId = filmSelect.value;
        if (filmId && confirm("Are you sure you want to delete this film?")) {
            fetch("", {
                method: "POST",
                headers: {
                    "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    film_id: filmId,
                    action: "delete-film-type",
                }),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert("Film deleted successfully.");
                        location.reload();
                    } else {
                        alert("An error occurred.");
                    }
                })
                .catch(error => console.error("Error:", error));
        } else {
            event.preventDefault();
        }
    });
});
