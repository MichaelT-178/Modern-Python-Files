import pandas as pd
import numpy as np
import openpyxl


path = ""
excel_path = "spread_sheet.xlsx"

full_path = f"{path}/{excel_path}"


df = pd.read_excel(full_path, engine="openpyxl")


# print(df['Unnamed: 0'])

# df.head() Used to see data if you can't find column name

columns = ['Unnamed: 5', 'Unnamed: 6', 'Unnamed: 7']

col_data = [df[col].tolist() for col in columns]

header = "\t".join(columns)


for row in zip(*col_data):

   filtered_row = [str(value) for value in row if not pd.isna(value) and value != ""]

   print("\t\t\t".join(map(str, filtered_row)))

   