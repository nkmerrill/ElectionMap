# process.py
# Written by nkmerrill
# 
# Takes presidential election data from MIT Election data in CSV format and converts it to JSON, 
# including yearly election results ratios and the change in ratio between 2016 and 2020, then
# combines it with geoJSON data from albersUSA, resulting in election data tied to geometry data
# that can be visualized on a map.

import json
import os
from csvtojson import convertToJSON

### File Paths ###
geoSourceFile = os.path.join(r"albersusa", r"composite_us_counties.geojson")
dataSourceFile = os.path.join(r"mit", r"presdata2012-2020DCFIX.csv")
dataintermFile = os.path.join(r"output", r"presdataJSON.json")
outputFile = os.path.join(r"output", r"output.geojson")

# importSource(value)
# Imports JSON at filepath value.
# Returns hash table representation of JSON data.
def importSource(value):
    with open(value) as input:
        return json.load(input)

# combineDataSets(geo, data)
# Combines relevant data from data into geo file to create one data set.
def combineDataSets(geo, data):
    for i in range(len(geo['features'])):
        fips = str(int(geo['features'][i]['properties']['fips']))
        if fips in data:
            d = data[str(int(geo['features'][i]['properties']['fips']))] #For some reason, the geojson file has leading 0s which this conversion easily removes.
            geo['features'][i]['properties']['change'] = d['change']
            geo['features'][i]['properties']['party'] = d['party']
            geo['features'][i]['properties']['flipped'] = d['flipped']

            if '2016' in d:
                geo['features'][i]['properties']['2016dvotes'] = d['2016']['DEMOCRAT']
                geo['features'][i]['properties']['2016rvotes'] = d['2016']['REPUBLICAN']
                geo['features'][i]['properties']['2016ovotes'] = d['2016']['OTHER']
            else:
                geo['features'][i]['properties']['2016dvotes'] = 0
                geo['features'][i]['properties']['2016rvotes'] = 0
                geo['features'][i]['properties']['2016ovotes'] = 0

            if '2020' in d:
                geo['features'][i]['properties']['2020dvotes'] = d['2020']['DEMOCRAT']
                geo['features'][i]['properties']['2020rvotes'] = d['2020']['REPUBLICAN']
                geo['features'][i]['properties']['2020ovotes'] = d['2020']['OTHER']
            else:
                geo['features'][i]['properties']['2020dvotes'] = 0
                geo['features'][i]['properties']['2020rvotes'] = 0
                geo['features'][i]['properties']['2020ovotes'] = 0             

        else:
            geo['features'][i]['properties']['avg'] = 0
            geo['features'][i]['properties']["change"] = 0
            geo['features'][i]['properties']['party'] = "NA"
            geo['features'][i]['properties']['flipped'] = "false"
            geo['features'][i]['properties']['2016dvotes'] = 0
            geo['features'][i]['properties']['2020dvotes'] = 0
            geo['features'][i]['properties']['2016rvotes'] = 0
            geo['features'][i]['properties']['2020rvotes'] = 0
            geo['features'][i]['properties']['2016ovotes'] = 0
            geo['features'][i]['properties']['20120ovotes'] = 0

    return geo

# genOutput(res)
# Outputs res data into outputFile as JSON.
def genOutput(res, output):
    with open(output, 'w') as jsonf:
        jsonf.write(json.dumps(res))

### MAIN ###
convertToJSON(dataSourceFile, dataintermFile)

geo = importSource(geoSourceFile)
data = importSource(dataintermFile)
res = combineDataSets(geo,data)

genOutput(res, outputFile)
