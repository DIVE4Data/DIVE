import pandas as pd
import numpy as np
from pathlib import Path
import json, os,datetime
from IPython.display import display
from sklearn.preprocessing import LabelEncoder
import sys

#Total number of preprocessing tasks currently offered
PreprocessingTasksNo = 11 #### All tasks will be applied except PreprocessingTask12_SetDataIndexColumn task

def apply_DataPreprocessing(datasetName,dataDirPath=True,PreprocessingTasks=['all'],session_path=None):
    try:
        config_File = get_ConfigFile()
        dataset = get_initialDataset(datasetName,dataDirPath,config_File)
        
        if len(PreprocessingTasks)== 1 and PreprocessingTasks[0].lower()== 'all':
            for taskID in range(1,PreprocessingTasksNo +1):
                dataset = call_PreprocessingTask(dataset,str(taskID),config_File, session_path,datasetName)
        else:
            for taskID in PreprocessingTasks:
                dataset = call_PreprocessingTask(dataset,str(taskID),config_File, session_path,datasetName)
        
        finalDataName = generate_UniqueFilename(datasetName)
        finalDataPath = str(get_Path('PreprocessedData',config_File))
        outputPath = finalDataPath + '/' + finalDataName+'.csv'
        dataset.to_csv(outputPath,index=False)

        if session_path:
            write_session(session_path, {"PreprocessedData": finalDataName+'.csv'})

        print('Done! the Preprocessed Data is available in:' + str(os.path.relpath(str(finalDataPath) + '/' +finalDataName+'.csv', Path.cwd().parent)))

        display(dataset)
        return True
    
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise

#Identify the preprocessing task to be performed
#-----------------------------------------------
def call_PreprocessingTask(dataset,taskID,config_File, session_path,datasetName):
    savePath = str(get_Path('PreprocessedData',config_File))
    match taskID:
        case '1' | 'DropDuplicates':
            return PreprocessingTask1_DropDuplicate(dataset)
        case '2' | 'HideProtectedAttributes':
            ProtectedAttributes = get_Path('ProtectedAttributes',config_File)
            return PreprocessingTask2_HideProtectedAttributes(dataset,ProtectedAttributes,savePath)
        case '3' | 'FillMissingData':
            dataToBeProcessed = get_Path('NullColsToNegativeOne',config_File)
            return PreprocessingTask3_FillMissingData(dataset,dataToBeProcessed)
        case '4' | 'ProcessConstructorArguments':
            return PreprocessingTask4_ProcessConstructorArguments(dataset)
        case '5' | 'ProcessOpcodes':
            return PreprocessingTask5_ProcessOpcodes(dataset)
        case '6' | 'RemoveUselesCols':
            dataToBeProcessed = get_Path('UselesCols',config_File)
            return PreprocessingTask6_RemoveUselesCols(dataset,dataToBeProcessed,savePath)
        case '7' | 'HandlingHexaData':
            dataToBeProcessed = get_Path('HexaColsToInt',config_File)
            return PreprocessingTask7_HandlingHexaData(dataset,dataToBeProcessed)
        case '8' | 'HandlingStringNumericalData':
            return PreprocessingTask8_HandlingStringNumericalData(dataset)
        case '9' | 'HandlingStringBoolColsToInt':
            return PreprocessingTask9_HandlingStringBoolColsToInt(dataset)
        case '10' | 'HandlingCategoricalData':
            dataToBeProcessed = get_Path('CategoricalCols',config_File)
            return PreprocessingTask10_HandlingCategoricalData(dataset,dataToBeProcessed,savePath,session_path,datasetName)
        case '11' | 'ConvertFloatColumns_to_Int':
            return PreprocessingTask11_ConvertFloatColumns_to_Int(dataset)
        case '12' | 'SetDataIndexColumn':
            dataToBeProcessed = get_Path('IndexCol',config_File)
            return PreprocessingTask12_SetDataIndexColumn(dataset,dataToBeProcessed)
        # default pattern
        case _:
            print(taskID + ' is an incorrect Task ID')

