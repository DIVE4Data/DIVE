import requests, json, datetime, time
from pathlib import Path
from IPython.display import display

def get_BlockFeatures(dataset, DatasetName='', Col='blockNumber'):
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

            transaction_counts = []

            UniqueFilename = generate_UniqueFilename(DatasetName,'blockInfo')
            outDir = self_main_dir/config_File['Features']['API-based']['BlockInfo']
            outDir.mkdir(parents=True, exist_ok=True)
            output_path = str(outDir) + '/' + UniqueFilename + ".csv"


            for i, blk in enumerate(blockInfo[Col]):
                try:
                    tx_count = get_transaction_count(int(blk), api_key)
                    transaction_counts.append(tx_count)
                    print(f"({i}) Block #{blk} contains {tx_count} transaction(s).")
                except Exception as e:
                    print(f"Failed to retrieve tx count for block {blk} (index {i}): {e}")
                    transaction_counts.append(None)

                if (i + 1) % 5 == 0:
                    time.sleep(1)
        else:
            print(f'The {Col} attribute is not present in the given dataset')
    
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise
    
    finally:
        relative_path = output_path.relative_to(Path.cwd())
        
        if transaction_counts:
            partial_df = blockInfo.iloc[:len(transaction_counts)].copy()
            partial_df['transactionCount'] = transaction_counts
            partial_df.to_csv(output_path, index=False)
            print(f"Data saved to: {relative_path}")

        if len(transaction_counts) == len(blockInfo):        
            print(f"Done! Full Block Info Data is available at: {relative_path}")
            display(partial_df)
            return partial_df
        else:
            print(f"Partial data saved after interruption or error.")
            return None

def get_transaction_count(blockNo, api_key):
    try:
        request_string = f'https://api.etherscan.io/api?module=proxy&action=eth_getBlockTransactionCountByNumber&tag={hex(blockNo)}&apikey={api_key}'
        response = requests.get(request_string)
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