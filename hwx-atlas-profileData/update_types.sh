#!/bin/bash

#
# Update types from the given jsonFileName
#

realScriptDir=$(cd "$(dirname "$0")"; pwd)

source ${realScriptDir}/env_atlas.sh
source ./env_atlas.sh

jsonFileName=$1

function checkUsage() {
  if [ -z "${jsonFileName}" ]
  then
	jsonFileName=data/update_types.json
  fi

  if [ ! -f "${jsonFileName}" ]
  then
    echo "${jsonFileName}: does not exist"
    exit 1
  fi
}
checkUsage

echo "updating types...";
${CURL_CMDLINE} -X PUT -u ${ATLAS_USER}:${ATLAS_PASS} -H "Accept: application/json" -H "Content-Type: application/json" ${ATLAS_URL}/api/atlas/types -d @${jsonFileName}
