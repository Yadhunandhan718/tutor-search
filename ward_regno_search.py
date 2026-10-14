import pandas as pd

def ward_search(dfs, reg_no):
    for df in dfs:
        results = df.loc[df["Registration No"].astype(str).str.contains(str(reg_no), na=False),  ["Tutor Name", "First Name", "Last Name", "Registration No"]]
        if results.empty:
            continue
        print(results)
    print("\n")

