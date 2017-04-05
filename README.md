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
