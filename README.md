# python_scripts
For interacting with the ArchivesSpace API.

# Authenticating with secrets.py
These scripts call a separate secrets.py that should be in the following format:

```secrets.py
backendurl='YOURBACKENDURL'
user='YOURUSER'
password='YOURPASSWORD'
```

## asCSV-aos.py
Generate a CSV of all AOs from a particular resource using agentarchives.

## asCSV-titles.py
Generate a CSV of the titles of all AOs from a particular resource using agentarchives.

## asLinkProfiles.py
Link a single container profile to all top_containers in a particular resource.

## get.py
Simple script to get from an endpoint (currently accessions).

## post.py
Post contents of a jsonfile.

## postNew.py
Post contents of a jsonfile.

## suppressSelectEnumerations.py
Suppress enumeration values as identified in an external json file.

## urlLinker.py
Updates/adds a web-accessible url to the first file version of a digital object already in ArchivesSpace.  Assumes the user has a 2-column csv like this:

| file                            | url                                      |
| ------------------------------- |:----------------------------------------:|
| existing digital_object title 1 | URL to add/replace in first file version |
| existing digital_object title 2 | URL to add/replace in first file version |
| existing digital_object title 3 | URL to add/replace in first file version |
