import pandas as pd
from pathlib import Path
import os, json, datetime

def construct_FinalData(Dataset, AccountInfo,ContractsInfo,Opcodes,CodeMetrics,Labels):

    AccountInfoDF = ReadFeaturesData(Dataset,AccountInfo,dataType = 'AccountInfo')
    ContractsInfoDF = ReadFeaturesData(Dataset,ContractsInfo, dataType = 'ContractsInfo')
    OpcodesDF = ReadFeaturesData(Dataset,Opcodes, dataType = 'Opcodes')
    CodeMetricsDF = ReadFeaturesData(Dataset,CodeMetrics, dataType = 'CodeMetrics')
    LabelsDF = ReadFeaturesData(Dataset,Labels, dataType = 'Labels')

    DigVulSCDS =pd.DataFrame()
    DigVulSCDS = AccountInfoDF
    DigVulSCDS = AccountInfoDF.merge(ContractsInfoDF, on = 'contractAddress', how = 'inner')
    DigVulSCDS = DigVulSCDS.merge(OpcodesDF, on = 'contractAddress', how = 'inner')
    DigVulSCDS = DigVulSCDS.merge(CodeMetricsDF, on = 'contractAddress', how = 'inner')

    DigVulSCDS_withoutLebels = DigVulSCDS
    DigVulSCDS_withoutLebels.reset_index(inplace=True,drop=True)
    
    #Extract label columns from LabelsDF
    LabelCols = get_Path('LabelsCols')
    commonCols = ['contractAddress'] + list(set(LabelsDF.columns) & set(LabelCols))
    LabelsDF = LabelsDF[commonCols]
    
    DigVulSCDS = DigVulSCDS.merge(LabelsDF, on = 'contractAddress', how = 'inner')
    DigVulSCDS.reset_index(inplace=True,drop=True)

    finalDataName = generate_UniqueFilename(Labels)
    finalDataPath = str(get_Path('FinalLabeledData'))
    DigVulSCDS.to_csv(finalDataPath + '/' +finalDataName+'.csv',index=False)

    return DigVulSCDS

#Read Features/Labels data to a dataframe
#----------------------------------------
def ReadFeaturesData(Dataset,dataComponent,dataType):
    path = str(get_Path(dataType)) + '/'
    if dataComponent[0].lower() == 'all' or len(dataComponent) > 1:
        dataComponentDF = pd.DataFrame()
        for filename in os.listdir(path):
            if 'csv' in filename and (dataComponent[0].lower() == 'all' or filename in dataComponent) and (filename.split('_')[-1].split('.')[0] in Dataset or (len(Dataset) == 1 and Dataset[0].lower() =='all')):
                df = pd.read_csv(path + filename)
                if len(dataComponentDF) == 0:
                    dataComponentDF = df
                else:
                    dataComponentDF = pd.concat([dataComponentDF, df])
        dataComponentDF.drop_duplicates(keep='first',inplace=True)
        dataComponentDF.reset_index(inplace=True, drop=True)
    else:
        dataComponentDF = pd.read_csv(path + dataComponent[0]) 
    return dataComponentDF

#Get dataComponent dir path
#--------------------------
def get_Path(dataType):
    #Get the correct path to the configuration file
    config_file_name = 'config.json'
    self_dir = Path(__file__).resolve().parent
    config_file_path = self_dir / config_file_name

    #Get the correct path to the main directory
    self_main_dir = Path(__file__).resolve().parents[1]
    
    configFile = open(config_file_path)
    config_File = json.load(configFile)
    configFile.close()
    
    if dataType == 'Labels':
        path = self_main_dir/config_File['DataLabels'][dataType]
    elif dataType == 'FinalLabeledData':
        path = self_main_dir/config_File['DigVulSCDS']['OutDir']
    elif dataType == 'LabelsCols':
        path = config_File['DataLabels'][dataType]
    else:
        path = self_main_dir/config_File['Features'][dataType]
    
    return path

def generate_UniqueFilename(Labels):
    if Labels[0].lower() == 'all' or len(Labels) > 1:
        DataType = 'DigVulSCDS'
    else:
        DataType = Labels[0].split('.')[0]
    
    UniqueFilename = str(datetime.datetime.now().date()).replace('-', '') + '_' + str(datetime.datetime.now().time()).replace(':', '').split('.')[0] + '_' + DataType

    return UniqueFilename