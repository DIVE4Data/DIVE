import pandas as pd
from pathlib import Path
import os, json

def get_Addresses(addressesFile):
    try:
        #Get the correct path to the configuration file
        #----------------------------------------------
        config_file_name = 'config.json'
        self_dir = Path(__file__).resolve().parents[1]
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
        #Get the RowID column possible names
        #-----------------------------------
        RowIDColNames = config_File['DataLabels']['RowID']

        if addressesFile[0].lower() == 'all' or '.csv' in addressesFile[0].lower():
            addresses = pd.DataFrame(columns=['contractAddress'])
            if addressesFile[0].lower() == 'all' or len(addressesFile)>1:
                for filename in os.listdir(path):
                    if 'csv' in filename and (addressesFile[0].lower() == 'all' or filename in addressesFile):
                        df = pd.read_csv(os.path.join(path,filename))
                        df = get_RowIDCol(df,RowIDColNames)
                        if len(addresses) == 0:
                            addresses['contractAddress'] = df['contractAddress']
                        else:
                            addresses = pd.concat([addresses, df['contractAddress']])
            else:
                df = pd.read_csv(str(path) + '/' + addressesFile[0])
                df = get_RowIDCol(df,RowIDColNames)
                addresses['contractAddress'] = df['contractAddress']
            
            addresses.dropna(inplace=True)
            addresses.drop_duplicates(keep='first',inplace=True)
            addresses.reset_index(inplace=True, drop=True)
            return addresses
        else:
            print('Invalid file name. \n To read all files, use "All" as the file name. \n To get addresses from a specific file, type the file name with ".csv"')
            return False
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise
    
def get_RowIDCol(df,RowIDColNames):
    for column in df.columns:
        if column.strip().lower() in RowIDColNames:
            df.rename(columns = {column:'contractAddress'}, inplace = True)
            return df