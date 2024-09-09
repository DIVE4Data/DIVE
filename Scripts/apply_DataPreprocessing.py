import pandas as pd
from pathlib import Path
import json, os,datetime
from IPython.display import display

#Total number of preprocessing tasks currently offered
PreprocessingTasksNo = 5

def apply_DataPreprocessing(datasetName,dataDirPath='Default_InitialCombinedDataDir',PreprocessingTasks=['all']):
    try:
        config_File = get_ConfigFile()
        dataset = get_initialDataset(datasetName,dataDirPath,config_File)
        
        if len(PreprocessingTasks)== 1 and PreprocessingTasks[0].lower == 'all':
            for taskID in range(1,PreprocessingTasksNo +1):
                dataset = call_PreprocessingTask(dataset,str(taskID))
        else:
            for taskID in PreprocessingTasks:
                dataset = call_PreprocessingTask(dataset,str(taskID))
        
        finalDataName = generate_UniqueFilename(datasetName)
        finalDataPath = str(get_Path('PreprocessedData',config_File))
        dataset.to_csv(finalDataPath + '/' +finalDataName+'.csv',index=False)

        print('Done! the Preprocessed Data is available in: ' + finalDataPath + '/' +finalDataName+'.csv')
        display(dataset)
        return True
    
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise

#Identify the preprocessing task to be performed
#-----------------------------------------------
def call_PreprocessingTask(dataset,taskID):
    match taskID:
        case '1':
            return PreprocessingTask1(dataset)
        case '2':
            return PreprocessingTask1(dataset)
        case '3':
            return PreprocessingTask1(dataset)

#Perform the chosen preprocessed task
#------------------------------------
def PreprocessingTask1(dataset):
    return dataset
def PreprocessingTask2(dataset):
    return dataset

#Get data to be preprocessed
#---------------------------
def get_initialDataset(datasetName,dataDirPath,config_File):
    if dataDirPath == 'Default_InitialCombinedDataDir':
        path = get_Path('InitialCombinedData',config_File)
    else:
        self_main_dir = get_Path('self_main_dir',config_File)
        path = os.path.join(self_main_dir,dataDirPath)

    initialDataset = pd.read_csv(path + datasetName.split('.')[0] + '.csv')
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
    return path

#Generate a unique name for the preprocessed data csv file
#----------------------------------------------------------
def generate_UniqueFilename(FinalDatasetName):
    if FinalDatasetName == '':
        FinalDatasetName = 'PreprocessedData'
    UniqueFilename = FinalDatasetName + '_' + str(datetime.datetime.now().date()).replace('-', '') + '_' + str(datetime.datetime.now().time()).replace(':', '').split('.')[0]
    return UniqueFilename