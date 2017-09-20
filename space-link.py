import json, requests, secrets, time

# import secrets
baseURL = secrets.baseURL
user = secrets.user
password = secrets.password

# authenticate to ArchivesSpace
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

print 'Editing Stage'

requests.packages.urllib3.disable_warnings()

dspaceURL = 'https://dspace-stage.library.jhu.edu'
handle = '1774.2/41445'

startTime = time.time()

endpoint = dspaceURL+'/rest/handle/'+handle
collection = requests.get(endpoint).json()
collectionID = collection['id']
collectionTitle = requests.get(endpoint).json()
endpoint = dspaceURL+'/rest/collections/'+str(collectionID)+'/items'
output = requests.get(endpoint).json()

for i in range (0, len (output)):
	itemList = []
	name = output[i]['name']
	itemID = output[i]['id']
	itemList.append(itemID)
	print itemList
	for j in itemList:
		itemsList = {}
		item = requests.get(dspaceURL + '/rest/items/' + str(itemID)).json()
		# bitstreams = requests.get(dspaceURL + '/rest/items/' + str(itemID) + '/bitstreams').json()
		title = item['name']
		# itemsList['filename'] = bitstreams[0]['name']
		query = '/search?page=1&filter_term[]={"primary_type":"archival_object"}&filter_term[]={"resource":"/repositories/3/resources/1045"}&q="' + title + '"'
		ASoutput = requests.get(baseURL + query, headers=headers).json()
		for ao in ASoutput['results']:
			asURI = ao['id']
			print itemID, asURI

elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print "%d:%02d:%02d" % (h, m, s)
