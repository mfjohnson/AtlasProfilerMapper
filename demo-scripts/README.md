The files within this folder contain the type definition as well as a basic shell script to validate type type definitions

# Type Setup Instructions:
 
1. (REALLY ???) Set atlas.rest-csrf.enabled=false in Ambari - Custom application.properties  and restart atlas
2. Execute demo-scripts/update_type.sh to update hive_table and hive_column_type . No args required

NOTE: This script has to run on the Atlas server host to leverage the localhost reference, or modify the script to contain the appropriate Atlas Server Hostname.


# Type test loader
* Execute demo-scripts/update_table_values.sh <ambari_cluster_name> <db_name> <table_name> <column_name>
 
eg: for column
./update_table_values.sh secgov_cl1 cost_savings claim_savings eligibilitycode
 
for table
./update_table_values.sh secgov_cl1 cost_savings claim_savings