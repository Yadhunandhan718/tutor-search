// -----------------------------------------------
// EXISTING SEARCH ELEMENTS
// -----------------------------------------------

const form = document.getElementById("search-form");

const queryInput = document.getElementById("query");

const searchType = document.getElementById("search-type");

const resultsDiv = document.getElementById("results");

const messageDiv = document.getElementById("message");


// -----------------------------------------------
// ACADEMIC YEAR ELEMENTS
// -----------------------------------------------

const academicYearSelect =
    document.getElementById("academic-year");

const yearMessageDiv =
    document.getElementById("year-message");

const tutorListDiv =
    document.getElementById("tutor-list");

const yearResultsDiv =
    document.getElementById("year-results");


// -----------------------------------------------
// REUSABLE TABLE RENDERING FUNCTION
// -----------------------------------------------

function renderTable(container, data) {

    container.replaceChildren();

    if (!data.results || data.results.length === 0) {

        const emptyMessage = document.createElement("p");

        emptyMessage.textContent = "No matching records found.";

        container.appendChild(emptyMessage);

        return;
    }


    const table = document.createElement("table");

    const header = document.createElement("tr");


    // Create table headers.

    data.columns.forEach(function (column) {

        const th = document.createElement("th");

        th.textContent = column;

        header.appendChild(th);

    });

    table.appendChild(header);


    // Create table rows.

    data.results.forEach(function (record) {

        const row = document.createElement("tr");

        data.columns.forEach(function (column) {

            const cell = document.createElement("td");

            cell.textContent = record[column] ?? "";

            row.appendChild(cell);

        });

        table.appendChild(row);

    });


    container.appendChild(table);

}


// -----------------------------------------------
// LOAD TUTORS WHEN A YEAR IS SELECTED
// -----------------------------------------------

academicYearSelect.addEventListener(
    "change",
    async function () {

        const year = academicYearSelect.value;

        tutorListDiv.replaceChildren();

        yearResultsDiv.replaceChildren();


        if (!year) {

            yearMessageDiv.textContent = "";

            return;
        }


        yearMessageDiv.textContent = "Loading tutors...";

        academicYearSelect.disabled = true;


        try {

            const response = await fetch(
                `/api/tutors/${encodeURIComponent(year)}`
            );

            const data = await response.json();


            if (!response.ok) {

                throw new Error(
                    data.error || "Could not load tutors."
                );

            }


            if (data.tutors.length === 0) {

                yearMessageDiv.textContent =
                    "No tutors found for this year.";

                return;
            }


            yearMessageDiv.textContent =
                `Tutors for ${data.sheet}:`;


            // Create a clickable button for each tutor.

            data.tutors.forEach(function (tutor) {

                const button = document.createElement("button");

                button.type = "button";

                button.className = "tutor-choice";

                button.textContent = tutor;

                button.dataset.tutor = tutor;

                button.dataset.year = year;

                tutorListDiv.appendChild(button);

            });


        } catch (error) {

            yearMessageDiv.textContent = error.message;

        } finally {

            academicYearSelect.disabled = false;

        }

    }
);


// -----------------------------------------------
// DISPLAY WARDS WHEN A TUTOR IS CLICKED
// -----------------------------------------------

tutorListDiv.addEventListener(
    "click",
    async function (event) {

        const button = event.target.closest(
            "button[data-tutor]"
        );

        if (!button) {
            return;
        }


        const tutor = button.dataset.tutor;

        const year = button.dataset.year;


        yearResultsDiv.replaceChildren();

        yearMessageDiv.textContent =
            `Loading wards for ${tutor}...`;


        // Prevent multiple clicks while loading.

        const tutorButtons =
            tutorListDiv.querySelectorAll("button");

        tutorButtons.forEach(function (item) {

            item.disabled = true;

        });


        try {

            const response = await fetch(
                "/api/tutor-wards",
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        tutor: tutor,
                        year: year
                    })
                }
            );


            const data = await response.json();


            if (!response.ok) {

                throw new Error(
                    data.error ||
                    "Could not load this tutor's wards."
                );

            }


            yearMessageDiv.textContent =
                `Wards of ${tutor} (${data.results.length})`;


            renderTable(yearResultsDiv, data);


        } catch (error) {

            yearMessageDiv.textContent = error.message;

        } finally {

            tutorButtons.forEach(function (item) {

                item.disabled = false;

            });

        }

    }
);


// -----------------------------------------------
// EXISTING SEARCH FUNCTIONALITY
// -----------------------------------------------

form.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();


        const query = queryInput.value.trim();

        const type = searchType.value;


        if (!query) {

            messageDiv.textContent =
                "Please enter a search query.";

            return;
        }


        resultsDiv.replaceChildren();

        messageDiv.textContent = "Searching...";


        const button = form.querySelector("button");

        button.disabled = true;


        try {

            const response = await fetch(
                "/search",
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        query: query,
                        type: type
                    })
                }
            );


            const data = await response.json();


            if (!response.ok) {

                throw new Error(
                    data.error || "Search failed."
                );

            }


            if (!data.results || data.results.length === 0) {

                messageDiv.textContent =
                    "No matching records found.";

                return;
            }


            messageDiv.textContent = "";

            renderTable(resultsDiv, data);


        } catch (error) {

            messageDiv.textContent = error.message;

        } finally {

            button.disabled = false;

        }

    }
);