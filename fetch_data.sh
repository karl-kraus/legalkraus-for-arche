#!/bin/bash

rm -rf main.zip
rm -rf legalkraus-data-main
rm -rf ./data/editions
rm -rf ./data/indices
rm -rf ./data/cases_tei
wget https://github.com/karl-kraus/legalkraus-data/archive/refs/heads/main.zip
unzip main

mv ./legalkraus-data-main/collections ./data/cases_tei
mv ./legalkraus-data-main/objects ./data/editions
mv ./legalkraus-data-main/indices ./data/indices
rm -rf main.zip
rm -rf legalkraus-data-main
find ./data/cases_tei/ -type f -name "C_*.xml"  -print0 | xargs -0 sed -i 's@ref target="https://id.acdh.oeaw.ac.at/D_@ref target="https://id.acdh.oeaw.ac.at/legalkraus/D_@g'

echo "fetch indices"
python download_index_files.py


echo "delete files without revisionDesc status='done'"
find ./data/editions/ -type f -name "D_*.xml" -print0 | xargs --null grep -Z -L 'revisionDesc status="done"' | xargs --null rm

echo "delete file which cannot be parsed by lxml parser"
python delete_invalid_files.py

echo "fixing titles"
python fix_titles.py

echo "fix entity reference IDs"
find ./data/indices/ -type f -name "*.xml"  -print0 | xargs -0 sed -i -e 's@<person xml:id="person__@<person xml:id="pmb@g'
find ./data/indices/ -type f -name "*.xml"  -print0 | xargs -0 sed -i -e 's@<bibl xml:id="work__@<bibl xml:id="pmb@g'
find ./data/indices/ -type f -name "*.xml"  -print0 | xargs -0 sed -i -e 's@<org xml:id="org__@<org xml:id="pmb@g'
find ./data/indices/ -type f -name "*.xml"  -print0 | xargs -0 sed -i -e 's@<place xml:id="place__@<place xml:id="pmb@g'
find ./data/indices/ -type f -name "*.xml"  -print0 | xargs -0 sed -i -e 's@<settlement key="@<settlement key="pmb@g'
find ./data/indices/ -type f -name "*.xml"  -print0 | xargs -0 sed -i -e 's@<orgName key="@<orgName key="pmb@g'
find ./data/indices/ -type f -name "*.xml"  -print0 | xargs -0 sed -i -e 's@<placeName key="place__@<placeName key="pmb@g'
find ./data/editions/ -type f -name "D_*.xml"  -print0 | xargs -0 sed -i 's@ref="#@ref="#pmb@g'
find ./data/editions/ -type f -name "D_*.xml"  -print0 | xargs -0 sed -i 's@ref="https://pmb.acdh.oeaw.ac.at/entity/@ref="#pmb@g'
find ./data/cases_tei/ -type f -name "C_*.xml"  -print0 | xargs -0 sed -i 's@ref="https://pmb.acdh.oeaw.ac.at/entity/@ref="#pmb@g'

echo "add xml:id, prev and next attributes"
add-attributes -g "./data/editions/*.xml" -b "https://id.acdh.oeaw.ac.at/legalkraus"
add-attributes -g "./data/indices/*.xml" -b "https://id.acdh.oeaw.ac.at/legalkraus"
add-attributes -g "./data/cases_tei/*.xml" -b "https://id.acdh.oeaw.ac.at/legalkraus"

# echo "update Fackel Register"
# python fackel_register.py

# echo "update listlegal.xml"
# python listlegal.py

# echo "denormalize indices in objects"
# denormalize-indices -f "./data/editions/D_*.xml" -i "./data/indices/*.xml" -m ".//*[@ref]/@ref" -x ".//tei:titleStmt/tei:title[1]/text()" -b pmb11988

# echo "denormalize indices in cases"
# denormalize-indices -f "./data/cases_tei/C_*.xml" -i "./data/indices/*.xml" -m ".//*[@ref]/@ref" -x ".//tei:titleStmt/tei:title[1]/text()" -b pmb11988

# # echo "create cases-index.json"
# # python create_case_index.py

# # echo "and now to Boehm"
# # ./boehm.sh

# echo "make typesense index"
# python make_typesense_index.py