#pip install hexbytes
from hexbytes import HexBytes
import pandas as pd
from collections import Counter
from IPython.display import display
from pathlib import Path
import os, json, datetime

TotalMethods = 1 

def Bytecode_FeatureExtraction(DatasetName,dataset, methods):
    print('FE_Method_1_get_Opcodes method, start..')
    try:
        if 'input' in dataset.columns:
            #Get configurations data
            print('read config file')
            config_File = get_ConfigFile()
            print('done')
            #---------------------------------------
            #Ensure the rowID column is named 'contractAddress'
            print('check rowID')
            dataset = get_RowIDCol(dataset,config_File)
            Bytecode_basedFeatures = dataset[['contractAddress', 'input']]
            print('done. \n get EVM_opcodes')
            EVM_Opcodes = get_EVM_OPCODES(config_File)
            print('done')

            if len(methods)== 1 and methods[0].lower()== 'all':
                for methodID in range(1,TotalMethods +1):
                    Bytecode_basedFeatures = call_FeatureExtractionMethod(Bytecode_basedFeatures,str(methodID),EVM_Opcodes)
            else:
                for methodID in methods:
                    Bytecode_basedFeatures = call_FeatureExtractionMethod(Bytecode_basedFeatures,str(methodID),EVM_Opcodes)
            
            UniqueFilename = generate_UniqueFilename(DatasetName,'Input-based')
            self_main_dir = Path(__file__).resolve().parents[2]
            path = self_main_dir/config_File['Features']['FE-based']['Input-based']
            Bytecode_basedFeatures.to_csv(str(path) + '/' + UniqueFilename + '.csv',index=False)

            path = self_main_dir.relative_to(Path.cwd().parent)/config_File['Features']['FE-based']['Input-based']

            print('Done! the Bytecode-based Data is available in: ' + str(path) + '/' + UniqueFilename + '.csv')
            display(Bytecode_basedFeatures)
            return True
        else:
            return 'Bytecode (input) attribute is not present in the given dataset'
    
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
    raise
#=============================================================================================================    
def call_FeatureExtractionMethod(dataset,methodID,EVM_Opcodes):
    match methodID:
        case '1' | 'get_Opcodes':
            dataset['ExtractedOpcodes'] = dataset['input'].apply(FE_Method_1_get_Opcodes,EVM_Opcodes)
            return dataset
        case '2' | '':
            return True #FE_Method_2_(dataset)
        # default pattern
        case _:
            print(methodID + ' is an incorrect Method ID')
#=============================================================================================================
def FE_Method_1_get_Opcodes(bytecode,EVM_Opcodes):
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
def get_EVM_OPCODES(config_File):
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
    self_dir = Path(__file__).resolve().parents[1] #Script Dir
    config_file_path = self_dir / config_file_name
    configFile = open(config_file_path)
    config_File = json.load(configFile)
    configFile.close()
    return config_File
#Get dataComponent dir path
#--------------------------
def get_Path(dataType,config_File):
    self_main_dir = Path(__file__).resolve().parents[2] #main Dir
    if dataType == 'self_main_dir':
        path = self_main_dir
    elif dataType == 'EVM_OpcodesDir':
        path = self_main_dir/config_File['Features']['EVM_OpcodesDir']
    return path
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