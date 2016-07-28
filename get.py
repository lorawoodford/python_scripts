import json
import requests

baseURL = 'http://YOURBACKEND:8089'
user='USERNAME'
password='PASSWORD'

auth = requests.post(baseURL + '/users/'+user+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session':session, 'Content_Type':'application/json'}

endpoint = '/repositories/3/accessions'
arguments = '?page=1&page_size=3000'

output = requests.get(baseURL + endpoint + arguments, headers=headers).json()
print(json.dumps(output.get('results'), indent=2))
