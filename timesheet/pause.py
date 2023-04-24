import pandas as pd


def calc_breaks(df):
    df['Datum_str'] = df['Datum'].astype(str)
    df['Startzeit_str'] = df['Startzeit'].astype(str)
    df['Startzeit_str'] = (df['Datum_str']+ ' ' + df['Startzeit_str'])
    df['Startzeit_date'] = pd.to_datetime(df['Startzeit_str'], format='%Y-%m-%d %H:%M:%S')
    df['Endzeit_str'] = df['Endzeit'].astype(str)
    df['Endzeit_str'] = (df['Datum_str']+ ' ' + df['Endzeit_str'])
    df['Endzeit_date'] = pd.to_datetime(df['Endzeit_str'], format='%Y-%m-%d %H:%M:%S')

    df_grouped = df.groupby('Datum')
    df_min_start = df_grouped['Startzeit_date'].min()
    df_min_end = df_grouped['Endzeit_date'].max()

    df = df.join(df_min_start, on='Datum', rsuffix='_min_start')
    df = df.join(df_min_end, on='Datum', rsuffix='_max_end')

    df['Arbeitstag'] = df.Endzeit_date_max_end - df.Startzeit_date_min_start
    df['Arbeitstag'] = df['Arbeitstag'].dt.total_seconds() / 3600

    df_datum = df.groupby(['Datum'])
    df_sum_arbeitszeit = df_datum.Arbeitszeit.sum()

    df = df.join(df_sum_arbeitszeit, on='Datum', rsuffix='_sum')
    df['Pausenzeit'] = df['Arbeitstag'] - df['Arbeitszeit_sum']

    return df
