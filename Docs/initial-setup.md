# 🔧 Initial Setup

1. **Clone the repository:**
```bash
      git clone https://github.com/SMART-DIVE/DIVE.git
```

2. **Add your API key**
* Edit [`config.json`](https://github.com/SMART-DIVE/DIVE/blob/main/config.json)
```json
"Etherscan_Account": 
    {
        "API_Key": "Your API Key"
    }
```

3. **Add contract addresses**
* Place your CSV file in [`RawData/SC_Addresses`](https://github.com/SMART-DIVE/DIVE/tree/main/RawData/SC_Addresses) folder.

> The DIVE framework is designed to read/write specific folders. It extracts contract addresses from specific columns as defined in the configuration file. If required, edit [`config.json`](https://github.com/SMART-DIVE/DIVE/blob/main/config.json) to meet your requirements.

4. **To utilize any script, first import it into your Python code:**
```python
from Scripts.get_Addresses import get_Addresses
from Scripts.get_ContractFeatures import get_ContractFeatures
from Scripts.get_CodeMetrics import get_CodeMetrics
from Scripts.construct_FinalData import construct_FinalData
from Scripts.get_DataStatistics import get_DataStatistics
from Scripts.extract_SourceCodes import extract_SourceCodes
```