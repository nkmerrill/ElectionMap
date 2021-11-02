# alaska.py
# Written by nkmerrill
# 
# Removes any element relating to Alaska from the project due to Alaska's inconsistent voting patterns.
from process import importSource, genOutput
import os

## FILES ##
targetFiles = ["avg20162020.geojson", "county_labels.geojson", "state_labels.geojson", "composite_us_states.geojson"]

# removeAlaska(source)
# Removes any element referencing alaska
# Saves result in the source + "noAlaska" file.
def removeAlaska(source):
    data = importSource(source)
    toDelete = []
    #find indexes to delete
    for i in range(len(data['features'])):
        if "fips_state" in data['features'][i]['properties']:
            if data['features'][i]['properties']['fips_state'] == '02':
                toDelete.append(i)

        elif "state_fips" in data['features'][i]['properties']:
            if data['features'][i]['properties']['state_fips'] == '02':
                toDelete.append(i)
        else:
            print("Missed Feature:\n" + data['features'][i] )

    #sort deletions in descending order to prevent mis-indexing
    toDelete = sorted(toDelete,reverse=True)

    for i in toDelete:
        data['features'].pop(i)
    
    genOutput(data, os.path.join("output",source+"noAlaska"))


for target in targetFiles:
    removeAlaska(target)