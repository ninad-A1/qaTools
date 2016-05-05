import json
import requests
from requests.auth import HTTPBasicAuth

with open("data.json") as data_file:
    data = json.load(data_file)
    host = data["host_docker"]
    port_auth = data["port_auth"]
    port_campaign = data["port_campaign"]
    tenantid = data["tenantid"]
    user = data["user"]
    passwd = data["passwd"]
    rootFolders = data["rootFolders"]
    datasetDefs = data["datasetDefs"]
    filesDatasetDefs = data["filesDatasetDefs"]
    campaignDefs = data["campaignDefs"]
    fileCampaignDefs = data["fileCampaignDefs"]

def login(user, passwd):
    url= "%s://%s:%s/%s" % ("http", host, port_auth, "authentication?action=login")
    headers = {"Content-Type": "application/json"}
    auth = HTTPBasicAuth(user, passwd)
    r = requests.post(url, headers=headers, auth=auth)
    return r.json()['token_type'] + " " + r.json()['access_token']

def getFiles(token):
    url = "%s://%s:%s/v2/%s%s" % ( "http", host, port_campaign, tenantid, "/files")
    headers = {"Authorization": token}
    r = requests.get(url, headers=headers)
    return json.loads(r.text)['_embedded']['files']

def postFiles(data, token):
    url = "%s://%s:%s/v2/%s%s" % ( "http", host, port_campaign, tenantid, "/files")
    headers = {"Authorization": token, "Content-Type": "application/json"}
    r = requests.post(url, headers=headers, json=data)
    return json.loads(r.text)['_embedded']['files']

def getDatasetDefs(token):
    url = "%s://%s:%s/v2/%s%s" % ( "http", host, port_campaign, tenantid, "/datasetDefs")
    headers = {"Authorization": token}
    r = requests.get(url, headers=headers)
    return json.loads(r.text)['_embedded']['datasetDefs']

def postDatasetDefs(data, token):
    url = "%s://%s:%s/v2/%s%s" % ( "http", host, port_campaign, tenantid, "/datasetDefs")
    headers = {"Authorization": token, "Content-Type": "application/json"}
    r = requests.post(url, headers=headers, json=data)
    return json.loads(r.text)['_embedded']['datasetDefs']

def getCampaignDefs(token):
    url = "%s://%s:%s/v2/%s%s" % ( "http", host, port_campaign, tenantid, "/campaignDefs")
    headers = {"Authorization": token}
    r = requests.get(url, headers=headers)
    return json.loads(r.text)['_embedded']['campaignDefs']

def postCampaignDefs(data, token):
    url = "%s://%s:%s/v2/%s%s" % ( "http", host, port_campaign, tenantid, "/campaignDefs")
    headers = {"Authorization": token, "Content-Type": "application/json"}
    r = requests.post(url, headers=headers, json=data)
    return json.loads(r.text)['_embedded']['campaignDefs']

token = login(user,passwd)
print "Login: %s" % (token)
#folders = getFiles(token)
folders = postFiles(rootFolders,token)

for folder in folders:
    if folder['name'] == 'CampaignDef':
        folderCampaignDef = folder['resourceId']
    elif folder['name'] == 'Playbooks':
        folderPlaybooks = folder['resourceId']
    elif folder['name'] == 'AudienceDefTemplates':
        folderAudienceDefTemplates = folder['resourceId']
    elif folder['name'] == 'ContentModels':
        folderContentModels = folder['resourceId']

print "folderCampaignDef: %s" % folderCampaignDef
print "folderPlaybooks: %s" % folderPlaybooks
print "folderDataSetDefs: %s" % folderAudienceDefTemplates
print "folderContentModels: %s" % folderContentModels

#datasets = getDatasetDefs(token)
datasets = postDatasetDefs(datasetDefs, token)

for dataset in datasets:
    if dataset['name'] == 'Customers who purchased a product in a category':
        dataSetPurCategory = dataset['resourceId']
    elif dataset['name'] == 'Customers who abandoned their cart':
        dataSetAbdnCart = dataset['resourceId']
    elif dataset['name'] == 'First Order Anniversary':
        dataSetOrdAnniversary = dataset['resourceId']

print "dataSetPurCategory: %s" % dataSetPurCategory
print "dataSetAbdnCart: %s" % dataSetAbdnCart
print "dataSetOrdAnniversary: %s" % dataSetOrdAnniversary

filesDatasetDefs[[i for i in range(len(filesDatasetDefs)) if filesDatasetDefs[i]['name'] == "Customers who purchased a product in a category"][0]]['parentResourceId'] = folderAudienceDefTemplates
filesDatasetDefs[[i for i in range(len(filesDatasetDefs)) if filesDatasetDefs[i]['name'] == "Customers who purchased a product in a category"][0]]['referenceEntityId'] = dataSetPurCategory

filesDatasetDefs[[i for i in range(len(filesDatasetDefs)) if filesDatasetDefs[i]['name'] == "Customers who abandoned their cart"][0]]['parentResourceId'] = folderAudienceDefTemplates
filesDatasetDefs[[i for i in range(len(filesDatasetDefs)) if filesDatasetDefs[i]['name'] == "Customers who abandoned their cart"][0]]['referenceEntityId'] = dataSetAbdnCart

filesDatasetDefs[[i for i in range(len(filesDatasetDefs)) if filesDatasetDefs[i]['name'] == "First Order Anniversary"][0]]['parentResourceId'] = folderAudienceDefTemplates
filesDatasetDefs[[i for i in range(len(filesDatasetDefs)) if filesDatasetDefs[i]['name'] == "First Order Anniversary"][0]]['referenceEntityId'] = dataSetOrdAnniversary

filesDatasets = postFiles(filesDatasetDefs,token)

#campaigns = getCampaignDefs(token)
campaigns = postCampaignDefs(campaignDefs, token)

for campaign in campaigns:
    if campaign['name'] == 'Abandoned Cart':
        campaignAbdnCart = campaign['resourceId']
    elif campaign['name'] == 'Purchased in Category':
        campaignPurCategory = campaign['resourceId']

print "campaignAbdnCart: %s" % campaignAbdnCart
print "campaignPurCategory: %s" % campaignPurCategory

fileCampaignDefs[[i for i in range(len(fileCampaignDefs)) if fileCampaignDefs[i]['name'] == "Abandoned Cart"][0]]['parentResourceId'] = folderPlaybooks
fileCampaignDefs[[i for i in range(len(fileCampaignDefs)) if fileCampaignDefs[i]['name'] == "Abandoned Cart"][0]]['referenceEntityId'] = campaignAbdnCart

fileCampaignDefs[[i for i in range(len(fileCampaignDefs)) if fileCampaignDefs[i]['name'] == "Customers who Purchased in a Category"][0]]['parentResourceId'] = folderPlaybooks
fileCampaignDefs[[i for i in range(len(fileCampaignDefs)) if fileCampaignDefs[i]['name'] == "Customers who Purchased in a Category"][0]]['referenceEntityId'] = campaignPurCategory

filesCampaigns = postFiles(fileCampaignDefs,token)

print json.dumps(getFiles(token), indent=2)