#Perform the chosen preprocessed task
#------------------------------------
def PreprocessingTask1_DropDuplicate(dataset):
    #DuplicateRows
    dataset.drop_duplicates(keep='first',inplace=True)
    dataset.reset_index(drop=True,inplace=True)
    
    #DuplicateCols
    # Check and drop each 'y' column individually if it exists
    if 'Opcodes_y' in dataset.columns:
        dataset.drop(columns=['Opcodes_y'], inplace=True)
    if 'input_y' in dataset.columns:
        dataset.drop(columns=['input_y'], inplace=True)

    # Check and rename each 'x' column individually if it exists
    if 'Opcodes_x' in dataset.columns:
        dataset.rename(columns={'Opcodes_x': 'Opcodes'}, inplace=True)
    if 'input_x' in dataset.columns:
        dataset.rename(columns={'input_x': 'input'}, inplace=True)
    return dataset
#------------------------------------
def PreprocessingTask2_HideProtectedAttributes(dataset,ProtectedAttributes,savePath):
    dataset.insert(0, 'contractID', range(1, len(dataset) + 1))
    protectedDatasetCols = ['contractID'] + ProtectedAttributes
    existing_cols = [col for col in protectedDatasetCols if col in dataset.columns]
    if existing_cols:
        protectedDataset = dataset[existing_cols]
        protectedDatasetName = generate_UniqueFilename('ProtectedAttributes')
        protectedDataset.to_csv(savePath + '/' + protectedDatasetName+'.csv',index=False)
        print('Done! the protected attirbutes data is available in:' + str(os.path.relpath(str(savePath) + '/' + protectedDatasetName+'.csv', Path.cwd().parent)))
        dataset = dataset.drop(columns=existing_cols)
    else:
        print("No valid protected columns found in dataset. Returning dataset unchanged.")
    return dataset
#------------------------------------
def PreprocessingTask3_FillMissingData(dataset,NullColsToNegativeOne):
    ## txreceipt_status values are 0 and 1, indicating failure and success, respectively.
    ## Blank means it is still waiting for confirmation
    cols = list(set(dataset.columns) & set(NullColsToNegativeOne))
    dataset[cols] = dataset[cols].fillna(-1)
    ## Fill all null values with zero
    dataset.fillna(0, inplace=True)
    return dataset
#------------------------------------
def PreprocessingTask4_ProcessConstructorArguments(dataset):
    # Split it into blocks to convert each to int
    if 'ConstructorArguments' in dataset.columns:
        max_ArgLength = 64 # 128bits
        dataset['ConstructorArguments'] =  dataset['ConstructorArguments'].str.extractall(f'(.{{1,{max_ArgLength}}})')[0].groupby(level=0).agg(list)
    return dataset
#------------------------------------
def PreprocessingTask5_ProcessOpcodes(dataset):
    # Convert each Opcode string to a list
    if 'Opcodes' in dataset.columns:
        dataset['Opcodes'] = dataset['Opcodes'].str.split('<br>')
    return dataset
#------------------------------------
def PreprocessingTask6_RemoveUselesCols(dataset,UselesCols,savePath):
    # UselessCols are columns that contain string values or that have already been engineered to extract useful features.
    ## Remove columns listed in UselessCols if they exist in the dataset
    cols_to_drop = list(set(dataset.columns) & set(UselesCols))
    dataset.drop(columns=cols_to_drop,axis=1,inplace=True)

    # UselessCols are columns that have a single value for all rows, usually zeros or nulls.
    ## Identify columns with a single unique value across the DataFrame
    cols_single_value = dataset.nunique(dropna=False) <= 1
    cols_single_value = cols_single_value[cols_single_value].index.tolist()
    dataset.drop(columns=cols_single_value, inplace=True)

    # Record detailed reasons for dropping columns to a JSON file
    removed_columns_info = {
        'Dropped_due_to_previous_engineering_or_non_numerical': cols_to_drop,
        'Dropped_due_to_lack_of_variance': cols_single_value
    }

    # Write all mappings to a single JSON file
    filename =  generate_UniqueFilename('DIVE_RemovedCols')
    with open(savePath + '/' + filename +'.json', 'w') as file:
        json.dump(removed_columns_info, file, indent=4)
    print('Done! Detailed reasons for column removal have been saved to:' + str(os.path.relpath(str(savePath) + '/' + filename +'.json', Path.cwd().parent)))
    return dataset
#------------------------------------
def PreprocessingTask7_HandlingHexaData(dataset,HexaColsToInt):
    cols = list(set(dataset.columns) & set(HexaColsToInt))
    ## convert hexa columns into integer
    for col in cols:
        if col in ['ConstructorArguments']:
            dataset[col] = dataset[col].apply(lambda x: list(map(lambda hex_val: int(hex_val, 16), x)) if isinstance(x, list) and x else []) #verify that it is a string (Hex) and not an empty list
        else:
            dataset[col]=dataset[col].astype(str).apply(int, base=16)
    return dataset
