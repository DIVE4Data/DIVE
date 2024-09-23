import pandas as pd
from Scripts.FeatureExtraction.ABI_FeatureExtraction import ABI_FeatureExtraction
from Scripts.FeatureExtraction.Bytecode_FeatureExtraction import Bytecode_FeatureExtraction
from Scripts.FeatureExtraction.Opcode_FeatureExtraction import Opcode_FeatureExtraction
from Scripts.FeatureExtraction.get_CodeMetrics import get_CodeMetrics

def apply_FeatureExtraction(DatasetName,dataset,attributes):
    try:
        for attribute in attributes:
            match attribute.lower():
                case 'all':
                    dataset = ABI_FeatureExtraction(DatasetName,dataset)
                    dataset = call_Bytecode_FeatureExtraction(DatasetName,dataset)
                    dataset = call_Opcode_FeatureExtraction(DatasetName,dataset)
                    call_get_CodeMetrics()
                case '1' | 'abi':
                    return ABI_FeatureExtraction(DatasetName,dataset)
                case '2' | 'input' | 'bytecode':
                    return call_Bytecode_FeatureExtraction(DatasetName,dataset)
                case '3' | 'opcode':
                    return call_Opcode_FeatureExtraction(DatasetName,dataset)
                case '4' | 'code metrics':
                    return call_get_CodeMetrics(DatasetName)
                # default pattern
                case _:
                    print(attribute + ' is an incorrect attribute')
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise

def call_get_CodeMetrics(DatasetName):
    SamplesFolderName = input('Enter the name of the samples folder')
    SamplesDirPath = input('If the samples folder is located in ./RawData/Samples press Enter, otherwise enter the path to the samples folder.')
    #DatasetName = input('Enter the dataset name.')
    get_CodeMetrics(SamplesFolderName,SamplesDirPath,DatasetName)

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