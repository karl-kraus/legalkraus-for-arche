from acdh_tei_pyutils.tei import TeiReader

ns = {
    "tei": "http://www.tei-c.org/ns/1.0",
    "xml": ""
}
BASE_URL = "https://raw.githubusercontent.com/arthur-schnitzler/schnitzler-entities/main/indices/"
URLS = [
    "bibl",
    "org",
    "place",
    "person"
]

for x in URLS:
    f_name = f"list{x}.xml"
    url = f"{BASE_URL}{f_name}"
    print(f"downloading {url}")
    doc = TeiReader(url)
    for bad in doc.any_xpath("//*[@xml:id and not(.//tei:bibl[@n='5'])]"):
        bad.getparent().remove(bad)
    if x == "bibl":
        doc.tree_to_file("./data/indices/listwork.xml")
    else:
        doc.tree_to_file(f"./data/indices/{f_name}")