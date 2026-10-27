import pandas as pd 
from rapidfuzz import process, fuzz

def ward_name_search(dfs, sname):

    final_df = pd.DataFrame()
    #concatenate all individual tables from every sheet into one big dataframe
    all_data = pd.concat(dfs, ignore_index=True)

    #put the names in a list
    student_names = all_data["Name"].unique().tolist()

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
        student_details = all_data[all_data["Name"].str.lower().eq(matched_name.lower()).fillna(False)]
        if student_details.empty:
            continue

        
        final_df = pd.concat([final_df, student_details], ignore_index=True)

    return final_df[["Registration No", "Name", "Tutor Name"]]
        



