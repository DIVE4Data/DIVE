#Requirements: install beautifulsoup4
#pip install requests beautifulsoup4

import requests,datetime, os,json
from pathlib import Path
from bs4 import BeautifulSoup
import pandas as pd

def get_OpcodesList():
    #Fetch Opcodes data
    OpcodesDF = fetch_opcodes()

    #Set Opcodes categories
    OpcodesDF = set_categories(OpcodesDF)
    
    #Write opcodes data to a new csv file
    self_main_dir = Path.cwd() 
    config_file_name = 'config.json'
    config_file_path = self_main_dir / config_file_name

    with open(config_file_path) as configFile:
        config_File = json.load(configFile)
    self_dir = Path(__file__).resolve().parent
    OpcodesFolder = str(self_dir) + config_File['Features']['EVM_OpcodesDir']

    #if the opcodes data not present, write it to a new file
    if OpcodesDataUpdated(OpcodesDF,OpcodesFolder):
        filename = 'EVM_Opcodes' + '_' + str(datetime.datetime.now().date()).replace('-', '') + '_' + str(datetime.datetime.now().time()).replace(':', '').split('.')[0] + '.csv'
        OpcodesDF.to_csv(os.path.join(OpcodesFolder, filename), index=False)
        print('Done! Opcode data saved to:' + str(os.path.relpath(str(OpcodesFolder) + '/' +filename, Path.cwd().parent)))
    else:
        print('Opcodes data is up-to-date no need to create a new opcodes file.')

def fetch_opcodes():
    url = "https://ethereum.org/en/developers/docs/evm/opcodes/"
    response = requests.get(url)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    opcode_table = soup.find('table')  # Find the first table in the page
    if opcode_table is None:
        print("No table found on the page.")
        return {}
    opcode_rows = opcode_table.find_all('tr')[1:]  # Skip header
    opcodes = []  # List to hold all the opcode data
    for row in opcode_rows:
        columns = row.find_all('td')

        Stack = columns[0].text.strip()
        Name = columns[1].text.strip()
        Gas = columns[2].text.strip()
        InitialStack = columns[3].text.strip()
        ResultingStack = columns[4].text.strip()
        MemStorage = columns[5].text.strip()
        Notes = columns[6].text.strip()  
        # Append the row to the opcodes list
        opcodes.append({
            'Stack': Stack,
            'Name': Name,
            'Gas': Gas,
            'InitialStack': InitialStack,
            'ResultingStack': ResultingStack,
            'MemStorage': MemStorage,
            'Notes': Notes,
            'Category': ''
        })
    OpcodesDF = pd.DataFrame(opcodes)
    OpcodesDF['Stack'] = OpcodesDF['Stack'].apply(lambda x: f"0x{x.lower()}" if isinstance(x, str) else x)

    return OpcodesDF   

# This method assigns the correct category to each opcode.
def set_categories(OpcodesDF): 
    #Categories are collected from Ethereum yellow paper: https://ethereum.github.io/yellowpaper/paper.pdf
    categories = {'Stop Operation': [0x00,0x00],
                  'Arithmetic Operation': [0x01,0x0F],
                  'Comparison Operation': [0x10,0x15],
                  'Bitwise Logic Operation': [0x16,0x1F],
                  'KECCAK256 Operation': [0x20,0x2F],
                  'Environmental Information Operation': [0x30,0x3F],
                  'Block Information Operation': [0x40,0x4F],
                  'Stack, Memory, Storage, and Flow Operation': [0x50,0x5E],
                  'Push Operation': [0x5F,0x7F],
                  'Duplication Operation': [0x80,0x8F],
                  'Exchange Operation': [0x90,0x9F],
                  'Logging Operation': [0xa0,0xa4],
                  'System Operation': [0xF0,0xFF],
                  }
    OpcodesDF['Stack'] = OpcodesDF['Stack'].apply(lambda x: int(x, 16) if isinstance(x, str) and x.startswith('0x') and not '-' in x else x)

    for index, row in OpcodesDF.iterrows():
        value = OpcodesDF.at[index,'Stack']
        if isinstance(value, str) and '-' in value:
            continue
        for key in categories.keys():
            if value >= categories[key][0] and value <= categories[key][1]:
                OpcodesDF.at[index,'Category'] = key
                OpcodesDF.at[index,'Stack'] = hex(OpcodesDF.at[index,'Stack'])
                break
    return OpcodesDF

# Check if the opcodes csv file already exists and if there are any updates requiring write a new file.
def OpcodesDataUpdated(OpcodesDF,OpcodesFolder):
    #get Opcodes csv files
    files = [file.name for file in os.scandir(OpcodesFolder) if file.is_file() and file.name.endswith('.csv')]
    if not files:
        print('Opcodes csv file not found. Creating a new Opcodes csv file...')
        return True
    #find the recent opcodes csv file
    recent_OpcodeFile = max(files, key=lambda x: os.path.getmtime(os.path.join(OpcodesFolder, x)))
    recent_OpcodesData = pd.read_csv(os.path.join(OpcodesFolder, recent_OpcodeFile))
    #compare the recent opcodes csv file contents with the collected opcodes data
    if not OpcodesDF.equals(recent_OpcodesData.fillna('')):
        print('Opcodes data has changed. Creating a new Opcodes csv file...')
        return True