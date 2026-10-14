import pandas as pd
import tutor_search as tsearch
import ward_search as wsearch

doc = pd.ExcelFile("tw-details.xlsx")
n = len(doc.sheet_names)
pd.set_option('display.float_format', '{:.0f}'.format) # To print reg. no's in full form


dfs = []

#reading the excel file
for i in range(n):
    df = pd.read_excel("tw-details.xlsx", sheet_name=i)
    dfs.append(df)

print("Tutor Name search to get details (or) Register No. search to get student details")
choice = int(input())


if(choice == 1):
    name = input("Enter name: ")
    tsearch.tutor_search(dfs, name)
elif(choice == 2):
    reg = float(input("Enter reg. no or subset of reg. no: "))
    wsearch.ward_search(dfs, reg)
else:
    print("Invalid Choice")


#TODO: Improve search accuracy


