import pandas as pd
from Scripts.FeatureExtraction.ABI_FeatureExtraction import ABI_FeatureExtraction
from Scripts.FeatureExtraction.Bytecode_FeatureExtraction import Bytecode_FeatureExtraction
from Scripts.FeatureExtraction.Opcode_FeatureExtraction import Opcode_FeatureExtraction
from Scripts.FeatureExtraction.get_CodeMetrics import get_CodeMetrics

def apply_FeatureExtraction(dataset,attributes):
    try:
        for attribute in attributes:
            match attribute.lower():
                case 'all':
                    dataset = ABI_FeatureExtraction(dataset)
                    dataset = Bytecode_FeatureExtraction(dataset)
                    dataset = Opcode_FeatureExtraction(dataset)
                    getCodeMetrics()
                case '1' | 'abi':
                    return ABI_FeatureExtraction(dataset)
                case '2' | 'input' | 'bytecode':
                    return Bytecode_FeatureExtraction(dataset)
                case '3' | 'opcode':
                    return Opcode_FeatureExtraction(dataset)
                case '4' | 'code metrics':
                    return getCodeMetrics()
                # default pattern
                case _:
                    print(attribute + ' is an incorrect attribute')
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise

def getCodeMetrics():
    SamplesFolderName = input('Enter the name of the samples folder')
    SamplesDirPath = input('If the samples folder is located in ./RawData/Samples press Enter, otherwise enter the path to the samples folder.')
    DatasetName = input('Enter the dataset name.')
    get_CodeMetrics(SamplesFolderName,SamplesDirPath,DatasetName)

def apply_Bytecode_FeatureExtraction(dataset):
    methods = input('Enter a list of the extraction methods to apply on Bytecodes')
    return Bytecode_FeatureExtraction(dataset, methods)

def apply_Opcode_FeatureExtraction(dataset):
    methods = input('Enter a list of the extraction methods to apply on Opcodes')
    return Opcode_FeatureExtraction(dataset,methods)