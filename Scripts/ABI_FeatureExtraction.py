import pandas as pd
import json

def ABI_FeatureExtraction(dataset):
    dataset['ABI'] = dataset['ABI'].apply(lambda s: json.loads(s.replace("'", '"')))
    #Apply feature extraction to each ABI row
    ABI_FeaturesDF = dataset['ABI'].apply(FeatureExtraction).apply(pd.Series)
    #Combine the original dataset with the ABI features
    dataset_with_ABI_Features = pd.concat([dataset, ABI_FeaturesDF], axis=1)
    return dataset_with_ABI_Features

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