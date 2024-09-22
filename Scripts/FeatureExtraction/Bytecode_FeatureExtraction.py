#pip install hexbytes
from hexbytes import HexBytes
import pandas as pd
from collections import Counter
from IPython.display import display
from pathlib import Path
import os, json

TotalMethods = 1 
EVM_Opcodes = pd.DataFrame()
def Bytecode_FeatureExtraction(dataset, methods):

    try:
        #config_File = get_ConfigFile()
        #dataset = get_initialDataset(datasetName,dataDirPath,config_File)
        EVM_Opcodes = get_EVM_OPCODES()

        if len(methods)== 1 and methods[0].lower()== 'all':
            for methodID in range(1,TotalMethods +1):
                dataset = call_FeatureExtractionMethod(dataset,str(methodID))
        else:
            for methodID in methods:
                dataset = call_FeatureExtractionMethod(dataset,str(methodID))
        
        #finalDataName = generate_UniqueFilename(datasetName)
        #finalDataPath = str(get_Path('PreprocessedData',config_File))
        #dataset.to_csv(finalDataPath + '/' + finalDataName+'.csv',index=False)

        #print('Done! the Preprocessed Data is available in: ' + finalDataPath + '/' +finalDataName+'.csv')
        display(dataset)
        return True
    
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
    raise
#=============================================================================================================    
def call_FeatureExtractionMethod(dataset,methodID):
    match methodID:
        case '1' | 'get_Opcodes':
            dataset['ExtractedOpcodes'] = dataset['input'].apply(FE_Method_1_get_Opcodes)
            return dataset
        case '2' | '':
            return True #FE_Method_2_(dataset)
        # default pattern
        case _:
            print(methodID + ' is an incorrect Method ID')
#=============================================================================================================
def FE_Method_1_get_Opcodes(bytecode):
    # Convert hex bytecode to bytes
    bytecode_bytes = bytes.fromhex(bytecode[2:])  # Skip the '0x' prefix
    opcodes = []
    # Loop through bytecode bytes to extract opcodes
    for byte in bytecode_bytes:
        hexOpcode = f'0x{byte:02x}'
        opcodeName = EVM_Opcodes.get(hexOpcode, 'Unknown')
        opcodes.append(f'{opcodeName} {hexOpcode}')
    return opcodes
#=============================================================================================================
#Read EVM Opcodes csv file
#--------------------------
def get_EVM_OPCODES():
    config_File = get_ConfigFile()
    OpcodesFolder = get_Path('EVM_OpcodesDir',config_File)
    #get recent Opcodes csv files
    files = [file.name for file in os.scandir(OpcodesFolder) if file.is_file() and file.name.endswith('.csv')]
    recent_OpcodeFile = max(files, key=lambda x: os.path.getmtime(os.path.join(OpcodesFolder, x)))
    recent_OpcodesData = pd.read_csv(os.path.join(OpcodesFolder, recent_OpcodeFile))
    #create OpcodeCategories Dic
    EVM_Opcodes = pd.Series(recent_OpcodesData.Name.values, index=recent_OpcodesData.Stack).to_dict()
    # Convert to DataFrame
    EVM_OpcodesDF = pd.DataFrame(EVM_Opcodes.items(), columns=['Stack', 'Name'])
    # Filter out invalid entries and convert keys to integers
    EVM_OpcodesDF = EVM_OpcodesDF[~EVM_OpcodesDF['Stack'].str.contains('-')]
    # Convert back to dictionary
    EVM_Opcodes = dict(zip(EVM_OpcodesDF['Stack'], EVM_OpcodesDF['Name']))
    return EVM_Opcodes
#Read Configuration file
#-----------------------
def get_ConfigFile(config_file_name = 'config.json'):
    self_dir = Path(__file__).resolve().parent #current Dir
    config_file_path = self_dir / config_file_name
    configFile = open(config_file_path)
    config_File = json.load(configFile)
    configFile.close()
    return config_File
#Get dataComponent dir path
#--------------------------
def get_Path(dataType,config_File):
    self_main_dir = Path(__file__).resolve().parents[1] #main Dir
    if dataType == 'self_main_dir':
        path = self_main_dir
    elif dataType == 'EVM_OpcodesDir':
        path = self_main_dir/config_File['Features']['EVM_OpcodesDir']
    return path