# Overview

# Setting up Atlas Types

There are two types which get updated to support the Atlas Data Profiler possible:

| Atlas Modified type | Description | Update Defining file |
|---------------------|-----------------------------------------|--------------------------|
| hive_table          | Adds table total table rows.  Note: this value comes from the first field in the tables specified numrow | |
| hive_column         | Adds the column statistics for display on the UI field detail views |  |

# Mapping Profiler Generator profileKind to AtlasType stats

## Numeric Specific Stat types
For non-numeric values a null will be entered into these fields

| Stat Description | profileKind | Atlas Stat type Name |
|------------------|-------------|----------------------|
| The maximum value found for the data value | max | stats:maxValue |
| The minimum value found for the data value | min | stats:minValue |
| The mean of all data values for column | mean | stats:meanValue |
| The total of all values | sum | stats:sumValue |
| A set containing decile frequency | decilefreq | stats:decileFreq

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
| The column cardinality count | distinct | stats:distinctCount |
| The total number of empty fields (null or blank string) | empties  | stats:empties |
| The total number of null values | nulls    | stats:nulls|
| While this value is also used to populate the table rowcount, the UI views also are supposed to show the numrows, so this value is also included at the column level | numrows  | stats:numRows|





 