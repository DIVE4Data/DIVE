import pandas as pd
import json
from pathlib import Path
from Scripts.FeatureExtraction.ABI_FeatureExtraction import ABI_FeatureExtraction
from Scripts.FeatureExtraction.Bytecode_FeatureExtraction import Bytecode_FeatureExtraction
from Scripts.FeatureExtraction.Opcode_FeatureExtraction import Opcode_FeatureExtraction
from Scripts.FeatureExtraction.get_CodeMetrics import get_CodeMetrics
from Scripts.FeatureExtraction.Timestamp_FeatureExtraction import Timestamp_FeatureExtraction
from Scripts.FeatureExtraction.transactionIndex_FeatureExtraction import transactionIndex_FeatureExtraction
from Scripts.FeatureExtraction.Library_FeatureExtraction import library_FeatureExtraction

def apply_FeatureExtraction(DatasetName,dataset_or_SamplesFolderName,attributes,session_path=None):
    try:
        if session_path is not None:
            session = read_session(session_path)
            AccountInfoPath = str(git_dir("AccountInfo")) + '/' + session.get("AccountInfo")
            contractInfoPath = str(git_dir("ContractsInfo")) + '/' + session.get("ContractsInfo")
            OpcodesPath = str(git_dir("Opcodes")) + '/' + session.get("Opcodes")
            SamplesFolderName = session.get("Samples")

            AccountInfoDF = pd.read_csv(AccountInfoPath)
            ContractsInfoDF = pd.read_csv(contractInfoPath)
            OpcodesDF = pd.read_csv(OpcodesPath)
        elif session_path is None and len(attributes)>1:

            AccountInfoPath = input("To extract features from timeStamp, transactionIndex, or Input, provide the complete path to the AccountInfo data file, or press Enter to skip:")
            contractInfoPath = input("To extract features from ABI or Library, provide the complete path to the ContractsInfo data file, or press Enter to skip: ")
            OpcodesPath = input("To extract features from Opcodes, provide the complete path to the Opcodes data file, or press Enter to skip:")
            SamplesFolderName = input("To extract features from code metrics, provide the name of the samples folder: ")

            AccountInfoDF = pd.read_csv(AccountInfoPath)
            ContractsInfoDF = pd.read_csv(contractInfoPath)
            OpcodesDF = pd.read_csv(OpcodesPath)
        else:
            AccountInfoDF = ContractsInfoDF = OpcodesDF = SamplesFolderName = dataset_or_SamplesFolderName

        for attribute in attributes:
            match attribute.lower():
                case 'all':
                    ABI_FeatureExtraction(DatasetName,ContractsInfoDF, Col='ABI', session_path=session_path)
                    Timestamp_FeatureExtraction(DatasetName,AccountInfoDF, Col='timeStamp', session_path=session_path)
                    library_FeatureExtraction(DatasetName, ContractsInfoDF, Col='Library', session_path=session_path)
                    transactionIndex_FeatureExtraction(DatasetName,AccountInfoDF, Col='transactionIndex', session_path=session_path)
                    call_Bytecode_FeatureExtraction(DatasetName,AccountInfoDF, session_path=session_path)
                    call_Opcode_FeatureExtraction(DatasetName,OpcodesDF, session_path=session_path)
                    call_get_CodeMetrics(DatasetName,SamplesFolderName,session_path)
                case '1' | 'abi':
                    ABI_FeatureExtraction(DatasetName,ContractsInfoDF, Col='ABI', session_path=session_path)
                case '2' | 'timestamp':
                    Timestamp_FeatureExtraction(DatasetName,AccountInfoDF, Col='timeStamp', session_path=session_path)
                case '3' | 'library':
                    library_FeatureExtraction(DatasetName, ContractsInfoDF, Col='Library', session_path=session_path)
                case '4' | 'transactionindex':
                    transactionIndex_FeatureExtraction(DatasetName,AccountInfoDF, Col='transactionIndex', session_path=session_path)
                case '5' | 'code metrics':
                    call_get_CodeMetrics(DatasetName,SamplesFolderName, session_path)
                case '6' | 'input' | 'bytecode':
                    call_Bytecode_FeatureExtraction(DatasetName,AccountInfoDF, session_path)
                case '7' | 'opcode':
                    call_Opcode_FeatureExtraction(DatasetName,OpcodesDF, session_path)
                case _:
                    print(attribute + ' is an incorrect attribute')
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise

def call_get_CodeMetrics(DatasetName,SamplesFolderName,session_path):
    if session_path is not None:
        session = read_session(session_path)
        SamplesDirPath = session.get("SamplesDirPath")
        if SamplesDirPath == "":
            SamplesDirPath = str(git_dir("Samples")) 
    else:
        SamplesDirPath = input('If the samples folder is located in ./RawData/Samples press Enter, otherwise enter the path to the samples folder.')

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

def git_dir(data):
    self_main_dir = Path(__file__).resolve().parents[1]
    config_file_name = 'config.json'
    config_file_path = self_main_dir / config_file_name
    configFile = open(config_file_path)
    config_File = json.load(configFile)
    configFile.close()
    if data == "Samples":
        return self_main_dir/config_File['RawData'][data]
    else:
        return self_main_dir/config_File['Features']['API-based'][data]