#------------------------------------
def PreprocessingTask8_HandlingStringNumericalData(dataset):
    return dataset.applymap(lambda x: int(x) if isinstance(x, str) and x.isnumeric() else x)
#------------------------------------
def PreprocessingTask9_HandlingStringBoolColsToInt(dataset):
    dataset = dataset.replace({'Yes':1,'No':0})
    return dataset
#------------------------------------
def PreprocessingTask10_HandlingCategoricalData(dataset,CategoricalCols,savePath,session_path,datasetName):
    cols = list(set(dataset.columns) & set(CategoricalCols))
    mappings = {}  # Dictionary to store mappings for all columns

    for col in cols:
        le= LabelEncoder()
        le.fit(dataset[col].unique().tolist())
        dataset[col]= le.transform(dataset[col])

        # Convert numpy types to Python native types for JSON serialization
        classes = le.classes_.tolist()  # Convert numpy array to list
        labels = le.transform(le.classes_).tolist()  # Transform and convert to list
        # Ensure all numeric types are converted to Python native types
        mappings[col] = {str(k): int(v) for k, v in zip(classes, labels)}

    # Write all mappings to a single JSON file
    filename =  generate_UniqueFilename(datasetName + '_CategoricalColsMappings')
    if session_path:
            write_session(session_path, {"CategoricalColsMappings": filename + '.json'})

    filepath = os.path.join(savePath, filename + '.json')
    with open(filepath, 'w') as file:
        json.dump(mappings, file, indent=4)
    print('Done! The categorical data mappings are available in:' + str(os.path.relpath(str(savePath) + '/' + filename +'.json', Path.cwd().parent)))
    return dataset
#------------------------------------
def PreprocessingTask11_ConvertFloatColumns_to_Int(dataset):
    for column in dataset.select_dtypes(include=['float']).columns:
        if dataset[column].apply(float.is_integer).all():
            dataset[column] = dataset[column].astype(int)
    return dataset
#------------------------------------
def PreprocessingTask12_SetDataIndexColumn(dataset,IndexCol):
    return dataset.set_index(IndexCol,drop=True,inplace=True)
#------------------------------------
#Get data to be preprocessed
#---------------------------
def get_initialDataset(datasetName,dataDirPath,config_File):
    if dataDirPath:
        path = get_Path('InitialCombinedData',config_File)
    else:
        self_main_dir = get_Path('self_main_dir',config_File)
        path = os.path.join(self_main_dir,dataDirPath)

    initialDataset = pd.read_csv(str(path) + '/' + datasetName.split('.')[0] + '.csv')
    return initialDataset

#Read Configuration file
#-----------------------
def get_ConfigFile(config_file_name = 'config.json'):
    self_dir = Path(__file__).resolve().parents[1]
    config_file_path = self_dir / config_file_name
    configFile = open(config_file_path)
    config_File = json.load(configFile)
    configFile.close()
    return config_File

#Get dataComponent dir path
#--------------------------
def get_Path(dataType,config_File):
    self_main_dir = Path(__file__).resolve().parents[1]
    if dataType == 'self_main_dir':
        path = self_main_dir
    elif dataType == 'InitialCombinedData':
        path = self_main_dir/config_File['FinalDS']['InitialCombinedData']
    elif dataType == 'PreprocessedData':
        path = self_main_dir/config_File['FinalDS']['PreprocessedData']
    elif dataType in ['NullColsToZero','NullColsToNegativeOne','HexaColsToInt','StringNumColsToInt','StringBoolColsToInt','CategoricalCols','UselesCols','IndexCol','ProtectedAttributes'] :
        path = config_File['DataToBeProcessed'][dataType]
    return path

#Generate a unique name for the preprocessed data csv file
#----------------------------------------------------------
def generate_UniqueFilename(FinalDatasetName):
    if FinalDatasetName == '':
        FinalDatasetName = 'PreprocessedData'
    UniqueFilename = FinalDatasetName + '_' + str(datetime.datetime.now().date()).replace('-', '') + '_' + str(datetime.datetime.now().time()).replace(':', '').split('.')[0]
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