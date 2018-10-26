import requests, json, secrets, time, logging, csv, urllib
logging.basicConfig(filename= time.strftime('%Y-%m-%d_%H%M%S') + '_urlLinker.log',format='%(levelname)s:%(message)s',level=logging.INFO)
startTime = time.time()

# import secrets
baseURL = secrets.baseURL
user = secrets.user
password = secrets.password

# authenticate to ArchivesSpace
auth = requests.post(baseURL + '/users/' + user + '/login?password=' + password).json()
session = auth["session"]
headers = {'X-ArchivesSpace-Session':session}

# User supplied variables
url_csv = raw_input('Enter csv filename: ')

# Open csv
csv_dict = csv.DictReader(open(url_csv))

for row in csv_dict:
    do_title = urllib.quote(row['file'])
    file_uri = row['url']

    # Search for digital object by digital object title in 'file' column of csv
    query = '/search?page=1&filter={"query":{"jsonmodel_type":"boolean_query","op":"AND","subqueries":[{"jsonmodel_type":"field_query","field":"primary_type","value":"digital_object","literal":true},{"jsonmodel_type":"field_query","field":"title","value":"' + do_title + '","literal":true},{"jsonmodel_type":"field_query","field":"types","value":"pui","literal":true}]}}'
    digital_object = requests.get(baseURL + query, headers=headers).json()

    try:
        if digital_object['results'] != []:
            do_uri = digital_object['results'][0]['uri']
            # Get the single digital object out
            get_do = requests.get(baseURL + do_uri, headers=headers)
            status_code = get_do.status_code
            if status_code == 200:
                doRecord = get_do.json()
                file_versions = doRecord['file_versions']
                # Replace the file uri with the value of 'uri' in the csv
                file_versions[0]['file_uri'] = file_uri
                # Post back the updated record
                post = requests.post(baseURL + do_uri, headers=headers, data=json.dumps(doRecord))
                status_code = post.status_code
                if status_code == 200:
                    print post.json()
                    logging.info(post.json())
                else:
                    print post.json()
                    logging.error("Error with: " + post.json())
            else:
                print "Error with: " + get_do.json()
                logging.error("Error with: " + get_do.json())
    except:
        logging.error("Skipping " + row['url'])
        continue

# show script runtime
elapsedTime = time.time() - startTime
m, s = divmod(elapsedTime, 60)
h, m = divmod(m, 60)
print 'Total script run time: ', '%d:%02d:%02d' % (h, m, s)
