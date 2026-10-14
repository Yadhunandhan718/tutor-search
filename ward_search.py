import pandas as pd

def ward_search(dfs, name):
    for df in dfs:
        results = df.loc[df["Registration No"].astype(str).str.contains(str(name), na=False),  ["Tutor Name", "First Name", "Last Name"]]
        if results.empty:
            continue
        print(results)
    print("\n")

