import json, datetime
from pathlib import Path
from IPython.display import display
import pandas as pd
from Scripts.get_BlockFeatures import get_BlockFeatures

def transactionIndex_FeatureExtraction(DatasetName,dataset, Col='transactionIndex',session_path=None):
    try:
        if Col in dataset.columns:
            self_main_dir = Path.cwd() 
            config_file_name = 'config.json'
            config_file_path = self_main_dir / config_file_name

            with open(config_file_path) as configFile:
                config_File = json.load(configFile)
            
            blockInfo = get_BlockFeatures(dataset, DatasetName)

            dataset = pd.merge(dataset, blockInfo[['blockNumber', 'transactionCount']], on='blockNumber', how='left')
            dataset['relative_tx_position'] = dataset['transactionIndex'] / dataset['transactionCount']
            dataset['block_position'] = dataset['relative_tx_position'].apply(categorize_position)

            # Determine the contract identifier column
            if 'contractID' in dataset.columns:
                contract_col = 'contractID'
            elif 'contractAddress' in dataset.columns:
                contract_col = 'contractAddress'
            else:
                raise KeyError('Neither "contractID" nor "contractAddress" found in dataset.')

            # Select output columns
            transactionIndex_Feature = dataset[[contract_col, 'blockNumber', 'transactionCount', Col, 'relative_tx_position', 'block_position']]

            UniqueFilename = generate_UniqueFilename(DatasetName,Col)
            outDir = self_main_dir/config_File['Features']['FE-based'][Col]
            outputPath = str(outDir) + '/' + UniqueFilename + ".csv"
            transactionIndex_Feature.to_csv(outputPath,index=False)
            if session_path:
                write_session(session_path, {"transactionIndex": outputPath})
            outDir = self_main_dir.relative_to(Path.cwd().parent)
            print('Done! the TransactionIndex-based Data is available in: ' + str(outDir) + '/' + UniqueFilename + ".csv")
            display(transactionIndex_Feature)
        else:
            print(f'The {Col} attribute is not present in the given dataset')
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise
#------------------------------------------
def categorize_position(ratio):
    if ratio <= 0.25:
        return 'early'
    elif ratio <= 0.75:
        return 'mid'
    else:
        return 'late'
#------------------------------------------
def generate_UniqueFilename(DatasetName,datatype):
    UniqueFilename = DatasetName + '_' + datatype + '_' + str(datetime.datetime.now().date()).replace('-', '') + '_' + str(datetime.datetime.now().time()).replace(':', '').split('.')[0]
    return UniqueFilename
#------------------------------------------
def read_session(path):
    with open(path, "r") as f:
        return json.load(f)
#------------------------------------------
def write_session(path, updates):
    session = read_session(path)
    session.update(updates)
    with open(path, "w") as f:
        json.dump(session, f, indent=2)