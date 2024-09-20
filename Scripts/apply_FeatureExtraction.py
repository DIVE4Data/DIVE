import pandas as pd
from Scripts.FeatureExtraction.ABI_FeatureExtraction import ABI_FeatureExtraction
from Scripts.FeatureExtraction.get_CodeMetrics import get_CodeMetrics

def apply_FeatureExtraction(dataset,attributes):
    try:
        for attribute in attributes:
            match attribute.lower():
                case 'all':
                    dataset = ABI_FeatureExtraction(dataset)
                    getCodeMetrics()
                case '1' | 'abi':
                    dataset = ABI_FeatureExtraction(dataset)
                case '2' | 'input':
                    return True
                case '3' | 'opcode':
                    return True
                case '4' | 'code metrics':
                    getCodeMetrics()
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