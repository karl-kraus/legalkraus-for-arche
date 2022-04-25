#!/usr/bin/env python
# coding: utf-8

import glob
import json
from acdh_tei_pyutils.tei import TeiReader
from dateutil.parser import parse
from tqdm import tqdm

files = glob.glob('./data/cases_tei/C*.xml')
tei_ns = {'tei': "http://www.tei-c.org/ns/1.0"}
faulty = []


def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try: 
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False


def date_from_tei(path_to_file, default=""):
    """
    Tries to extract some iso-date from the passed in doc

    :param path_to_file: str, path the TEI-Doc
    :param default: str; a default value to be returned in case no useful date could be found
    """
    try:
        doc = TeiReader(path_to_file)
    except Exception as e:
        return default
    try:
        date_el = doc.any_xpath('.//tei:creation/tei:date')[0]
    except IndexError:
        return default
    date_attr = date_el.attrib.items()
    try:
        date = [x[1] for x in date_attr if is_date(x[1])][0]
    except IndexError:
        return default
    return date.strip()

def yield_cases(files):
    faulty = []
    class_codes = {}
    persons = {}
    orgs = {}
    roles = {}
    org_roles = {}
    for x in files:
        doc = None
        try:
            doc = TeiReader(x)
        except Exception as e:
            faulty.append([x, e])
            continue
        case = {}
        case['id'] = doc.any_xpath('./@xml:id')[0]
        case['title'] = doc.any_xpath('.//tei:title/text()')[0]
        case['docs'] = [x.text for x in doc.any_xpath('.//tei:list[1]/tei:item/tei:ref')]
        case['docs_count'] = len(case['docs'])
        case['keywords'] = []
        case['doc_objs'] = []
        kws = []
        for t in doc.any_xpath('.//tei:term/text()'):
            kws.append(t)
        case['keywords'] = list(set(kws))
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
        org_actors = []
        for a in doc.any_xpath('.//tei:org[@role]'):
            actor = {}
            actor['id'] = a.xpath('./@ref')[0]
            actor['title'] = a.xpath('./tei:orgName/text()', namespaces=tei_ns)[0]
            actor['role_id'] = a.xpath('@role', namespaces=tei_ns)[0]
            actor['role_label'] = a.xpath('./tei:ab/text()', namespaces=tei_ns)[0] 
            org_actors.append(actor)
            orgs[actor['id']] = actor['title']
            roles[actor['role_id']] = actor['role_label']
        case['org_actor'] = org_actors
        case['org_actor_count'] = len(org_actors)
        case['actors'] = actors
        case['actor_count'] = len(actors)
        try:
            case['first_doc'] = case['docs'][0]
            case['last_doc'] = case['docs'][-1]
        except IndexError:
            case['first_doc'] = ""
            case['last_doc'] = ""
        case['start_date'] = date_from_tei(f"./data/editions/{case['first_doc']}")
        case['end_date'] = date_from_tei(f"./data/editions/{case['last_doc']}", default='')
        for y in case['docs']:
            cur_doc = None
            item = {}
            item['works'] = {}
            item['orgs'] = {}
            item['persons'] = {}
            item['places'] = {}
            materiality = set()
            classcodes = set()
            keywords = set()
            item['id'] = y
            tei_path = f"./data/editions/{y}"
            try:
                cur_doc = TeiReader(tei_path)
            except:
                continue
            try:
                item['title'] = cur_doc.any_xpath('.//tei:title[1]/text()')[0]
            except IndexError:
                item['title'] = "no title"
            item['date'] = date_from_tei(tei_path, default="")
            for ent in cur_doc.any_xpath('.//tei:back/tei:listBibl/tei:bibl'):
                xml_id = ent.attrib["{http://www.w3.org/XML/1998/namespace}id"]
                title = ent.xpath('./*[1]')[0]
                norm_title =  ''.join(title.itertext()).strip()
                item['works'][xml_id] = " ".join(norm_title.split())
            for ent in cur_doc.any_xpath('.//tei:back/tei:listOrg/tei:org'):
                xml_id = ent.attrib["{http://www.w3.org/XML/1998/namespace}id"]
                title = ent.xpath('./*[1]')[0]
                norm_title =  ''.join(title.itertext()).strip()
                item['orgs'][xml_id] = " ".join(norm_title.split())
            for ent in cur_doc.any_xpath('.//tei:back/tei:listPlace/tei:place'):
                xml_id = ent.attrib["{http://www.w3.org/XML/1998/namespace}id"]
                title = ent.xpath('./*[1]')[0]
                norm_title =  ''.join(title.itertext()).strip()
                item['places'][xml_id] = " ".join(norm_title.split())
            for ent in cur_doc.any_xpath('.//tei:back/tei:listPerson/tei:person'):
                xml_id = ent.attrib["{http://www.w3.org/XML/1998/namespace}id"]
                title = ent.xpath('./*[1]')[0]
                norm_title =  ''.join(title.itertext()).strip()
                item['persons'][xml_id] = " ".join(norm_title.split())
            for x in cur_doc.any_xpath('.//tei:ab[@type="materiality"]/tei:objectType'):
                materiality.add(" ".join(x.text.split()))
            for x in cur_doc.any_xpath('.//tei:keywords/tei:term'):
                keywords.add(x.text)
            for x in cur_doc.any_xpath('.//tei:textClass/tei:classCode'):
                classcodes.add(x.text)
            item['classcodes'] = list(classcodes)
            item['keywords'] = list(keywords)
            item['materiality'] = list(materiality)
            try:
                item['facs'] = cur_doc.any_xpath('.//tei:graphic[@source="wienbibliothek"]/@url')[0]
            except IndexError:
                item['facs'] = "no facs"
            case['doc_objs'].append(item)
        yield case

