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


def get_all_alias():
    server_properties_file = open('server.properties')
    server_properties_lines = server_properties_file.readlines()
    alias_lines = [alias_line[:-1] for alias_line in server_properties_lines if 'ALIAS' in alias_line]
    server_properties_file.close()
    return alias_lines


# def cut_variation_url(variation_url):
#     mysql_substr = 'mysql/'
#     index = variation_url.find(mysql_substr)
#     return variation_url[:index + len(mysql_substr)]


# def get_ensembl_properties(phylo):
#     ensembl_properties = {'host': phylo[db_host], 'port': phylo[db_port]}
#
#     # sequence url
#     seq_url = list({item['sequence_url'] for item in phylo['items']})
#     ensembl_properties['sequence_url'] = seq_url[0]
#
#     #variation url
#     complete_var_urls = [item['variation_url'] for item in phylo['items'] if 'variation_url' in item]
#     trimmed_var_urls = set(map(cut_variation_url, complete_var_urls))
#     ensembl_properties['variation_url'] = list(trimmed_var_urls)[0]
#
#     return ensembl_properties


def get_species_id(species_name, all_alias):
    specie_aliases = [line.split("ALIAS = ")[1] for line in all_alias if species_name in line]
    if len(specie_aliases) == 1:
        return specie_aliases[0].split(',')[2]
    else:
        print species_name + ' has ' + str(len(specie_aliases)) + ' aliases'
        return ''


def get_species_properties(phylo, all_alias):
    scientific_name_tag = 'scientificName'
    ensembl_version_tag = 'ensemblVersion'
    species = []
    for specie in phylo['items']:
        species_name = specie['text']
        existing_specie = [ sp for sp in species if sp[scientific_name_tag] == species_name ]
        if 'core_' in specie['database']:
            ensembl_version = specie['database'].split('core_')[1]
        elif specie['text'] == 'Saccharomyces cerevisiae':
            ensembl_version = '24_77_4'
        if len(existing_specie) == 0:
            species_dict = collections.OrderedDict()
            species_dict['id'] = get_species_id(species_name, all_alias)
            species_dict[scientific_name_tag] = species_name
            species_dict['assemblies'] = [{'name':specie['assembly'], ensembl_version_tag:ensembl_version}]
            species_dict['data'] = ["genome_info", "genome_sequence", "gene", "variation", "regulation"]
            species.append(species_dict)
        else:
            #print specie
            existing_specie[0]['assemblies'].append({'name':specie['assembly'], ensembl_version_tag:ensembl_version})
            #species_dict['database'] = specie['database']

    return species


# def process_phylo(phylo, all_alias):
#     phylo_dict = {}
#     #phylo_dict['ensembl_database'] = get_ensembl_properties(phylo)
#     phylo_dict['species'] = get_species_properties(phylo, all_alias)
#     return phylo_dict


def sort_download_properties(download_properties):
    sorted_download_properties = collections.OrderedDict()
    ordered_phylos = ['Vertebrates', 'Metazoa', 'Fungi', 'Protist', 'Plants']
    for phylo_name in ordered_phylos:
        phylo = download_properties[phylo_name]
        sorted_download_properties[phylo_name.lower()] = phylo
    return sorted_download_properties

f1 = open('species.json')
text = f1.read()
f1.close()
spinfo = json.loads(text)

f1 = open('generalOptions.json')
text = f1.read()
f1.close()
general_info = json.loads(text, object_pairs_hook=collections.OrderedDict)

all_alias = get_all_alias()

download_properties = {}
for phylo in spinfo['items']:
    phylo_name = phylo['text']
    #phylo_dict = process_phylo(phylo, all_alias)
    download_properties[phylo_name] = get_species_properties(phylo, all_alias)

sorted_download_properties = sort_download_properties(download_properties)

general_info['species'] = sorted_download_properties

print json.dumps(general_info)
