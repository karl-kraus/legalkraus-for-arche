# bin/bash

rm -rf boehm_dl && rm -rf boehm_data && rm -rf boehm_tei
wget -O boehm_dl --header "PRIVATE-TOKEN: ${GITLAB_TOKEN}" https://gitlab.com/api/v4/projects/13601493/repository/archive?path=boehm/tei-files
mkdir boehm_data && mkdir boehm_tei
tar -xf boehm_dl -C boehm_data
find -path "*boehm/tei-files/boehm_*.xml" -exec cp -prv '{}' './boehm_tei' ';'
rm -rf boehm_data && rm -rf boehm_dl
