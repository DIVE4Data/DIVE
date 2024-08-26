from pathlib import Path
import json

def extract_SourceCodes(ContractsInfo, UniqueFilename):
    #Get the correct path to the configuration file
    #-------------------------------------------
    config_file_name = 'config.json'
    self_dir = Path(__file__).resolve().parent
    config_file_path = self_dir / config_file_name
    #-------------------------------------------
    #Get the correct path to the main directory
    #-------------------------------------------
    self_main_dir = Path(__file__).resolve().parents[1]
    #-------------------------------------------
    configFile = open(config_file_path)
    config_File = json.load(configFile)
    configFile.close()

    outDir = self_main_dir/config_File['RawData']['Samples']
    write_SourceCodesToSolfiles(ContractsInfo,outDir)
    outDir = self_main_dir/config_File['RawData']['SamplesSummary']
    get_SamplesSummary(ContractsInfo,outDir,UniqueFilename)

    ContractsInfo.drop(columns=['SourceCode'],axis=1,inplace=True)

    return ContractsInfo

def write_SourceCodesToSolfiles(ContractsInfo,outDir):
    for index, row in ContractsInfo.iterrows():
        file = open(outDir+ ContractsInfo.at[index,'contractAddress']+'.sol','w')
        file.write(ContractsInfo.at[index,'SourceCode'])
        file.close()

def get_SamplesSummary(ContractsInfo,outDir,UniqueFilename):
    file = open(outDir + UniqueFilename +'_Summary.txt','w')
    
    for index, row in ContractsInfo.iterrows():
        version = ContractsInfo.at[index,'CompilerVersion'].rsplit('+')[0][1:]
        
        if 'nightly' in version:
            version = version.rsplit('-')[0]
        file.write(ContractsInfo.at[index,'contractAddress'] + ':' + version)
        
        if index !=len(ContractsInfo) -1:
            file.write('\n')
    
    file.close()