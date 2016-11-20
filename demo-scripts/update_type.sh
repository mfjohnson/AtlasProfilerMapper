#!/bin/sh

echo "updating table type...";
curl -u admin:admin -X PUT -H "Content-Type: application/json" --data @update_hive_table_type.json http://localhost:21000/api/atlas/types

echo "updating column type...";
curl -u admin:admin -X PUT -H "Content-Type: application/json" --data @update_hive_column_type.json http://localhost:21000/api/atlas/types
