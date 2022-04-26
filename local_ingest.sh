vendor/bin/arche-import-metadata html/arche-cases.rdf http://127.0.0.1/api username password
vendor/bin/arche-import-metadata html/arche.rdf http://127.0.0.1/api username password --retriesOnConflict 25
vendor/bin/arche-import-metadata html/arche-cases2.rdf http://127.0.0.1/api username password --retriesOnConflict 25
vendor/bin/arche-import-metadata html/arche-boehm.rdf http://127.0.0.1/api username password --retriesOnConflict 25
vendor/bin/arche-import-metadata html/arche-indices.rdf http://127.0.0.1/api username password --retriesOnConflict 25

# vendor/bin/arche-delete-resource https://id.acdh.oeaw.ac.at/legalkraus/title-img.jpg  http://127.0.0.1/api username password --recursively
# vendor/bin/arche-delete-resource https://id.acdh.oeaw.ac.at/legalkraus  http://127.0.0.1/api username password --recursively
# vendor/bin/arche-delete-resource https://id.acdh.oeaw.ac.at/pub-boehm1995 http://127.0.0.1/api username password --recursively