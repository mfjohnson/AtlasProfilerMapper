#---------------------------------------------------------------------
# profile_bridge: program which will receive the generated profile data stream/file
#
# All of the defined functions reside in the profiler_builder to facilitate testing
#---------------------------------------------------------------------
from profiler_builder import *
import ConfigParser
import logging


logging.basicConfig(filename="AtlasDataProfilerBridge.log", level=logging.DEBUG)

logging.info("Beginning ATLAS Data Profiler Bridge")
config = ConfigParser.ConfigParser()
config.read("profileBridge.ini")
CLUSTER_NAME = config.get('HDPClusterReference', 'ClusterName')
logging.info("Processing Table for CLUSTERNAME={0}".format(CLUSTER_NAME))

df, outputFile = extractArguments()
tableFQDN = df['database'].iloc[0]+"."+df['table'].iloc[0]+'@'+CLUSTER_NAME
logging.info("Parsed Input file:{0}".format(tableFQDN))
colStats = prepare_profile_variables(CLUSTER_NAME, df)
logging.info("Processed Profile Variables")
prepare_table_profile_stats(tableFQDN, colStats, outputFile)
logging.info("Processed and wrote Table Stats to Atlas")
prepareColumnProfileStats(colStats, outputFile)
logging.info("Processed and wrote Column Stats to Atlas")
