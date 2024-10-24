import pandas as pd
from pathlib import Path
import json, os
from sklearn.preprocessing import LabelEncoder

PreprocessingTasksNo = 10

def preprocessing(dataset,PreprocessingTasks):
    try:
        config_File = get_ConfigFile()
        
        if len(PreprocessingTasks)== 1 and PreprocessingTasks[0].lower()== 'all':
            for taskID in range(1,PreprocessingTasksNo +1):
                dataset = call_PreprocessingTask(dataset,str(taskID),config_File)
        else:
            for taskID in PreprocessingTasks:
                dataset = call_PreprocessingTask(dataset,str(taskID),config_File)
        return dataset
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise

#Identify the preprocessing task to be performed
#-----------------------------------------------
def call_PreprocessingTask(dataset,taskID,config_File):
    match taskID:
        case '1' | 'DropDuplicateRows':
            return PreprocessingTask1_DropDuplicateRows(dataset)
        case '2' | 'RemoveUselesCols':
            dataToBeProcessed = get_Path('UselesCols',config_File)
            return PreprocessingTask2_RemoveUselesCols(dataset,dataToBeProcessed)
        case '3' | 'FillMissingDataWithNegativeOne':
            dataToBeProcessed = get_Path('NullColsToNegativeOne',config_File)
            return PreprocessingTask3_FillMissingDataWithNegativeOne(dataset,dataToBeProcessed)
        case '4' | 'FillMissingDataWithZero':
            dataToBeProcessed = get_Path('NullColsToZero',config_File)
            return PreprocessingTask4_FillMissingDataWithZero(dataset,dataToBeProcessed)
        case '5' | 'ProcessConstructorArguments':
            return PreprocessingTask5_ProcessConstructorArguments(dataset)
        case '6' | 'HandlingHexaData':
            dataToBeProcessed = get_Path('HexaColsToInt',config_File)
            return PreprocessingTask6_HandlingHexaData(dataset,dataToBeProcessed)
        case '7' | 'HandlingStringNumericalData':
            dataToBeProcessed = get_Path('StringNumColsToInt',config_File)
            return PreprocessingTask7_HandlingStringNumericalData(dataset,dataToBeProcessed)
        case '8' | 'HandlingStringBoolColsToInt':
            dataToBeProcessed = get_Path('StringBoolColsToInt',config_File)
            return PreprocessingTask8_HandlingStringBoolColsToInt(dataset,dataToBeProcessed)
        case '9' | 'HandlingCategoricalData':
            dataToBeProcessed = get_Path('CategoricalCols',config_File)
            return PreprocessingTask9_HandlingCategoricalData(dataset,dataToBeProcessed)
        case '10' | 'SetDataIndexColumn':
            dataToBeProcessed = get_Path('IndexCol',config_File)
            return PreprocessingTask10_SetDataIndexColumn(dataset,dataToBeProcessed)
        # default pattern
        case _:
            print(taskID + ' is an incorrect Task ID')

#Perform the chosen preprocessed task
#------------------------------------
def PreprocessingTask1_DropDuplicateRows(dataset):
    dataset.drop_duplicates(keep='first',inplace=True)
    dataset.reset_index(drop=True,inplace=True)
    return dataset
def PreprocessingTask2_RemoveUselesCols(dataset,UselesCols):
    cols = list(set(dataset.columns) & set(UselesCols))
    dataset.drop(columns=cols,axis=1,inplace=True)
    return dataset
def PreprocessingTask3_FillMissingDataWithNegativeOne(dataset,NullColsToNegativeOne):
    ## txreceipt_status values are 0 and 1, indicating failure and success, respectively.
    ## Blank means it is still waiting for confirmation
    cols = list(set(dataset.columns) & set(NullColsToNegativeOne))
    if len(cols) > 0:
        dataset[cols] = dataset[cols].fillna(-1)
    return dataset
def PreprocessingTask4_FillMissingDataWithZero(dataset,NullColsToZero):
    '''cols = list(set(dataset.columns) & set(NullColsToZero))
    dataset[cols] = dataset[cols].fillna(0)'''
    dataset.fillna(0, inplace=True)
    return dataset
def PreprocessingTask5_ProcessConstructorArguments(dataset):
    if 'ConstructorArguments' in dataset.columns:
        max_ArgLength = 64 # 128bits
        dataset['ConstructorArguments'] =  dataset['ConstructorArguments'].str.extractall(f'(.{{1,{max_ArgLength}}})')[0].groupby(level=0).agg(list)
    return dataset
def PreprocessingTask6_HandlingHexaData(dataset,HexaColsToInt):
    cols = list(set(dataset.columns) & set(HexaColsToInt))
    if len(cols) > 0:
        ## convert hexa columns into integer
        for col in cols:
            if col in ['ConstructorArguments']:
                dataset[col] = dataset[col].apply(lambda x: list(map(lambda hex_val: int(hex_val, 16), x)) if isinstance(x, list) and x else []) #verify that it is a string (Hex) and not an empty list
            else:
                dataset[col]=dataset[col].astype(str).apply(int, base=16)
    return dataset
def PreprocessingTask7_HandlingStringNumericalData(dataset,StringNumColsToInt):
    cols = list(set(dataset.columns) & set(StringNumColsToInt))
    if len(cols) > 0:
        dataset[cols]=dataset[cols].apply(pd.to_numeric)
    return dataset
def PreprocessingTask8_HandlingStringBoolColsToInt(dataset,StringBoolColsToInt):
    dataset = dataset.replace({'Yes':1,'No':0})
    dataset = dataset.infer_objects(copy=False)
    '''cols = list(set(dataset.columns) & set(StringBoolColsToInt))  ## ToBeRemoved if "StringBoolColsToInt":["Experimental Features"] handled with the previous code line. Update config file and the call statement
    for col in cols:
        dataset[col] = np.where(dataset[col] != 0, 1, 0)'''
    return dataset
def PreprocessingTask9_HandlingCategoricalData(dataset,CategoricalCols):
    cols = list(set(dataset.columns) & set(CategoricalCols)) ##  a special handling function might be added for Opcodes
    if len(cols) > 0:
        for col in cols:
            le= LabelEncoder()
            le.fit(dataset[col].unique().tolist())
            dataset[col]= le.transform(dataset[col])
    return dataset
def PreprocessingTask10_SetDataIndexColumn(dataset,IndexCol):
    dataset.set_index(IndexCol,drop=True,inplace=True)
    return dataset

#Read Configuration file
#-----------------------
def get_ConfigFile(config_file_name = 'config.json'):
    self_dir = Path(__file__).resolve().parent
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
    elif dataType in ['NullColsToZero','NullColsToNegativeOne','HexaColsToInt','StringNumColsToInt','StringBoolColsToInt','CategoricalCols','UselesCols','IndexCol'] :
        path = config_File['DataToBeProcessed'][dataType]
    return path