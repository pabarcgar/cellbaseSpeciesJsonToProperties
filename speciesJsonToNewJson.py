#!/usr/bin/python

# __author__ = 'parce'
import json
import collections

db_host = 'databaseHost'
db_port = 'databasePort'
seq_url = 'sequence_url'
var_url = 'variation_url'
reg_url = 'regulation_url'
database = 'database'


def cut_variation_url(variation_url):
    mysql_substr = 'mysql/'
    index = variation_url.find(mysql_substr)
    return variation_url[:index + len(mysql_substr)]


def get_ensembl_properties(phylo):
    ensembl_properties = {'host': phylo[db_host], 'port': phylo[db_port]}

    # sequence url
    seq_url = list({item['sequence_url'] for item in phylo['items']})
    ensembl_properties['sequence_url'] = seq_url[0]

    #variation url
    complete_var_urls = [item['variation_url'] for item in phylo['items'] if 'variation_url' in item]
    trimmed_var_urls = set(map(cut_variation_url, complete_var_urls))
    ensembl_properties['variation_url'] = list(trimmed_var_urls)[0]

    return ensembl_properties


# def get_utl(phylo):
#     seq_url = p
#     url_properties = {'sequence': }

def get_species_properties(phylo):
    species = []
    for specie in phylo['items']:
        species_dict = {}
        species_dict['name'] = specie['text']
        species_dict['assembly'] = [{'name':specie['assembly'], 'database':specie['database']}]
        #species_dict['database'] = specie['database']
        species.append(species_dict)

    return species


def process_phylo(phylo):
    phylo_dict = {}
    phylo_dict['ensembl_database'] = get_ensembl_properties(phylo)
    phylo_dict['species'] = get_species_properties(phylo)
    return phylo_dict


def sort_download_properties(download_properties):
    sorted_download_properties = {'items':[]}
    ordered_phylos = ['Vertebrates', 'Metazoa', 'Fungi', 'Protist', 'Plants']
    for phylo_name in ordered_phylos:
        phylo = download_properties[phylo_name]
        phylo['name'] = phylo_name
        sorted_download_properties['items'].append(phylo)
    return sorted_download_properties

f1 = open('species.json')
text = f1.read()
f1.close()
spinfo = json.loads(text)


download_properties = {}
for phylo in spinfo['items']:
    phylo_name = phylo['text']
    phylo_dict = process_phylo(phylo)
    download_properties[phylo_name] = phylo_dict

sorted_download_properties = sort_download_properties(download_properties)

properties = {'download': sorted_download_properties}

print json.dumps(properties)