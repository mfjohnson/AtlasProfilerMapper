#---------------------------------------------------------------------
# profile_bridge: program which will receive the generated profile data stream/file
#
# All of the defined functions reside in the profiler_builder to facilitate testing
#---------------------------------------------------------------------
from profiler_builder import *

df,outputfile = extractArguments()
colStats = prepareProfileVariables(df)
prepareTableProfileStats(colStats, outputfile)
prepareColumnProfileStats(colStats, outputfile)