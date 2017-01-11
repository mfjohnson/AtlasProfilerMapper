# Overview

# Bridge Requirements
 * Python 2.7
 * HDP 2.5.0 or 2.5.3
 * pandas 0.18
 * numpy 1.11.1
 * Mosaic Profile Generator
 
# Testing the deployment and running the Bridge

## Setting up Atlas Types
Within the 'hwx-atlas-profileData' directory, run the update types script as shown below. 

`
./update_types.sh
`

This will add the necessary data profile types to Atlas.  Once this step is complete any tables processed by the Mosaic data generator and the mosaic bridge will be visible within the Atlas Profiler tab.

## Configure Mosaic to Atlas Data Profiler Bridge
You will need to specify the folowing properties in the file `profileBridge.ini` in order for the profiler_bridge to write to the correct Atlas server instance.

| Property | description |
|----------|-------------|
| ATLAS_DOMAIN | Contains the server reference to the Atlas Server.  The exact domain can be retrieved from Amabri Atlas configs. |
| ATLAS_PORT | Contains the Atlas server port.  Normally this is 21000. |

Below we can see an example of the profileBridge.ini file.
`
[AtlasServerReference]

ATLAS_SERVER: server1.hdp

ATLAS_PORT: 21000
`

## Generating Profile stats and post those stats to Atlas Data Profiler


`./bin/mosaic-profile-hive.sh {databasename} {tablename} | python profiler_bridge.py`

# Viewing the generated stats
 
 From your browser connect via the ATLAS Server web page and then search for the table from which you generated and bridged the statistics.  Then select the profile tab option.
 