import requests
import json 
import time
import datetime
import pandas as pd
from pathlib import Path
from Scripts.extract_SourceCodes import extract_SourceCodes

#-------------------------------------------
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

def get_ContractFeatures(FeatureType,addresses):

    configFile = open(config_file_path)
    config_File = json.load(configFile)
    configFile.close()

    api_key = config_File['Etherscan_Account']['API_Key']

    match FeatureType.lower():
        case 'all':
            get_AccountInfo(api_key,addresses, outDir = self_main_dir/config_File['Features']['AccountInfo']+'/')
            get_ContractInfo(api_key,addresses,outDir = self_main_dir/config_File['Features']['ContractsInfo']+'/')
            get_Opcodes(api_key,addresses,outDir = self_main_dir/config_File['Features']['Opcodes']+'/')
        case 'accountinfo' | '1':
            get_AccountInfo(api_key,addresses, outDir = self_main_dir/config_File['Features']['AccountInfo']+'/')
        case 'contractinfo' | '2':
            get_ContractInfo(api_key,addresses,outDir = self_main_dir/config_File['Features']['ContractsInfo']+'/')
        case 'opcodes' | '3':
            get_Opcodes(api_key,addresses,outDir = self_main_dir/config_File['Features']['Opcodes']+'/')

    return True

#Fetched SCs Account Info from Etherscan.io
#------------------------------------------
def get_AccountInfo(api_key,addresses,outDir):
    counter =1
    info =[]
    NotFound = []

    for i in range(0,len(addresses)): 
        address = addresses['contractAddress'][i].strip()
        #print('Address: '+ address)
        if len(address) > 0 :
            request_string = f'https://api.etherscan.io/api?module=account&action=txlist&address={address}&apikey={api_key}'
            response = requests.get(request_string,verify=False) ###### Add verify=False to stop error messages
            #print(response.text)
            #--------------------------------------
            if response.ok:
                data = {} 
                noOfTransactions = len(json.loads(response.text) ['result'])
                if noOfTransactions >0:
                    data['contractAddress']=address
                    data['NoOfTransactions'] = noOfTransactions
                    data |= json.loads(response.text) ['result'][0]
                    #print('data is: ', data)
                    info.append(data)
                else:
                    NotFound.append(address)
                #--------------------------------------
                print(str(counter)+": ["+ address + "] Done")
                counter = counter + 1
                if counter%5 == 0:
                    time.sleep(1)
            else:
                print(address,response.text)
    
    UniqueFilename = generate_UniqueFilename('AccountInfo')
    if len(NotFound) > 0:
        AccountInfo_NotFound = pd.DataFrame(data=NotFound)
        AccountInfo_NotFound.to_csv(outDir + UniqueFilename + "_NotFound.csv",index=False)
    
    AccountInfo = pd.DataFrame(data=info)
    AccountInfo.to_csv(outDir + UniqueFilename + ".csv",index=False)
    print('Done! Account Info Data is available in ' + outDir + UniqueFilename + ".csv")
    #return AccountInfo

#Fetched contracts Info from Etherscan.io
#------------------------------------------
def get_ContractInfo(api_key,addresses,outDir):
    counter =1
    info =[]
    for i in range(0,len(addresses)): 
        address = addresses['contractAddress'][i].strip()
        #print('Address: '+ address)
        if len(address)>0:
            request_string = f'https://api.etherscan.io/api?module=contract&action=getsourcecode&address={address}&apikey={api_key}'
            response = requests.get(request_string, verify=False) ###### Add verify=False to stop error messages
            #print(response.text)
        #--------------------------------------
            data = {} 
            data['contractAddress']=address
            data |= json.loads(response.text) ['result'][0]
            #print('data is: ', data)
            info.append(data)
        #--------------------------------------
            print(str(counter)+": ["+ address + "] Done")
            counter = counter + 1
            if counter%5 == 0:
                time.sleep(1)
    
    ContractsInfo = pd.DataFrame(data=info)
    UniqueFilename = generate_UniqueFilename('ContractsInfo')
    #Extract Source Codes then remove it from the dataframe
    ContractsInfo = extract_SourceCodes(ContractsInfo,UniqueFilename)
    ContractsInfo.to_csv(outDir + UniqueFilename + ".csv",index=False)
    print('Done! Contracts Info Data is available in ' + outDir + UniqueFilename + ".csv")
    #return ContractsInfo

#Fetched SCs Opcodes from Etherscan.io
#------------------------------------------
def get_Opcodes(api_key,addresses,outDir):
    counter =1
    info =[]
    NotFound = []

    for i in range(0,len(addresses)): 
        address = addresses['contractAddress'][i].rstrip()
        if len(address) > 0:
            request_string = f'https://api.etherscan.io/api?module=opcode&action=getopcode&address={address}&apikey={api_key}'
            response = requests.get(request_string,verify=False) ###### Add verify=False to stop error messages
            #print(response.text)
            #--------------------------------------
            if response.ok:
                data = {} 
                data['contractAddress']=address
                data['Opcodes']= json.loads(response.text) ['result']
                #print('data is: ', data)
                info.append(data)
                #--------------------------------------
                print(str(counter)+": ["+ address + "] Done")
                counter = counter + 1
                if counter%5 == 0:
                    time.sleep(1)
            else:
                print(address,response.text)
        else:
            NotFound.append(i)
    
    UniqueFilename = generate_UniqueFilename('Opcodes')
    if len(NotFound)>0:
        Opcodes_NotFound = pd.DataFrame(data=NotFound)
        Opcodes_NotFound.to_csv(outDir + UniqueFilename + "_NotFound.csv",index=False)
    
    Opcodes=pd.DataFrame(data=info)
    Opcodes.to_csv(outDir + UniqueFilename + ".csv",index=False)
    print('Done! Opcodes Data is available in ' + outDir + UniqueFilename + ".csv")
    #return Opcodes

#------------------------------------------
def generate_UniqueFilename(FeatureType):
    UniqueFilename = str(datetime.datetime.now().date()).replace('-', '') + '_' + str(datetime.datetime.now().time()).replace(':', '').split('.')[0] + FeatureType
    return UniqueFilename