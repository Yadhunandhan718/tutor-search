const form = document.getElementById("search-form");
const queryInput = document.getElementById("query");
const searchType = document.getElementById("search-type");
const resultsDiv = document.getElementById("results");
const messageDiv = document.getElementById("message");

form.addEventListener("submit", async function (event) {
    event.preventDefault();

    const query = queryInput.value.trim();
    const type = searchType.value;

    if (!query) {
        messageDiv.textContent = "Please enter a search query.";
        return;
    }

    resultsDiv.replaceChildren();
    messageDiv.textContent = "Searching...";

    const button = form.querySelector("button");
    button.disabled = true;

    try {
        const response = await fetch("/search", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                query: query,
                type: type
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Search failed.");
        }

        messageDiv.textContent = "";

        if (data.results.length === 0) {
            messageDiv.textContent = "No matching records found.";
            return;
        }

        const table = document.createElement("table");
        const header = document.createElement("tr");

        data.columns.forEach(function (column) {
            const th = document.createElement("th");
            th.textContent = column;
            header.appendChild(th);
        });

        table.appendChild(header);

        data.results.forEach(function (record) {
            const row = document.createElement("tr");

            data.columns.forEach(function (column) {
                const cell = document.createElement("td");
                cell.textContent = record[column] ?? "";
                row.appendChild(cell);
            });

            table.appendChild(row);
        });

        resultsDiv.appendChild(table);

    } catch (error) {
        messageDiv.textContent = error.message;

    } finally {
        button.disabled = false;
    }
});
