//SPDX-License-Identifier: MIT
pragma solidity 0.8.7;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract RewardToken is ERC20 {
    constructor() ERC20("RewardToken", "REWARD") {}

    function mint(address to, uint256 amount) public {
        _mint(to, amount);
    }
}
