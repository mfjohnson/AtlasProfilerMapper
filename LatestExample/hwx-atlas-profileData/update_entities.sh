./update_entity.sh hive_table  qualifiedName default.testtable@cl1             data/hive_table-profileData.json
./update_entity.sh hive_column qualifiedName default.testtable.id@cl1          data/hive_column-profileData-numeric.json
./update_entity.sh hive_column qualifiedName default.testtable.name@cl1        data/hive_column-profileData-string.json
./update_entity.sh hive_column qualifiedName default.testtable.dateofbirth@cl1 data/hive_column-profileData-date.json
