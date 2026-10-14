import pandas as pd
import tutor_search as tsearch
import ward_regno_search as wrsearch
import ward_name_search as wnsearch

filename = "tw-details.xlsx"

doc = pd.ExcelFile(filename)
n = len(doc.sheet_names)
pd.set_option('display.float_format', '{:.0f}'.format) # To print reg. no's in full form


dfs = []
tutors = []

#reading the excel file
for i in range(n):
    df = pd.read_excel(filename, sheet_name=i)
    for name in df["Tutor Name"].unique().dropna().tolist():
        tutors.append(name)
    dfs.append(df)

print('''1. Tutor Name search to get details
(or) 
2. Register No. search to get student details 
(or) 
3. Name search to get student details''')
choice = int(input())

1
if(choice == 1):
    name = input("Enter name: ")
    tsearch.tutor_search(dfs, tutors, name)
elif(choice == 2):
    reg = float(input("Enter reg. no or subset of reg. no: "))
    wrsearch.ward_search(dfs, reg)
elif(choice == 3):
    sname = input("Enter student name: ")
    wnsearch.ward_name_search(dfs, sname)
else:
    print("Invalid Choice")


#TODO: Add a simple and effective frontend with this backend :)




