import pandas as pd
from rapidfuzz import process, fuzz

def tutor_search(dfs, tutors, tname):

    #store fuzzy search results in the tuple of tuples "results"
    results = process.extract(
        tname, 
        tutors,
        scorer=fuzz.WRatio,
        processor=str.lower,
        limit=5,
        score_cutoff=65
    )

    if results:
        #results is a tuple with name, score, index
        for name, score, index in results:
            print("Closest Matching Name: ", name)

            for df in dfs:
                #to handle empty tutor values and equality values
                tutor_details = df[df["Tutor Name"].str.lower().eq(name.lower()).fillna(False)]

                if tutor_details.empty:
                    continue
                else:
                    return tutor_details[["First Name", "Last Name", "Registration No"]]
    else:
        print("No matching name found.")

    print("\n")
