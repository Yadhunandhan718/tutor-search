import pandas as pd
import tutor_search as tsearch
import ward_search as wsearch

doc = pd.ExcelFile("tw-details.xlsx")
n = len(doc.sheet_names)
pd.set_option('display.float_format', '{:.0f}'.format) # To print reg. no's in full form


dfs = []
tutors = []

#reading the excel file
for i in range(n):
    df = pd.read_excel("tw-details.xlsx", sheet_name=i)
    for name in df["Tutor Name"].unique().dropna().tolist():
        tutors.append(name)
    dfs.append(df)

print("Tutor Name search to get details (or) Register No. search to get student details")
choice = int(input())

1
if(choice == 1):
    name = input("Enter name: ")
    tsearch.tutor_search(dfs, tutors, name)
elif(choice == 2):
    reg = float(input("Enter reg. no or subset of reg. no: "))
    wsearch.ward_search(dfs, reg)
else:
    print("Invalid Choice")


#TODO: Improve search accuracy'''1


