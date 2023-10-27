import pandas as pd
import openpyxl

"""
This is a rough template to read an excel sheet

"""

# Load the Excel file. example.xlsx should be the path
workbook = openpyxl.load_workbook('example.xlsx')

# Select the desired worksheet
worksheet = workbook["cool"]

# Initialize lists to store the values
cars = []
books = []

# Iterate through the rows from 2 to 50
for row in worksheet.iter_rows(min_row=2, max_row=50, min_col=1, max_col=2, values_only=True):
    cars.append(row[0]) 
    books.append(row[1]) 


for i in range(len(books)):
    formatted_text = "%-45s" % f"Car: {books[i]}" 

    print(formatted_text, end="")
    print(f"|         Book: {cars[i]}")