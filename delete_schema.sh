# bin/bash
echo "delete schema linking"
find ./data/editions/ -type f -name "D_*.xml"  -print0 | xargs -0 sed -i 's@^.*TEI xmlns@<TEI xmlns@g'
find ./data/cases_tei/ -type f -name "C_*.xml"  -print0 | xargs -0 sed -i 's@^.*TEI xmlns@<TEI xmlns@g'
echo "done with delete schema linking"