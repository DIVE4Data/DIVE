# DigVulSC
A Blockchain digging framework and constructing vulnerability-tagged smart contract datasets.
## Features
The DigVulSC framework provides several functions through the following components:
* **Feature Collecting:** This component enables fetching information about the smart contract and its account from a public Blockchain network. Currently, it only supports the <A Href="https://ethereum.org/en/">Ethereum</A> Blockchain. It makes use of <A Href="https://etherscan.io/">Etherscan.io</A>, an Ethereum Blockchain Explorer, to obtain Ethereum block data. This component can collect three distinct feature sets: (1) Contract information. (2) Account information. (3) Opcodes.
* **Solidity Codes Extraction:** This component assists in extracting the contract's source code and creating the <A Href="https://soliditylang.org/">Solidity</A> code file.
* **Code Metrics Generation:** This component extracts useful code metrics by analyzing the contract's source code. It makes use of the <A Href="https://classic.yarnpkg.com/en/package/solidity-code-metrics">Solidity Code Metrics</A>, an open-source package, to generate an analysis markdown report that contains different useful information including the code metrics.
* **Labeled Data Construction:**
* **Statistical Data Generation:**
## Requirements
*  <A Href="https://www.python.org/">Python</A> >=3.12.2
## Usage
* 
## Demo
* 
