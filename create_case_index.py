#!/usr/bin/env python
# coding: utf-8

import glob
import json
from acdh_tei_pyutils.tei import TeiReader
from lxml import etree as ET

files = glob.glob('./data/cases_tei/C*.xml')
tei_ns = {'tei': "http://www.tei-c.org/ns/1.0"}
faulty = []
cases = []
class_codes = {}
keywords = []
persons = {}
roles = {}
for x in files:
    try:
        doc = TeiReader(x)
    except Exception as e:
        faulty.append([x, e])
    case = {}
    case['id'] = doc.any_xpath('./@xml:id')[0]
    case['title'] = doc.any_xpath('.//tei:title/text()')[0]
    case['docs'] = [x.text for x in doc.any_xpath('.//tei:list[1]/tei:item/tei:ref')]
    case['docs_count'] = len(case['docs'])
    case['keywords'] = []
    for t in doc.any_xpath('.//tei:term/text()'):
       case['keywords'].append(t)
       keywords.append(t)
    for c in doc.any_xpath('.//tei:classCode'):
        cc = {}
        cc['id'] = c.attrib['scheme']
        cc['label'] = c.text
        class_codes[c.attrib['scheme']] = c.text
    actors = []
    for a in doc.any_xpath('.//tei:person[@role]'):
        actor = {}
        actor['id'] = a.xpath('./@ref')[0]
        actor['title'] = a.xpath('./tei:persName/text()', namespaces=tei_ns)[0]
        actor['role_id'] = a.xpath('@role', namespaces=tei_ns)[0]
        actor['role_label'] = a.xpath('./tei:ab/text()', namespaces=tei_ns)[0] 
        actors.append(actor)
        persons[actor['id']] = actor['title']
        roles[actor['role_id']] = actor['role_label']
    case['actors'] = actors
    case['actor_count'] = len(actors)
    cases.append(case)
data = {
    'cases': cases,
    'persons': persons,
    'roles': roles,
    'keywords': list(set(keywords)),
    'class_codes': class_codes
}
with open('cases-index.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)