print("writing case index part I")
with open('cases-index.json', 'w', encoding='utf-8') as f:
    f.write('{"cases": [')
    for i, x in tqdm(enumerate(yield_cases(files)), total=len(files)):
        json.dump(x, f, ensure_ascii=False)
        if int(i)+1 != len(files):
            f.write(', ')
    f.write(']}')

with open('./cases-index.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

class_codes = {}
keywords = set()
persons = {}
roles = {}
orgs = {}
org_roles = {}
for x in data['cases']:
    keywords.update(x['keywords'])
    for a in x['actors']:
        persons[a['id']] = a['title']
        roles[a['role_id']] = a['role_label']
    for a in x['org_actor']:
        orgs[a['id']] = a['title']
        org_roles[a['role_id']] = a['role_label']

data['roles'] = roles
data['org_roles'] = org_roles
data['keywords'] = list(keywords)
data['persons'] = persons
data['orgs'] = orgs

with open('./cases-index.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)

with open('./cases-index.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("writing case index part II")

failed = []
for case in tqdm(data['cases'], total=len(data['cases'])):
    persons = dict()
    places = dict()
    orgs = dict()
    works = dict()
    subjects = set()
    class_codes = set()
    materiality = dict()
    hands = set()
    for d in case['docs']:
        try:
            doc = TeiReader(f"./data/editions/{d}")
        except:
            failed.append(d)
            continue
        for ent in doc.any_xpath('.//tei:back/tei:listPerson/tei:person'):
            xml_id = ent.attrib["{http://www.w3.org/XML/1998/namespace}id"]
            title = ent.xpath('./*[1]')[0]
            norm_title =  ''.join(title.itertext()).strip()
            persons[xml_id] = " ".join(norm_title.split())
        for ent in doc.any_xpath('.//tei:back/tei:listPlace/tei:place'):
            xml_id = ent.attrib["{http://www.w3.org/XML/1998/namespace}id"]
            title = ent.xpath('./*[1]')[0]
            norm_title =  ''.join(title.itertext()).strip()
            places[xml_id] = " ".join(norm_title.split())
        for ent in doc.any_xpath('.//tei:back/tei:listOrg/tei:org'):
            xml_id = ent.attrib["{http://www.w3.org/XML/1998/namespace}id"]
            title = ent.xpath('./*[1]')[0]
            norm_title =  ''.join(title.itertext()).strip()
            orgs[xml_id] = " ".join(norm_title.split())
        for ent in doc.any_xpath('.//tei:back/tei:listBibl/tei:bibl'):
            xml_id = ent.attrib["{http://www.w3.org/XML/1998/namespace}id"]
            title = ent.xpath('./*[1]')[0]
            norm_title =  ''.join(title.itertext()).strip()
            works[xml_id] = " ".join(norm_title.split())
        for x in doc.any_xpath('.//tei:keywords/tei:term'):
            subjects.add(x.text)
        for x in doc.any_xpath('.//tei:textClass/tei:classCode'):
            class_codes.add(x.text)
        for x in doc.any_xpath('.//tei:ab[@type="materiality"]/tei:objectType'):
            materiality[x.attrib['ref']] = " ".join(x.text.split())
        for x in doc.any_xpath('.//tei:handNote/@scribeRef'):
            if len(x) > 3:
                hands.add(x.replace('#', 'pmb'))
    case['men_pers'] = persons
    case['men_pl'] = places
    case['men_orgs'] = orgs
    case['men_works'] = works
    case['men_subjects'] = list(subjects)
    case['men_class_codes'] = list(class_codes)
    case['hands'] = list(hands)
    case['materiality'] = materiality

with open('./cases-index.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)