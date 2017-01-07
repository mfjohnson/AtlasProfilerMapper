import json
import pandas as pd
import numpy as np
from ATLASAPI import *
import sys, getopt
import operator

# TODO Document the methods
#------ SPECIFY DEFAULT PROPERTIES
clustername = "HDP"


#------ UTILITY METHODS
def extractArguments():
    # ------- Get Command line properties
    global isOutputRESTCommand
    inputfile = sys.stdin
    outputfile = None

    try:
        cmd_opts, args = getopt.getopt(sys.argv[1:], "i:o:")
    except getopt.GetoptError:
        print 'test.py -i <inputfile> -o <outputfile>'
        sys.exit(2)

    ###############################
    # o == option
    # a == argument passed to the o
    ###############################
    for o, a in cmd_opts:
        if o == '-i':
            inputfile = open(a)
        elif o == '-o':
            outputfile = a
        else:
            print("Usage: %s -i input -o output" % sys.argv[0])

    json_data = inputfile.read()
    df = pd.read_json(json_data)
    return(df,outputfile)

def prepareProfileVariables(df):
    # ------- Calculate new columns of data and pivot table
    df['qualifiedName'] = df['database'] + "." + df['table'].str.lower() + "." + df['field'].str.lower() + "@" + clustername
    a = df[['qualifiedName','dataType','profileKind','value']]
#    colStats = a.pivot(index='qualifiedName', columns='profileKind', values='value')
    colStats = pd.pivot_table(a, values='value', index=['qualifiedName','dataType'], columns=['profileKind'],aggfunc=np.sum)
    return colStats;


#  TODO: Cleanup the tableId and the numRows calculator
def prepareTableProfileStats(stats,outputfile):
    """
    :param stats:
    :param outputfile:
    :return:


    """
    global tableFQDN, table_properties
    tableId = "-1234"
    print(stats)
    numRows = 5000
    tableFQDN = "default.customer_info1@HDP"
    tableResult = None
    table_properties = {
        "jsonClass": "org.apache.atlas.typesystem.json.InstanceSerialization$_Reference",
        "id": {
            "jsonClass": "org.apache.atlas.typesystem.json.InstanceSerialization$_Id",
            "id": "-1234",
            "typeName": "hive_table"
        },
        "typeName": "hive_table",
        "values": {
            "profileData": {
                "jsonClass": "org.apache.atlas.typesystem.json.InstanceSerialization$_Struct",
                "typeName": "hive_table_profile_data",
                "values": {
                    "rowCount": numRows
                }
            }
        },
        "traits": {
        }
    }
    if not outputfile:
        tableResult = atlasPOST(
            "/api/atlas/entities/qualifiedName?type=hive_table&property=qualifiedName&value=%s" % (tableFQDN),
            table_properties)

    return(tableResult);

def buildValueFreqData(s):
    decileList = []
    if s:
        decileJSON = json.loads(s)

        for d in decileJSON:
            value = {
                d['key']:d['value']
            }
            decileList.append(value)
    resultStr = convertJSONSet(decileList)
    return resultStr;


def convertJSONSet(jsonObject):
    strJSONList = json.dumps(jsonObject)
    strJSONList = strJSONList.replace("{", "")
    strJSONList = strJSONList.replace("}", "")
    strJSONList = strJSONList.replace("[", "{")
    strJSONList = strJSONList.replace("]", "}")
    return(strJSONList)


# TODO Finish implementing the Annual frequency
def buildAnnualFrequencyData(annual, monthly):
    print("Builder")
    distrAnnualList = []
    if monthly:
        monthlyList = pd.DataFrame(json.loads(monthly))
        if annual:
            annualFreqJSON = json.loads(annual)

            for y in annualFreqJSON:
                dataYear = y['year']
                data = {
                    "{0}:count".format(dataYear):y['count']
                }
                distrAnnualList.append(data)
                currentYearMonths = monthlyList[monthlyList.year==dataYear]
                for index, m in currentYearMonths.iterrows():
                    monthValue = {"{0}:{1}".format(dataYear,m['month']):m['count']}
                    distrAnnualList.append(monthValue);

    resultStr = convertJSONSet(distrAnnualList)
    return(resultStr);

def getFreqListKey(item):
    return item[0]

def sortFrequencyKeys(freq):
#    sorted_x = freq.sort(key=lambda x: x.get(1), reverse=True)
#    sorted_x = sorted(freq, key=operator.itemgetter(0))
    return(freq)

def mapDistributionObjects(colDef, dataType):
    keyOrder = None

    if (dataType=='string'):
        distType="count-frequency"
        distData= buildValueFreqData(colDef['countfreq'])
        keyOrder = sortFrequencyKeys(distData);
    elif (dataType=='date'):
        distType = "annual"
        distData = buildAnnualFrequencyData(colDef['annual'], colDef['monthly']);
    else:  # Assuming if not string nor date it must be numeric
        distType = "decile-frequency"
        distData = buildValueFreqData(colDef['decilefreq'])

    return(distType, distData,keyOrder);

def convertNumDictValue(colValue, type):
    result = None
    if (type=='Num'):
        result = colValue if colValue else 0
    return(result)

def prepareColumnProfileStats(colStats, outputfile):
    """
     Output Column Stats to Atlas REST
    :param colStats:
    :param outputfile:
    :return:
    """
    columnProfile = []
    for index, colDef in colStats.iterrows():
        colId = "-1234"
        colFQDN = index[0]

        (distributionType, distributionData,distributionKeyOrder) = mapDistributionObjects(colDef, index[1])

        column_properties = {
            "jsonClass": "org.apache.atlas.typesystem.json.InstanceSerialization$_Reference",
            "id": {
                "jsonClass": "org.apache.atlas.typesystem.json.InstanceSerialization$_Id",
                "id": colId,
                "typeName": "hive_column",
            },
            "typeName": "hive_column",
            "values": {
                "profileData": {
                    "jsonClass": "org.apache.atlas.typesystem.json.InstanceSerialization$_Struct",
                    "typeName": "hive_column_profile_data",
                    "values": {
                        "maxValue": convertNumDictValue(colDef['max'],"Num"),
                        "minValue": convertNumDictValue(colDef['min'],"Num"),
                        "meanValue": convertNumDictValue(colDef['mean'],"Num"),
#                       "sumValue": convertNumDictValue(colDef['sum'],"Num"),
                        "averageLength": convertNumDictValue(colDef['avg_length'],"Num"),
                        "maxLength": convertNumDictValue(colDef['max_length'],"Num"),
                        "cardinality": convertNumDictValue(colDef['distincts'],"Num"),
 #                      "empties": convertNumDictValue(colDef['empties'],"Num"),
                        "nonNullData": convertNumDictValue((colDef['numrows'] - colDef['nulls']),"Num"),
                        "distributionType": distributionType,
                        "distributionData": distributionData
                    }
                }
            },
            "traits": {
            }
        }
        print json.dumps(column_properties, indent=4, sort_keys=True)
        result = atlasPOST(
            "/api/atlas/entities/qualifiedName?type=hive_column&property=qualifiedName&value=%s" % (colFQDN),
            column_properties)
        print json.dumps(result, indent=2, sort_keys=True)
        columnProfile.append(column_properties)
        if outputfile:
            with open("{0}Column.json".format(colFQDN), 'w') as fp:
                json.dump(columnProfile, fp)
    return;


