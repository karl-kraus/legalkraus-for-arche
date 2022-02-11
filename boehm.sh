# bin/bash

rm -rf boehm_dl && rm -rf boehm_data && rm -rf boehm_tei
wget -O boehm_dl --header "PRIVATE-TOKEN: ${GITLAB_TOKEN}" https://gitlab.com/api/v4/projects/13601493/repository/archive?path=boehm/tei-files
mkdir boehm_data && mkdir boehm_tei
tar -xf boehm_dl -C boehm_data
find -path "*boehm/tei-files/boehm_*.xml" -exec cp -prv '{}' './boehm_tei' ';'
rm -rf boehm_data && rm -rf boehm_dl
find ./boehm_tei/ -type f -name "*.xml"  -print0 | xargs -0 sed -i -e 's@.jpg"@.tif"@g'
find ./boehm_tei/ -type f -name "*.xml"  -print0 | xargs -0 sed -i -e 's@<div xmlns="http://www.tei-c.org/ns/1.0"@<div@g'
find ./boehm_tei/ -type f -name "*.xml"  -print0 | xargs -0 sed -i -e 's@ xmlns:ko="https://www.kraus.wienbibliothek.at/"@@g'
find ./boehm_tei/ -type f -name "*.xml"  -print0 | xargs -0 sed -i -e 's@<TEI xmlns="http://www.tei-c.org/ns/1.0"@ <TEI xmlns="http://www.tei-c.org/ns/1.0" xmlns:ko="https://www.kraus.wienbibliothek.at/"@g'