import pandas as pd
import json, datetime
from IPython.display import display
from pathlib import Path
from feature_engine.creation import CyclicalFeatures

import json

def Timestamp_FeatureExtraction(DatasetName, dataset):
    try:
        #Get the correct path to the configuration file
        config_file_name = 'config.json'
        self_dir = Path(__file__).resolve().parents[2]
        config_file_path = self_dir / config_file_name
        configFile = open(config_file_path)
        config_File = json.load(configFile)
        configFile.close()
        #---------------------------------------

        dataset['timeStamp'] = pd.to_numeric(dataset['timeStamp'], errors='coerce')
        dataset['timeStamp'] = pd.to_datetime(dataset['timeStamp'], unit='s', errors='coerce')

        dataset['hour'] = dataset['timeStamp'].dt.hour
        dataset['dayofweek'] = dataset['timeStamp'].dt.dayofweek
        dataset['quarter'] = dataset['timeStamp'].dt.quarter
        dataset['part_of_day'] = pd.cut(dataset['hour'],bins=[-1, 6, 12, 18, 24],labels=['night', 'morning', 'afternoon', 'evening'])

        cyclical = CyclicalFeatures(variables=['hour', 'dayofweek'], drop_original=True)
        dataset = cyclical.fit_transform(dataset)  # Apply directly to dataset
        dataset = get_RowIDCol(dataset, config_File)
        new_cols = ['quarter', 'part_of_day',
                    'hour_sin', 'hour_cos', 'dayofweek_sin', 'dayofweek_cos']
        Timestamp_basedFeatures = dataset[['contractAddress'] + new_cols].copy()

        '''# Reorder: keep 'timeStamp', insert new_cols, then the rest
        new_cols = ['quarter', 'part_of_day',
                    'hour_sin', 'hour_cos', 'dayofweek_sin', 'dayofweek_cos']
        cols = dataset_encoded.columns.tolist()
        ts_index = cols.index('timeStamp') + 1

        for col in new_cols:
            cols.remove(col)
        cols[ts_index:ts_index] = new_cols 
        dataset = dataset_encoded[cols]'''

        UniqueFilename = generate_UniqueFilename(DatasetName,'Timestamp-based')
        self_main_dir = Path(__file__).resolve().parents[2]
        path = self_main_dir/config_File['Features']['FE-based']['Timestamp-based']
        Timestamp_basedFeatures.to_csv(str(path) + '/' + UniqueFilename + '.csv',index=False)

        path = self_main_dir.relative_to(Path.cwd().parent)/config_File['Features']['FE-based']['Timestamp-based']

        print('Done! the Timestamp-based Data is available in: ' + str(path) + '/' + UniqueFilename + '.csv')
        display(Timestamp_basedFeatures)

        return True
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise
#------------------------------------------
def get_RowIDCol(df,config_File):
    #Get the RowID column possible names
    RowIDColNames = config_File['DataLabels']['RowID']
    for column in df.columns:
        if column.lower() in RowIDColNames:
            df.rename(columns = {column:'contractAddress'}, inplace = True)
            return df
#------------------------------------------
def generate_UniqueFilename(DatasetName,datatype):
    UniqueFilename = DatasetName + '_' + datatype + '_' + str(datetime.datetime.now().date()).replace('-', '') + '_' + str(datetime.datetime.now().time()).replace(':', '').split('.')[0]
    return UniqueFilename