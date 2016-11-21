from ATLASAPI import *
import json


#------------ Define utility functions
def loadJSONfile(f):
    with open(f) as json_data:
        d = json.load(json_data)
        print(d)
    return d;

#------------- Load the Atlas Profiler Modified types and Sub-Types
histogramTypeJSON = loadJSONfile("histogram_countsType.json")
decileFreqJSON = loadJSONfile("decileFreqType.json")
hive_tableJSON = loadJSONfile("update_hive_table_type.json")
hive_columnJSON = loadJSONfile("update_hive_column_type.json")

#------------- Add the Sub-types
print("**********************************")
histResult = atlasPUT("/api/atlas/types", histogramTypeJSON)
print json.dumps(histResult, indent=4, sort_keys=True)

decileResult = atlasPUT("/api/atlas/types", decileFreqJSON)
print json.dumps(decileResult, indent=4, sort_keys=True)

#------------- Update the standard Hive Types
print("************* UPDATE HIVE COL")
hiveColResult = atlasPUT("/api/atlas/types", hive_columnJSON)
print json.dumps(hiveColResult, indent=4, sort_keys=True)

print("************* UPDATE HIVE TABLE")
hiveTableResult = atlasPUT("/api/atlas/types", hive_tableJSON)
print json.dumps(hiveTableResult, indent=4, sort_keys=True)


