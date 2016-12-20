import json
import pandas as pd
import numpy as np
from ATLASAPI import *
import sys, getopt

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
            outputfile = open(a)
        else:
            print("Usage: %s -i input -o output" % sys.argv[0])

    json_data = inputfile.read()
    df = pd.read_json(json_data)
    return(df,outputfile)

def prepareProfileVariables(df):
    # ------- Calculate new columns of data and pivot table
    df['qualifiedName'] = df['database'] + "." + df['table'] + "." + df['field'] + "@" + clustername
    colStats = df.pivot(index='qualifiedName', columns='profileKind', values='value')
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
    numRows = 0
    tableFQDN = "default.customer_info1@HDP"
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
    else:
        json.dump(table_properties, outputfile)
        tableResult = None

    return(tableResult);

def buildValueFreqData(s):
    decileList = []
    if s:
        decileJSON = json.loads(s)

        for d in decileJSON:
            value = {
                "jsonClass": "org.apache.atlas.typesystem.json.InstanceSerialization$_Struct",
                "typeName": "value_frequency_data",
                "values": {
                    "value":d['key'],
                    "count":d['value']
                }
            }
            decileList.append(value)

    return decileList;

# TODO Finish implementing the Annual frequency
def buildAnnualFrequencyData(annual, monthly):
    distrAnnualList = []
    if monthly:
        monthlyList = pd.DataFrame(json.loads(monthly))
        if annual:
            annualFreqJSON = json.loads(annual)

            for y in annualFreqJSON:
                dataYear = y['year']
                currentYearMonths = monthlyList[monthlyList.year==dataYear]
                monthlyCounts = []
                for index, m in currentYearMonths.iterrows():
                    monthValue = {str(m['month']):m['count']}
                    monthlyCounts.append(monthValue);

                year = {
                    "jsonClass": "org.apache.atlas.typesystem.json.InstanceSerialization$_Struct",
                    "typeName": "annual_frequency_data",
                    "values": {
                        "year": dataYear,
                        "count": y['count'],
                        "monthlyCounts" : monthlyCounts
                    }
                }
                distrAnnualList.append(year)

    return(distrAnnualList);



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
        colFQDN = index
        colDecileFreq = buildValueFreqData(colDef['decilefreq'])
        countFreq = buildValueFreqData(colDef['countfreq'])
        distrAnnual = buildAnnualFrequencyData(colDef['annual'], colDef['monthly'])
        column_properties = {
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
                "maxValue": colDef['max'],
                "minValue": colDef['min'],
                "meanValue": colDef['mean'],
                "sumValue": colDef['sum'],
                "averageLength": colDef['avg_length'],
                "maxLength": colDef['max_length'],
                "minLength": colDef['min_length'],
                "cardinality": colDef['distincts'],
                "empties": colDef['empties'],
                "nonNullData": (colDef['numrows'] - colDef['nulls']),
                "medianValue": None,
                "numRows": colDef['numrows'],
                "distributionDecile": colDecileFreq,
                "distributionCount": countFreq,
                "distributionAnnual": distrAnnual,
                "minDate" : None,
                "maxDate" : None
            },
            "traitNames": [
            ],
            "traits": {
            }
        }
        print json.dumps(column_properties, indent=4, sort_keys=True)
        atlasPOST(
            "/api/atlas/entities/qualifiedName?type=hive_column&property=qualifiedName&value=%s" % (colFQDN),
            column_properties)
        columnProfile.append(column_properties)
    if outputfile:
        with open('result.json', 'w') as fp:
            json.dump(columnProfile, fp)
    return;


