//SPDX-License-Identifier: MIT
pragma solidity 0.8.7;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract HonestStaking is Ownable {
    IERC20 public rewardsToken;
    IERC20 public stakingToken;

    uint public rewardRate = 100;
    uint public lastUpdateTime;
    uint public rewardPerTokenStored;

    mapping(address => uint) public userRewardPerTokenPaid;
    mapping(address => uint) public rewards;

    uint private _totalSupply;
    mapping(address => uint) private _balances;

    constructor(){}

    function setStakingAndRewardTokens(address _stakingToken, address _rewardsToken) public {
        stakingToken = IERC20(_stakingToken);
        rewardsToken = IERC20(_rewardsToken);
    }

    function rewardPerToken() public view returns (uint) {
        if (_totalSupply == 0) {
            return rewardPerTokenStored;
        }
        return
            rewardPerTokenStored +
            (((block.timestamp - lastUpdateTime) * rewardRate * 1e18) / _totalSupply);
    }

    function earned(address account) public view returns (uint) {
        return
            ((_balances[account] *
                (rewardPerToken() - userRewardPerTokenPaid[account])) / 1e18) +
            rewards[account];
    }

    modifier updateReward(address account) {
        rewardPerTokenStored = rewardPerToken();
        lastUpdateTime = block.timestamp;

        rewards[account] = earned(account);
        userRewardPerTokenPaid[account] = rewardPerTokenStored;
        _;
    }

    function stake(uint _amount) external updateReward(msg.sender) {
        _totalSupply += _amount;
        _balances[msg.sender] += _amount;
        stakingToken.transferFrom(msg.sender, address(this), _amount);
    }

    function withdraw(uint _amount) external updateReward(msg.sender) {
        _totalSupply -= _amount;
        _balances[msg.sender] -= _amount;
        stakingToken.transfer(msg.sender, _amount);
    }

    function getReward() external updateReward(msg.sender) {
        uint reward = rewards[msg.sender];
        rewards[msg.sender] = 0;
        rewardsToken.transfer(msg.sender, reward);
    }


    function kill() public {
        selfdestruct(payable(msg.sender));
    }
}


// contract HonestStaking is ERC20 {

//     IERC20 public stakedToken; 

//     mapping(address => uint256) public amountStaked;

//     constructor () ERC20("stakedHonestToken", "stHONEST"){}

//     function setStakingToken(IERC20 stakedTokenAddress) public {
//         stakedToken = stakedTokenAddress;
//     }

//     function stake(uint256 amount) public {
//         amountStaked[msg.sender] += amount;
//         stakedToken.transferFrom(msg.sender, address(this), amount);
//     }

//     function checkStakedBalance() public view returns (uint256) {
//         return stakedToken.balanceOf(address(this));
//     }

//     function kill() public {
//         selfdestruct(payable(msg.sender));
//     }
// }