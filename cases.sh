# bin/bash
echo "fetch cases data"
rm -rf cases_dl && rm -rf cases_data && rm -rf data/cases_tei
wget -O cases_dl --header "PRIVATE-TOKEN: ${GITLAB_TOKEN}" https://gitlab.com/api/v4/projects/13601493/repository/archive?path=collections
mkdir cases_data && mkdir -p data/cases_tei
tar -xf cases_dl -C cases_data
find -path "*collections/C_*.xml" -exec cp -prv '{}' './data/cases_tei' ';'
rm -rf cases_data && rm -rf cases_dl