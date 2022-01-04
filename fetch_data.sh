# bin/bash
echo $GITLAB_TOKEN
wget -O downloaded_data --header "PRIVATE-TOKEN: ${GITLAB_TOKEN}" https://gitlab.com/api/v4/projects/13601493/repository/archive?path=objects
tar -xf downloaded_data && rm downloaded_data
rm -rf ./data/editions && mkdir -p ./data/editions
rm -rf ./data/indices && mkdir -p ./data/indices
find -path "*objects/D_*.xml" -exec cp -prv '{}' './data/editions' ';'
rm -rf ./data-*

