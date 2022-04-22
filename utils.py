from io import BytesIO
import requests
import pandas as pd

G_SHEET_FACKEL = "1YuisJT2W7qSBqhlAMykUN2lpvVp_H-wiakhKN2KNfTw"
G_SHEET_LEGAL = "1rBGpl4WYibua5w6rYYxZ6d9CdpGS704DnH3ycH2lxrA"

def gsheet_to_df(gdrive_url):
    GDRIVE_BASE_URL = "https://docs.google.com/spreadsheet/ccc?key="
    url = f"{GDRIVE_BASE_URL}{gdrive_url}&output=csv"
    r = requests.get(url)
    print(r.status_code)
    data = r.content
    df = pd.read_csv(BytesIO(data))
    return df