#!/bin/sh
#set -vx

if [ "$#" -lt 3 ] ; then
  echo "Usage: $0 <ClusterName> <DBName> <TableName> [ColumnName]" >&2
  exit 1
fi

clusterName=$1;
dbName=$2;
tableName=$3;

if [ -z "$4" ]; then
  tableQFName=$dbName"."$tableName"@"$clusterName;
  echo "Updating table with qualifiedName :  "$tableQFName;
  curl -u admin:admin -H "Content-Type: application/json" -X POST --data @table_entity_update.json  "http://localhost:21000/api/atlas/entities/qualifiedName?type=hive_table&property=qualifiedName&value=$tableQFName"
else 
  columnName=$4;	
  colQFName=$dbName"."$tableName"."$columnName"@"$clusterName;
  echo "Updating column with qualifiedName :  "$colQFName;
  curl -u admin:admin -H "Content-Type: application/json" -X POST --data @col_entity_update.json  "http://localhost:21000/api/atlas/entities/qualifiedName?type=hive_column&property=qualifiedName&value=$colQFName"
fi
