#!/usr/bin/env python

import os, requests, json, sys, logging, ConfigParser, urllib2, csv
sys.path.append('agentarchives')
from agentarchives import archivesspace

config = ConfigParser.ConfigParser()
config.read('secrets.cfg')

# Logging configuration
logging.basicConfig(filename=config.get('Logging', 'filename'),format=config.get('Logging', 'format', 1), datefmt=config.get('Logging', 'datefmt', 1), level=config.get('Logging', 'level', 0))
# Sets logging of requests to WARNING to avoid unneccessary info
logging.getLogger("requests").setLevel(logging.WARNING)

config = {'repository':config.get('ArchivesSpace', 'repository'), 'user': config.get('ArchivesSpace', 'user'), 'password': config.get('ArchivesSpace', 'password'), 'baseURL': config.get('ArchivesSpace', 'baseURL')}

def compile_data(data):
	for child in data["children"]:
		make_row(child)
		if child["has_children"]:
			compile_data(child)

def make_row(component):
	row = [component["levelOfDescription"].encode("utf-8"), component["title"].encode("utf-8"), component["dates"].encode("utf-8"), component["date_expression"].encode("utf-8"), component["instance_type_1"].encode("utf-8"), component["instance_indicator_1"].encode("utf-8"), component["instance_type_2"].encode("utf-8"), component["instance_indicator_2"].encode("utf-8"),  component["instance_barcode"].encode("utf-8"), component["id"].encode("utf-8")]
	writer.writerow(row)

# have user enter resource identifier
resource_id = raw_input('Enter resource id: ')

print 'Creating a csv'
spreadsheet = '{}_allAOs.csv'.format(resource_id)
writer = csv.writer(open(spreadsheet, 'w'))
writer.writerow(["levelOfDescription", "title", "dates", "date_expression", "instance_type_1", "instance_indicator_1", "instance_type_2", "instance_indicator_2", "instance_barcode", "id"])
client = archivesspace.ArchivesSpaceClient(config["baseURL"], config["user"], config["password"])
print 'Getting children of resource ' + resource_id
data = client.get_resource_component_children('repositories/3/resources/'+str(resource_id))
compile_data(data)
print 'Done!'
