import json

file_directory = "sample.json"
json_data=open(file_directory).read()

data = json.loads(json_data)
print json.dumps(data, indent=4, sort_keys=True)