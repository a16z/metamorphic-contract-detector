//SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.2;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract HonestERC20 is ERC20 {
    constructor() ERC20("HonestToken", "HONEST") {}

    function mint(address to, uint256 amount) public {
        _mint(to, amount);
    }
}
