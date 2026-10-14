import pandas as pd 
from rapidfuzz import process, fuzz

def ward_name_search(dfs, sname):

    #concatenate all individual tables from every sheet into one big dataframe
    all_data = pd.concat(dfs, ignore_index=True)

    #create a new column "Full Name" which is First Name + Last Name
    all_data["Full Name"] = all_data["First Name"] + " " + all_data["Last Name"]

    #put the names in a list
    student_names = all_data["Full Name"].unique().tolist()

    results = process.extract(
        sname,
        student_names,
        scorer=fuzz.WRatio,
        processor=str.lower,
        limit=5,
        score_cutoff=75
    )

    if not results:
        print("No matching student name found")
        return

    for matched_name, score, index in results:
        print("Closest matching name: ", matched_name)
        student_details = all_data[all_data["Full Name"].str.lower().eq(matched_name.lower()).fillna(False)]
        if student_details.empty:
            continue
        print(student_details[["Registration No", "Full Name", "Tutor Name"]])
        return 



