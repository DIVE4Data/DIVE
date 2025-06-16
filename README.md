# 🚀 DIVE Framework  
*A blockchain digging framework for constructing vulnerability-tagged smart contract datasets.*

---

## 🔍 Key Features

The DIVE framework offers powerful tools through five main components:

### 1. 🧾 Feature Collecting  
Fetch smart contract and account data from public blockchains.  
- ✅ Currently supports [Ethereum](https://ethereum.org/en/).  
- 🔗 Uses [Etherscan.io](https://etherscan.io/) as a data source.  
- 📊 Collects:
  - Contract information  
  - Account information  
  - Opcodes  

### 2. 🧠 Solidity Code Extraction  
Extract and save contract source code as `.sol` files using [Solidity](https://soliditylang.org/).

### 3. 📈 Code Metrics Generation  
Analyze source code using:
- [`solidity-code-metrics`](https://classic.yarnpkg.com/en/package/solidity-code-metrics)  
- [`mrkdwn_analysis`](https://pypi.org/project/markdown-analysis/) to parse markdown and extract features.

### 4. 🏷️ Labeled Data Construction  
Merge outputs from previous steps to construct a labeled dataset.

### 5. 📊 Statistical Data Generation  
Generate statistics and visualizations that provide insights into the dataset.

---

## 📦 Requirements

- [Python](https://www.python.org/) >= **3.12.2**  
- [`solidity-code-metrics`](https://classic.yarnpkg.com/en/package/solidity-code-metrics) >= **0.0.26**  
- [`mrkdwn_analysis`](https://pypi.org/project/markdown-analysis/) == **0.0.5**  
- 🔑 Etherscan API Key  
  > Create an account at [Etherscan.io](https://etherscan.io/) and follow their [API key guide](https://docs.etherscan.io/getting-started/viewing-api-usage-statistics).  
  > ⚠️ **Do not share your API key publicly.**

---

## ⚙️ Usage

### 🔧 Initial Setup
1. **Clone the repository:**
```bash
      git clone https://github.com/SMART-DIVE/DIVE.git
```
2. **Add your API key**
* Edit <A Href="https://github.com/SMART-DIVE/DIVE/blob/main/Scripts/config.json">Scripts/config.json</A>
```json
"Etherscan_Account": 
    {
        "API_Key": "Your API Key"
    }
```
3. **Add contract addresses**
Place your CSV file in <A Href="https://github.com/SMART-DIVE/DIVE/tree/main/RawData/SC_Addresses">RawData/SC_Addresses</A> folder.

> The DIVE framework is designed to read/write specific folders. It also targets certain columns to get contract addresses or data labels. If required, you can edit the configuration file (<A Href="https://github.com/SMART-DIVE/DIVE/blob/main/config.json">config.json</A>) to meet your requirements.

4. **To utilize any script, first import it into your Python code:**
```python
from Scripts.get_Addresses import get_Addresses
from Scripts.get_ContractFeatures import get_ContractFeatures
from Scripts.get_CodeMetrics import get_CodeMetrics
from Scripts.construct_FinalData import construct_FinalData
from Scripts.get_DataStatistics import get_DataStatistics
from Scripts.extract_SourceCodes import extract_SourceCodes
```

### 🛠️ Using Framework Functions

### 1️⃣ Feature Collection

1. **Read contract addresses to a dataframe**
```python
addresses = get_Addresses(FileNames as list)
```
**Options:**
- **All files** → `["All"]`  
- **Specific file(s)** → `["file1.csv", "file2.csv"]`

   > The function reads files from the directory <A Href="https://github.com/SMART-DIVE/DIVE/tree/main/RawData/SC_Addresses">RawData/SC_Addresses</A> (Edit the <A Href="https://github.com/SMART-DIVE/DIVE/blob/main/config.json">config.json</A> file to read files from a different directory)

2. **Get contract features:**
```python
get_ContractFeatures(DatasetName as a string, FeatureType as list,addresses as dataframe)
```
**Feature types:**

- `'AccountInfo'` or `'1'`  
- `'ContractInfo'` or `'2'`  
- `'Opcodes'` or `'3'`  
- **Multiple types** → `["AccountInfo", "Opcodes"]`

> 📁 Results are saved in: [`Features/`](https://github.com/SMART-DIVE/DIVE/tree/main/Features) (Edit the <A Href="https://github.com/SMART-DIVE/DIVE/blob/main/config.json">config.json</A> file to store the function output in a different directory)

### 2️⃣ Solidity Codes Extraction
* This function is called automatically after fetching the contract information. However, it can be called independently if needed as follows:
```python
extract_SourceCodes(DatasetName as a string,ContractsInfo as a dataframe,UniqueFilename as a string)
```
> 📁 Results are saved in: [`RawData/Samples/`](https://github.com/SMART-DIVE/DIVE/tree/main/RawData/Samples>RawData/Samples) and [`RawData/SamplesSummary/`](https://github.com/SMART-DIVE/DIVE/tree/main/RawData/SamplesSummary) (To save in different directories, edit [`config.json`](https://github.com/SMART-DIVE/DIVE/blob/main/config.json))

### 3️⃣ Code Metrics Generation
```python
get_CodeMetrics(DatasetName as a string, SamplesDir as a path)
```
* **Note:** 
  * To process samples that are stored in the default directory: SamplesDir = '' or SamplesDir = 'All'
  * To process samples stored in a different directory: SamplesDir = 'Type the path to the samples directory.'
  * The default samples path is <A Href="https://github.com/SMART-DIVE/DIVE/tree/main/RawData/Samples">RawData/Samples</A>
  * The function's output is saved in the directory <A Href="https://github.com/SMART-DIVE/DIVE/tree/main/Features/CodeMetrics">Features/CodeMetrics/</A> 
  * Edit the <A Href="https://github.com/SMART-DIVE/DIVE/blob/main/Scripts/config.json">Scripts/config.json</A> file to read from or store in a different directory.
    
### 4️⃣ Labeled Data Construction
```python
construct_FinalData(Dataset = ['Dataset1Name','Dataset2Name',...], AccountInfo = FileNames as a list,ContractsInfo=FileNames as a list,Opcodes=FileNames as a list,CodeMetrics=FileNames as a list,Labels=FileNames as a list)
```
* **Note:**
   * To get all files, pass ['All'] for the FileNames.
   * To get specific files, pass ['File1Name','FileName2',...] for the FileNames.
   * The function's output is saved in the directory <A Href="https://github.com/SMART-DIVE/DIVE/tree/main/DIVE_Dataset">DIVE_Dataset</A> (Edit the <A Href="https://github.com/SMART-DIVE/DIVE/blob/main/Scripts/config.json">Scripts/config.json</A> file to store the function output in a different directory)

### 5️⃣ Statistical Data Generation
* If the dataset is available in the default directory, pass its name as follows:
```python
get_DataStatistics(dataset='DatasetFileName.csv',defaultDir = True)
```
* If the dataset is available in a different directory, Edit the <A Href="https://github.com/SMART-DIVE/DIVE/blob/main/Scripts/config.json">Scripts/config.json</A> file or pass its path as follows:
```python
get_DataStatistics(dataset='DatasetFilePath',defaultDir = False)
```
* The function's output is saved in the directory <A Href= "https://github.com/SMART-DIVE/DIVE/tree/main/Statistics">Statistics/</A> (Edit the <A Href="https://github.com/SMART-DIVE/DIVE/blob/main/Scripts/config.json">Scripts/config.json</A> file to store the function output in a different directory)
---
## Demo
*  
---

## 📦 License

This project is licensed under the [Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0)](https://creativecommons.org/licenses/by-nc/4.0/).

🚫 **Patent Rights Reserved**  
* This project may be covered by pending or granted patents. The authors reserve all rights under applicable patent laws.  
* The use of this software does **not grant any rights to use patented inventions**.  
* For commercial licensing or patent-related inquiries, please contact the authors directly.

**🛡️ Disclaimer**
* DIVE is provided as a research tool and is under active development. While we strive for reliability, we do not provide warranties or guarantees. Please use it responsibly and at your own discretion.
