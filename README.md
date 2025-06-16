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
Combines extracted features and ground-truth labels into a structured dataset

### 5. 📊 Statistical Data Generation  
Generate statistics and visualizations that provide insights into the dataset.

---

## 📦 Requirements

- [Python](https://www.python.org/) >= **3.12.2**  
- [`solidity-code-metrics`](https://classic.yarnpkg.com/en/package/solidity-code-metrics) >= **0.0.26**
  > Install using one of the following:
  ```bash
  # Using Yarn
  yarn global add solidity-code-metrics@^0.0.26
  
  # Or using npm
  npm install -g solidity-code-metrics@^0.0.26
  ```
 
- 🔑 Etherscan API Key  
  > Create an account at [Etherscan.io](https://etherscan.io/) and follow their [API key guide](https://docs.etherscan.io/getting-started/viewing-api-usage-statistics).  
  > ⚠️ **Do not share your API key publicly.**

- **Python dependencies** are listed in [`requirements.txt`](https://github.com/SMART-DIVE/DIVE/blob/main/requirements.txt).  
You can install them using:

  ```bash
  pip install -r requirements.txt
  ```
---
## 📁 Folder Structure
```
DIVE/
├── Datasets/                    # Generated datasets
│   ├── InitialCombinedData/     # Merged raw features before preprocessing
│   └── PreprocessedData/        # Cleaned, transformed datasets for ML
│
├──Docs/
│   ├── initial-setup.md        # Step-by-step guide for project installation and configuration
│   └── usage.md                # Detailed documentation for using framework functions and scripts
│
├── Features/                    # Extracted features
│   ├── API-based/               # Features collected from Etherscan APIs
│   │   ├── AccountInfo/         # Account-level features
│   │   ├── ContractsInfo/       # Contract metadata from Etherscan
│   │   └── Opcodes/             # Opcode data from Etherscan
│   ├── FE-based/                # Feature engineering outputs
│   │   ├── ABI-based/           # Features extracted from ABI
│   │   ├── CodeMetrics/         # Code metric data
│   │   │   ├── CodeMetrics/     # Parsed metric values
│   │   │   └── Reports/         # Raw/edited Markdown metric reports
│   │   │       ├── EditedReports/
│   │   │       ├── OriginalReports/
│   │   │       └── Raw_CodeMetrics/
│   │   ├── Input-based/         # Features derived from the Input attribute
│   │   └── Opcode-based/        # Features derived from opcode-level analysis
│
├── Labels/                      # Ground-truth labels for contracts
│
├── RawData/                     # Data collected or downloaded
│   ├── Samples/                 # Extracted Solidity source code samples
│   ├── SamplesSummary/          # 
│   └── SC_Addresses/            # CSVs of smart contract addresses
│
├── Scripts/                             # Main processing and utility scripts
│
│   ├── FeatureExtraction/               # Scripts for extracting low-level features
│   │   ├── EVM_Opcodes/                 # Contains opcode-related resources
│   │   │   ├── EVM_Opcodes_*.xlsx       # Excel file(s) listing EVM opcodes and metadata
│   │   ├── ABI_FeatureExtraction.py     # Extracts features from ABI (Application Binary Interface)
│   │   ├── Bytecode_FeatureExtraction.py# Extracts bytecode-level features
│   │   ├── get_Bytecode.py              # Retrieves bytecode for contracts
│   │   ├── get_CodeMetrics.py           # Calls external tools (i.e., solidity-code-metrics) to compute code metrics
│   │   ├── get_OpcodesList.py           # Generates the EVM opcode reference list (EVM_Opcodes_*.xlsx)
│   │   └── Opcode_FeatureExtraction.py  # Extracts features from opcodes (e.g., opcode metrics) 
│
│   ├── FeatureSelection/                # Script for selecting relevant features for analysis/modeling
│   │   └── get_FilteredFeatures.py      # Applies feature selection (uses classification defined in Feature list.xlsx)
│
│   ├── apply_DataPreprocessing.py       # Cleans, normalizes, and transforms data
│   ├── apply_FeatureExtraction.py       # Coordinates the execution of multiple feature extraction steps
│   ├── construct_FinalData.py           # Merges feature sets and labels to construct the final dataset
│   ├── extract_SourceCodes.py           # Extracts Solidity source code (included in Etherscan API responses) 
│   ├── get_Addresses.py                 # Loads and filters smart contract addresses from input CSV files
│   ├── get_ContractFeatures.py          # Orchestrates retrieval of contract info from Etherscan
│   └── get_DataStatistics.py            # Generates summary statistics and visualizations for the dataset
│
├── Statistics/                  # Analysis outputs and statistical summaries
│
├── config.json                  # Configuration file for paths and API key
├── DIVE.ipynb                   # Interactive notebook for demonstrating the framework
├── Feature list.xlsx            # Documentation of features and their descriptions
├── LICENSE.md                   # License: CC BY-NC 4.0
├── README.md                    # Project overview and usage instructions
└── requirements.txt             # Python package dependencies
```

---
## 🧭 Getting Started

### 🔧 Initial Setup

- See full instructions in [Docs/initial-setup.md](https://github.com/SMART-DIVE/DIVE/blob/main/Docs/initial-setup.md)

### 🛠️ Using Framework Functions

- Each function is explained in detail in [Docs/usage.md](https://github.com/SMART-DIVE/DIVE/blob/main/Docs/usage.md)

---

## 🎥 Demo
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
