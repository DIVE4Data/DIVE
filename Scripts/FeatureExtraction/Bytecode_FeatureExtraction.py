import pandas as pd
from IPython.display import display
from pathlib import Path
import os, json, datetime

def Bytecode_FeatureExtraction(DatasetName,dataset, Col='input', ConstructorArgumentsCol=None, session_path=None):
    try:
        if Col in dataset.columns:
            #Get configurations data
            config_File = get_ConfigFile()
            #---------------------------------------
            #Ensure the rowID column is named 'contractAddress'
            dataset = get_RowIDCol(dataset,config_File)
            Bytecode_basedFeatures = dataset[['contractAddress', Col]]            

            if ConstructorArgumentsCol and ConstructorArgumentsCol in dataset.columns:
                Bytecode_basedFeatures['ConstructorArguments'] = dataset[ConstructorArgumentsCol]
            else:
                Bytecode_basedFeatures['ConstructorArguments'] = None

            # 1) Extract pure creation bytecode from input (strip constructor args if present)
            Bytecode_basedFeatures['creationBytecode'] = Bytecode_basedFeatures.apply(lambda r: extract_creation_bytecode(str(r[Col]), r['ConstructorArguments']),axis=1)

            # 2) Disassemble creation bytecode → opcodes
            EVM_Opcodes = get_EVM_OPCODES(config_File)

            Bytecode_basedFeatures['ExtractedOpcodes'] = Bytecode_basedFeatures['creationBytecode'].apply(lambda x: disassemble_hex(x, EVM_Opcodes))

            UniqueFilename = generate_UniqueFilename(DatasetName,'Input-based')
            self_main_dir = Path(__file__).resolve().parents[2]
            path = self_main_dir/config_File['Features']['FE-based']['Input-based']
            outputPath = str(path) + '/' + UniqueFilename + '.csv'
            Bytecode_basedFeatures.to_csv(outputPath,index=False)

            if session_path:
                write_session(session_path, {"Input": outputPath})

            path = self_main_dir.relative_to(Path.cwd().parent)/config_File['Features']['FE-based']['Input-based']

            print('Done! the Bytecode-based Data is available in: ' + str(path) + '/' + UniqueFilename + '.csv')
            display(Bytecode_basedFeatures)
        else:
            print(f'The {Col} attribute is not present in the given dataset')
    
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise
#=============================================================================================================
#--------------------------
# Extract bytecode from input
#--------------------------
def extract_creation_bytecode(tx_input_hex, constructor_args_hex=None):

    if not isinstance(tx_input_hex, str) or not tx_input_hex.startswith('0x'):
        return '0x'
    s = tx_input_hex.lower()
    if constructor_args_hex and isinstance(constructor_args_hex, str) and constructor_args_hex.startswith('0x'):
        ca = constructor_args_hex.lower()
        if s.endswith(ca):
            return '0x' + s[2:-len(ca)]
    return s  
#--------------------------
def disassemble_hex(hexdata, opcode_map):
    if not isinstance(hexdata, str) or not hexdata.startswith('0x'):
        return []
    
    data = bytes.fromhex(hexdata[2:])
    i, n = 0, len(data)
    opcodes = []

    while i < n:
        op = data[i]
        name = opcode_map.get(op, 'UNKNOWN')
        opcodes.append(f'{name} 0x{op:02x}')
        i += 1

        # Handle PUSH1..PUSH32 (0x60..0x7f): skip immediate data bytes
        if 0x60 <= op <= 0x7f:
            push_len = op - 0x5f
            i += min(push_len, max(0, n - i))  # skip data safely
    return opcodes
#--------------------------
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
#--------------------------
#Read Configuration file
#-----------------------
def get_ConfigFile(config_file_name = 'config.json'):
    self_dir = Path(__file__).resolve().parents[2] #DIVE Dir
    config_file_path = self_dir / config_file_name
    configFile = open(config_file_path)
    config_File = json.load(configFile)
    configFile.close()
    return config_File
#--------------------------
#Get dataComponent dir path
#--------------------------
def get_Path(dataType,config_File):
    self_main_dir = Path(__file__).resolve().parents[2] #DIVE Dir
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
#------------------------------------------
def read_session(path):
    with open(path, "r") as f:
        return json.load(f)
#------------------------------------------
def write_session(path, updates):
    session = read_session(path)
    session.update(updates)
    with open(path, "w") as f:
        json.dump(session, f, indent=2)