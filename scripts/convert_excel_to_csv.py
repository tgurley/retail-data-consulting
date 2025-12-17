import pandas as pd

print("Loading Excel file...")
df = pd.read_excel(
    "data/Online Retail.xlsx",
    engine="openpyxl"
)

print("Writing CSV...")
df.to_csv("data/online_retail.csv", index=False)

print("Done.")
