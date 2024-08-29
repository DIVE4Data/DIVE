# DigVulSC
A Blockchain digging framework and constructing vulnerability-tagged smart contract datasets.
## Features
The DigVulSC framework provides several functions through the following components:
* **Feature Collecting:** This component enables fetching information about the smart contract and its account from a public Blockchain network. Currently, it only supports the <A Href="https://ethereum.org/en/">Ethereum</A> Blockchain. It makes use of <A Href="https://etherscan.io/">Etherscan.io</A>, an Ethereum Blockchain Explorer, to obtain Ethereum block data. This component can collect three distinct feature sets: (1) Contract information. (2) Account information. (3) Opcodes.
* **Solidity Codes Extraction:** This component assists in extracting the contract's source code and creating the <A Href="https://soliditylang.org/">Solidity</A> code file.
* **Code Metrics Generation:** This component gathers useful code metrics by analyzing the contract's source code. It leverages <A Href="https://classic.yarnpkg.com/en/package/solidity-code-metrics">Solidity Code Metrics</A>, an open-source package that generates an analysis markdown report containing a variety of valuable data besides Solidity code metrics. It employs <A Href="https://pypi.org/project/markdown-analysis/"> Mrkdwn_analysis</A> Python library to parse markdown reports and extract useful features. 
* **Labeled Data Construction:** 
* **Statistical Data Generation:**
## Requirements
*  <A Href="https://www.python.org/">Python</A> >=3.12.2
*  <A Href="https://classic.yarnpkg.com/en/package/solidity-code-metrics">Solidity Code Metrics</A> >= 0.0.26
*  <A Href="https://pypi.org/project/markdown-analysis/"> Mrkdwn_analysis Python library</A> = 0.0.5
*  An API-key on <A Href="https://etherscan.io/">Etherscan.io</A>. If you don't have an account, you can create a free account on <A Href="https://etherscan.io/">Etherscan.io</A>, and then generate your API key. For further details, check the <A Href="https://docs.etherscan.io/getting-started/viewing-api-usage-statistics">Getting an API key</A> webpage on <A Href="https://etherscan.io/">Etherscan.io</A>. ***Please note that your key should not be shared with others***.
## Usage
### Initials Steps
* Clone <A Href="https://github.com/DigVulSC/DigVulSC"> DigVulSC repository </A>
```
      git clone https://github.com/DigVulSC/DigVulSC.git
```
* Edit <A Href="https://github.com/DigVulSC/DigVulSC/blob/main/Scripts/config.json">Scripts/config.json</A> file to add your API-Key.
```
"Etherscan_Account": 
    {
        "API_Key": "Your API Key"
    }
```
* Add the csv file containing the contract addresses to the <A Href="https://github.com/DigVulSC/DigVulSC/tree/main/RawData/SC_Addresses">RawData/SC_Addresses</A> folder.
* The DigVulSC framework is designed to read/write specific folders. It also targets certain columns to get contract addresses or data labels. If required, you can edit the configuration file (<A Href="https://github.com/DigVulSC/DigVulSC/blob/main/Scripts/config.json">Scripts/config.json</A>) to meet your requirements.
* To utilize any script, first import it into your Python code.
```
from Scripts.get_Addresses import get_Addresses
from Scripts.get_ContractFeatures import get_ContractFeatures
from Scripts.get_CodeMetrics import get_CodeMetrics
from Scripts.construct_FinalData import construct_FinalData
from Scripts.get_DataStatistics import get_DataStatistics
```
### Using Framework Functions
#### **1. Feature Collecting**
* **First, Read Contract Addresses to a dataframe**
```
addresses = get_Addresses(FileNames as list)
```
* **Note:**
    * **To read all files:** Pass ["All"] for the file name. 
    * **To get addresses from a specific file:** Type the file name with ".csv"
    * **To get addresses from multiple files:** type ['file1.csv','file2.csv',...'fileN.csv']
    *  The function reads files from the directory <A Href="https://github.com/DigVulSC/DigVulSC/tree/main/RawData/SC_Addresses">RawData/SC_Addresses</A> (Edit the <A Href="https://github.com/DigVulSC/DigVulSC/blob/main/Scripts/config.json">Scripts/config.json</A> file to read files from a different directory)
* **Get contract features:**
```
get_ContractFeatures(DatasetName as a string, FeatureType as list,addresses as dataframe)
```
* **Note:**
   * **To get all feature types:** Pass ["All"] for FeatureType. 
   * **To get specific feature type:** Pass the feature type/s as follows:
      *   **Account Info:** ['AccountInfo] or ['1']
      *   **Contract Info:** ['ContractInfo] or ['2']
      *   **Opcodes:** ['Opcodes] or ['3']
      *   **Multiple Types:** ['FeatureType 1','FeatureType 2',...]
  * The function's output is saved in the directory <A Href= "https://github.com/DigVulSC/DigVulSC/tree/main/Features">Features/FEATURETYPE/</A> (Edit the <A Href="https://github.com/DigVulSC/DigVulSC/blob/main/Scripts/config.json">Scripts/config.json</A> file to store the function output in a different directory)
#### **2. Solidity Codes Extraction**

#### **3. Code Metrics Generation**
```
get_CodeMetrics(DatasetName as a string, SamplesDir as a path)
```
* **Note:** 
  * To process samples that are stored in the default directory: SamplesDir = '' or SamplesDir = 'All'
  * To process samples stored in a different directory: SamplesDir = 'Type the path to the samples directory.'
  * The default samples path is <A Href="https://github.com/DigVulSC/DigVulSC/tree/main/RawData/Samples">RawData/Samples</A>
  * The function's output is saved in the directory <A Href="https://github.com/DigVulSC/DigVulSC/tree/main/Features/CodeMetrics">Features/CodeMetrics/</A> 
  * Edit the <A Href="https://github.com/DigVulSC/DigVulSC/blob/main/Scripts/config.json">Scripts/config.json</A> file to read from or store in a different directory.
#### **4. Labeled Data Construction**
```
construct_FinalData(Dataset = ['Dataset1Name','Dataset2Name',...], AccountInfo = FileNames as a list,ContractsInfo=FileNames as a list,Opcodes=FileNames as a list,CodeMetrics=FileNames as a list,Labels=FileNames as a list)
```
* **Note:**
   * To get all files, pass ['All'] for the FileNames.
   * To get specific files, pass ['File1Name','FileName2',...] for the FileNames.
   * The function's output is saved in the directory <A Href="https://github.com/DigVulSC/DigVulSC/tree/main/DigVulSCDS">DigVulSCDS</A> (Edit the <A Href="https://github.com/DigVulSC/DigVulSC/blob/main/Scripts/config.json">Scripts/config.json</A> file to store the function output in a different directory)
#### **5. Statistical Data Generation**
* If the dataset is available in the default directory, pass its name as follows:
```
get_DataStatistics(dataset='DatasetFileName.csv',defaultDir = True)
```
* If the dataset is available in a different directory, Edit the <A Href="https://github.com/DigVulSC/DigVulSC/blob/main/Scripts/config.json">Scripts/config.json</A> file or pass its path as follows:
```
get_DataStatistics(dataset='DatasetFilePath',defaultDir = False)
```
* The function's output is saved in the directory <A Href= "https://github.com/DigVulSC/DigVulSC/tree/main/Statistics">Statistics/</A> (Edit the <A Href="https://github.com/DigVulSC/DigVulSC/blob/main/Scripts/config.json">Scripts/config.json</A> file to store the function output in a different directory)
## Demo
* 
