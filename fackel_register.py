import glob
import collections
import pandas as pd
from acdh_tei_pyutils.tei import TeiReader
from lxml import etree as ET
from collections import defaultdict
from utils import gsheet_to_df, G_SHEET_FACKEL

df = gsheet_to_df(G_SHEET_FACKEL)
LIST_FACKEL = "./data/indices/listfackel.xml"

df[['p_from', 'p_to']] = df['pages'].str.split('–', 1, expand=True)

def full_idno(row):
    if not pd.isna(row['p_from']):
        corresp = f"{row['idno']},{int(row['p_from']):03}"
    else:
        corresp = f"{row['idno']}"
    return "".join(corresp.split())

df['corresp'] = df.apply (lambda row: full_idno(row), axis=1)
df['p_to'] = df['p_to'].fillna(df['p_from'])
fackel_doc = TeiReader(LIST_FACKEL)
for x in fackel_doc.any_xpath('.//tei:listBibl/tei:bibl'):
    x.getparent().remove(x)
list_bibl_node = fackel_doc.any_xpath('.//tei:listBibl')[0]
for i, row in df.iterrows():
    bibl = ET.Element("{http://www.tei-c.org/ns/1.0}bibl")
    if not pd.isna(row['p_to']):
        corresp = f"{row['idno']},{int(row['p_to']):03}"
    else:
        corresp = f"{row['idno']}"
    bibl.attrib['corresp'] = row['corresp']
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

new_df = df[~df["idno"].str.contains(',')]
new_df[['p_to', 'p_from']] = new_df[['p_to', 'p_from']].astype('int')
files = glob.glob('./data/editions/D_*.xml')
idnos = set(df['idno'].values)
fackel_refs = defaultdict(set)
for x in files:
    try:
        doc = TeiReader(x)
    except:
        continue
    xml_id = x.split('/')[-1]
    for ref in doc.any_xpath('.//tei:rs[@subtype="fackel"]/@ref'):
        fid, value = ref.split(',')
        title = " ".join(doc.any_xpath('.//tei:title')[0].text.split())
        try:
            match = new_df.query(
                    f'idno=="{fid}" and p_from<={int(value)} and p_to>={int(value)}'
                )['corresp'].values[0]
        except:
            if ref in idnos:
                match = ref
            else:
                "NO MATCH"
        try:
            fackel_refs[match].add(f"{title}|{xml_id}__{ref}")
        except:
            pass
ref_lookup = collections.OrderedDict(sorted(fackel_refs.items()))

for x in fackel_doc.any_xpath('.//tei:bibl'):
    corresp = x.attrib['corresp']
    try:
        match = ref_lookup[corresp]
    except:
        continue
    for y in match:
        ref = ET.Element("{http://www.tei-c.org/ns/1.0}ref")
        ref.attrib['target'] = y.split('__')[1]
        ref.text = f"{y.split('__')[0]}"
        x.append(ref)
    
fackel_doc.tree_to_file(LIST_FACKEL)