import numpy as np
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import matplotlib.pyplot as plt
from datetime import datetime
from pathlib import Path 
import argparse as _argparse

import glob
import os
import sys, getopt
import math
import plotext as plt
import math

from timesheet.configer import get_config
from timesheet.csv_exporter import csv_export
from timesheet.excel import format_excel, read_excel
from timesheet.pause import calc_breaks




def print_plotext(items, values):
    values = [x[0] for x in values]
    if len(items) != len(values):
        print("Wrong data")
        return 
    plt.bar(items, values, orientation = 'h', width = 3/5)
    plt.title('Verteilung')
    plt.clc()
    plt.plotsize(100, 2 * len(items) + 4)
    plt.show()
    
def visual(percent):
    counter = math.floor(float(percent)/3)
    rval = ""
    for i in range (counter):
        rval += "#"
    return rval

def get_latest_input():
    try:
        list_of_files = glob.glob('./t*.xls') # * means all if need specific format then *.csv
        return  Path(max(list_of_files, key=os.path.getctime))
    except:
        return None

def parse_arguments():
    
    parser = _argparse.ArgumentParser(
        prog='timesheet',
        usage='timesheet -i <inputfile> -t <days to export>',
        description=
        """This program takes the export of timesheet app
        """,
    )

    parser.add_argument(
        '-i', '--input',
        type=str,
        required=False,
        default= None,
        help='input file'
    )
    parser.add_argument(
        '-t', 
        type=int,
        required=False,
        help="Days to export in csv"
    )

    return parser.parse_args()

def main():

    latest_file = get_latest_input()
    args = parse_arguments()
    if args.input:
        latest_file = args.input
    
    if not latest_file or not latest_file.exists():
        print("Keine Datei gefunden")
        return -1
    print(f"Benutzte Daten: {latest_file}")

    df = read_excel(latest_file)

    df_excel = df.groupby(['Datum','Projekt']).sum()
    sheet_name = "Timmesheet"
    new_file = "./Calced_timesheet.xlsx"
    with pd.ExcelWriter(new_file, mode='w', engine='openpyxl') as writer:  
        df_excel.to_excel(writer, sheet_name= sheet_name)

    days_to_export = 365
    if args.t:
        days_to_export = args.t
    csv_export(df, days_to_export)

    #Information for cli
    print("\n#################\nWochen:\n")

    df['Woche'] = df['Datum'].dt.isocalendar().week

    df_week = df.groupby(['Woche']).agg({"Arbeitszeit": np.sum, "Datum": pd.Series.nunique})
    df_week['Soll_Zeit']= df_week['Datum'] * 7.8
    df_week['Diff'] = df_week['Arbeitszeit'] - df_week['Soll_Zeit']
    print(df_week)
    with pd.ExcelWriter(new_file, mode='a', engine='openpyxl') as writer:  
        df_week.to_excel(writer, sheet_name= "Zeit pro Woche")
    print(f"\n\tSumme der Differenz: {'{0:.2f}h'.format(df_week['Diff'].sum())}")

    df_perWeek = df.groupby(['Woche','Projekt']).agg({'Arbeitszeit':['sum']})
    df_perWeek['percent'] = df_perWeek.Arbeitszeit['sum']/39 *100
    df_perWeek['percent'] = pd.Series(["{0:.0f}%".format(val) for val in df_perWeek['percent']], index = df_perWeek.index)

    sheet_name2 = "ProjectPerWeek"
    with pd.ExcelWriter(new_file, mode='a', engine='openpyxl') as writer:  
        df_perWeek.to_excel(writer, sheet_name= sheet_name2)

    df_prj = df.groupby(['Projekt']).agg({'Arbeitszeit':['sum']})
    df_prj['percent']  = (df_prj['Arbeitszeit'] / df_prj['Arbeitszeit'].sum()) * 100
    df_prj['percent_visual'] = df_prj.apply(lambda row : visual(row['percent']), axis = 1)
    df_prj['percent'] = pd.Series(["{0:.2f}%".format(val) for val in df_prj['percent']], index = df_prj.index)

    #df_prj.drop('Woche',axis='columns', inplace=True)
    print("\nVerteilung:")
    print(df_prj)
    print_plotext(df_prj.index.array.to_numpy(),df_prj['Arbeitszeit'].to_numpy())

    # breaks
    df_noDrop = read_excel(latest_file, drop=False)
    df_breaks = calc_breaks(df_noDrop)
    df_breaks = df_breaks.groupby(['Datum']).first()
    selected_columns = ['Pausenzeit']
    df_out = df_breaks[((df_breaks['Arbeitszeit_sum'] <= 8) & (df_breaks['Pausenzeit'] < 0.5) & (df_breaks['Pausenzeit'] > 0))|((df_breaks['Arbeitszeit_sum'] > 8) & (df_breaks['Pausenzeit'] < 0.75) & (df_breaks['Pausenzeit'] > 0))]
    df_out = df_out.loc[:, selected_columns]
    print(df_out)
    
    print(f"Geschrieben: {new_file}")

    format_excel(new_file, sheet_name2)
    format_excel(new_file, sheet_name)

if __name__ == '__main__':
    main()
   