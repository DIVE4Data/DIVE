import pandas as pd
from pathlib import Path
import os, json

def get_Addresses(addressesFile):
    #Get the correct path to the configuration file
    #----------------------------------------------
    config_file_name = 'config.json'
    self_dir = Path(__file__).resolve().parent
    config_file_path = self_dir / config_file_name

    #Get the correct path to the main directory
    #-------------------------------------------
    self_main_dir = Path(__file__).resolve().parents[1]
    
    #Get Adresses dir path
    #---------------------
    configFile = open(config_file_path)
    config_File = json.load(configFile)
    configFile.close()
    path = self_main_dir/config_File['RawData']['SC_Addresses']
    #-------------------------------------------

    if addressesFile.lower == 'all' or '.csv' in addressesFile.lower:
        if addressesFile[0].lower == 'all' or len(addressesFile)>1:
            for filename in os.listdir(path):
                if 'csv' in filename and (addressesFile[0].lower == 'all' or filename in addressesFile):
                    df = pd.read_csv(path + filename)
                    if len(addresses) == 0:
                        addresses = df['contractAddress']
                    else:
                        addresses = pd.concat([addresses, df['contractAddress']])
            addresses.drop_duplicates(keep='first',inplace=True)
            addresses.reset_index(inplace=True, drop=True)
        else:
            df = pd.read_csv(path + addressesFile)
            addresses = df['contractAddress']
        return addresses
    else:
        print('Invalid file name. \n To read all files, use "All" as the file name. \n To get addresses from a specific file, type the file name with ".csv"')
    return False