#!/bin/sh
ATLAS_SERVER="server1.hdp:21000"

echo "Create histogram_type...";
curl -u admin:admin -X PUT -H "Content-Type: application/json" --data @histogram_countsType.json http://$ATLAS_SERVER/api/atlas/types

echo "Create decile_freqency type...";
curl -u admin:admin -X PUT -H "Content-Type: application/json" --data @decileFreqType.json http://$ATLAS_SERVER/api/atlas/types

echo "updating table type...";
curl -u admin:admin -X PUT -H "Content-Type: application/json" --data @update_hive_table_type.json http://$ATLAS_SERVER/api/atlas/types

echo "updating column type...";
curl -u admin:admin -X PUT -H "Content-Type: application/json" --data @update_hive_column_type.json http://$ATLAS_SERVER/api/atlas/types
