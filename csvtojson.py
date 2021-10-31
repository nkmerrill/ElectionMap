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
            if rows['mode'] != 'TOTAL':
                if rows['party'] != 'REPUBLICAN' and rows['party'] != 'DEMOCRAT':
                    if 'OTHER' not in data[key][rows['year']]:
                        data[key][rows['year']]['OTHER'] = rows['candidatevotes']
                    else:
                        data[key][rows['year']]['OTHER'] = str(int(data[key][rows['year']]['OTHER']) + int(rows['candidatevotes']))
                else:
                    if rows['party'] not in data[key][rows['year']]:
                        data[key][rows['year']][rows['party']] = rows['candidatevotes']
                    else:
                        data[key][rows['year']][rows['party']] = str(int(data[key][rows['year']][rows['party']]) + int(rows['candidatevotes']))
            else:
                if rows['party'] != 'REPUBLICAN' and rows['party'] != 'DEMOCRAT':
                    if 'OTHER' not in data[key][rows['year']] or data[key][rows['year']]['OTHER'] == 'NA':
                        data[key][rows['year']]['OTHER'] = rows['candidatevotes']
                    elif rows['candidatevotes'] != 'NA':
                        data[key][rows['year']]['OTHER'] = str(int(data[key][rows['year']]['OTHER']) + int(rows['candidatevotes']))
                else:
                    data[key][rows['year']][rows['party']] = rows['candidatevotes']

    for i in data:
        for j in data[i]:
            repub = data[i][j]['REPUBLICAN']
            demo = data[i][j]['DEMOCRAT']
            if 'OTHER' in data[i][j]:
                other = data[i][j]['OTHER']
            else:
                other = 'NA'

            if demo != "NA" and repub != "NA":
                repub = int(repub)
                demo = int(demo)
                other = 0 if other == 'NA' else int(other)

                if repub == 0 or demo == 0:
                    data[i][j]['ratio'] = 0
                else:
                    data[i][j]['ratio'] = max( demo/(demo+repub+other),repub/(demo+repub+other) )
                    data[i][j]['losratio'] = min(demo/(demo+repub+other),repub/(demo+repub+other))
                if repub > demo:
                    data[i][j]['winner'] = 'Republican'
                elif demo > repub:
                    data[i][j]['winner'] = 'Democrat'
                else:
                    data[i][j]['winner'] = 'Tie'
            else:
                data[i][j]['ratio'] = 'NA'
                data[i][j]['winner'] = 'NA'


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
            if data[i]['2020']['winner'] == data[i]['2016']['winner']:
                data[i]['change'] = float(data[i]['2020']['ratio']) - float(data[i]['2016']['ratio']) 
                data[i]['party'] = data[i]['2020']['winner']
                data[i]['flipped'] = 'false'
            else:
                data[i]['change'] = float(data[i]['2020']['ratio']) - float(data[i]['2016']['losratio'])
                data[i]['party'] = data[i]['2020']['winner']
                data[i]['flipped'] = 'true'
        else:
            data[i]['change'] = 'NA'
            data[i]['party'] = 'NA'
            data[i]['flipped'] = 'NA'

    with open("presdataJSON.json", 'w') as jsonf:
        jsonf.write(json.dumps(data, indent=4))

convertToJSON()