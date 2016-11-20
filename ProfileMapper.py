import json
import pandas as pd
from ATLASAPI import *


#------ SPECIFY DEFAULT PROPERTIES
clustername = "HDP"
file_directory = "sample.json"

#------- LOAD AND PREPARE THE JSON FILE
#--- TODO need to enable stdin access
json_data=open(file_directory).read()
df = pd.read_json(json_data)

#------- Calculate new columns of data and pivot table
df['qualifiedName'] = df['database']+"."+df['table']+"."+df['field']+"@"+clustername
colStats = df.pivot(index='qualifiedName',columns='profileKind',values="value")
print(colStats.head(n=10))

#------- Output table  to Atlas REST
tableId = "-1234"
numRows = str(colStats['numrows'][0])
tableFQDN = "abc"
table_properties = {
    "jsonClass": "org.apache.atlas.typesystem.json.InstanceSerialization$_Reference",
    "id": {
      "jsonClass": "org.apache.atlas.typesystem.json.InstanceSerialization$_Id",
      "id": tableId,
      "version": 0,
      "typeName": "hive_table",
      "state": "ACTIVE"
    },
    "typeName": "hive_table",
    "values": {
      "stats:numRows": numRows
    },
    "traitNames": [
    ],
    "traits": {
    }
}

#tableResult = atlasPOST("/api/atlas/entities/qualifiedName?type=hive_table&property=qualifiedName&value=%s" % (tableFQDN), table_properties)

#-------- Output Column Stats to Atlas REST

for colDef in colStats:
    colId = "-1234"
    column_properties =  {
        "jsonClass": "org.apache.atlas.typesystem.json.InstanceSerialization$_Reference",
        "id": {
          "jsonClass": "org.apache.atlas.typesystem.json.InstanceSerialization$_Id",
          "id": colId,
          "version": 0,
          "typeName": "hive_column",
          "state": "ACTIVE"
        },
        "typeName": "hive_column",
        "values": {
          "stats:maxValue": "85",
          "stats:minValue": "1",
          "stats:avgLength": "10",
          "stats:maxLength": "20",
          "stats:distinctCount": "20",
          "stats:total":"10"
        },
        "traitNames": [
        ],
        "traits": {
        }
    }

#columnResult = atlasPOST("/api/atlas/entities/qualifiedName?type=hive_column&property=qualifiedName&value=%s" % (colFQDN), column_properties)




