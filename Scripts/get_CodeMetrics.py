import datetime, os, json
import pandas as pd
import numpy as np
from mrkdwn_analysis import MarkdownAnalyzer
from pathlib import Path
from IPython.display import display


def get_CodeMetrics(DatasetName,SamplesDir):
    if SamplesDir == '' or SamplesDir.lower() == 'default':
        SamplesDir = './' + str(get_Path('Samples',DatasetName)) + '/' + DatasetName + '/'
    else:
        SamplesDir = './' + str(SamplesDir) + '/' 
    
    OriginalDestinationPath = str(get_Path('OriginalReports',DatasetName)) + '/'
    EditedDestinationPath = str(get_Path('EditedReports',DatasetName)) + '/'
    Raw_CodeMetrics_OutDir = str(get_Path('Raw_CodeMetrics',DatasetName)) + '/'
    CodeMetrics_OutDir  = str(get_Path('CodeMetrics',DatasetName)) + '/'

    generate_MetricsReports(SamplesDir,OriginalDestinationPath)
    prepare_GeneratedMetricsReports(OriginalDestinationPath,EditedDestinationPath)
    
    metricsDF = parse_MetricsReports(ReportsFolder = EditedDestinationPath)
    UniqueFilename = generate_UniqueFilename(DatasetName,'Raw_CodeMetrics')
    metricsDF.to_csv(Raw_CodeMetrics_OutDir + UniqueFilename + '.csv',index=False)

    preProcessed_metricsDF = preprocesse_MetricsData(metricsDF)
    UniqueFilename = generate_UniqueFilename(DatasetName,'CodeMetrics')
    preProcessed_metricsDF.to_csv(CodeMetrics_OutDir + UniqueFilename + '.csv' ,index=False)
    
    #display(preProcessed_metricsDF)
    return 

#Get dataComponent dir path
#--------------------------
def get_Path(dataType,DatasetName):
    #Get the correct path to the configuration file
    config_file_name = 'config.json'
    self_dir = Path(__file__).resolve().parent
    config_file_path = self_dir / config_file_name

    #Get the correct path to the main directory
    self_main_dir = Path(__file__).resolve().parents[1]
    
    configFile = open(config_file_path)
    config_File = json.load(configFile)
    configFile.close()
    
    if 'Reports' in dataType or 'Raw' in dataType:
        #path = self_main_dir/config_File['solidity-code-metrics']['Reports'][dataType]
        path = './Features/CodeMetrics/Reports/' + dataType
        if 'Reports' in dataType:
            outDir = os.path.join(path, DatasetName)
            os.mkdir(outDir)
            path = str(path) + '/' + DatasetName
    elif dataType == 'Samples':
        path = config_File['RawData'][dataType]
    else:
        path = self_main_dir/config_File['Features'][dataType]
    
    return path

#Generate Metrics Reports
#------------------------
def generate_MetricsReports(SamplesDir,OriginalDestinationPath):
    for file in os.scandir(SamplesDir):
        filePath = ''
        if file.is_file() and '.sol' in file.name:
            try:
                filePath = SamplesDir + file.name
                #Save the output to a Markdown file
                OutPath = OriginalDestinationPath + file.name.split('.')[0] + '.md'
                os.system('solidity-code-metrics ' + filePath + '>' + OutPath)
                
                #Save the output to a HTML file
                '''OutPath = OriginalDestinationPath + file.name.split('.')[0] + '.html'
                os.system('solidity-code-metrics ' + filePath + ' --html > ' + OutPath)'''
            except Exception as err:
                print(f"Unexpected {err=}, {type(err)=}")
                raise
#Prepare generated Metrics reports (Apply strip() to file contents)
#------------------------------------------------------------------
def prepare_GeneratedMetricsReports(OriginalDestinationPath,EditedDestinationPath):
    for filename in os.listdir(OriginalDestinationPath):
        filePath = ''
        filePath1 = ''
        if '.md' in filename:
            filePath = OriginalDestinationPath + filename

            file =open(filePath,'r')
            markdown = file.readlines()
            stripped_markdown = list(map(str.strip, markdown))
            file.close()

            filePath1 = EditedDestinationPath + filename
            
            updatedFile = open(filePath1,'w')
            updatedFile.write('\n'.join(stripped_markdown))
            updatedFile.close()
