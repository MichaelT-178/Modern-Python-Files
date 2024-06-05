import pandas as pd

excel_path = "spread_sheet.xlsx"

df = pd.read_excel(excel_path, engine="openpyxl")

# print(df['Unnamed: 0'])


count = 0

# df.head() Used to see data if you can't find column name

for cool in df['Unnamed: 5']:
    if isinstance(cool, str):
        print(cool)