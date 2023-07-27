import pandas as pd
import math
from datetime import datetime, timedelta

from timesheet.configer import get_config


def divide(df: pd.DataFrame,
           searched_project: str,
           new_projects: dict) -> pd.DataFrame:

    filtered_df = df[df['Projekt'] == searched_project]

    for project_name in new_projects.keys():
        copied_df = filtered_df.copy()
        copied_df['Projekt'] = project_name
        multiplicator = new_projects[project_name]
        copied_df['Arbeitszeit'] = copied_df['Arbeitszeit'] * multiplicator

        df = pd.concat([df, copied_df], ignore_index=True)

    df = df[df['Projekt'] != searched_project]
    return df


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


def filter_df(df, days_to_export=0):
    if days_to_export == 0:
        return df
    date_to_export = datetime.today() - timedelta(days=days_to_export)
    value_to_check = pd.Timestamp(date_to_export.year, date_to_export.month, date_to_export.day)
    filter_mask = df['Datum'] > value_to_check
    return df[filter_mask]


def csv_export(df, days_to_export):
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
    if codes: 
        df["aktivitätencode"] = df["Projekt"].map(codes)
        df["aktivitätencode"] = df["aktivitätencode"].fillna('')
    
    if "dividers" in config["csv"].keys():
        for divider in config["csv"]["dividers"]:
            project = divider['divider']['name']
            new_projects = divider['divider']['targets']
            df = divide(df, project, new_projects)

    df["element"] = df["Projekt"].map(elements)
    if days_to_export > 0:
        df = filter_df(df, days_to_export)
    df2 = df[df['element'].notnull()]

    df2 = df2.rename(columns={"Datum": "date"})
    df2 = df2.rename(columns={"Arbeitszeit": "hours"})
    df2.sort_values(by='date', inplace=True)

    df_grp = df2.sort_values(['date','element'],ascending=False).groupby(['date','element','aktivitätencode']).sum(numeric_only=True)
    if round: 
        df_grp["hours"] = df_grp["hours"].map(round_hours)
    df_grp["comment"] = ""

    df_grp.to_csv(fileName,sep=';')

    fd = pd.read_csv(fileName, sep=";")
    fd["date"] = pd.to_datetime(fd["date"])
    fd['date'] = fd['date'].dt.strftime('%d.%m.%Y')
    fd.to_csv(fileName,sep=';', columns=["date","element","hours","comment","aktivitätencode"], header=True, index=False)
    pass