#Parse MD Metrics Reports
#------------------------
def parse_MetricsReports(ReportsFolder):
    metricsDF = createMetricsDF()
    counter = 0

    for file in os.scandir(ReportsFolder):
        filePath = ''
        codeMetrics = []
        GeneralMetrics = []
        Components = []
        ExposedFunctions = []
        StateVariables = []
        Capabilities = []
        
        if file.is_file() and '.md' in file.name:
            contractAddress = file.name.split('.')[0]
            codeMetrics.append(contractAddress)
            try:
                filePath = ReportsFolder + file.name
                analyzer = MarkdownAnalyzer(filePath)

                tables = analyzer.identify_tables()

                for index in range(0,len(tables['Table'])):
                    #1. GeneralMetrics
                    #--------------
                    if 'nSLOC' in  list(map(str.strip, tables['Table'][index])):
                        GeneralMetrics = list(map(str.strip, tables['Table'][index+2][3:-2]))

                    #2. Components
                    #----------
                    elif '🎨Abstract' in list(map(str.strip, tables['Table'][index])):
                        Components = list(map(str.strip, tables['Table'][index+2][1:-1]))

                    #3. ExposedFunctions
                    #----------------
                    elif '🌐Public' in list(map(str.strip, tables['Table'][index])) and '💰Payable' in list(map(str.strip, tables['Table'][index])):
                        ExposedFunctions = list(map(str.strip, tables['Table'][index+2][1:-1])) 
                    elif 'View' in list(map(str.strip, tables['Table'][index])):
                        ExposedFunctions = ExposedFunctions + list(map(str.strip, tables['Table'][index+2][1:-1]))

                    #4. StateVariables
                    #--------------
                    elif 'Total' in list(map(str.strip, tables['Table'][index])):
                        StateVariables = list(map(str.strip, tables['Table'][index+2][1:-1]))

                    #5. Capabilities
                    #------------
                    elif 'Solidity Versions observed' in list(map(str.strip, tables['Table'][index])):
                        Capabilities = list(map(str.strip, tables['Table'][index+2][2:-1]))
                    elif '🌀 New/Create/Create2' in list(map(str.strip, tables['Table'][index])):
                        Capabilities = Capabilities + list(map(str.strip, tables['Table'][index+2][1:-1]))
                    elif 'Σ Unchecked' in list(map(str.strip, tables['Table'][index])):
                        Capabilities = Capabilities + list(map(str.strip, tables['Table'][index+2][1:-1]))

                codeMetrics = codeMetrics + GeneralMetrics + Components + ExposedFunctions + StateVariables + Capabilities

                if len(metricsDF) == 0:
                    metricsDF.loc[0] = codeMetrics
                else:
                    metricsDF.loc[len(metricsDF)] = codeMetrics
                counter += 1
                print(str(counter) + '] ' + contractAddress + ': Done')
            except Exception as err:
                print(f"Unexpected {err=}, {type(err)=}")
                raise
    return metricsDF

#Create Metrics dataframe
#------------------------
def createMetricsDF():
    metrics = ['Logic Contracts', 'Interfaces', 'Lines', 'nLines', 'nSLOC', 'Comment Lines', 'Complex. Score',
            'Contracts', 'Libraries', 'Interfaces', 'Abstract',
            'Public Functions','Payable Functions','External Functions','Internal Functions','Private Functions','Pure Functions','View Functions',
            'StateVariablesTotal','PublicStateVariables',
            'Experimental Features','Can Receive Funds','Uses Assembly','Has Destroyable Contracts','Transfers ETH', 'Low-Level Calls', 'DelegateCall', 'Uses Hash Functions', 'ECRecover', 'New/Create/Create2','TryCatch','Unchecked']
    metricsDF = pd.DataFrame(columns= ['contractAddress'] + metrics)
    return metricsDF

#Preprocess Metrics Data
#------------------------
def preprocesse_MetricsData(metricsDF):
    
    #Drop duplicate columns
    metricsDF = metricsDF.loc[:,~metricsDF.columns.duplicated()].copy()
    #Drop empty rows
    metricsDF.drop(metricsDF[metricsDF['Lines'] == '**undefined**'].index,inplace=True)

    booleenColumns = ['Can Receive Funds','Uses Assembly','Has Destroyable Contracts','Transfers ETH', 
                        'Low-Level Calls', 'DelegateCall', 'Uses Hash Functions', 'ECRecover', 
                        'New/Create/Create2','TryCatch','Unchecked']
    numericalColumns = list(set(metricsDF.columns) - set(booleenColumns) - set(['contractAddress','Experimental Features']))

    metricsDF[booleenColumns] = metricsDF[booleenColumns].astype(str).replace({'****':'No','`yes`':'Yes'})
    for column in booleenColumns:
        metricsDF[column] = np.where(metricsDF[column].str.contains('`yes`'),'Yes',metricsDF[column])

    metricsDF[numericalColumns] = metricsDF[numericalColumns].astype(str).replace('****', 0)
    metricsDF['Experimental Features'] = metricsDF['Experimental Features'].astype(str).replace('`ABIEncoderV2`','ABIEncoderV2')
    metricsDF = metricsDF.replace(np.nan, None)
    
    return metricsDF

def generate_UniqueFilename(DatasetName,dataType):
    UniqueFilename = str(datetime.datetime.now().date()).replace('-', '') + '_' + str(datetime.datetime.now().time()).replace(':', '').split('.')[0] + '_' + dataType + '_' + DatasetName
    return UniqueFilename