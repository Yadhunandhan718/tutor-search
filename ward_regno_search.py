import pandas as pd

def ward_search(dfs, reg_no):
    for df in dfs:
        results = df.loc[df["Registration No"].astype(str).str.contains(str(reg_no), na=False),  ["Tutor Name", "Name", "Registration No"]]
        if results.empty:
            continue
        return results
    print("\n")

