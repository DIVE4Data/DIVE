import pandas as pd
from collections import Counter
from IPython.display import display
from pathlib import Path
import os, json
from sklearn.feature_extraction.text import CountVectorizer

TotalMethods = 2 
def Opcode_FeatureExtraction(DatasetName,dataset, methods):
    try:
        #config_File = get_ConfigFile()
        #dataset = get_initialDataset(datasetName,dataDirPath,config_File)
        
        if len(methods)== 1 and methods[0].lower()== 'all':
            for methodID in range(1,TotalMethods +1):
                dataset = call_FeatureExtractionMethod(dataset,str(methodID))
        else:
            for methodID in methods:
                dataset = call_FeatureExtractionMethod(dataset,str(methodID))
        
        #finalDataName = generate_UniqueFilename(datasetName)
        #finalDataPath = str(get_Path('PreprocessedData',config_File))
        #dataset.to_csv(finalDataPath + '/' + finalDataName+'.csv',index=False)

        #print('Done! the Preprocessed Data is available in: ' + finalDataPath + '/' +finalDataName+'.csv')
        display(dataset)
        return True
    
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
    raise
#=============================================================================================================    
def call_FeatureExtractionMethod(dataset,methodID):
    match methodID:
        case '1' | '':
            return FE_Method_1_StatisticalFeatures(dataset)
        case '2' | '':
            return FE_Method_2_(dataset)
        # default pattern
        case _:
            print(methodID + ' is an incorrect Method ID')
#=============================================================================================================
#Method #1 Tokenization, Opcode Statistical, Distributional Features
#-------------------------------------------------------------------
def FE_Method_1_StatisticalFeatures(dataset):
    #opcodes = dataset['Opcodes'].str.split('<br>').apply(lambda x: pd.Series(x).str.split().str[0].tolist())
    opcodes = dataset['Opcodes'].str.split('<br>').apply(lambda x: pd.Series(x).str.split().str[0].replace(to_replace='.*Unknown.*', value='Unknown', regex=True).tolist())

    opcodeCategories = get_OpcodeCategories()

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
def get_OpcodeCategories():
    config_File = get_ConfigFile()
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
    self_dir = Path(__file__).resolve().parent #current Dir
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