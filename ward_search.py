import pandas as pd

pd.set_option('display.float_format', '{:.0f}'.format) # To print reg. no's in full form

dfs = []

name = float(input("Enter ward reg. no to get details: "))

for i in range(4):
    df = pd.read_excel("tw-details.xlsx", sheet_name=i)
    dfs.append(df)

for df in dfs:
    results = df.loc[df["Registration No"].astype(str).str.contains(str(name), na=False),  ["Tutor Name", "First Name", "Last Name"]]
    if results.empty:
        continue
    print(results)
print("\n")