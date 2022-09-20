import pandas as pd
import os
import jinja2
import glob

from tqdm import tqdm
from datetime import date
from acdh_tei_pyutils.tei import TeiReader

files = sorted(glob.glob('./data/editions/*.xml'))
CUT_OFF = len(files)
CMIF = './data/indices/cmif.xml'
# CUT_OFF = 300

def fix_hashtag(pmb_id):
    if pmb_id.startswith('#'):
        return pmb_id
    else:
        f"#{pmb_id}"

letters = []
for x in tqdm(files[:CUT_OFF], total=CUT_OFF):
    _, tail = os.path.split(x)
    try:
        doc = TeiReader(x)
    except:
        continue
    try:
        sender_pmb = doc.any_xpath('.//tei:correspAction[1]/tei:*/@ref')[0]
    except:
        continue
    try:
        sender_place_pmb = doc.any_xpath('.//tei:correspAction[1]//tei:settlement/@ref')[0]
    except:
        continue
    try:
        receiver_pmb = doc.any_xpath('.//tei:correspAction[2]/tei:*/@ref')[0]
    except:
        receiver_pmb = 'unbekannt'
    try:
        receiver_place_pmb = doc.any_xpath('.//tei:correspAction[2]//tei:settlement/@ref')[0]
    except:
        receiver_place_pmb = 'unbekannt'
    try:
        sent_date = doc.any_xpath('.//tei:date[@type="sortDate"]')[0]
    except IndexError:
        sent_date = None
    if sent_date is not None:
        try:
            sent_date_str = sent_date.text
            sent_date = sent_date.attrib['when-iso']
        except:
            sent_date = None
            sent_date_str = 'unbekannt'
            
    item = {
        'id': tail.replace('.xml', '.html'),
        'sender_pmb': fix_hashtag(sender_pmb),
        'sender_place_pmb': fix_hashtag(sender_place_pmb),
        'receiver_pmb': fix_hashtag(receiver_pmb),
        'receiver_place_pmb': fix_hashtag(receiver_place_pmb),
        'sent_date': sent_date,
        'sent_date_str': sent_date_str
    }
    letters.append(item)

df = pd.DataFrame(letters)
doc = TeiReader('./data/indices/listperson.xml')
items = []
for x in doc.any_xpath('.//tei:person[@xml:id]'):
    item = {
        'id': f"#{x.attrib['{http://www.w3.org/XML/1998/namespace}id']}",
        'type': 'person'
    }
    try:
        gnd = x.xpath('./*[@subtype="gnd"]')[0]
        gnd = gnd.text
    except IndexError:
        gnd = None
    if gnd is None:
        try:
            gnd = x.xpath('.//*[@type="uri_gnd"]')[0].text
        except:
            gnd = None
    item['gnd'] = gnd
    try:
        first_name = x.xpath('.//tei:forename', namespaces=doc.nsmap)[0].text
    except:
        first_name = ''
    try:
        surname = x.xpath('.//tei:surname', namespaces=doc.nsmap)[0].text
    except:
        surname = ''
    item['name'] = f"{first_name} {surname}".strip() 
    items.append(item)
doc = TeiReader('./data/indices/listorg.xml')
for x in doc.any_xpath('.//tei:org[@xml:id]'):
    item = {
        'id': f"#{x.attrib['{http://www.w3.org/XML/1998/namespace}id']}",
        'type': 'org'
    }
    gnd = None
    for idno in x.xpath('./tei:idno', namespaces=doc.nsmap):
        if 'd-nb.info' in idno.text:
            gnd = idno.text
            continue
    if gnd is None:
        try:
            gnd = x.xpath('.//*[@type="uri_gnd"]')[0].text
        except:
            gnd = None
    item['gnd'] = gnd
    try:
        name = x.xpath('./tei:orgName', namespaces=doc.nsmap)[0].text
    except:
        name = 'unbekannt'
    item['name'] = name.replace('&', '&amp;')
    items.append(item)
df_persons = pd.DataFrame(items)
df = df.merge(df_persons, how='left', left_on='sender_pmb', right_on='id')
df = df.merge(df_persons, how='left', left_on='receiver_pmb', right_on='id')
items = []
doc = TeiReader('./data/indices/listplace.xml')
for x in doc.any_xpath('.//tei:place[@xml:id]'):
    item = {
        'place_id': f"#{x.attrib['{http://www.w3.org/XML/1998/namespace}id']}"
    }
    try:
        name = x.xpath('./tei:placeName', namespaces=doc.nsmap)[0].text
    except:
        name = 'unbekannt'
    item['place_name'] = name.replace('&', '&amp;')
    gnd = None
    for idno in x.xpath('./tei:idno', namespaces=doc.nsmap):
        if 'geonames.org' in idno.text:
            gnd = idno.text
            continue
    item['geonames'] = gnd
    items.append(item)
places_df = pd.DataFrame(items)
df = df.merge(places_df, how='left', left_on='sender_place_pmb', right_on='place_id')
df = df.merge(places_df, how='left', left_on='receiver_place_pmb', right_on='place_id')
df.fillna('', inplace=True)
df.to_csv('main.csv', index=False)

templateLoader = jinja2.FileSystemLoader(searchpath=".")
templateEnv = jinja2.Environment(loader=templateLoader)
template = templateEnv.get_template('./templates/cmif.j2')
data = []
for i, row in df.iterrows():
    data.append(dict(row))

with open(CMIF, 'w') as f:
    f.write(
        template.render(
            {
                "data": data,
                "date": f"{date.today()}"
            }
        )
    )

doc = TeiReader(CMIF)
doc.tree_to_file(CMIF)