This tool is meant to bundle in a single file all dependencies of a given Solidity smart contract.

QANPlatform testnet allows developers to compile and deploy Solidity smart contracts by using its qvmtcl tool. As a requirement (and as a security recommendation), all dependencies of the contract have to be bundled into a single file in order for the tool to deploy the contract successfully.

The following logic has been implemented into this tool:
- The script accepts 3 parameters:
	1. The contract to be deployed (mandatory)
	2. The target file where the contract and all its dependencies will be deployed (mandatory)
	3. An optional parameter to specify the folder where the dependencies are located. By default, the script assumes the dependencies are installed globally and executes "npm root -g" to find the right location.
- The function resolve_imports finds all the import statements in the contract, add the content to the target file and for each one of the dependencies it does the same recursively, keeping track of already imported dependencies to avoid duplications and taking care of loops.
- Duplicated pragma statements are removed, keeping at the top only the one from the main contract file
- If you want to use import statements that refer to a specific version, the regex will need to be modified (by default versions are stripped)