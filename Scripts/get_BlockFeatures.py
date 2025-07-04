import requests, json, datetime
from pathlib import Path
from IPython.display import display

def get_ContractFeatures(dataset, DatasetName='', Col='blocknumber'):
    try:
        if Col in dataset.columns:
            self_main_dir = Path.cwd() 
            config_file_name = 'config.json'
            config_file_path = self_main_dir / config_file_name

            with open(config_file_path) as configFile:
                config_File = json.load(configFile)

            blockInfo = dataset[Col].value_counts().reset_index()
            blockInfo.columns = [Col, 'occurrences']
            blockInfo = blockInfo.sort_values(by=Col).reset_index(drop=True)

            api_key = config_File['Etherscan_Account']['API_Key']

            blockInfo['transactionCount'] = blockInfo[Col].apply(lambda blk: get_transaction_count(blk, api_key))

            UniqueFilename = generate_UniqueFilename(DatasetName,'blockInfo')
            outDir = self_main_dir/config_File['Features']['API-based']['BlockInfo']
            blockInfo.to_csv(str(outDir) + '/' + UniqueFilename + ".csv",index=False)
            outDir = self_main_dir.relative_to(Path.cwd().parent)
            print('Done! Block Info Data is available in: ' + str(outDir) + '/' + UniqueFilename + ".csv")
            display(blockInfo)
            return blockInfo
        else:
            print(f'The {Col} attribute is not present in the given dataset')
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise

def get_transaction_count(blockNo, api_key):
    try:
        request_string = f'https://api.etherscan.io/api?module=proxy&action=eth_getBlockTransactionCountByNumber&tag={hex(blockNo)}&apikey={api_key}'
        response = requests.get(request_string, verify=False)
        if response.ok:
            data = response.json()
            if 'result' in data and data['result']:
                return int(data['result'], 16)
        else:
            print(blockNo, response.text)
    except Exception as err:
        print(f"The run is aborted due to unexpected {err=}, {type(err)=}")
        raise
#------------------------------------------
def generate_UniqueFilename(DatasetName,datatype):
    UniqueFilename = DatasetName + '_' + datatype + '_' + str(datetime.datetime.now().date()).replace('-', '') + '_' + str(datetime.datetime.now().time()).replace(':', '').split('.')[0]
    return UniqueFilename