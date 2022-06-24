//SPDX-License-Identifier: MIT
pragma solidity 0.8.7;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract HonestERC20 is ERC20 {
    constructor() ERC20("HonestToken", "HONEST") {}

    function mint(address to, uint256 amount) public {
        _mint(to, amount);
    }
}
