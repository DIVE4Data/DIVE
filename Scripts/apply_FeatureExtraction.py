import pandas as pd
from Scripts.FeatureExtraction.ABI_FeatureExtraction import ABI_FeatureExtraction
from Scripts.FeatureExtraction.Bytecode_FeatureExtraction import Bytecode_FeatureExtraction
from Scripts.FeatureExtraction.Opcode_FeatureExtraction import Opcode_FeatureExtraction
from Scripts.FeatureExtraction.get_CodeMetrics import get_CodeMetrics
from Scripts.FeatureExtraction.Timestamp_FeatureExtraction import Timestamp_FeatureExtraction
from Scripts.FeatureExtraction.transactionIndex_FeatureExtraction import transactionIndex_FeatureExtraction

def apply_FeatureExtraction(DatasetName,dataset_or_SamplesFolderName,attributes):
    try:
        for attribute in attributes:
            match attribute.lower():
                case 'all':
                    dataset = dataset_or_SamplesFolderName
                    ABI_FeatureExtraction(DatasetName,dataset)
                    Timestamp_FeatureExtraction(DatasetName,dataset)
                    call_transactionIndex_FeatureExtraction(DatasetName,dataset)
                    call_get_CodeMetrics()
                    #dataset = call_Bytecode_FeatureExtraction(DatasetName,dataset)
                    #dataset = call_Opcode_FeatureExtraction(DatasetName,dataset)
                case '1' | 'abi':
                    dataset = dataset_or_SamplesFolderName
                    return ABI_FeatureExtraction(DatasetName,dataset)
                case '2' | 'input' | 'bytecode':
                    dataset = dataset_or_SamplesFolderName
                    return call_Bytecode_FeatureExtraction(DatasetName,dataset)
                case '3' | 'opcode':
                    dataset = dataset_or_SamplesFolderName
                    return call_Opcode_FeatureExtraction(DatasetName,dataset)
                case '4' | 'timestamp':
                    dataset = dataset_or_SamplesFolderName
                    return Timestamp_FeatureExtraction(DatasetName,dataset)
                case '5' | 'transactionIndex':
                    dataset = dataset_or_SamplesFolderName
                    return  transactionIndex_FeatureExtraction(DatasetName,dataset)
                case '6' | 'code metrics':
                    SamplesFolderName = dataset_or_SamplesFolderName
                    return call_get_CodeMetrics(DatasetName,SamplesFolderName)
                case _:
                    print(attribute + ' is an incorrect attribute')
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise

def call_get_CodeMetrics(DatasetName,SamplesFolderName):
    SamplesDirPath = input('If the samples folder is located in ./RawData/Samples press Enter, otherwise enter the path to the samples folder.')
    #DatasetName = input('Enter the dataset name.')
    get_CodeMetrics(SamplesFolderName,SamplesDirPath,DatasetName)

def call_transactionIndex_FeatureExtraction(DatasetName,dataset):
    blockInfo_fileName = input('Provide the name of the blockInfo file. If the file not in the default dir, provide the full path.')
    return transactionIndex_FeatureExtraction(DatasetName,dataset,blockInfo_fileName)

def call_Bytecode_FeatureExtraction(DatasetName,dataset):
    methods = get_FeatureExtractionMethods('Bytecodes')
    return Bytecode_FeatureExtraction(DatasetName,dataset, methods)

def call_Opcode_FeatureExtraction(DatasetName,dataset):
    methods = get_FeatureExtractionMethods('Opcodes')
    return Opcode_FeatureExtraction(DatasetName,dataset,methods)

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