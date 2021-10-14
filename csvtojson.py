import csv
import json

def convertToJSON():
    data = {}

    with open("presdata2012-2020.csv") as csvf:
        csvReader = csv.DictReader(csvf)

        for rows in csvReader:
            key = rows['county_fips']
            if key not in data:
                data[key] = {}
            if rows['year'] not in data[key]:
                data[key][rows['year']] = {}
            data[key][rows['year']][rows['party']] = rows['candidatevotes']

    for i in data:
        for j in data[i]:
            repub = data[i][j]['REPUBLICAN']
            demo = data[i][j]['DEMOCRAT']
            
            if demo != "NA" and repub != "NA":
                if int(repub) == 0:
                    data[i][j]['ratio'] = 10
                elif int(demo) == 0:
                    data[i][j]['ratio'] = 0
                else:
                    data[i][j]['ratio'] = int(demo)/int(repub)
            else:
                data[i][j]['ratio'] = 'NA'


    for i in data:
        length = len(data[i])
        avg = 0
        for j in data[i]:
            if data[i][j]['ratio'] == 'NA':
                length -= 1
            else:
                avg += float(data[i][j]['ratio'])

        data[i]['averageRatio'] = avg/length

        if '2020' in data[i] and '2016' in data[i]:
            data[i]['16to20change'] = float(data[i]['2020']['ratio']) - float(data[i]['2016']['ratio']) 
        else:
            data[i]['16to20change'] = 'NA'

    with open("presdataJSON.json", 'w') as jsonf:
        jsonf.write(json.dumps(data, indent=4))
