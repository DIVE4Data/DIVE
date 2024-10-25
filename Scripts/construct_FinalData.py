import pandas as pd
from pathlib import Path
import os, json, datetime
from IPython.display import display
from functools import reduce
from Scripts.preprocessing import preprocessing
#---------------------------------------
#Get the correct path to the configuration file
config_file_name = 'config.json'
self_dir = Path(__file__).resolve().parent
config_file_path = self_dir / config_file_name

#Get the correct path to the main directory
self_main_dir = Path(__file__).resolve().parents[1]

configFile = open(config_file_path)
config_File = json.load(configFile)
configFile.close()
#---------------------------------------
def construct_FinalData(FinalDatasetName = '', Dataset =[],FeatureTypes = {}, Preprocessing =False): #, AccountInfo=[],ContractsInfo=[],Opcodes=[],CodeMetrics=[],Labels=[]):
    try:
        #read data and unify rowID column name
        FinalData =pd.DataFrame()

        for key in FeatureTypes:
            part = pd.DataFrame(ReadFeaturesData(Dataset,FeatureTypes[key],dataType = key,Preprocessing = Preprocessing))
            if len(FinalData) == 0:
                FinalData = part
            else:
                FinalData = FinalData.join(part)

        finalDataName = generate_UniqueFilename(FinalDatasetName)
        if preprocessing:
            finalDataPath = str(get_Path('PreprocessedData'))
        else:
            finalDataPath = str(get_Path('FinalLabeledData'))
        FinalData.to_csv(finalDataPath + '/' +finalDataName+'.csv',index=False)

        print('Done! the Combined Data is available in: ' + str(os.path.relpath(str(finalDataPath) + '/' +finalDataName+'.csv', Path.cwd().parent)))
        display(FinalData)
        return True
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise

#Get dataset features (columns) using filtering data
#---------------------------------------------------
def get_DatasetFeatures(FeatureTypes):
    #get features dic
    features = pd.read_excel(get_Path('Feature List File'),sheet_name='Features')
    #featuresDic = features.to_dict('records')
    #featuresDic = {item['Feature']:item for item in featuresDic}

    #convert keys and values of FeatureTypes dic to small letter
    FeatureTypes = dict((key.lower(), [value.lower() for value in values]) for key, values in FeatureTypes.items())
    #FeatureTypes = dict((key.casefold(), [value.casefold() for value in values]) for key, values in FeatureTypes.items())

    if len(FeatureTypes) == 1 and FeatureTypes == 'all' and FeatureTypes.values() == ['all']:
        datasetFeatures.append('all')
    else:
        #This steps to collect the correct names of feature list columns.
        filterKeys = features.columns.str.lower().tolist()
        filters = {}
        for key in FeatureTypes:
            if key in filterKeys:
                keyIndex = filterKeys.index(key)
                filterName = features.columns[keyIndex]

                #Convert the filter list to casefolded format
                filterValues = pd.Series(FeatureTypes[key]).str.casefold()
                # Filter rows where 'Name' matches any name in names_to_filter (ignoring case)
                filters[filterName] = features[features[filterName].str.casefold().isin(filterValues)][filterName].tolist()
        #This step to get feature cols
        mask = pd.Series(True, index=features.index) #Initialize a mask of True values
        #Apply filters using bitwise AND
        for key, values in filters.items():
            mask &= features[key].isin(values)
        #get filtered features
        datasetFeatures = features.loc[mask, 'Feature'].tolist()      
    return datasetFeatures

#Read Features/Labels data to a dataframe
#----------------------------------------
def ReadFeaturesData(Dataset,dataComponent,dataType,Preprocessing):
    path = str(get_Path(dataType)) + '/'
    if dataComponent[0].lower() == 'all' or len(dataComponent) > 1:
        dataComponentDF = pd.DataFrame()
        for filename in os.listdir(path):
            #if 'csv' in filename and (dataComponent[0].lower() == 'all' or filename in dataComponent) and (filename.split('_')[-1].split('.')[0] in Dataset or (len(Dataset) == 1 and Dataset[0].lower() =='all')):
            if '.csv' in filename and (filename in dataComponent or (dataComponent[0].lower() == 'all' and (filename.split('.')[0].split('_')[0] in Dataset or (len(Dataset) == 1 and Dataset[0].lower() =='all')))):
                df = pd.read_csv(path + filename,low_memory=False)
                if len(dataComponentDF) == 0:
                    dataComponentDF = df
                else:
                    dataComponentDF = pd.concat([dataComponentDF, df])
        dataComponentDF.drop_duplicates(keep='first',inplace=True)
        dataComponentDF.reset_index(inplace=True, drop=True)
    else:
        dataComponentDF = pd.read_csv(path + dataComponent[0],low_memory=False)
    if Preprocessing:
        dataComponentDF = preprocessing(dataComponentDF,['All'])
    return dataComponentDF

#Get dataComponent dir path
#--------------------------
def get_Path(dataType):
    if dataType == 'Labels':
        path = self_main_dir/config_File['DataLabels'][dataType]
    elif dataType == 'FinalLabeledData':
        path = self_main_dir/config_File['FinalDS']['InitialCombinedData']
    elif dataType == 'PreprocessedData':
        path = self_main_dir/config_File['FinalDS']['PreprocessedData']
    elif dataType == 'LabelsCols':
        path = config_File['DataLabels'][dataType]
    else:
        if dataType in ['AccountInfo','ContractsInfo','Opcodes']:
            path = self_main_dir/config_File['Features']['API-based'][dataType]
        elif dataType in ['ABI-based','CodeMetrics','Input-based','Opcode-based']:
            path = self_main_dir/config_File['Features']['FE-based'][dataType]
        else:
            path = self_main_dir/config_File['Features'][dataType]
    return path

def get_RowIDCol(df):
    #Get the RowID column possible names
    #-----------------------------------
    RowIDColNames = config_File['DataLabels']['RowID']
    for column in df.columns:
        if column.lower() in RowIDColNames:
            df.rename(columns = {column:'contractAddress'}, inplace = True)
            return df
        
def generate_UniqueFilename(FinalDatasetName):
    if FinalDatasetName == '':
        FinalDatasetName = 'InitialCombinedData'
    UniqueFilename = FinalDatasetName + '_' + str(datetime.datetime.now().date()).replace('-', '') + '_' + str(datetime.datetime.now().time()).replace(':', '').split('.')[0]

    return UniqueFilename