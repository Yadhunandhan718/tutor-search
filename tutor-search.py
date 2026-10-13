import pandas as pd


pd.set_option('display.float_format', '{:.0f}'.format) # To print reg. no's in full form

name = input("Enter tutor name to get their wards: ")

dfs = []

for i in range(4):
    df = pd.read_excel("tw-details.xlsx", sheet_name=i)
    dfs.append(df)

for df in dfs:
    results = df.loc[df["Tutor Name"].str.contains(name, case=False), ["Registration No", "First Name", "Last Name"]]

    if(results.empty):
        continue
    else:
        print("Matching Tutor Name: " + df.iloc[0]["Tutor Name"])
        print(results)

print("\n")