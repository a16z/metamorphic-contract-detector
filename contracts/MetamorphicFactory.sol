//SPDX-License-Identifier: MIT
pragma solidity 0.8.7;
import {Create2} from "@openzeppelin/contracts/utils/Create2.sol";

// source code from https://ethereum-blockchain-developer.com/110-upgrade-smart-contracts/12-metamorphosis-create2/

// I replaced the CREATE2 address calculation with the OpenZeppelin library for readability

contract MetamorphicFactory {
    mapping(address => address) _implementations;

    event Deployed(address _addr);

    // simple deploy
    function deploy(uint256 salt, bytes calldata bytecode) public {
        bytes memory implInitCode = bytecode;

        // assign the initialization code for the metamorphic contract.
        bytes memory metamorphicCode = (
            hex"5860208158601c335a63aaf10f428752fa158151803b80938091923cf3"
        );

        // determine the address of the metamorphic contract.
        address metamorphicContractAddress = _getMetamorphicContractAddress(
            salt,
            metamorphicCode
        );

        // declare a variable for the address of the implementation contract.
        address implementationContract;

        // load implementation init code and length, then deploy via CREATE.
        /* solhint-disable no-inline-assembly */
        assembly {
            let encoded_data := add(0x20, implInitCode) // load initialization code.
            let encoded_size := mload(implInitCode) // load init code's length.
            implementationContract := create(
                // call CREATE with 3 arguments.
                0, // do not forward any endowment.
                encoded_data, // pass in initialization code.
                encoded_size // pass in init code's length.
            )
        } /* solhint-enable no-inline-assembly */

        //first we deploy the code we want to deploy on a separate address
        // store the implementation to be retrieved by the metamorphic contract.
        _implementations[metamorphicContractAddress] = implementationContract;

        address addr;
        assembly {
            let encoded_data := add(0x20, metamorphicCode) // load initialization code.
            let encoded_size := mload(metamorphicCode) // load init code's length.
            addr := create2(0, encoded_data, encoded_size, salt)
        }

        require(
            addr == metamorphicContractAddress,
            "Failed to deploy the new metamorphic contract."
        );

        emit Deployed(addr);
    }

    /**
     * @dev Deploy a metamorphic contract by submitting a given salt or nonce
     * along with the initialization code for the metamorphic contract, and
     * optionally provide calldata for initializing the new metamorphic contract.
     * To replace the contract, first selfdestruct the current contract, then call
     * with the same salt value and new initialization code (be aware that all
     * existing state will be wiped from the existing contract). Also note that
     * the first 20 bytes of the salt must match the calling address, which
     * prevents contracts from being created by unintended parties.
     * @param salt bytes32 The nonce that will be passed into the CREATE2 call and
     * thus will determine the resulant address of the metamorphic contract.
     * @param implementationContractInitializationCode bytes The initialization
     * code for the implementation contract for the metamorphic contract. It will
     * be used to deploy a new contract that the metamorphic contract will then
     * clone in its constructor.
     * @param metamorphicContractInitializationCalldata bytes An optional data
     * parameter that can be used to atomically initialize the metamorphic
     * contract.
     */
    function deployMetamorphicContract(
        uint256 salt,
        bytes calldata implementationContractInitializationCode,
        bytes calldata metamorphicContractInitializationCalldata
    ) external payable {
        bytes memory metamorphicCode = (
            hex"5860208158601c335a63aaf10f428752fa158151803b80938091923cf3"
        );

        // move implementation init code and initialization calldata to memory.
        bytes memory implInitCode = implementationContractInitializationCode;
        bytes memory data = metamorphicContractInitializationCalldata;

        // move the initialization code from storage to memory.
        bytes memory initCode = metamorphicCode;

        // declare variable to verify successful metamorphic contract deployment.
        address deployedMetamorphicContract;

        // determine the address of the metamorphic contract.
        address metamorphicContractAddress = _getMetamorphicContractAddress(
            salt,
            initCode
        );

        // declare a variable for the address of the implementation contract.
        address implementationContract;

        // load implementation init code and length, then deploy via CREATE.
        /* solhint-disable no-inline-assembly */
        assembly {
            let encoded_data := add(0x20, implInitCode) // load initialization code.
            let encoded_size := mload(implInitCode) // load init code's length.
            implementationContract := create(
                // call CREATE with 3 arguments.
                0, // do not forward any endowment.
                encoded_data, // pass in initialization code.
                encoded_size // pass in init code's length.
            )
        } /* solhint-enable no-inline-assembly */

        require(
            implementationContract != address(0),
            "Could not deploy implementation."
        );

        // store the implementation to be retrieved by the metamorphic contract.
        _implementations[metamorphicContractAddress] = implementationContract;

        // load metamorphic contract data and length of data and deploy via CREATE2.
        /* solhint-disable no-inline-assembly */
        assembly {
            let encoded_data := add(0x20, initCode) // load initialization code.
            let encoded_size := mload(initCode) // load the init code's length.
            deployedMetamorphicContract := create2(
                // call CREATE2 with 4 arguments.
                0, // do not forward any endowment.
                encoded_data, // pass in initialization code.
                encoded_size, // pass in init code's length.
                salt // pass in the salt value.
            )
        } /* solhint-enable no-inline-assembly */

        // ensure that the contracts were successfully deployed.
        require(
            deployedMetamorphicContract == metamorphicContractAddress,
            "Failed to deploy the new metamorphic contract."
        );

        // initialize the new metamorphic contract if any data or value is provided.
        if (data.length > 0 || msg.value > 0) {
            /* solhint-disable avoid-call-value */
            (bool success, ) = deployedMetamorphicContract.call{
                value: msg.value
            }(data);
            /* solhint-enable avoid-call-value */

            require(
                success,
                "Failed to initialize the new metamorphic contract."
            );
        }

        emit Deployed(deployedMetamorphicContract);
    } /* solhint-enable function-max-lines */

    /**
     * @dev Internal view function for calculating a metamorphic contract address
     * given a particular salt.
     */
    function _getMetamorphicContractAddress(
        uint256 salt,
        bytes memory metamorphicCode
    ) internal view returns (address) {
        return
            Create2.computeAddress(
                bytes32(salt),
                keccak256(abi.encodePacked(metamorphicCode)),
                address(this)
            );
    }

    function getMetamorphicContractAddress(uint256 salt)
        external
        view
        returns (address)
    {
        bytes memory mmCode = (
            hex"5860208158601c335a63aaf10f428752fa158151803b80938091923cf3"
        );
        return
            Create2.computeAddress(
                bytes32(salt),
                keccak256(abi.encodePacked(mmCode)),
                address(this)
            );
    }

    //those two functions are getting called by the metamorphic Contract
    function getImplementation()
        external
        view
        returns (address implementation)
    {
        return _implementations[msg.sender];
    }
}
