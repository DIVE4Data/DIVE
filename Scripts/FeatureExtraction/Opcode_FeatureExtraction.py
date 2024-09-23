import pandas as pd
from collections import Counter
from IPython.display import display
from pathlib import Path
import os, json, datetime
from sklearn.feature_extraction.text import CountVectorizer

TotalMethods = 2 
def Opcode_FeatureExtraction(DatasetName,dataset, methods):
    try:
        if 'Opcodes' in dataset.columns:
            #Get configurations data
            config_File = get_ConfigFile()
            #---------------------------------------
            #Ensure the rowID column is named 'contractAddress'
            dataset = get_RowIDCol(dataset,config_File)
            Opcode_basedFeatures = dataset[['contractAddress', 'Opcodes']]

            if len(methods)== 1 and methods[0].lower()== 'all':
                for methodID in range(1,TotalMethods +1):
                    Opcode_basedFeatures = call_FeatureExtractionMethod(config_File,Opcode_basedFeatures,str(methodID))
            else:
                for methodID in methods:
                    Opcode_basedFeatures = call_FeatureExtractionMethod(config_File,Opcode_basedFeatures,str(methodID))
            
            UniqueFilename = generate_UniqueFilename(DatasetName,'Opcode-based')
            self_main_dir = Path(__file__).resolve().parents[2]
            path = self_main_dir/config_File['Features']['FE-based']['Opcode-based']
            Opcode_basedFeatures.to_csv(str(path) + '/' + UniqueFilename + '.csv',index=False)

            print('Done! the Opcode-based Data is available in: ' + str(path) + '/' + UniqueFilename + '.csv')
            display(Opcode_basedFeatures)
            return True
        else:
            return 'Opcodes  attribute is not present in the given dataset'
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
    raise
#=============================================================================================================    
def call_FeatureExtractionMethod(config_File,dataset,methodID):
    match methodID:
        case '1' | 'StatisticalFeatures':
            return FE_Method_1_StatisticalFeatures(config_File,dataset)
        case '2' | '':
            return FE_Method_2_(dataset)
        # default pattern
        case _:
            print(methodID + ' is an incorrect Method ID')
#=============================================================================================================
#Method #1 Tokenization, Opcode Statistical, Distributional Features
#-------------------------------------------------------------------
def FE_Method_1_StatisticalFeatures(config_File,dataset):
    #opcodes = dataset['Opcodes'].str.split('<br>').apply(lambda x: pd.Series(x).str.split().str[0].tolist())
    opcodes = dataset['Opcodes'].str.split('<br>').apply(lambda x: pd.Series(x).str.split().str[0].replace(to_replace='.*Unknown.*', value='Unknown', regex=True).tolist())

    opcodeCategories = get_OpcodeCategories(config_File)

    StatisticsF = {
            'opcodeLength': [len(opcode) for opcode in dataset['Opcodes']],
            'noOfOpcodes': [len(opcode) for opcode in opcodes], 
            'noOfUniqueOpcodes': [len(set(opcode)) for opcode in opcodes],
            'mostFrequentOpcode': [Counter(opcode).most_common(1)[0][0] if opcode else None for opcode in opcodes],
            'uniqueOpcodesRatio': [(len(set(opcode)) / len(opcode) * 100) if (len(opcode)) > 0 else 0 for opcode in opcodes]
        }
    opcodesDistributionsDF = pd.DataFrame(opcodes.apply(lambda opcode: {f'{op}_Distribution': count / len(opcode) for op, count in Counter(opcode).items()}).tolist())

    #Create categories Dic to store the total opcode for each category per instance
    categoryCount = {category: [] for category in set(opcodeCategories.values())}
    #Count occurrences of opcode categories
    for opcode in opcodes:
        counts = Counter(opcode)
        for category in categoryCount.keys():
            categoryOpcodes = list(filter(lambda op: opcodeCategories[op] == category, opcodeCategories))
            categoryCount[category].append(sum(counts[op] for op in categoryOpcodes))

        for category, counts in categoryCount.items():
            StatisticsF[f'{category} count'] = counts

    StatisticsDF = pd.DataFrame(StatisticsF)

    updatedDataset = pd.concat([dataset, StatisticsDF,opcodesDistributionsDF], axis=1)
    return updatedDataset
#=============================================================================================================
#Method #2
#--------------------------
def FE_Method_2_(dataset):
    opcodes = dataset['Opcodes'].str.split('<br>').apply(lambda x: pd.Series(x).str.split().str[0].replace(to_replace='.*Unknown.*', value='Unknown', regex=True).tolist())

    # Function to extract features using CountVectorizer
    vectorizer = CountVectorizer(tokenizer=lambda x: x.split(','), lowercase=False)
    features = vectorizer.fit_transform(opcodes)
    
    return features, vectorizer.get_feature_names_out()

    # Extract features
    features, feature_names = extract_features(opcode_list)

    # Convert to DataFrame for better readability
    features_df = pd.DataFrame(features.toarray(), columns=feature_names)

#=============================================================================================================
#Read EVM Opcodes csv file
#--------------------------
def get_OpcodeCategories(config_File):
    OpcodesFolder = get_Path('EVM_OpcodesDir',config_File)
    #get recent Opcodes csv files
    files = [file.name for file in os.scandir(OpcodesFolder) if file.is_file() and file.name.endswith('.csv')]
    recent_OpcodeFile = max(files, key=lambda x: os.path.getmtime(os.path.join(OpcodesFolder, x)))
    recent_OpcodesData = pd.read_csv(os.path.join(OpcodesFolder, recent_OpcodeFile))
    #drop rows with Null category
    recent_OpcodesData = recent_OpcodesData.dropna(subset=['Category'])
    #create OpcodeCategories Dic
    OpcodeCategories = pd.Series(recent_OpcodesData.Category.values, index=recent_OpcodesData.Name).to_dict()
    return OpcodeCategories
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
    self_main_dir = Path(__file__).resolve().parents[1] #main Dir
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