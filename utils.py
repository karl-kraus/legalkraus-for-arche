from io import BytesIO
import requests
import pandas as pd


def gsheet_to_df(gdrive_url):
    url = f"{gdrive_url}&output=csv"
    r = requests.get(url)
    print(r.status_code)
    data = r.content
    df = pd.read_csv(BytesIO(data))
    return df