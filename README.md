# FlattenJson
Convert an array of flat non-hierarchial json objects to a csv file

This program takes a file containing an array of flat, non­hierarchical JSON objects, convert it into CSV format, and write it to disk.

The script will be able to translate this JSON file into a CSV file using the following rules:
1. Each JSON object gets its own row in the CSV.
2. Each key in the JSON object should have its value written to the corresponding column in
the CSV
3. Keys that are in multiple JSON objects should only have one corresponding column created
in the CSV
4. There is no known schema for the input JSON – the keys for each object can be
anything.
5. Column order is not important.

The JSON objects themselves are composed of simple key-value pairs, where the values are either strings, integers, or booleans. We can assume that there are no nested JSON objects or arrays used as values. The keys themselves can vary between the different JSON objects contained in the array.

A sample JSON input file is as follows:
```
[
	{
  		"id": 1,
  		"first_name": "jane",
  		"last_name": "doe",
  		"description": "foobar"
	},
	{
  		"id": 2,
  		"first_name": "john",
  		"middle_name": "scott",
  		"last_name": "public",
  		"birth_year": 1971,
  		"address": "835 Dorset Street, Roulette, Wisconsin, 2802"
	},
	{
  		"id": 3,
  		"anonymous_user": true,
  		"crm_id": "abc123"
	},
	{
  		"id": 4,
  		"first_name": "Albert",
  		"middle_name": "Einstein",
  		"profession": "Scientist",
  		"birth_year": 1879,
  		"e_equals_mc_cube": false,
  		"anonymous_user": false
	}
]
```

this script should generate the following output:
```
first_name,last_name,id,description,middle_name,address,birth_year,crm_id,anonymous_user,profession,e_equals_mc_cube
jane,doe,1,foobar,,,,,,,
john,public,2,,scott,"u'835 Dorset Street, Roulette, Wisconsin, 2802'",1971,,,,
,,3,,,,,abc123,True,,
Albert,,4,,Einstein,,1879,,False,Scientist,False
```
