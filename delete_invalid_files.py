import csv
import glob
import os
from acdh_tei_pyutils.tei import TeiReader

files = glob.glob('./data/*/*.xml')
print(f"selected {len(files)}")

faulty = []
for x in files:
    try:
        doc = TeiReader(x)
    except Exception as e:
        faulty.append([x, e])

with open('faulty.csv', 'w', newline='') as csvfile:
    my_writer = csv.writer(csvfile, delimiter=',')
    my_writer.writerow(['path', 'error'])
    for x in faulty:
        my_writer.writerow([x[0], x[1]])

for x in faulty:
    new = x[0].replace('.xml', '.faulty')
    os.remove(x[0])

print(f"deleted {len(faulty)}, see `faulty.csv` for a list of invalid files")