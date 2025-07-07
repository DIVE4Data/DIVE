import pandas as pd
import json
from Scripts.FeatureExtraction.ABI_FeatureExtraction import ABI_FeatureExtraction
from Scripts.FeatureExtraction.Bytecode_FeatureExtraction import Bytecode_FeatureExtraction
from Scripts.FeatureExtraction.Opcode_FeatureExtraction import Opcode_FeatureExtraction
from Scripts.FeatureExtraction.get_CodeMetrics import get_CodeMetrics
from Scripts.FeatureExtraction.Timestamp_FeatureExtraction import Timestamp_FeatureExtraction
from Scripts.FeatureExtraction.transactionIndex_FeatureExtraction import transactionIndex_FeatureExtraction
from Scripts.FeatureExtraction.Library_FeatureExtraction import library_FeatureExtraction

def apply_FeatureExtraction(DatasetName,dataset_or_SamplesFolderName,attributes,session_path=None):
    try:
        #read data
        #specify code folder
        for attribute in attributes:
            match attribute.lower():
                case 'all':
                    dataset = dataset_or_SamplesFolderName
                    ABI_FeatureExtraction(DatasetName,dataset, Col='ABI', session_path=session_path)
                    Timestamp_FeatureExtraction(DatasetName,dataset, Col='timeStamp', session_path=session_path)
                    library_FeatureExtraction(DatasetName, dataset, Col='Library', session_path=session_path)
                    transactionIndex_FeatureExtraction(DatasetName,dataset, Col='transactionIndex', session_path=session_path)
                    call_Bytecode_FeatureExtraction(DatasetName,dataset, session_path=session_path)
                    call_Opcode_FeatureExtraction(DatasetName,dataset, session_path=session_path)
                    call_get_CodeMetrics(DatasetName,SamplesFolderName,session_path)
                case '1' | 'abi':
                    dataset = dataset_or_SamplesFolderName
                    ABI_FeatureExtraction(DatasetName,dataset, Col='ABI', session_path=session_path)
                case '2' | 'timestamp':
                    dataset = dataset_or_SamplesFolderName
                    Timestamp_FeatureExtraction(DatasetName,dataset, Col='timeStamp', session_path=session_path)
                case '3' | 'library':
                    dataset = dataset_or_SamplesFolderName
                    library_FeatureExtraction(DatasetName, dataset, Col='Library', session_path=session_path)
                case '4' | 'transactionIndex':
                    dataset = dataset_or_SamplesFolderName
                    transactionIndex_FeatureExtraction(DatasetName,dataset, Col='transactionIndex', session_path=session_path)
                case '5' | 'code metrics':
                    SamplesFolderName = dataset_or_SamplesFolderName
                    call_get_CodeMetrics(DatasetName,SamplesFolderName, session_path)
                case '6' | 'input' | 'bytecode':
                    dataset = dataset_or_SamplesFolderName
                    call_Bytecode_FeatureExtraction(DatasetName,dataset, session_path)
                case '7' | 'opcode':
                    dataset = dataset_or_SamplesFolderName
                    call_Opcode_FeatureExtraction(DatasetName,dataset, session_path)
                case _:
                    print(attribute + ' is an incorrect attribute')
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise

def call_get_CodeMetrics(DatasetName,SamplesFolderName,session_path):
    SamplesDirPath = input('If the samples folder is located in ./RawData/Samples press Enter, otherwise enter the path to the samples folder.')
    #DatasetName = input('Enter the dataset name.')
    get_CodeMetrics(SamplesFolderName,SamplesDirPath,DatasetName, session_path)

def call_Bytecode_FeatureExtraction(DatasetName,dataset, session_path):
    #methods = get_FeatureExtractionMethods('Bytecodes')
    #Bytecode_FeatureExtraction(DatasetName,dataset, methods)
    Bytecode_FeatureExtraction(DatasetName,dataset, session_path)

def call_Opcode_FeatureExtraction(DatasetName,dataset, session_path):
    #methods = get_FeatureExtractionMethods('Opcodes')
    #Opcode_FeatureExtraction(DatasetName,dataset, methods='1', Col='Opcodes')
    Opcode_FeatureExtraction(DatasetName,dataset, Col='Opcodes', session_path=session_path)

def get_FeatureExtractionMethods(FeatureType):
    Flag = True
    methods = []
    while Flag:
        method = input('Enter the name or id of Feature extraction method to apply on ' + FeatureType + 
                       '\n Press Enter without typing anything to exit..')
        if len(method) > 0:
            methods.append(method)
        else:
            Flag = False
    return methods

def read_session(path):
    with open(path, "r") as f:
        return json.load(f)