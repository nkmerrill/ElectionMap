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
            geo['features'][i]['properties']['change'] = d['change']
            geo['features'][i]['properties']['party'] = d['party']
            geo['features'][i]['properties']['flipped'] = d['flipped']
            
            if '2016' in d:
                geo['features'][i]['properties']['2016dvotes'] = d['2016']['DEMOCRAT']
                geo['features'][i]['properties']['2016rvotes'] = d['2016']['REPUBLICAN']
            if '2020' in d:
                geo['features'][i]['properties']['2020dvotes'] = d['2020']['DEMOCRAT']
                geo['features'][i]['properties']['2020rvotes'] = d['2020']['REPUBLICAN']
        else:
            geo['features'][i]['properties']['avg'] = 0
            geo['features'][i]['properties']["change"] = 0
            geo['features'][i]['properties']['party'] = "NA"
            geo['features'][i]['properties']['flipped'] = "false"
            geo['features'][i]['properties']['2016dvotes'] = 0
            geo['features'][i]['properties']['2020dvotes'] = 0
            geo['features'][i]['properties']['2016rvotes'] = 0
            geo['features'][i]['properties']['2020rvotes'] = 0

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
