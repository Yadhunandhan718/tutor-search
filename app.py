from flask import Flask, render_template, request, jsonify
import pandas as pd

# Import your existing search functions.
from tutor_search import tutor_search
from ward_name_search import ward_name_search
from ward_regno_search import ward_search

app = Flask(__name__)

filename = "tw-details.xlsx"

# Map academic year numbers to the exact Excel sheet names.
YEAR_SHEETS = {
    1: "First Years",
    2: "Second Years",
    3: "Third Years",
    4: "Fourth Years",
}

# Load the workbook once when the application starts.
workbook = pd.ExcelFile(filename)

# Store each sheet's DataFrame using its sheet name.
sheet_data = {}

# Store all DataFrames for the existing search functions.
dfs = []

# Store all tutor names for the existing tutor search.
tutors = []

for sheet_name in workbook.sheet_names:
    df = pd.read_excel(filename, sheet_name=sheet_name)

    sheet_data[sheet_name] = df
    dfs.append(df)

    if "Tutor Name" in df.columns:
        names = (
            df["Tutor Name"]
            .dropna()
            .astype(str)
            .str.strip()
            .tolist()
        )

        tutors.extend(name for name in names if name)

# Remove duplicate tutor names while preserving their order.
tutors = list(dict.fromkeys(tutors))

# Combine sheets for use if needed by other functions.
all_data = pd.concat(dfs, ignore_index=True)


def prepare_results(result):
    """Convert a DataFrame into JSON-compatible data."""

    if result is None:
        result = pd.DataFrame()

    if not isinstance(result, pd.DataFrame):
        raise TypeError("Search function must return a DataFrame.")

    # Replace missing values with None.
    result = result.astype(object).where(result.notna(), None)

    return {
        "columns": result.columns.tolist(),
        "results": result.to_dict(orient="records")
    }


@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------------------------
# EXISTING SEARCH FUNCTIONALITY
# -----------------------------------------------

@app.route("/search", methods=["POST"])
def search():

    data = request.get_json(silent=True) or {}

    query = str(data.get("query", "")).strip()
    search_type = data.get("type", "")

    if not query:
        return jsonify({
            "error": "Enter a search query."
        }), 400

    try:

        if search_type == "tutor":

            result = tutor_search(dfs, tutors, query)

        elif search_type == "student":

            result = ward_name_search(dfs, query)

        elif search_type == "regno":

            result = ward_search(dfs, query)

        else:

            return jsonify({
                "error": "Invalid search type."
            }), 400

        return jsonify(prepare_results(result))

    except Exception:

        app.logger.exception("Search failed")

        return jsonify({
            "error": "An error occurred during the search."
        }), 500


# -----------------------------------------------
# GET TUTORS FOR A SELECTED ACADEMIC YEAR
# -----------------------------------------------

@app.route("/api/tutors/<int:year>", methods=["GET"])
def tutors_for_year(year):

    sheet_name = YEAR_SHEETS.get(year)

    if sheet_name is None:
        return jsonify({
            "error": "Choose a year between 1 and 4."
        }), 400

    df = sheet_data.get(sheet_name)

    if df is None:
        return jsonify({
            "error": f'Excel sheet "{sheet_name}" was not found.'
        }), 500

    if "Tutor Name" not in df.columns:
        return jsonify({
            "error": f'The sheet "{sheet_name}" has no "Tutor Name" column.'
        }), 500

    # Extract tutor names from the selected year's sheet.
    names = (
        df["Tutor Name"]
        .dropna()
        .astype(str)
        .str.strip()
        .tolist()
    )

    # Remove duplicates and sort alphabetically.
    names = sorted(
        {name for name in names if name},
        key=str.casefold
    )

    return jsonify({
        "year": year,
        "sheet": sheet_name,
        "tutors": names
    })


# -----------------------------------------------
# GET THE WARDS OF A SELECTED TUTOR
# -----------------------------------------------

@app.route("/api/tutor-wards", methods=["POST"])
def tutor_wards():

    data = request.get_json(silent=True) or {}

    tutor_name = str(data.get("tutor", "")).strip()
    year = data.get("year")

    if not tutor_name:
        return jsonify({
            "error": "Choose a tutor."
        }), 400

    try:
        year = int(year)
    except (TypeError, ValueError):
        return jsonify({
            "error": "Choose an academic year."
        }), 400

    sheet_name = YEAR_SHEETS.get(year)

    if sheet_name is None:
        return jsonify({
            "error": "Choose a year between 1 and 4."
        }), 400

    df = sheet_data.get(sheet_name)

    if df is None:
        return jsonify({
            "error": f'Excel sheet "{sheet_name}" was not found.'
        }), 500

    if "Tutor Name" not in df.columns:
        return jsonify({
            "error": f'The sheet "{sheet_name}" has no "Tutor Name" column.'
        }), 500

    # Get tutor names from this sheet only.
    year_tutors = (
        df["Tutor Name"]
        .dropna()
        .astype(str)
        .str.strip()
        .tolist()
    )

    try:

        # Reuse your existing function.
        # Restrict the search to the selected academic year.
        result = tutor_search(
            [df],
            year_tutors,
            tutor_name
        )

        response_data = prepare_results(result)

        response_data["tutor"] = tutor_name
        response_data["year"] = year

        return jsonify(response_data)

    except Exception:

        app.logger.exception(
            "Could not retrieve wards for selected tutor"
        )

        return jsonify({
            "error": "Could not retrieve this tutor's wards."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)