import json
import requests

baseURL = 'http://YOURBACKENDURL:8089'
user='YOURUSERNAME'
password='YOURPASSWORD'

auth = requests.post(baseURL + '/users/'+user+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session':session, 'Content_Type':'application/json'}

with open('YOURJSONFILE.json') as jsonfile:
    for line in jsonfile:
	json_obj = json.loads(line)
        uri_print = json_obj['uri']
	json_string = json.dumps(json_obj)
	pushit = requests.post(baseURL + uri_print, headers=headers, data=json_string).json()
	print pushit
