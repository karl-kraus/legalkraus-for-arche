import glob
import os
import ciso8601
import time
import typesense

from typesense.api_call import ObjectNotFound
from acdh_tei_pyutils.tei import TeiReader
from tqdm import tqdm
from create_case_index import date_from_tei


files = glob.glob('./data/editions/*.xml')
TYPESENSE_API_KEY = os.environ.get("TYPESENSE_API_KEY", "xyz")


client = typesense.Client({
  'nodes': [{
    'host': os.environ.get('TYPESENSE_HOST','localhost'), # For Typesense Cloud use xxx.a1.typesense.net
    'port': os.environ.get('TYPESENSE_PORT', '8108'),      # For Typesense Cloud use 443
    'protocol': os.environ.get('TYPESENSE_PROTOCOL', 'http')   # For Typesense Cloud use https
  }],
  'api_key': TYPESENSE_API_KEY,
  'connection_timeout_seconds': 120
})

try:
    client.collections['legalkraus'].delete()
except ObjectNotFound:
    pass

current_schema = {
    'name': 'legalkraus',
    'fields': [
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
            'optional': True
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
for x in tqdm(files, total=len(files)):
    record = {}
    doc = TeiReader(x)
    body = doc.any_xpath('.//tei:body')[0]
    record['rec_id'] = os.path.split(x)[-1]
    record['title'] = " ".join(" ".join(doc.any_xpath('.//tei:titleStmt/tei:title[1]//text()')).split())
    date_str = date_from_tei(doc,'1800-01-01' )
    try:
        ts = ciso8601.parse_datetime(date_str)
    except ValueError:
        ts = ciso8601.parse_datetime('1800-01-01')

    record['date'] = int(time.mktime(ts.timetuple()))
    record['persons'] = [
        " ".join(" ".join(x.xpath('.//text()')).split()) for x in doc.any_xpath('.//tei:person/tei:persName')
    ]
    record['places'] = [
         " ".join(" ".join(x.xpath('.//text()')).split()) for x in doc.any_xpath('.//tei:place[@xml:id]/tei:placeName')
    ]
    record['works'] = [
         " ".join(" ".join(x.xpath('.//text()')).split()) for x in doc.any_xpath('.//tei:listBibl//tei:bibl[@xml:id]/tei:title')
    ]
    record['keywords'] = [
        x.text for x in doc.any_xpath('.//tei:keywords/tei:term')
    ]
    record['materials'] = [
        x.text for x in doc.any_xpath('.//tei:ab[@type="materiality"]/tei:objectType')
    ]
    record['full_text'] = " ".join(''.join(body.itertext()).split())
    records.append(record)

make_index = client.collections['legalkraus'].documents.import_(records)
# print(make_index)
print('done with indexing')