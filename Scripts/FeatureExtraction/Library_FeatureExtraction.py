import json, datetime
from pathlib import Path
from IPython.display import display
import pandas as pd

def library_FeatureExtraction(DatasetName, dataset, Col='Library'):
    try:
        if Col in dataset.columns:
            self_main_dir = Path.cwd() 
            config_file_path = self_main_dir / 'config.json'

            with open(config_file_path) as configFile:
                config_File = json.load(configFile)

            # Extract library names as a list
            dataset['ExternalLibNames'] = dataset[Col].apply(extract_libNames)
            dataset['NoOfExternalLib'] = dataset['ExternalLibNames'].apply(len)

            # Determine contract identifier column
            if 'contractID' in dataset.columns:
                contract_col = 'contractID'
            elif 'contractAddress' in dataset.columns:
                contract_col = 'contractAddress'
            else:
                raise KeyError('Neither "contractID" nor "contractAddress" found in dataset.')

            library_Feature = dataset[[contract_col, Col, 'ExternalLibNames', 'NoOfExternalLib']]

            UniqueFilename = generate_UniqueFilename(DatasetName, 'Library')
            outDir = self_main_dir / config_File['Features']['FE-based']['Library-based']
            outDir.mkdir(parents=True, exist_ok=True)
            library_Feature.to_csv(str(outDir / (UniqueFilename + ".csv")), index=False)

            relOutDir = self_main_dir.relative_to(Path.cwd().parent)
            print('Done! The Library-based data is available in: ' + str(relOutDir / (UniqueFilename + ".csv")))
            display(library_Feature)
        else:
            print(f'The {Col} attribute is not present in the given dataset')
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise
# ------------------------------------------
def extract_libNames(row):
    lib_names = []
    if pd.notna(row):
        for pair in str(row).split(";"):
            segments = pair.split(":")
            if len(segments) > 1:
                name = segments[1].strip() if segments[0] == '' else segments[0].strip()
                if name:
                    lib_names.append(name)
    return lib_names  # Always return a list (even if empty)
# ------------------------------------------
def generate_UniqueFilename(DatasetName, datatype):
    now = datetime.datetime.now()
    return f"{DatasetName}_{datatype}_{now.date().isoformat().replace('-', '')}_{now.time().isoformat().replace(':', '').split('.')[0]}"