import pandas as pd
from lxml import etree as ET
from acdh_tei_pyutils.tei import TeiReader
from utils import gsheet_to_df, G_SHEET_LEGAL

df = gsheet_to_df(G_SHEET_LEGAL)
df['date_iso'] = df.apply(lambda row: f"{row['datum']}-01-01", axis=1)
doc = TeiReader('./data/indices/listlegal.xml')
for x in doc.any_xpath('.//tei:listBibl//tei:item'):
    x.getparent().remove(x)
list_bibl_node = doc.any_xpath('.//tei:listBibl')[0]

for i, row in df.iterrows():
    bibl = ET.Element("{http://www.tei-c.org/ns/1.0}bibl")
    bibl.attrib['corresp'] = row['idno']
    bibl.attrib['type'] = 'law'
    title = ET.Element("{http://www.tei-c.org/ns/1.0}title")
    title.attrib['level'] = 's'
    title.text = f"{row['title']}"
    if not pd.isna(row['title']):
        a_title = ET.Element("{http://www.tei-c.org/ns/1.0}title")
        a_title.attrib['level'] = 'a'
        a_title.text = f"{row['paragraphs']}, {row['title']}"
        bibl.append(a_title)
    bibl.append(title)
    date = ET.Element("{http://www.tei-c.org/ns/1.0}date")
    date.attrib['when-iso'] = row['date_iso']
    date.text = f"{row['datum']}"
    bibl.append(date)
    list_bibl_node.append(bibl)
    pages = ET.Element("{http://www.tei-c.org/ns/1.0}biblScope")
    pages.text = f"{row['paragraphs']}"
    bibl.append(pages)