# Overview

# Setting up Atlas Types

# Mapping Profiler Generator profileKind to AtlasType stats

## Numeric Specific Stat types
For non-numeric values a null will be entered into these fields

| Stat Description | profileKind | Atlas Stat type Name |
|------------------|-------------|----------------------|
| The maximum value found for the data value | max | stats:maxValue |
| The minimum value found for the data value | min | stats:minValue |
| The mean of all data values for column | mean | stats:meanValue |
| The total of all values | sum | stats:sumValue |
| A set containing decile frequency TODO-Need to fix the atlas type to properly include this information | decilefreq | stats:decileFreq

## String Specific stat types
for non-string values a null will be entered into these fields

| Stat Description | profileKind | Atlas Stat type Name |
|------------------|-------------|----------------------|
| The maximum string length found for the data value | max_length | stats:maxLength |
| The minimum string length found for the data value | min_minlength | stats:minLength |
| The average string length of all data values for column | avg_length | stats:avgLength|
| A map which has a count of each key value TODO-Need to fix the atlas type to properly include this information| countfreq| stats:countFrequency |

## String Specific stat types

TODO - Need to finish the mappings

## Common Stat types

These stats will be populated for all datatypes

| Stat Description | profileKind | Atlas Stat type Name |
|------------------|-------------|----------------------|
|  | distinct | stats:distinctCount |
|  | empties  | stats:empties |
|  | nulls    | stats:nulls|
|  | numrows  | stats:numRows|





      "stats:maxValue": "85",
      "stats:minValue": "1",
      "stats:avgLength": "10",
      "stats:maxLength": "20",
      "stats:distinctCount": "20"