import pandas as pd
import numpy as np
from pathlib import Path
import json, os,datetime
from IPython.display import display
from sklearn.preprocessing import LabelEncoder
import sys
sys.set_int_max_str_digits(0)

#Total number of preprocessing tasks currently offered
PreprocessingTasksNo = 13

def apply_DataPreprocessing(datasetName,dataDirPath='Default_InitialCombinedDataDir',PreprocessingTasks=['all']):
    try:
        config_File = get_ConfigFile()
        dataset = get_initialDataset(datasetName,dataDirPath,config_File)
        
        if len(PreprocessingTasks)== 1 and PreprocessingTasks[0].lower()== 'all':
            for taskID in range(1,PreprocessingTasksNo +1):
                dataset = call_PreprocessingTask(dataset,str(taskID),config_File)
        else:
            for taskID in PreprocessingTasks:
                dataset = call_PreprocessingTask(dataset,str(taskID),config_File)
        
        finalDataName = generate_UniqueFilename(datasetName)
        finalDataPath = str(get_Path('PreprocessedData',config_File))
        dataset.to_csv(finalDataPath + '/' + finalDataName+'.csv',index=False)

        print('Done! the Preprocessed Data is available in: ' + finalDataPath + '/' +finalDataName+'.csv')
        display(dataset)
        return True
    
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise

#Identify the preprocessing task to be performed
#-----------------------------------------------
def call_PreprocessingTask(dataset,taskID,config_File):
    match taskID:
        case '1' | 'DropDuplicateRows':
            return PreprocessingTask1_DropDuplicateRows(dataset)
        case '2' | 'FillMissingDataWithZero':
            dataToBeProcessed = get_Path('NullColsToZero',config_File)
            return PreprocessingTask2_FillMissingDataWithZero(dataset,dataToBeProcessed)
        case '3' | 'FillMissingDataWithNegativeOne':
            dataToBeProcessed = get_Path('NullColsToNegativeOne',config_File)
            return PreprocessingTask3_FillMissingDataWithNegativeOne(dataset,dataToBeProcessed)
        case '4' | 'ProcessBytecodes':
            return PreprocessingTask4_ProcessBytecodes(dataset)
        case '5' | 'ProcessABI':
            return PreprocessingTask5_ProcessABI(dataset)
        case '6' | 'ProcessConstructorArguments':
            return PreprocessingTask6_ProcessConstructorArguments(dataset)
        case '7' | 'ProcessOpcodes':
            return PreprocessingTask7_ProcessOpcodes(dataset)
        case '8' | 'RemoveUselesCols':
            dataToBeProcessed = get_Path('UselesCols',config_File)
            return PreprocessingTask8_RemoveUselesCols(dataset,dataToBeProcessed)
        case '9' | 'HandlingHexaData':
            dataToBeProcessed = get_Path('HexaColsToInt',config_File)
            return PreprocessingTask9_HandlingHexaData(dataset,dataToBeProcessed)
        case '10' | 'HandlingStringNumericalData':
            dataToBeProcessed = get_Path('StringNumColsToInt',config_File)
            return PreprocessingTask10_HandlingStringNumericalData(dataset,dataToBeProcessed)
        case '11' | 'HandlingStringBoolColsToInt':
            dataToBeProcessed = get_Path('StringBoolColsToInt',config_File)
            return PreprocessingTask11_HandlingStringBoolColsToInt(dataset,dataToBeProcessed)
        case '12' | 'HandlingCategoricalData':
            dataToBeProcessed = get_Path('CategoricalCols',config_File)
            return PreprocessingTask12_HandlingCategoricalData(dataset,dataToBeProcessed)
        case '13' | 'SetDataIndexColumn':
            dataToBeProcessed = get_Path('IndexCol',config_File)
            PreprocessingTask13_SetDataIndexColumn(dataset,dataToBeProcessed)
        # default pattern
        case _:
            print(taskID + ' is an incorrect Task ID')

#Perform the chosen preprocessed task
#------------------------------------
def PreprocessingTask1_DropDuplicateRows(dataset):
    dataset.drop_duplicates(keep='first',inplace=True)
    dataset.reset_index(drop=True,inplace=True)
    return dataset
