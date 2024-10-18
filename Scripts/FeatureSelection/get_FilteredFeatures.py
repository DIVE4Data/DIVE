import pandas as pd
from pathlib import Path
import json

def get_FilteredFeatures(filters):
    try:
        #get feature list file path
        configFile = readConfigFile()
        main_dir = Path(__file__).resolve().parents[1]
        featureList = str(main_dir) + configFile['Features']['Feature List File']
        # Read the CSV file
        featureListDF = pd.read_excel(featureList,sheet_name = configFile['Features']['Feature List Sheet'])

        # Check if any provided filter exists as a column
        valid_filters = {filter: value for filter, value in filters.items() if filter in featureListDF.columns}
        
        if not valid_filters:
            print("No valid filters provided. Returning all features.")
            return featureListDF['Feature'].tolist()

        # Print accepted filters
        print("Accepted Filters:")
        for filter in valid_filters.keys():
            print(f"- {filter}: {valid_filters[filter]}")

        # Apply filters provided by the caller
        for filter, value in filters.items():
            if filter in featureListDF.columns:
                featureListDF = featureListDF[featureListDF[filter].isin(value)]
            else:
                print(f"Warning: Filter '{filter}' not found in Feature CSV List File. Skipping...")

        return featureListDF['Feature'].tolist()

    except FileNotFoundError:
        print(f"Error: The file '{featureList}' was not found.")
    except pd.errors.EmptyDataError:
        print("Error: The file is empty.")
    except Exception as e:
        print(f"An error occurred: {e}")

def readConfigFile():
    config_file_name = 'config.json'
    self_dir = Path(__file__).resolve().parent
    config_file_path = self_dir / config_file_name
    
    configFile = open(config_file_path)
    config_File = json.load(configFile)
    configFile.close()
    return config_File