#---------------------------------------------------------------------
# profile_bridge: program which will receive the generated profile data stream/file
#
# All of the defined functions reside in the profiler_builder to facilitate testing
#---------------------------------------------------------------------
from profiler_builder import *
import ConfigParser

config = ConfigParser.ConfigParser()
config.read("profileBridge.ini")
CLUSTER_NAME = config.get('HDPClusterReference', 'ClusterName')

df, outputFile = extractArguments()
tableFQDN = df['database'].iloc[0]+"."+df['table'].iloc[0]+'@'+CLUSTER_NAME
colStats = prepare_profile_variables(CLUSTER_NAME, df)
prepare_table_profile_stats(tableFQDN, colStats, outputFile)
prepareColumnProfileStats(colStats, outputFile)
