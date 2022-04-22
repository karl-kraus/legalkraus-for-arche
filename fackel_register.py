import glob

import pandas as pd
from lxml import etree as ET

from acdh_tei_pyutils.tei import TeiReader
from utils import gsheet_to_df, G_SHEET_FACKEL

def full_idno(row):
    if not pd.isna(row['p_to']):
        corresp = f"{row['idno']},{int(row['p_to']):03}"
    else:
        corresp = f"{row['idno']}"
    return corresp


df = gsheet_to_df(G_SHEET_FACKEL)
df[['p_from', 'p_to']] = df['pages'].str.split('–', 1, expand=True)
df['p_to'] = df['p_to'].fillna(df['p_from'])
df['corresp'] = df.apply (lambda row: full_idno(row), axis=1)
fackel_doc = TeiReader('./data/indices/listfackel.xml')
for x in fackel_doc.any_xpath('.//tei:listBibl/tei:bibl'):
    x.getparent().remove(x)
list_bibl_node = fackel_doc.any_xpath('.//tei:listBibl')[0]
for i, row in df.iterrows():
    bibl = ET.Element("{http://www.tei-c.org/ns/1.0}bibl")
    if not pd.isna(row['p_to']):
        corresp = f"{row['idno']},{int(row['p_to']):03}"
    else:
        corresp = f"{row['idno']}"
    bibl.attrib['corresp'] = "".join(corresp.split())
    bibl.attrib['type'] = 'fackel'
    title = ET.Element("{http://www.tei-c.org/ns/1.0}title")
    title.attrib['level'] = 's'
    title.text = f"{row['titel']}"
    if not pd.isna(row['title text']):
        a_title = ET.Element("{http://www.tei-c.org/ns/1.0}title")
        a_title.attrib['level'] = 'a'
        a_title.text = " ".join(row['title text'].split())
        bibl.append(a_title)
    bibl.append(title)
    author = ET.Element("{http://www.tei-c.org/ns/1.0}author")
    author.attrib['key'] = 'pmb11988'
    author.text = 'Karl Kraus'
    editor = ET.Element("{http://www.tei-c.org/ns/1.0}editor")
    editor.attrib['key'] = 'pmb11988'
    editor.text = 'Karl Kraus'
    bibl.append(author)
    bibl.append(editor)
    date = ET.Element("{http://www.tei-c.org/ns/1.0}date")
    date.attrib['when-iso'] = row['date_iso']
    date.text = row['date_written']
    bibl.append(date)
    num_issue = ET.Element("{http://www.tei-c.org/ns/1.0}num")
    num_issue.attrib['type'] = 'issue'
    num_issue.text = row['Nummer']
    num = ET.Element("{http://www.tei-c.org/ns/1.0}num")
    num.attrib['type'] = 'volume'
    num.text = row['Jahrgang']
    bibl.append(num)
    bibl.append(num_issue)
    list_bibl_node.append(bibl)
    if not pd.isna(row['pages']):
        pages = ET.Element("{http://www.tei-c.org/ns/1.0}biblScope")
        pages.text = f"{row['pages']}"
        pages.attrib['from'] = row['p_from']
        pages.attrib['to'] = row['p_to']
        bibl.append(pages)
    

with open('hans.xml', 'w', encoding='utf-8') as f:
    f.write(ET.tostring(list_bibl_node, pretty_print=True, encoding='utf-8').decode('utf-8'))

files = glob.glob('../data/objects/D_*.xml')
fackel_refs = set()
for x in files:
    try:
        doc = TeiReader(x)
    except:
        continue
    for ref in doc.any_xpath('.//tei:rs[@subtype="fackel"]/@ref'):
        fackel_refs.add(ref)
fackel_pages = {}
for x in fackel_refs:
    page = x.split(',')[-1]
    try:
        int(page)
    except:
        continue
    fackel_pages[x] = int(page)