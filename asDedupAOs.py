import os, json, requests, ConfigParser, time
from jsonmerge import Merger
merger = Merger(schema)

startTime = time.time()

# setup jsonmerge
schema = {
            "properties": {
                "bar": {
                    "mergeStrategy": "append"
                    }
                }
            }

# function to find key in nested dicts: see http://stackoverflow.com/questions/9807634/find-all-occurences-of-a-key-in-nested-python-dictionaries-and-lists
def gen_dict_extract(key, var):
    if hasattr(var,'iteritems'):
        for k, v in var.iteritems():
            if k == key:
                yield v
            if isinstance(v, dict):
                for result in gen_dict_extract(key, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in gen_dict_extract(key, d):
                        yield result

# get local_settings
config = ConfigParser.ConfigParser()
config.read("secrets.cfg")

baseURL = config.get('ArchivesSpace', 'baseURL')
repository = config.get('ArchivesSpace', 'repository')
user = config.get('ArchivesSpace', 'user')
password = config.get('ArchivesSpace', 'password')

# authenticate
auth = requests.post(baseURL + '/users/'+user+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session':session}

# test for successful connection
def test_connection():
	try:
		requests.get(baseURL)
		print 'Connected!'
		return True

	except requests.exceptions.ConnectionError:
		print 'Connection error. Please confirm ArchivesSpace is running.  Trying again in 10 seconds.'

is_connected = test_connection()

while not is_connected:
	time.sleep(10)
	is_connected = test_connection()

# provide instructions
# print ''

# have user enter resource id
resource_id = raw_input('Enter resource id: ')

# return AO display title with container info
endpoint = '/repositories/' + repository + '/resources/' + resource_id + '/tree'
output = requests.get(baseURL + endpoint, headers=headers).json()

archivalObjects = []
for value in gen_dict_extract('record_uri', output):
    if 'archival_objects' in value:
        archivalObjects.append(value)

records = []
for archivalObject in archivalObjects:
    output = requests.get(baseURL + archivalObject, headers=headers).json()
    for display in gen_dict_extract('display_string', output):
        for level in gen_dict_extract('level', output):
            if 'Go-go posters, 1984-2005' in display and 'file' in level:
                records.append(output)

for j in records:
    base = None
    base = merger.merge(base, v1, meta={'version': 1})
    base = merger.merge(base, v2, meta={'version': 2})

# show script runtime
elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print 'Complete. Total script run time: ', '%d:%02d:%02d' % (h, m, s)
