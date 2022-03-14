import glob
import json
import xmltodict
from acdh_tei_pyutils.tei import TeiReader

files = glob.glob('./data/indices/*.xml')

for x in files:
    doc = TeiReader(x)
    for bad in doc.any_xpath('.//tei:listEvent'):
        bad.getparent().remove(bad)
    for bad in doc.any_xpath('.//tei:place//tei:listBibl'):
        bad.getparent().remove(bad)
    for bad in doc.any_xpath('.//tei:person//tei:listBibl'):
        bad.getparent().remove(bad)
    for bad in doc.any_xpath('.//tei:org//tei:listBibl'):
        bad.getparent().remove(bad)
    data = xmltodict.parse(doc.return_string())
    json_file = f"{x.replace('.xml', '.json')}"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)