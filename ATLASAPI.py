import requests
import json
import sys


ATLAS_DOMAIN="server1"
ATLAS_PORT="21000"

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


