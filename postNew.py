import secrets
import json
import requests

baseURL = 'http://'+secrets.backendurl+':8089'
user=secrets.user
password=secrets.password

auth = requests.post(baseURL + '/users/'+user+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session':session, 'Content_Type':'application/json'}

with open('YOURJSONFILE.json') as jsonfile:
    for line in jsonfile:
        json_obj = json.loads(line)
        json_string = json.dumps(json_obj)
        subjects = requests.post(baseURL+'/subjects', headers=headers, data=json_string).json()
        print subjects
