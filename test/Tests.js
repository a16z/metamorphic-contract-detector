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

        // get deterministic metamorphic conctract address
        METAMORPHIC_CONTRACT_ADDRESS = await MetamorphicFactory.getMetamorphicContractAddress(SALT)

        // deploy staking Honest ERC20 token and rewards token contract
        HonestERC20 = await deployContract("HonestERC20")
        RewardToken = await deployContract("RewardToken")

        // mint Reward tokens to staking contract so it has a positive balance 
        RewardToken.mint(METAMORPHIC_CONTRACT_ADDRESS, 1000000000)

        // deploy metamorphic contract factory
        MetamorphicFactory = await deployContract("MetamorphicFactory")

        // get contract factory for honest and bad staking contracts
        HonestStaking = await ethers.getContractFactory("HonestStaking");
        EvilStaking = await ethers.getContractFactory("EvilStaking");


        

    })

    describe("Simple Tests", function(){
        this.timeout(0)

        it("Mint ERC20 tokens", async()=>{
            await HonestERC20.mint(owner, 1000)

            let balance = await HonestERC20.balanceOf(owner)
            expect(balance == 1000)
        })


        it("Deploy an Honest Staking Contract", async()=>{

            let metamorphicContractInitCode = HonestStaking.interface.encodeFunctionData("setStakingAndRewardTokens", [HonestERC20.address, RewardToken.address])
            await MetamorphicFactory.deployMetamorphicContract(SALT, HonestStaking.bytecode,metamorphicContractInitCode )

            // set staking token address in the metamorphic contranct
            let honestContract = new Contract(METAMORPHIC_CONTRACT_ADDRESS, HonestStaking.interface, accounts[0])
            let a = await honestContract.rewardsToken()
            console.log(a)
            // await honestContract.setStakingToken(HonestERC20.address)

            // // check token address set properly
            // let stakingToken = await honestContract.stakingToken()
            // expect(stakingToken == HonestERC20.address)
        })


        // it("stake tokens in the Honest Staking Contract", async()=>{

        //     // set staking token address in the metamorphic contranct
        //     let honestContract = new Contract(METAMORPHIC_CONTRACT_ADDRESS, HonestStaking.interface, accounts[0])
            
        //     // approve ERC20 to transfer
        //     await HonestERC20.approve(METAMORPHIC_CONTRACT_ADDRESS, 1000)

        //     // stake tokens in HonestERC20
        //     await honestContract.approveAndStake(1000)

        //     // check staking contract balance updated
        //     let balance = await honestContract.checkStakedBalance()
        //     expect(balance == 1000)
        // })



        // it("kill the HonestStaking contract but check that its balance is still 1000 in honestERC20 contract", async()=>{

        //     // set staking token address in the metamorphic contranct
        //     let honestContract = new Contract(METAMORPHIC_CONTRACT_ADDRESS, HonestStaking.interface, accounts[0])


        //     // self destruct honest staking contract
        //     await honestContract.kill()

        //     // check that according to HonestERC20, the balance of destroyed contract is still 1000
        //     let balance = await HonestERC20.balanceOf(METAMORPHIC_CONTRACT_ADDRESS)
        //     expect(balance == 1000)

        // })



        // it("deploy the BadStaking contract to replace the HonestStaking contract", async()=>{

        //     await MetamorphicFactory.deploy(SALT, BadStaking.bytecode)

        //     // set staking token address in the metamorphic contranct
        //     let badContract = new Contract(METAMORPHIC_CONTRACT_ADDRESS, BadStaking.interface, accounts[0])
        //     await badContract.setStakingToken(HonestERC20.address)
            

        //     // check bad staking contract still has a balance of 1000 HonestERC20s
        //     let balance = await badContract.checkStakedBalance()
        //     expect(balance == 1000)

        // })



        // it("rug tokens in the bad staking contract", async()=>{

        //     // set staking token address in the metamorphic contranct
        //     let badContract = new Contract(METAMORPHIC_CONTRACT_ADDRESS, BadStaking.interface, accounts[0])
            
        //     // steal all HonestERC20 tokens from the Bad Staking contract
        //     await badContract.rugTokens(owner)



        //     // check Bad staking contract now has a 0 balance of HonestERC20
        //     let balance = await badContract.checkStakedBalance()
        //     expect(balance == 0)
            

        //     // check that the ruggers balance is now 1000 HonestERC20 tokens
        //     let ruggerBalance = await HonestERC20.balanceOf(owner)
        //     expect(ruggerBalance == 1000)

        // })




    })
})