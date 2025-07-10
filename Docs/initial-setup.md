## 🔧 Initial Setup

Follow these steps to set up and run the **DIVE framework**:

---

### 1. **Clone the repository:**
```bash
      git clone https://github.com/SMART-DIVE/DIVE.git
```

### 2. **Add your API key**
* Edit [`config.json`](https://github.com/SMART-DIVE/DIVE/blob/main/config.json)
```json
"Etherscan_Account": 
    {
        "API_Key": "Your API Key"
    }
```

### 3. **Add contract addresses**
* Place your CSV file in [`RawData/SC_Addresses`](https://github.com/SMART-DIVE/DIVE/tree/main/RawData/SC_Addresses) folder.

> The DIVE framework is designed to read/write specific folders. It extracts contract addresses from specific columns as defined in the configuration file. If required, edit [`config.json`](https://github.com/SMART-DIVE/DIVE/blob/main/config.json) to meet your requirements.

### 4. **Edit the pipeline configuration**
Open and edit [`DIVE_pipeline.yaml`](https://github.com/SMART-DIVE/DIVE/blob/main/DIVE_pipeline.yaml) to configure the pipeline steps (e.g., selected feature extractors, filenames, etc.).

### 5. **Run the pipeline**
You can run the full pipeline ([`run_DIVE_Pipeline.py`](https://github.com/SMART-DIVE/DIVE/blob/main/run_DIVE_Pipeline.py)) in two ways:
- From a Python environment:
  ```Python
        !python3 run_DIVE_Pipeline.py DIVE_pipeline.yaml
  ```
- From the command line (CLI):
  ```bash
        python3 run_DIVE_Pipeline.py DIVE_pipeline.yaml
  ```
### ⚙️ **Optional: Use individual scripts**
> To use any script independently, import it into your Python code.
```python
from Scripts.get_Addresses import get_Addresses
from Scripts.get_ContractFeatures import get_ContractFeatures
from Scripts.get_CodeMetrics import get_CodeMetrics
from Scripts.construct_FinalData import construct_FinalData
from Scripts.get_DataStatistics import get_DataStatistics
from Scripts.extract_SourceCodes import extract_SourceCodes
```
> 🔍 **For detailed usage instructions**, refer to the [usage guide](https://github.com/SMART-DIVE/DIVE/blob/main/Docs/usage.md).  
> 📓 **For an interactive walkthrough**, see the [DIVE Template Notebook](https://github.com/SMART-DIVE/DIVE/blob/main/DIVE.ipynb).
