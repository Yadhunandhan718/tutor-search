from flask import Flask, render_template, request, jsonify
import pandas as pd

# Import your existing search functions.
from tutor_search import tutor_search
from ward_name_search import ward_name_search
from ward_regno_search import ward_search

app = Flask(__name__)
filename = "tw-details.xlsx" #define filename here to remove arbitrary names elsewhere

# Load the workbook once when the application starts.
workbook = pd.ExcelFile(filename)

#create list to store list of tutor names
tutors = []

#list to store all dataframes in given sheet
dfs = []

#no. of sheets defined here
n = len(workbook.sheet_names)

for i in range(n):
    df = pd.read_excel(filename, sheet_name=i)
    for name in df["Tutor Name"].unique().dropna().tolist():
        tutors.append(name)
    dfs.append(df)


# Combine the sheets if your student-search function needs all records.
all_data = pd.concat(dfs, ignore_index=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    data = request.get_json(silent=True) or {}

    query = data.get("query", "").strip()
    search_type = data.get("type", "")

    if not query:
        return jsonify({"error": "Enter a search query."}), 400

    try:
        if search_type == "tutor":
            
            result = tutor_search(dfs, tutors, query)

        elif search_type == "student":
            
            result = ward_name_search(dfs, query)

        elif search_type == "regno":
            
            result = ward_search(dfs, query)

        else:
            return jsonify({"error": "Invalid search type."}), 400

        if result is None:
            result = pd.DataFrame()

        if not isinstance(result, pd.DataFrame):
            raise TypeError("Search function must return a DataFrame.")

        # Convert missing values to None and prepare JSON-compatible records.
        result = result.astype(object).where(result.notna(), None)

        return jsonify({
            "columns": result.columns.tolist(),
            "results": result.to_dict(orient="records")
        })

    except Exception:
        app.logger.exception("Search failed")
        return jsonify({"error": "An error occurred during the search."}), 500


if __name__ == "__main__":
    app.run(debug=True)