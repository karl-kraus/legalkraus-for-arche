import glob
from collections import defaultdict, OrderedDict
import pandas as pd
from lxml import etree as ET
from acdh_tei_pyutils.tei import TeiReader
from utils import gsheet_to_df, G_SHEET_LEGAL
from tqdm import tqdm

df = gsheet_to_df(G_SHEET_LEGAL)
LIST_LEGAL = "./data/indices/listlegal.xml"

df['date_iso'] = df.apply(lambda row: f"{row['datum']}-01-01", axis=1)
legal_doc = TeiReader(LIST_LEGAL)
for x in legal_doc.any_xpath('.//tei:listBibl/tei:*'):
    x.getparent().remove(x)
list_bibl_node = legal_doc.any_xpath('.//tei:listBibl')[0]

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

files = glob.glob('./data/editions/D_*.xml')
refs = defaultdict(set)
for x in tqdm(files, total=len(files)):
    try:
        doc = TeiReader(x)
    except:
        continue
    xml_id = x.split('/')[-1]
    for ref in doc.any_xpath('.//tei:rs[@type="law"]/@ref'):
        title = " ".join(doc.any_xpath('.//tei:title')[0].text.split())
        refs[ref].add(f"{title}|{xml_id}")

ref_lookup = OrderedDict(sorted(refs.items()))
for x in legal_doc.any_xpath('.//tei:bibl'):
    corresp = x.attrib['corresp']
    try:
        match = ref_lookup[corresp]
    except:
        continue
    for y in match:
        ref = ET.Element("{http://www.tei-c.org/ns/1.0}ref")
        ref.attrib['target'] = y.split('|')[1]
        ref.text = f"{y.split('|')[0]}"
        x.append(ref)

legal_doc.tree_to_file(LIST_LEGAL)