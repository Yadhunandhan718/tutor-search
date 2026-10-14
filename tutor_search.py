import pandas as pd

def tutor_search(dfs, name):

    for df in dfs:
        results = df.loc[df["Tutor Name"].str.contains(name, case=False), ["Registration No", "First Name", "Last Name"]]

        if(results.empty):
            continue
        else:
            print("Matching Tutor Name: " + df.iloc[0]["Tutor Name"])
            print(results)

    print("\n")
