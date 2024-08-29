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
* Edit <A Href="https://github.com/DigVulSC/DigVulSC/blob/main/Scripts/config.json">Scripts/config.json</A> file to add your API-Key.
* Add the csv file containing the contract addresses to the <A Href="https://github.com/DigVulSC/DigVulSC/tree/main/RawData/SC_Addresses">RawData/SC_Addresses</A> folder.
* The DigVulSC framework is designed to read/write specific folders. It also targets certain columns to get contract addresses or data labels. If required, you can edit the configuration file (<A Href="https://github.com/DigVulSC/DigVulSC/blob/main/Scripts/config.json">Scripts/config.json</A>) to meet your requirements.
## Demo
* 
