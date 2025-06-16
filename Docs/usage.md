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
get_ContractFeatures(DatasetName as a string, FeatureType as list,addresses as dataframe)
```
**Feature types:**

- `'AccountInfo'` or `'1'`  
- `'ContractInfo'` or `'2'`  
- `'Opcodes'` or `'3'`  
- **Multiple types** → `["AccountInfo", "Opcodes"]`

> 📁 Results are saved in: [`Features/`](https://github.com/SMART-DIVE/DIVE/tree/main/Features) (To save in a different directory, edit [`config.json`](https://github.com/SMART-DIVE/DIVE/blob/main/config.json))
---

## 2️⃣ Solidity Code Extraction
* This function is automatically invoked after fetching contract information, but can also be called manually
```python
extract_SourceCodes(DatasetName as a string,ContractsInfo as a dataframe,UniqueFilename as a string)
```
> 📁 Results are saved in: [`RawData/Samples/`](https://github.com/SMART-DIVE/DIVE/tree/main/RawData/Samples) and [`RawData/SamplesSummary/`](https://github.com/SMART-DIVE/DIVE/tree/main/RawData/SamplesSummary) (To save in different directories, edit [`config.json`](https://github.com/SMART-DIVE/DIVE/blob/main/config.json))

---
## 3️⃣ Code Metrics Generation
```python
get_CodeMetrics(DatasetName as a string, SamplesDir as a path)
```
**Options:**

- To process samples from the **default directory**, set:  
  `SamplesDir = ""` or `SamplesDir = "All"`

- To process samples from a **custom directory**, set:  
  `SamplesDir = "path/to/your/samples"`
    
  > Default samples path: [`RawData/Samples`](https://github.com/SMART-DIVE/DIVE/tree/main/RawData/Samples)
  > 📁 Results are saved in: [`Features/CodeMetrics/`](https://github.com/SMART-DIVE/DIVE/tree/main/Features/CodeMetrics)
  > (To read or save in a different directory, edit [`config.json`](https://github.com/SMART-DIVE/DIVE/blob/main/config.json))
---

## 4️⃣ Labeled Data Construction
```python
construct_FinalData(Dataset = ['Dataset1Name','Dataset2Name',...], AccountInfo = FileNames as a list,ContractsInfo=FileNames as a list,Opcodes=FileNames as a list,CodeMetrics=FileNames as a list,Labels=FileNames as a list)
```
**Options:**
- **All files** → `["All"]`  
- **Specific file(s)** → `["File1Name", "FileName2"]`

> 📁 Results are saved in: [`DIVE_Dataset/`](https://github.com/SMART-DIVE/DIVE/tree/main/DIVE_Dataset) (To save in a different directory, edit [`config.json`](https://github.com/SMART-DIVE/DIVE/blob/main/config.json))
---  

## 5️⃣ Statistical Data Generation

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
