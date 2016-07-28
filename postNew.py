import json
import requests

baseURL = 'http://YOURBACKEDNURL:8089'
user='YOURUSERNAME'
password='YOURPASSWORD'

auth = requests.post(baseURL + '/users/'+user+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session':session, 'Content_Type':'application/json'}

with open('YOURJSONFILE.json') as jsonfile:
    for line in jsonfile:
        json_obj = json.loads(line)
        json_string = json.dumps(json_obj)
        subjects = requests.post(baseURL+'/subjects', headers=headers, data=json_string).json()
        print subjects
