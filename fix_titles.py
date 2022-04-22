import glob
from acdh_tei_pyutils.tei import TeiReader
from tqdm import tqdm

files = glob.glob('./data/editions/D_*.xml')

for x in tqdm(files, total=len(files)):
    try:
        doc = TeiReader(x)
    except:
        continue
    f_name = [str(int(y)) for y in x.split('/')[-1].replace('D_', '').replace('.xml', '').split('-')[:2]]
    title = doc.any_xpath('.//tei:title[1]')[0]
    
    new_title = f"{f_name[0]}.{f_name[1]} {' '.join(title.text.split())}"
    title.text = new_title
    doc.tree_to_file(x)


files = glob.glob('./data/cases_tei/C_*.xml')

for x in tqdm(files, total=len(files)):
    try:
        doc = TeiReader(x)
    except:
        continue
    f_name = [str(int(y)) for y in x.split('/')[-1].replace('C_', '').replace('.xml', '').split('-')[:2]]
    title = doc.any_xpath('.//tei:title[1]')[0]
    
    new_title = f"Akte {f_name[0]} {' '.join(title.text.split())}"
    title.text = new_title
    doc.tree_to_file(x)