def PreprocessingTask2_FillMissingDataWithZero(dataset,NullColsToZero):
    cols = list(set(dataset.columns) & set(NullColsToZero))
    dataset[cols] = dataset[cols].fillna(0)
    return dataset
def PreprocessingTask3_FillMissingDataWithNegativeOne(dataset,NullColsToNegativeOne):
    ## txreceipt_status values are 0 and 1, indicating failure and success, respectively.
    ## Blank means it is still waiting for confirmation
    cols = list(set(dataset.columns) & set(NullColsToNegativeOne))
    dataset[cols] = dataset[cols].fillna(-1)
    return dataset

def PreprocessingTask4_ProcessBytecodes(dataset):
    
    return dataset
def PreprocessingTask5_ProcessABI(dataset):

    return dataset
def PreprocessingTask6_ProcessConstructorArguments(dataset):
    min_ArgLength = 1  # 4bits
    max_ArgLength = 64 # 128bits
    dataset['ConstructorArguments'] = dataset['ConstructorArguments'].str.findall(fr'\d{{{min_ArgLength},{max_ArgLength}}}').apply(lambda x: list(map(int, x)) if isinstance(x, list) else [])
    return dataset
def PreprocessingTask7_ProcessOpcodes(dataset):
    #Convert Opcodes values into a list
    dataset['Opcodes'] = dataset['Opcodes'].str.split('<br>')
    return dataset
def PreprocessingTask8_RemoveUselesCols(dataset,UselesCols):
    cols = list(set(dataset.columns) & set(UselesCols))
    dataset.drop(columns=cols,axis=1,inplace=True)
    return dataset
def PreprocessingTask9_HandlingHexaData(dataset,HexaColsToInt):
    cols = list(set(dataset.columns) & set(HexaColsToInt))
    ## convert hexa columns into integer
    for col in cols:
        dataset[col]=dataset[col].astype(str).apply(int, base=16)
    return dataset
def PreprocessingTask10_HandlingStringNumericalData(dataset,StringNumColsToInt):
    cols = list(set(dataset.columns) & set(StringNumColsToInt))
    dataset[cols]=dataset[cols].apply(pd.to_numeric)
    return dataset
def PreprocessingTask11_HandlingStringBoolColsToInt(dataset,StringBoolColsToInt):
    dataset = dataset.replace({'Yes':1,'No':0})
    '''cols = list(set(dataset.columns) & set(StringBoolColsToInt))  ## ToBeRemoved if "StringBoolColsToInt":["Experimental Features"] handled with the previous code line. Update config file and the call statement
    for col in cols:
        dataset[col] = np.where(dataset[col] != 0, 1, 0)'''
    return dataset
def PreprocessingTask12_HandlingCategoricalData(dataset,CategoricalCols):
    cols = list(set(dataset.columns) & set(CategoricalCols)) ##  a special handling function might be added for Opcodes
    for col in cols:
        le= LabelEncoder()
        le.fit(dataset[col].unique().tolist())
        dataset[col]= le.transform(dataset[col])
    return dataset
def PreprocessingTask13_SetDataIndexColumn(dataset,IndexCol):
    dataset.set_index(IndexCol,drop=True,inplace=True)
    return dataset
#Get data to be preprocessed
#---------------------------
def get_initialDataset(datasetName,dataDirPath,config_File):
    if dataDirPath == 'Default_InitialCombinedDataDir':
        path = get_Path('InitialCombinedData',config_File)
    else:
        self_main_dir = get_Path('self_main_dir',config_File)
        path = os.path.join(self_main_dir,dataDirPath)

    initialDataset = pd.read_csv(str(path) + '/' + datasetName.split('.')[0] + '.csv')
    return initialDataset

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

#Generate a unique name for the preprocessed data csv file
#----------------------------------------------------------
def generate_UniqueFilename(FinalDatasetName):
    if FinalDatasetName == '':
        FinalDatasetName = 'PreprocessedData'
    UniqueFilename = FinalDatasetName + '_' + str(datetime.datetime.now().date()).replace('-', '') + '_' + str(datetime.datetime.now().time()).replace(':', '').split('.')[0]
    return UniqueFilename