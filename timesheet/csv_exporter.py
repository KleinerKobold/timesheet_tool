import pandas as pd
import math

from timesheet.configer import get_config

def round_hours(hours):
    full_hours = math.floor(hours)
    part = hours % 1
    if part == 0 or part == 0.25 or part == 0.5 or part == 0.75:
        return hours
    if part < 1 and part > 0.75:
        full_hours = full_hours + 1 
        part = 0
    if part < 0.75 and part > 0.5:
        part = 0.75
    if part < 0.5 and part > 0.25:
        part = 0.5
    if part > 0 and part < 0.25:        
        part = 0.25
    return full_hours+part

def csv_export(df):
    fileName, elements, round, codes, time = None, dict(), False, dict(), None
    config = get_config()
    try: 
        fileName = config["csv"]["fileName"]
        elements = config["csv"]["elements"]
        round = config["csv"]["round"]
    except:
        return None
    
    try:
        codes = config["csv"]["codes"]
    except:
        print("config: no codes found")
    
    try:
        time = config["csv"]["time"]
    except:
        pass

    if codes: 
        df["aktivitätencode"] = df["Projekt"].map(codes)
        df["aktivitätencode"] = df["aktivitätencode"].fillna('')
    df["element"] = df["Projekt"].map(elements)
    df2 = df[df['element'].notnull()]

    df2 = df2.rename(columns={"Datum": "date"})
    df2 = df2.rename(columns={"Arbeitszeit": "hours"})
    df2.sort_values(by='date', inplace=True)
    
    df_grp = df2.sort_values(['date','element'],ascending=False).groupby(['date','element','aktivitätencode']).sum()
    if round: 
        df_grp["hours"] = df_grp["hours"].map(round_hours)
    df_grp["comment"] = ""
    df_grp.to_csv(fileName,sep=';')

    fd = pd.read_csv(fileName, sep=";")
    fd["date"] = pd.to_datetime(fd["date"])
    fd['date'] = fd['date'].dt.strftime('%d.%m.%Y')
    fd.to_csv(fileName,sep=';', columns=["date","element","hours","comment","aktivitätencode"], header=True, index=False)
    pass