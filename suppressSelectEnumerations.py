import json
import requests
import secrets

# import from secrets.py file
baseURL = secrets.baseURL
user = secrets.user
password = secrets.password

# authenticate using info from secrets.py
auth = requests.post(baseURL + '/users/'+user+'/login?password='+password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session':session, 'Content_Type':'application/json'}

# get enumeration_value_ids from external json file containing only those enumerations you wish to suppress
enumerations = json.load(open('suppressEnumerations.json'))
for i in range (0, len (enumerations)):
    enumeration = json.dumps(enumerations[i])
    enumeration_value_id = enumerations[i]['id']
    getEnumeration = requests.get("{}/config/enumeration_values/{}".format(baseURL, enumeration_value_id), headers=headers).json()

# post to suppression endpoint for each of the enumeration_value_ids collected in the get above
    postEnumeration = requests.post("{}/config/enumeration_values/{}/suppressed".format(baseURL, enumeration_value_id), params="suppressed=true", data=json.dumps(getEnumeration), headers=headers)
    print postEnumeration
