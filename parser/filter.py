import pandas as pd
import datetime
from urllib.parse import quote
from urllib import request
import json

from database import engine


def date_filter(start_date, connection):
    headers = ['build_id', 'longitude', 'latitude']
    mydata = pd.DataFrame(columns=headers)
    end_date = start_date + datetime.timedelta(days=7)

    df = pd.read_sql_table('dataframe', con=connection)
    df['start_date'] = pd.to_datetime(df['start_date'], format='%d-%m-%Y', errors='coerce')
    df['end_date'] = pd.to_datetime(df['end_date'], format='%d-%m-%Y', errors='coerce')

    start_slice = df[
        ((df['start_date'] >= start_date) & (df['start_date'] <= end_date)) &
        ((df['end_date'] >= start_date) & (df['end_date'] <= end_date))
    ]

    res = start_slice["address"].tolist()
    for i in res:
        x = i.strip('"}{"').split('","')
        if len(x) == 1:
            x = x[0].split(', ')
        for j in x:
            new_string = []
            geocode_url = "https://geocode.gate.petersburg.ru/parse/free?street={0}".format(
                quote(j)
            )
            with request.urlopen(geocode_url) as geocode_res:
                json_res = json.load(geocode_res)
                if json_res.get('Building_ID'):
                    new_string.append(json_res['Building_ID'])
                    new_string.append(json_res['Longitude'])
                    new_string.append(json_res['Latitude'])
            if len(new_string) == len(headers):
                length = len(mydata)
                mydata.loc[length] = new_string
    mydata.to_sql('build_ids', con=connection, if_exists='replace')


if __name__ == "__main__":
    with engine.connect() as conn:
        date_filter(datetime.datetime.now(), conn)
