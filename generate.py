import numpy as np
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path 
import yaml
import sys
import glob
import os
import math
def visual(percent):
    counter = math.floor(float(percent)/3)
    rval = ""
    for i in range (counter):
        rval += "#"
    return rval


list_of_files = glob.glob('./T*.xls') # * means all if need specific format then *.csv
latest_file = Path(max(list_of_files, key=os.path.getctime))
print(f"Benutzte Daten: {latest_file}")

df = pd.read_excel(latest_file, sheet_name="Timesheet")
df.drop('Startzeit',axis='columns', inplace=True)
df.drop('Endzeit',axis='columns', inplace=True)
df.drop('Nummer',axis='columns', inplace=True)
df.drop('Beschreibung',axis='columns', inplace=True)
df = df.rename(columns={"Dauer (rel.)": "Arbeitszeit"})

df_excel = df.groupby(['Datum','Projekt']).sum()
sheet_name = "Timmesheet"
new_file = "./Calced_timesheet.xlsx"
with pd.ExcelWriter(new_file, mode='w', engine='openpyxl') as writer:  
    df_excel.to_excel(writer, sheet_name= sheet_name)

#Information for cli
print("\n#################\nWochen:\n")

df['Woche'] = df['Datum'].dt.week

df_week = df.groupby(['Woche']).agg({"Arbeitszeit": np.sum, "Datum": pd.Series.nunique})
df_week['Soll_Zeit']= df_week['Datum'] * 7.8
df_week['Diff'] = df_week['Arbeitszeit'] - df_week['Soll_Zeit']
print(df_week)
print(f"\n\tSumme der Differenz: {'{0:.2f}h'.format(df_week['Diff'].sum())}")

df_prj = df.groupby(['Projekt']).sum()
df_prj['percent']  = (df_prj['Arbeitszeit'] / df_prj['Arbeitszeit'].sum()) * 100
df_prj['percent_visual'] = df_prj.apply(lambda row : visual(row['percent']), axis = 1)
df_prj['percent'] = pd.Series(["{0:.2f}%".format(val) for val in df_prj['percent']], index = df_prj.index)

df_prj.drop('Woche',axis='columns', inplace=True)
print("\nVerteilung:")
print(df_prj)

print(f"Geschrieben: {new_file}")

# Format excel

from openpyxl import load_workbook
from openpyxl.styles import PatternFill, Color
#pattern = PatternFill(bgColor="#346A8C", fill_type = "solid")
wb = load_workbook(filename = new_file)
ws = wb.active

blueFill = PatternFill(start_color='00CCFFFF',
                   end_color='00CCFFFF',
                   fill_type='solid')
orangeFill = PatternFill(start_color='00FFCC99',
                   end_color='00FFCC99',
                   fill_type='solid')
pinkFill = PatternFill(start_color='00FF99CC',
                   end_color='00FF99CC',
                   fill_type='solid')

def format_cell(row_number, style):
    ws.cell(row_number, 2).fill = style
    ws.cell(row_number, 3).fill = style
    ws.cell(row_number, 4).fill = style

with open('config.yaml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)
    for row_number in range(1,ws.max_row+1):
        for dictonary in config["colors"]:
            for key in dictonary.keys():
                if ws.cell(row_number, 2).value == key:
                    format_cell(row_number, PatternFill(start_color=Color(dictonary[key]),
                                                        end_color=Color(dictonary[key]),
                                                        fill_type='solid'))
#resize
dims = {}
for row in ws.rows:
    for cell in row:
        if cell.value:
            dims[cell.column_letter] = max((dims.get(cell.column_letter, 0), len(str(cell.value))))    

for col, value in dims.items():
    ws.column_dimensions[str(col)].width = value

wb.save(new_file)
   