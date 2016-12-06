Shell scripts to:
 - add profileData attribute to hive_table and hive_column types
 - populate sample profileData to hive_table and hive_column entities

How to use these scripts?
  1. Update env_atlas.sh with details to contact Atlas Server - url, username/password

  2. Add profileData attribute to hive_table and hive_column entity-types
       ./update_types.sh data/update_types.json

  3. Popuate profileData attribute for hive_table whose qualifiedName is default.testtable@cl1
       ./update_entity.sh hive_table  qualifiedName default.testtable@cl1 data/hive_table-profileData.json

  4. Populate profileData attribute for numeric-type hive_column whose qualifiedName is default.testtable.id@cl1
       ./update_entity.sh hive_column qualifiedName default.testtable.id@cl1 data/hive_column-profileData-numeric.json

  5. Populate profileData attribute for string-type hive_column whose qualifiedName is default.testtable.name@cl1
       ./update_entity.sh hive_column qualifiedName default.testtable.name@cl1 data/hive_column-profileData-string.json

  5. Populate profileData attribute for date-type hive_column whose qualifiedName is default.testtable.dateofbirth@cl1
       ./update_entity.sh hive_column qualifiedName default.testtable.dateofbirth@cl1 data/hive_column-profileData-date.json

  6. update_entities.sh is simply a wrapper script that calls update_entity.sh to update a hive table and 3 columns
