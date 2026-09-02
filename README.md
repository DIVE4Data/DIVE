[![Paper](https://img.shields.io/badge/Paper-Scientific%20Data-blue)](https://doi.org/10.1038/s41597-026-07025-5)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18779606.svg)](https://doi.org/10.5281/zenodo.18779606)
[![GitHub release](https://img.shields.io/github/v/release/DIVE4Data/DIVE)](https://github.com/DIVE4Data/DIVE/releases)
[![GitHub Downloads](https://img.shields.io/github/downloads/DIVE4Data/DIVE/total)](https://github.com/DIVE4Data/DIVE/releases)
[![License](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](LICENSE.md)
[![GitHub stars](https://img.shields.io/github/stars/DIVE4Data/DIVE?style=social)](https://github.com/DIVE4Data/DIVE/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/DIVE4Data/DIVE?style=social)](https://github.com/DIVE4Data/DIVE/network/members)

# DIVE Framework  
*A blockchain digging framework for constructing vulnerability-tagged smart contract datasets.*

---

## 🔍 Key Features

The DIVE framework provides a powerful pipeline for blockchain dataset creation through six core components:

---

### 1. 🧾 Feature Collection  
Fetch smart contract and account data from public blockchains.  
- ✅ Currently supports [`Ethereum`](https://ethereum.org/en/).  
- 🔗 Uses [`Etherscan.io`](https://etherscan.io/) as a data source.  
- 📊 Collects:
  - Contract metadata  
  - Account-level information  
  - Opcodes  

### 2. 🧠 Solidity Code Extraction  
Retrieve and store verified contract source code as `.sol` files using [`Solidity`](https://soliditylang.org/).

### 3. 🧪 Feature Extraction  
Extract structured features from various smart contract attributes, including: `ABI`, `Timestamp`, `Library`, `TransactionIndex`, `Code Metrics`, `Input` / `Bytecode`, and `Opcode`

### 4. 🏷️ Labeled Data Construction  
Merge extracted features with ground-truth vulnerability labels to build a structured dataset.

### 5. 🧹 Data Preprocessing  
Clean, normalize, and transform the data to prepare it for downstream analysis or machine learning tasks.

### 6. 📊 Statistical Analysis & Visualization  
Generate statistical summaries and visualizations to better understand the dataset's structure and characteristics.

---


## 📦 Requirements

- [`Python`](https://www.python.org/) = **3.12.2**  
- [`solidity-code-metrics`](https://classic.yarnpkg.com/en/package/solidity-code-metrics) = **0.0.26**
  > Install using one of the following:
  ```bash
  # Using Yarn
  yarn global add solidity-code-metrics@0.0.26
  
  # Or using npm
  npm install -g solidity-code-metrics@0.0.26
  ```
 
- 🔑 Etherscan API Key  
  > Create an account at [`Etherscan.io`](https://etherscan.io/) and follow their [`API key guide`](https://docs.etherscan.io/getting-started/viewing-api-usage-statistics).  
  > ⚠️ **Do not share your API key publicly.**

- **Python dependencies** are listed in [`requirements.txt`](https://github.com/DIVE4Data/DIVE/blob/main/requirements.txt).  
You can install them using:

  ```bash
  pip install -r requirements.txt
  ```
---
## 📁 Repository Structure
```
DIVE/
├── Datasets/                    # Generated datasets
│   ├── InitialCombinedData/     # Merged raw features before preprocessing
│   └── PreprocessedData/        # Cleaned, transformed datasets for ML
│
├── Docs/
│   ├── initial-setup.md        # Step-by-step guide for project installation and configuration
│   └── usage.md                # Detailed documentation for using framework functions and scripts
│
├── Features/                    # Extracted features
│   ├── API-based/               # Features collected from Etherscan APIs
│   │   ├── AccountInfo/         # Account-level features
│   │   ├── BlockInfo/           # Block transaction counts
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
│   │   ├── Library-based/       # Features derived from the Library attribute
│   │   ├── Opcode-based/        # Features derived from opcode-level analysis
│   │   ├── Timestamp-based/     # Features derived from the Timestamp attribute
│   │   └── TransactionIndex/    # Features derived from the TransactionIndex attribute
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
│   │   ├── get_CodeMetrics.py           # Calls external tools (i.e., solidity-code-metrics) to compute code metrics
│   │   ├── get_OpcodesList.py           # Generates the EVM opcode reference list (EVM_Opcodes_*.xlsx)
│   │   ├── Library_FeatureExtraction.py # Extracts library-based features
│   │   ├── Opcode_FeatureExtraction.py  # Extracts features from opcodes (e.g., opcode metrics)
│   │   ├── Timestamp_FeatureExtraction.py # Extracts timestamp-based features
│   │   └── transactionIndex_FeatureExtraction.py # Extracts transactionIndex-based features
│
│   ├── FeatureSelection/                # Script for selecting relevant features for analysis/modeling
│   │   └── get_FilteredFeatures.py      # Applies feature selection (uses classification defined in Feature list.xlsx)
│
│   ├── apply_DataPreprocessing.py       # Cleans, normalizes, and transforms data
│   ├── apply_FeatureExtraction.py       # Coordinates the execution of multiple feature extraction steps
│   ├── construct_FinalData.py           # Merges feature sets and labels to construct the final dataset
│   ├── extract_SourceCodes.py           # Extracts Solidity source code (included in Etherscan API responses) 
│   ├── get_Addresses.py                 # Loads and filters smart contract addresses from input CSV files
│   ├── get_BlockFeatures.py             # Retrieves transaction counts for each block
│   ├── get_ContractFeatures.py          # Orchestrates retrieval of contract info from Etherscan
│   └── get_DataStatistics.py            # Generates summary statistics and visualizations for the dataset
│
├── Statistics/                  # Analysis outputs and statistical summaries
│
├── CITATION.cff                 # Citation metadata for the DIVE framework and publication
├── config.json                  # Configuration file for paths and API key
├── DIVE_pipeline.yaml           # YAML config defining the full data creation pipeline execution
├── DIVE.ipynb                   # Interactive notebook for demonstrating the framework
├── Feature list.xlsx            # Documentation of features and their descriptions
├── LICENSE.md                   # License: CC BY-NC 4.0
├── README.md                    # Project overview and usage instructions
├── requirements.txt             # Python package dependencies
└── run_DIVE_Pipeline.py         # Entrypoint to run the entire pipeline as a script
```

---
## 🧭 Getting Started

### 🔧 Initial Setup

- See full instructions in [`Docs/initial-setup.md`](https://github.com/DIVE4Data/DIVE/blob/main/Docs/initial-setup.md)

### 🛠️ Using Framework Functions

- Each function is explained in detail in [`Docs/usage.md`](https://github.com/DIVE4Data/DIVE/blob/main/Docs/usage.md)

---
## 📚 Publication

The DIVE dataset and its framework are described in the following publication:

**Alsunaidi, S. J., Aljamaan, H., & Hammoudeh, M. (2026).**  
*DIVE: A Multi-Label Smart Contract Vulnerability Dataset.*  
**Scientific Data, 13**, 664.  
https://doi.org/10.1038/s41597-026-07025-5

If you use the DIVE dataset or its framework in your research, please cite:

```bibtex
@article{alsunaidi2026dive,
  title   = {DIVE: A Multi-Label Smart Contract Vulnerability Dataset},
  author  = {Alsunaidi, Shikah J. and Aljamaan, Hamoud and Hammoudeh, Mohammad},
  journal = {Scientific Data},
  volume  = {13},
  pages   = {664},
  year    = {2026},
  doi     = {10.1038/s41597-026-07025-5},
  url     = {https://doi.org/10.1038/s41597-026-07025-5}
}
```
### 📦 Archived Resources

The DIVE framework and dataset are archived on Zenodo:

- **DIVE Framework:** [https://doi.org/10.5281/zenodo.18779606](https://doi.org/10.5281/zenodo.18779606)
- **DIVE Dataset:** [https://doi.org/10.5281/zenodo.18519253](https://doi.org/10.5281/zenodo.18519253)
---

## 📦 License

This project is licensed under the [`Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0)`](https://creativecommons.org/licenses/by-nc/4.0/).

🚫 **Patent Rights Reserved**  
* This project may be covered by pending or granted patents. The authors reserve all rights under applicable patent laws.  
* The use of this software does **not grant any rights to use patented inventions**.  
* For commercial licensing or patent-related inquiries, please contact the authors directly.

**🛡️ Disclaimer**
* DIVE is provided as a research tool and is under active development. While we strive for reliability, we do not provide warranties or guarantees. Please use it responsibly and at your own discretion.
