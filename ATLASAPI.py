import requests
import json
import ConfigParser

config = ConfigParser.ConfigParser()
config.read("profileBridge.ini")

ATLAS_DOMAIN=config['AtlasServerReference']['ATLAS_DOMAIN']
ATLAS_PORT=config['AtlasServerReference']['ATLAS_DOMAIN']

def atlasGET( restAPI ) :
## TODO Verify received code = 200 or else produce an error
    url = "http://"+ATLAS_DOMAIN+":"+ATLAS_PORT+restAPI
    r= requests.get(url, auth=("admin", "admin"))
    return(json.loads(r.text));


def atlasPOST( restAPI, data) :
    # TODO update to support Atlas kerberos based authentication
    url = "http://" + ATLAS_DOMAIN + ":" + ATLAS_PORT + restAPI
    r = requests.post(url, auth=("admin", "admin"),json=data)
    return (json.loads(r.text));


def atlasPUT( restAPI, data) :
    # TODO update to support Atlas kerberos based authentication
    url = "http://" + ATLAS_DOMAIN + ":" + ATLAS_PORT + restAPI
    r = requests.put(url, auth=("admin", "admin"),json=data)
    return (json.loads(r.text));

