# 🛠️ Using Framework Functions

## 1️⃣ Feature Collection

1. **Read contract addresses to a dataframe**
```python
addresses = get_Addresses(FileNames as list)
```
**Options:**
- **All files** → `["All"]`  
- **Specific file(s)** → `["file1.csv", "file2.csv"]`

   > The function reads files from the directory [`RawData/SC_Addresses/`](https://github.com/SMART-DIVE/DIVE/tree/main/RawData/SC_Addresses) (To read files from a different directory, edit [`config.json`](https://github.com/SMART-DIVE/DIVE/blob/main/config.json))

2. **Get contract features:**
```python
get_ContractFeatures(FeatureType as list, addresses as dataframe, DatasetName as a string)
```
**Feature types:**

- `'AccountInfo'` or `'1'`  
- `'ContractInfo'` or `'2'`  
- `'Opcodes'` or `'3'`  
- **Multiple types** → `["AccountInfo", "Opcodes"]`
- **All supported types** →`["All"]`

> 📁 Results are saved in: [`Features/`](https://github.com/SMART-DIVE/DIVE/tree/main/Features) (To save in a different directory, edit [`config.json`](https://github.com/SMART-DIVE/DIVE/blob/main/config.json))
---

## 2️⃣ Solidity Code Extraction
* This function extracts the source code for each contract and saves it as a `.sol` file. It also generates a summary file listing contract addresses and their compiler versions, which is useful in many cases, such as setting the correct `solc` version when running analysis tools. It is automatically invoked after fetching contract information, but can also be called manually
```python
extract_SourceCodes(ContractsInfo as a dataframe, UniqueFilename as a string, DatasetName as a string)
```
> 📁 Results are saved in: [`RawData/Samples/`](https://github.com/SMART-DIVE/DIVE/tree/main/RawData/Samples) and [`RawData/SamplesSummary/`](https://github.com/SMART-DIVE/DIVE/tree/main/RawData/SamplesSummary) (To save in different directories, edit [`config.json`](https://github.com/SMART-DIVE/DIVE/blob/main/config.json))

---
## 3️⃣ Code Metrics Generation
```python
get_CodeMetrics(SamplesFolderName as a string, SamplesDirPath as a path, DatasetName as a string)
```
**Options:**

- To process samples from the **default directory**, set:  
  `SamplesDir = ""` or `SamplesDir = "default"`

- To process samples from a **custom directory**, set:  
  `SamplesDir = "path/to/your/samples"`
    
  > Default samples path: [`RawData/Samples`](https://github.com/SMART-DIVE/DIVE/tree/main/RawData/Samples)
  > 📁 Results are saved in: [`Features/CodeMetrics/`](https://github.com/SMART-DIVE/DIVE/tree/main/Features/CodeMetrics)
  > (To read or save in a different directory, edit [`config.json`](https://github.com/SMART-DIVE/DIVE/blob/main/config.json))
---

## 4️⃣ Construction Final Data
```python
construct_FinalData(FinalDatasetName as a string, Dataset = ['Dataset1Name','Dataset2Name',...], FeatureTypes = {'Type1':['All' 'or list files'], 'Type2':['All' 'or list files'] , ... }, applyPreprocessing = False)
```
**Parameters:**
- **`FinalDatasetName`** → Name of the final dataset to be created.
- **`Dataset`** → List of dataset names to include, e.g., `['Dataset1Name', 'Dataset2Name']`.
- **`FeatureTypes`** → A dictionary specifying the feature types and corresponding files to include.  
  Available types include: `"AccountInfo"`, `"ContractsInfo"`, `"Opcodes"`, `"CodeMetrics"`, `"Opcode-based"`, `"Input-based"`, `"ABI-based"`, and `"Labels"`.  
  For each type, you can use:
  - `'all'` → to include all available files, or  
  - a list like `['File1.csv', 'File2.csv']` → to include specific files.
- **`applyPreprocessing`** → Set to `True` to apply preprocessing during construction, otherwise `False`.

> 📁 Data are collected from their default directories. Results are saved in: [`DIVE_Dataset/`](https://github.com/SMART-DIVE/DIVE/tree/main/DIVE_Dataset).  
> To use a different directory for saving or reading, edit [`config.json`](https://github.com/SMART-DIVE/DIVE/blob/main/config.json).

--- 

## 5️⃣ Apply Data Preprocessing
```python
apply_DataPreprocessing(datasetName as string, dataDirPath as bool or string, PreprocessingTasks as a list)
```
**Parameters:**
- **`datasetName`** → Name of the dataset.
- **`dataDirPath`** → `True` to use the default directory, or provide a custom path like `"path/to/your/samples"`.
- **`PreprocessingTasks`** → Use `['all']` to perform all tasks, or specify a list of tasks to apply. Supported tasks include:

  - `1` or `'DropDuplicates'`
  - `2` or `'HideProtectedAttributes'`
  - `3` or `'FillMissingData'`
  - `4` or `'ProcessConstructorArguments'`
  - `5` or `'ProcessOpcodes'`
  - `6` or `'RemoveUselesCols'`
  - `7` or `'HandlingHexaData'`
  - `8` or `'HandlingStringNumericalData'`
  - `9` or `'HandlingStringBoolColsToInt'`
  - `10` or `'HandlingCategoricalData'`
  - `11` or `'ConvertFloatColumns_to_Int'`
  - `12` or `'SetDataIndexColumn'`

> 📁 Results are saved in: [`Features/FE-based/CodeMetrics/CodeMetrics`](https://github.com/SMART-DIVE/DIVE/tree/main/Features/FE-based/CodeMetrics/CodeMetrics)
> To use a different directory for saving or reading, edit [`config.json`](https://github.com/SMART-DIVE/DIVE/blob/main/config.json).
     
---

## 6️⃣ Statistical Data Generation

**If the dataset is in the default directory**, pass its name as follows:

```python
get_DataStatistics(dataset='DatasetFileName.csv',defaultDir = True)
```

**If the dataset is available in a different directory**, edit [`config.json`](https://github.com/SMART-DIVE/DIVE/blob/main/config.json) file or pass its path as follows:
```python
get_DataStatistics(dataset='DatasetFilePath',defaultDir = False)
```
> 📁 Results are saved in: [`Statistics`](https://github.com/SMART-DIVE/DIVE/tree/main/Statistics) (To save in a different directory, edit [`config.json`](https://github.com/SMART-DIVE/DIVE/blob/main/config.json))
---
