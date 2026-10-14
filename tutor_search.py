import pandas as pd
from rapidfuzz import process, fuzz

def tutor_search(dfs, tutors, tname):

    results = process.extract(
        tname, 
        tutors,
        scorer=fuzz.WRatio,
        processor=str.lower,
        limit=5,
        score_cutoff=65
    )

    if results:
        for name, score, index in results:
            print("Closest Matching Name: ", name)

            for df in dfs:
                tutor_details = df[df["Tutor Name"].str.lower() == name.lower()]

                if tutor_details.empty:
                    continue
                else:
                    print(tutor_details[["First Name", "Last Name", "Registration No"]])
    else:
        print("No matching name found.")

    print("\n")
