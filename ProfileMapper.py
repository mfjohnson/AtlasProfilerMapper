import json
import pandas as pd
import numpy as np
from ATLASAPI import *


#------ SPECIFY DEFAULT PROPERTIES
clustername = "HDP"
file_directory = "customer_info_gen.json"

#------- Define utility Methods
#def defineDecilFeq(freq) :

#------- LOAD AND PREPARE THE JSON FILE
#--- TODO need to enable stdin access
json_data=open(file_directory).read()
df = pd.read_json(json_data)

#------- Calculate new columns of data and pivot table
df['qualifiedName'] = df['database']+"."+df['table']+"."+df['field']+"@"+clustername

# colStats = pd.pivot_table(df, index=["qualifiedName"],columns=["profileKind"],values=["value"], aggfunc=[np.sum])
colStats = df.pivot(index='qualifiedName', columns='profileKind', values='value')
#------- Output table  to Atlas REST
tableId = "-1234"
print(colStats)

numRows = str(0)
tableFQDN = "profile.profilesample@HDP"
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

tableResult = atlasPOST("/api/atlas/entities/qualifiedName?type=hive_table&property=qualifiedName&value=%s" % (tableFQDN), table_properties)

#-------- Output Column Stats to Atlas REST
columnProfile = []
for index,colDef in colStats.iterrows():
    colId = "-1234"
    colFQDN = index
#    decileFreq = json.loads(colDef['decilefreq'])
#    countFreq = json.loads(colDef['countfreq'])
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
          "stats:maxValue"  : colDef['max'],
          "stats:minValue"  : colDef['min'],
          "stats:meanValue" : colDef['mean'],
          "stats:sumValue"  : colDef['sum'],
          "stats:avgLength": colDef['avg_length'],
          "stats:maxLength": colDef['max_length'],
          "stats:minLength": colDef['min_length'],
          "stats:distinctCount": colDef['distincts'],
          "stats:empties": colDef['empties'],
          "stats:nulls": colDef['nulls'],
          "stats:numRows":colDef['numrows']
        },
        "traitNames": [
        ],
        "traits": {
        }
    }

    columnResult = atlasPOST("/api/atlas/entities/qualifiedName?type=hive_column&property=qualifiedName&value=%s" % (colFQDN), column_properties)
    columnProfile.append(column_properties)
    print("---- Posted %s" % (colFQDN));



with open('result.json', 'w') as fp:
    json.dump(columnProfile, fp)

