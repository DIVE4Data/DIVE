import requests, json
import datetime, time
import pandas as pd
from pathlib import Path
from IPython.display import display
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

def get_ContractFeatures(FeatureType,addresses,DatasetName=''):
    try:
        configFile = open(config_file_path)
        config_File = json.load(configFile)
        configFile.close()

        api_key = config_File['Etherscan_Account']['API_Key']
        for type in FeatureType:
            match type.lower():
                case 'all':
                    AccountInfo = get_AccountInfo(DatasetName,api_key,addresses, outDir = self_main_dir/config_File['Features']['AccountInfo'])
                    display(AccountInfo)
                    ContractInfo = get_ContractInfo(DatasetName,api_key,addresses,outDir = self_main_dir/config_File['Features']['ContractsInfo'])
                    display(ContractInfo)
                    Opcodes = get_Opcodes(DatasetName,api_key,addresses,outDir = self_main_dir/config_File['Features']['Opcodes'])
                    display(Opcodes)
                case 'accountinfo' | '1':
                    AccountInfo = get_AccountInfo(DatasetName,api_key,addresses, outDir = self_main_dir/config_File['Features']['AccountInfo'])
                    display(AccountInfo)
                case 'contractsinfo' | '2':
                    ContractInfo = get_ContractInfo(DatasetName,api_key,addresses,outDir = self_main_dir/config_File['Features']['ContractsInfo'])
                    display(ContractInfo)
                case 'opcodes' | '3':
                    Opcodes = get_Opcodes(DatasetName,api_key,addresses,outDir = self_main_dir/config_File['Features']['Opcodes'])
                    display(Opcodes)
                 # default pattern
                case _:
                    print(type + ' is an incorrect Feature Type')
        return True

    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise
#Fetched SCs Account Info from Etherscan.io
#------------------------------------------
def get_AccountInfo(DatasetName,api_key,addresses,outDir):
    counter =1
    info =[]
    NotFound = []
    print('Account information is now being retrieved from Etherscan data; please wait...')
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
                    data |= json.loads(response.text)['result'][0]
                    #print('data is: ', data)
                    info.append(data)
                else:
                    NotFound.append(address)
                #--------------------------------------
                #print(str(counter)+": ["+ address + "] Done")
                counter = counter + 1
                if counter%5 == 0:
                    time.sleep(1)
            else:
                print(address,response.text)
    
    UniqueFilename = generate_UniqueFilename(DatasetName,'AccountInfo')
    if len(NotFound) > 0:
        AccountInfo_NotFound = pd.DataFrame(data=NotFound)
        AccountInfo_NotFound.to_csv(str(outDir) + '/NotFound/' + UniqueFilename + "_NotFound.csv",index=False)
    
    AccountInfo = pd.DataFrame(data=info)
    AccountInfo.to_csv(str(outDir) + '/' + UniqueFilename + ".csv",index=False)
    print('Done! Account Info Data is available in: ' + str(outDir) + '/' + UniqueFilename + ".csv")
    return AccountInfo

#Fetched contracts Info from Etherscan.io
#------------------------------------------
def get_ContractInfo(DatasetName,api_key,addresses,outDir):
    counter =1
    info =[]
    print('Contract information is now being retrieved from Etherscan data; please wait...')
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
            data |= json.loads(response.text)['result'][0]
            #print('data is: ', data)
            info.append(data)
        #--------------------------------------
            #print(str(counter)+": ["+ address + "] Done")
            counter = counter + 1
            if counter%5 == 0:
                time.sleep(1)
    
    ContractsInfo = pd.DataFrame(data=info)
    UniqueFilename = generate_UniqueFilename(DatasetName,'ContractsInfo')
    
    #Extract Source Codes then remove it from the dataframe
    ContractsInfo = extract_SourceCodes(ContractsInfo,UniqueFilename,DatasetName)
    ContractsInfo.to_csv(str(outDir) + '/' + UniqueFilename + ".csv",index=False)
    print('Done! Contracts Info Data is available in: ' + str(outDir) + '/' + UniqueFilename + ".csv")
    return ContractsInfo

#Fetched SCs Opcodes from Etherscan.io
#------------------------------------------
def get_Opcodes(DatasetName,api_key,addresses,outDir):
    counter =1
    info =[]
    NotFound = []
    print('Opcodes data is now being retrieved from Etherscan data; please wait...')
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
                data['Opcodes']= json.loads(response.text)['result']
                #print('data is: ', data)
                info.append(data)
                #--------------------------------------
                #print(str(counter)+": ["+ address + "] Done")
                counter = counter + 1
                if counter%5 == 0:
                    time.sleep(1)
            else:
                print(address,response.text)
        else:
            NotFound.append(i)
    
    UniqueFilename = generate_UniqueFilename(DatasetName,'Opcodes')
    if len(NotFound)>0:
        Opcodes_NotFound = pd.DataFrame(data=NotFound)
        Opcodes_NotFound.to_csv(str(outDir) + '/NotFound/' + UniqueFilename + "_NotFound.csv",index=False)
    
    Opcodes=pd.DataFrame(data=info)
    Opcodes.to_csv(str(outDir) + '/' + UniqueFilename + ".csv",index=False)
    print('Done! Opcodes Data is available in: ' + str(outDir) + '/' + UniqueFilename + ".csv")
    return Opcodes

#------------------------------------------
def generate_UniqueFilename(DatasetName,datatype):
    '''if DatasetName == 'DS':
        DatasetName = datatype'''
    UniqueFilename = DatasetName + '_' + datatype + '_' + str(datetime.datetime.now().date()).replace('-', '') + '_' + str(datetime.datetime.now().time()).replace(':', '').split('.')[0]
    return UniqueFilename