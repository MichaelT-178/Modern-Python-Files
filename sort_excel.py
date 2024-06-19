"""
Sorts the rows in an excel file by numbers in a string. 
Then displays the rows largest to smallest.

Also includes code for extracting hyperlinks
"""

# pip3 install pandas openpyxl if not already installed
import pandas as pd
import openpyxl
import re

# Change the path 
excel_path = f"PATH_TO_YOUR_EXCEL_FILE"


df = pd.read_excel(excel_path, engine="openpyxl")

col_a = df["Unnamed: 0"][4:].tolist()
col_e = df["Unnamed: 4"][4:].tolist()
col_f = df["Unnamed: 5"][4:].tolist()
col_h = df["Unnamed: 6"][4:].tolist()
col_k = df["Unnamed: 10"][4:].tolist()
counts  = [int(cell.split(" ")[2]) for cell in col_f]

wb = openpyxl.load_workbook(excel_path)
ws = wb.active 

# Hyperlinks from col_b
col_b = []

# Extract fist parameter hyperlink from formula 
pattern = r'=HYPERLINK\("([^"]+)"'

# min_col=2, max_col=2 and the column you want to iterate over. Starts at 1.
for row in ws.iter_rows(min_row=6, min_col=2, max_col=2, values_only=True):
    formula = row[0]
    match = re.search(pattern, formula)

    if match:
        url = match.group(1)
        col_b.append(url)

class ExcelRow:
    def __init__(self, a, b, e, f, h, k, count):
        self.row_a = a
        self.row_b = b
        self.row_e = e
        self.row_f = f
        self.row_h = h
        self.row_k = k
        self.count = count
        
    # Was {:<140} for self.row_k
    def __str__(self): 
        return "{:<15}{:<20}{:<15}{:<20}{:<80}" \
                 .format(self.row_a, self.row_f, self.row_e, self.row_h, self.row_b)

all_rows = [ExcelRow(col_a[i], col_b[i], col_e[i], col_f[i], col_h[i], col_k[i], counts[i]) \
            for i in range(len(col_a))]


sorted_rows = sorted(all_rows, key=lambda row: row.count)

print("{:<15}{:<20}{:<15}{:<20}{:<80}" \
        .format('Col A', 'Col F', 'Col E', 'Col H', 'Col B'))

for row in sorted_rows:
    print(row)

