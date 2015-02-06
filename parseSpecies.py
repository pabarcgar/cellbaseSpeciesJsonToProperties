#!/usr/bin/python

# __author__ = 'parce'
import json

f1 = open('species.json')
text = f1.read()
f1.close()
spinfo = json.loads(text)

db_host = 'databaseHost'
db_port = 'databasePort'
seq_url = 'sequence_url'
var_url = 'variation_url'
reg_url = 'regulation_url'
database = 'database'

for phylo in spinfo['items']:
    phylo_name = phylo['text']
    print phylo_name + '.' + db_host + '=' + phylo[db_host]
    print phylo_name + '.' + db_port + '=' + phylo[db_port]
    for specie in phylo['items']:
        specie_name = specie['text']
        assembly = specie['assembly'].replace('.','_')
        specie_database = specie[database]
        print ".".join([phylo_name, specie_name, assembly, database]).replace(' ', '_') + '=' + specie_database
        if seq_url in specie:
            sequence_url = specie[seq_url]
            print ".".join([phylo_name, specie_name, assembly, seq_url]).replace(' ', '_') + '=' + sequence_url
        if var_url in specie:
            variation_url = specie[var_url]
            print ".".join([phylo_name, specie_name, assembly, var_url]).replace(' ', '_') + '=' + variation_url
        if reg_url in specie:
            regulation_url = specie[reg_url]
            print ".".join([phylo_name, specie_name, assembly, reg_url]).replace(' ', '_') + '=' + regulation_url
