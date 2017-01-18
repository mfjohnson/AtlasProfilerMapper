import requests
import json
import ConfigParser

config = ConfigParser.ConfigParser()
config.read("profileBridge.ini")

ATLAS_DOMAIN=config.get('AtlasServerReference','ATLAS_SERVER')
ATLAS_PORT=config.get('AtlasServerReference','ATLAS_PORT')
#ATLAS_DOMAIN="server1.hdp"
#ATLAS_PORT="21000"

def atlasGET( restAPI ) :
## TODO Verify received code = 200 or else produce an error
    url = "http://"+ATLAS_DOMAIN+":"+ATLAS_PORT+restAPI
    r= requests.get(url, auth=("admin", "admin"))
    return(json.loads(r.text));


def atlasPOST( restAPI, data) :
    url = "http://" + ATLAS_DOMAIN + ":" + ATLAS_PORT + restAPI
    r = requests.post(url, auth=("admin", "admin"),json=data)
    if (r.status_code != 200):
        print("Error:{0}\n{1}".format(r.text,url))
    return (json.loads(r.text));


def atlasPUT( restAPI, data) :
    url = "http://" + ATLAS_DOMAIN + ":" + ATLAS_PORT + restAPI
    r = requests.put(url, auth=("admin", "admin"),json=data)
    if (r.status_code != 200):
        print("Error:{0}\n{1}".format(r.text,url))
    return (json.loads(r.text));

