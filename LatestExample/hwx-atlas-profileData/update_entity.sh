#!/bin/bash

#
# Update an entity given its: type, uniqueAttributeName, uniqueAttributeValue, jsonFileName
#

realScriptDir=$(cd "$(dirname "$0")"; pwd)

source ${realScriptDir}/env_atlas.sh
source ./env_atlas.sh


entityType=$1
unqiueAttributeName=$2
unqiueAttributeValue=$3
jsonFileName=$4

function checkUsage() {
  if [ -z "${entityType}" -o -z "${unqiueAttributeName}" -o -z "${unqiueAttributeValue}" -o -z "${jsonFileName}" ]
  then
    echo "Usage: $0 <entityType> <uniqueAttributeName> <uniqueAttributeValue> <jsonFileName>"
    exit 1
  fi

  if [ ! -f "${jsonFileName}" ]
  then
    echo "${jsonFileName}: does not exist"
    exit 1
  fi
}
checkUsage


echo "Updating ${entityType} entity with ${unqiueAttributeName}=${unqiueAttributeValue}"

output=`${CURL_CMDLINE} -X POST -u ${ATLAS_USER}:${ATLAS_PASS} -H "Accept: application/json" -H "Content-Type: application/json" "${ATLAS_URL}/api/atlas/entities/${unqiueAttributeName}?type=${entityType}&property=${unqiueAttributeName}&value=${unqiueAttributeValue}" -d @${jsonFileName}`
ret=$?


if [ $ret == 0 ]
then
  echo ${output}
else
  echo "failed with error code: ${ret}"
fi
