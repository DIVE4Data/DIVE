import os
import pandas as pd
from solcx import compile_standard, install_solc

# Function to install the Solidity compiler version
def install_solidity(version):
    install_solc(version)

# Function to map bytecode to opcodes
def bytecode_to_opcodes(bytecode):
    opcodes_map = {
        '60': 'PUSH1', '61': 'PUSH2', '62': 'PUSH3', '63': 'PUSH4', 
        '64': 'PUSH5', '65': 'PUSH6', '66': 'PUSH7', '67': 'PUSH8',
        '68': 'PUSH9', '69': 'PUSH10', '6A': 'PUSH11', '6B': 'PUSH12', 
        '6C': 'PUSH13', '6D': 'PUSH14', '6E': 'PUSH15', '6F': 'PUSH16',
        # Add more opcodes as needed
        # Here are a few common opcodes for illustration
        '0x': 'NOP',
        '1': 'ADD', '2': 'MUL', '3': 'SUB', '4': 'DIV',
        '5': 'SDIV', '6': 'MOD', '7': 'SMOD', '8': 'ADDMOD',
        '9': 'MULMOD', 'A': 'EXP', 'B': 'SIGNEXTEND', 
        # You can expand this mapping with more opcodes as needed
    }
    
    opcodes = []
    for i in range(0, len(bytecode), 2):
        opcode = bytecode[i:i + 2]
        if opcode in opcodes_map:
            # Get the immediate value following the opcode
            if opcode.startswith('5') or opcode.startswith('6'):  # PUSH1 to PUSH16 have immediate values
                value = bytecode[i + 2:i + 4] if i + 2 < len(bytecode) else ''
                opcodes.append(f"{opcodes_map[opcode]} 0x{value}")
                i += 2  # Skip the immediate value
            else:
                opcodes.append(opcodes_map[opcode])
        else:
            opcodes.append(f"UNKNOWN_OPCODE {opcode}")

    return opcodes

# Function to compile Solidity files in a given folder
def compile_solidity_files(folder_path):
    bytecode_data = []

    # Get a list of all Solidity files in the specified folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.sol'):
            file_path = os.path.join(folder_path, filename)
            
            with open(file_path, 'r') as file:
                source_code = file.read()

            # Compile the Solidity code
            compiled_sol = compile_standard({
                'language': 'Solidity',
                'sources': {filename: {'content': source_code}},
                'settings': {
                    'outputSelection': {
                        '*': {
                            '*': ['*']
                        }
                    }
                }
            })

            # Extract bytecode
            contract_name = list(compiled_sol['contracts'][filename].keys())[0]
            bytecode = compiled_sol['contracts'][filename][contract_name]['evm']['bytecode']['object']
            
            # Extract opcodes from bytecode
            opcodes = bytecode_to_opcodes(bytecode)

            bytecode_data.append({
                'file_name': filename,
                'bytecode': bytecode,
                'extractedOpcodes': opcodes  # Add opcodes to the data
            })

    return pd.DataFrame(bytecode_data)

# Main function
def main():
    # Specify the folder containing Solidity files
    folder_path = input("Enter the folder path containing Solidity files: ")
    
    # Optionally install a specific version of the Solidity compiler
    install_solidity('0.8.0')  # Replace with your desired version

    # Compile the Solidity files and get the DataFrame
    bytecode_df = compile_solidity_files(folder_path)
    
    # Display the resulting DataFrame
    print(bytecode_df)

if __name__ == "__main__":
    main()