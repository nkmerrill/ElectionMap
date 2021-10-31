# csvtojson.py
# Written by nkmerrill
# 
# Takes presidential election data from MIT Election data in CSV format and converts it to JSON, 
# including yearly election results ratios and the change in ratio between 2016 and 2020.

import csv
import os
import json

### File Paths ###
sourceFile = os.path.join(r'mit',r'presdata2012-2020.csv')
outputFile = os.path.join(r'output',r'presdataJSON.json')

# pullCSVData
# Grabs relevant CSV data from sourceFile and puts it into a hashtable
# Output data is a hash table with county IDs as keys and election data seperated by year.
def pullCSVData(source):
    data = {}

    with open(source) as csvf:
        csvReader = csv.DictReader(csvf) #convert csv to hash table.

        for rows in csvReader: #data is broken by candidential results per county
            key = rows['county_fips']
            if key not in data:
                data[key] = {} #if first time county appears, create a new hash table for its data.
            if rows['year'] not in data[key]: 
                data[key][rows['year']] = {} #if first time year for county appears, create a new hash table.

            #Starting in 2020, some states started seperating results by vote types. This section handles that logic.
            if rows['mode'] != 'TOTAL':
                if rows['party'] != 'REPUBLICAN' and rows['party'] != 'DEMOCRAT': #Note: Third parties are combined into one data point to make parsing easier later.
                    #If the first time adding data, set value equal to current row. Otherwise, sum with previous values.
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
                    if 'OTHER' not in data[key][rows['year']] or data[key][rows['year']]['OTHER'] == 'NA': #If previous third party data was 'NA' then replace with new data.
                        data[key][rows['year']]['OTHER'] = rows['candidatevotes']
                    elif rows['candidatevotes'] != 'NA': #Ignore 'NA' results if there is already a third party vote in the data.
                        data[key][rows['year']]['OTHER'] = str(int(data[key][rows['year']]['OTHER']) + int(rows['candidatevotes'])) 
                else:
                    data[key][rows['year']][rows['party']] = rows['candidatevotes']

    return data

# calculateYearlyData(data)
# Calculates yearly election ratio and adds that data to dataset.
# Data added includes:
# ratio: The percentage of the vote received by the winning party as a floating point.
# winner: The winning party.
# losratio: The percentage of the vote received by the losing party as a floating point.
# An NA result for any data besides OTHER means there is insufficient data to determine a ratio.
def calculateYearlyData(data):
    for i in data:
        for j in data[i]:
            repub = data[i][j]['REPUBLICAN']
            demo = data[i][j]['DEMOCRAT']
            if 'OTHER' in data[i][j]:
                other = data[i][j]['OTHER']
            else:
                other = 'NA'

            if demo == "NA" or repub == "NA" or (demo == 0 and repub == 0): #Either party data being unavailable makes the data tainted and should not be considered.
                data[i][j]['ratio'] = 'NA'
                data[i][j]['winner'] = 'NA'
            else: 
                repub = int(repub)
                demo = int(demo)
                other = 0 if other == 'NA' else int(other)

                #Calculate percentage of vote for each party.
                if repub > demo:
                    data[i][j]['winner'] = 'Republican'
                    data[i][j]['ratio'] = repub/(demo+repub+other)
                    data[i][j]['losratio'] = demo/(demo+repub+other)
                elif demo > repub:
                    data[i][j]['winner'] = 'Democrat'
                    data[i][j]['ratio'] = demo/(demo+repub+other)
                    data[i][j]['losratio'] = repub/(demo+repub+other)
                else:
                    data[i][j]['winner'] = 'Tie'
                    data[i][j]['ratio'] = demo/(demo+repub+other)
                    data[i][j]['losratio'] = repub/(demo+repub+other)

    return data

# calculateCompData(data)
# Calculates data comparisons as first order data for each county.
# Adds the following to the data:
# change: the difference in percentage for the winning party going from 2016 to 2020.
# party: The party that won in 2020
# flipped: if true, the party that one in 2020 is different than the party that won in 2016.
def calculateCompData(data):
    for i in data: 
        #Determines ratio change from 2020 and 2016 for the party that won in 2020.
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

    return data

# writeoutput(dest,data)
# Writes resultant data to new JSON file.
def writeOutput(dest,data):
    with open(dest, 'w') as jsonf:
        jsonf.write(json.dumps(data, indent=4))

# convertToJSON()
# Converts sourceFile to JSON and gathers needed data.
def convertToJSON(source,dest):
    data = pullCSVData(source)
    data = calculateYearlyData(data)
    data = calculateCompData(data)

    writeOutput(dest,data)

### MAIN ###
convertToJSON(sourceFile, outputFile)