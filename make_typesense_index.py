import glob
import os
import ciso8601
import time
import typesense

from typesense.api_call import ObjectNotFound
from acdh_cfts_pyutils import TYPESENSE_CLIENT as client
from acdh_cfts_pyutils import CFTS_COLLECTION
from acdh_tei_pyutils.tei import TeiReader
from tqdm import tqdm
from create_case_index import date_from_doc


files = glob.glob('./data/editions/*.xml')

try:
    client.collections['legalkraus'].delete()
except ObjectNotFound:
    pass

current_schema = {
    'name': 'legalkraus',
    'fields': [
        {
            'name': 'id',
            'type': 'string'
        },
        {
            'name': 'rec_id',
            'type': 'string'
        },
        {
            'name': 'title',
            'type': 'string'
        },
        {
            'name': 'full_text',
            'type': 'string'
        },
        {
            'name': 'date',
            'type': 'int64',
            'optional': True,
            'facet': True,
        },
        {
            'name': 'year',
            'type': 'int32',
            'optional': True,
            'facet': True,
        },
        {
            'name': 'persons',
            'type': 'string[]',
            'facet': True,
            'optional': True
        },
        {
            'name': 'places',
            'type': 'string[]',
            'facet': True,
            'optional': True
        },
        {
            'name': 'orgs',
            'type': 'string[]',
            'facet': True,
            'optional': True
        },
        {
            'name': 'works',
            'type': 'string[]',
            'facet': True,
            'optional': True
        },
        {
            'name': 'keywords',
            'type': 'string[]',
            'facet': True,
            'optional': True
        },
        {
            'name': 'materials',
            'type': 'string[]',
            'facet': True,
            'optional': True
        },
    ]
}

client.collections.create(current_schema)

records = []
cfts_records = []
for x in tqdm(files, total=len(files)):
    record = {}
    cfts_record = {
        'project': 'legalkraus',
    }
    doc = TeiReader(x)
    body = doc.any_xpath('.//tei:body')[0]
    record['id'] = os.path.split(x)[-1].replace('.xml', '')
    cfts_record['id'] = record['id']
    cfts_record['resolver'] = f"https://acdh-oeaw.github.io/kraus-static/{record['id']}.html"
    record['rec_id'] = os.path.split(x)[-1]
    cfts_record['rec_id'] = record['rec_id']
    record['title'] = " ".join(" ".join(doc.any_xpath('.//tei:titleStmt/tei:title[1]//text()')).split())
    cfts_record['title'] = record['title']
    date_str = date_from_doc(doc,'1920-01-01')
    try:
        record['year'] = int(date_str[:4])
        cfts_record['year'] = record['year']
    except ValueError:
        pass
    try:
        ts = ciso8601.parse_datetime(date_str)
    except ValueError:
        ts = ciso8601.parse_datetime('1920-01-01')

    record['date'] = int(time.mktime(ts.timetuple()))
    cfts_record['date'] = record['date']
    record['persons'] = [
        " ".join(" ".join(x.xpath('.//text()')).split()) for x in doc.any_xpath('.//tei:back//tei:person/tei:persName')
    ]
    cfts_record['persons'] = record['persons']
    record['places'] = [
         " ".join(" ".join(x.xpath('.//text()')).split()) for x in doc.any_xpath('.//tei:back//tei:place[@xml:id]/tei:placeName')
    ]
    cfts_record['places'] = record['places']
    record['orgs'] = [
         " ".join(" ".join(x.xpath('.//text()')).split()) for x in doc.any_xpath('.//tei:back//tei:org[@xml:id]/tei:orgName')
    ]
    cfts_record['orgs'] = record['orgs']
    record['works'] = [
         " ".join(" ".join(x.xpath('.//text()')).split()) for x in doc.any_xpath('.//tei:back//tei:listBibl//tei:bibl[@xml:id]/tei:title')
    ]
    cfts_record['works'] = record['works']
    record['keywords'] = [
        x.text for x in doc.any_xpath('.//tei:keywords/tei:term')
    ]
    cfts_record['keywords'] = record['keywords']

    record['materials'] = [
        x.text for x in doc.any_xpath('.//tei:ab[@type="materiality"]/tei:objectType')
    ]
    record['full_text'] = " ".join(''.join(body.itertext()).split())
    cfts_record['full_text'] = record['full_text']
    records.append(record)
    cfts_records.append(cfts_record)

make_index = client.collections['legalkraus'].documents.import_(records)
print('done with indexing')

make_index = CFTS_COLLECTION.documents.import_(cfts_records)
print('done with central indexing')