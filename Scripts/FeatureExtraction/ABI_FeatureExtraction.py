import pandas as pd
from IPython.display import display
from pathlib import Path
import json, datetime

def ABI_FeatureExtraction(DatasetName, dataset, Col='ABI'): #String: DatasetName, DataFrame: dataset
    if Col in dataset.columns:
        #Get the correct path to the configuration file
        config_file_name = 'config.json'
        self_dir = Path(__file__).resolve().parents[2]
        config_file_path = self_dir / config_file_name
        configFile = open(config_file_path)
        config_File = json.load(configFile)
        configFile.close()
        #---------------------------------------
        #Apply feature extraction to each ABI row
        ABI_FeaturesDF = dataset[Col].apply(FeatureExtraction).apply(pd.Series)

        #Ensure the rowID column is named 'contractAddress'
        dataset = get_RowIDCol(dataset,config_File)
        #Combine the dataset index column with the ABI features
        ABI_basedFeatures = pd.concat([dataset['contractAddress'], ABI_FeaturesDF], axis=1)

        UniqueFilename = generate_UniqueFilename(DatasetName,'ABI-based')
        self_main_dir = Path(__file__).resolve().parents[2]
        path = self_main_dir/config_File['Features']['FE-based']['ABI-based']
        ABI_basedFeatures.to_csv(str(path) + '/' + UniqueFilename + '.csv',index=False)

        path = self_main_dir.relative_to(Path.cwd().parent)/config_File['Features']['FE-based']['ABI-based']

        print('Done! the ABI-based Data is available in: ' + str(path) + '/' + UniqueFilename + '.csv')
        display(ABI_basedFeatures)
    else:
        print(f'The {Col} attribute is not present in the given dataset')

def FeatureExtraction(ABI):
    try:
        #Load the ABI string as JSON
        functions = [function for function in json.loads(ABI) if function['type'] == 'function']
        events = [event for event in json.loads(ABI) if event['type'] == 'event']
        #No of X in the contract
        NoOfFunctions = len(functions)
        NoOfInputs = sum(len(function.get('inputs', [])) for function in functions)
        NoOfOutputs = sum(len(function.get('outputs', [])) for function in functions)
        NoOfConstantFunctions = sum(1 for function in functions if function.get('constant', False))
        NoPayableFunctions = sum(1 for function in functions if function.get('payable', False))
        # No and types of inputs and outputs used in the contract
        unique_input_types = set(param['type'] for function in functions for param in function.get('inputs', []))
        unique_output_types = set(param['type'] for function in functions for param in function.get('outputs', []))
        NoOfUniqueInputTypes = len(unique_input_types)
        NoOfUniqueOutputTypes = len(unique_output_types)

        NoOfEvent = len(events)
        fallback_exists = any(function['type'] == 'fallback' for function in json.loads(ABI))
        constructor_exists = any(function['type'] == 'constructor' for function in json.loads(ABI))

        avg_FunctionLength = NoOfFunctions and sum(len(function['name']) for function in functions) / NoOfFunctions or 0
        #Max Inputs/Outputs per Function
        max_InputsOutputs = max((len(function.get('inputs', [])) + len(function.get('outputs', [])) for function in functions), default=0)
        #Average Inputs/Outputs per Function
        avg_InputsOutputs = NoOfFunctions and (NoOfInputs + NoOfOutputs) / NoOfFunctions or 0
        #Average Constant Functions per Function
        avg_ConstantPerFunction = NoOfConstantFunctions / NoOfFunctions if NoOfFunctions else 0
        #Average Payable Functions per Function
        avg_PayablePerFunction = NoPayableFunctions / NoOfFunctions if NoOfFunctions else 0
        
        return {
            'functions' : functions,
            'NoOfFunctions': NoOfFunctions,
            'NoOfInputs': NoOfInputs,
            'NoOfOutputs': NoOfOutputs,
            'NoOfConstantFunctions': NoOfConstantFunctions,
            'NoPayableFunctions': NoPayableFunctions,
            'UniqueInputTypes': unique_input_types,
            'UniqueOutputTypes': unique_output_types,
            'NoOfUniqueInputTypes': NoOfUniqueInputTypes,
            'NoOfUniqueOutputTypes': NoOfUniqueOutputTypes,
            'events': events,
            'NoOfEvent': NoOfEvent,
            'FallbackExists': 'Yes' if fallback_exists else 'No',
            'ConstructorExists': 'Yes' if constructor_exists else 'No',
            'avg_FunctionLength': avg_FunctionLength,
            'max_InputsOutputs': max_InputsOutputs,
            'avg_InputsOutputs': avg_InputsOutputs,
            'avg_ConstantPerFunction': avg_ConstantPerFunction,
            'avg_PayablePerFunction': avg_PayablePerFunction
        }
    except Exception as err:
        print(f"Unexpected {err=},{type(err)=}")
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