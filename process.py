import json
from csvtojson import convertToJSON;

def importSource(value):
    with open(value) as input:
        return json.load(input)

def combineDataSets(geo, data):
    for i in range(len(geo['features'])):
        fips = str(int(geo['features'][i]['properties']['fips']))
        if fips in data:
            d = data[str(int(geo['features'][i]['properties']['fips']))]
            geo['features'][i]['properties']['avg'] = d['averageRatio']
            geo['features'][i]['properties']['16to20change'] = d['16to20change']
        else:
            geo['features'][i]['properties']['avg'] = 0
            geo['features'][i]['properties']["16to20change"] = 0

    return geo

def genOutput(res):
    with open("output.geojson", 'w') as jsonf:
        jsonf.write(json.dumps(res))

#Main
convertToJSON()

geo = importSource("composite_us_counties.geojson")
data = importSource("presdataJSON.json")
res = combineDataSets(geo,data)

genOutput(res)
