INTRO = """
A critical Ethereum security assumption is that smart contract code is immutable and therefore cannot be changed once it is deployed on the blockchain. In practice, some smart contracts can change – even after they’ve been deployed. 

Metamorphic smart contracts are mutable, meaning developers can change the code inside them. These smart contracts pose a serious risk to web3 users who put their trust in code that they expect to run with absolute consistency, especially as bad actors can exploit this shape-shifting ability. 

Anyone can use this tool to check whether a given contract exhibits red flags that could indicate the potential for metamorphism. The method is not fool-proof: just because a smart contract shows a flag, doesn’t mean it’s necessarily metamorphic; and just because it doesn’t, doesn’t mean it’s safe. The checker merely offers a quick initial assessment that a contract might be metamorphic based on possible indicators. 
"""

DETECTING_METAMORPHIC_CONTRACTS_DROPDOWN = """
The Detector analyzes six properties that may indicate if a smart contract is metamorphic.

1. **Was known metamorphic code used to deploy the contract?** If known metamorphic bytecode – the lower-level, virtual machine-readable code that Ethereum smart contracts, typically written in Solidity, turn into after getting compiled – shows up in a transaction for a given smart contract’s deployment, that’s a major red flag. In the sections that follow, we’ll discuss one such example of metamorphic bytecode developed by 0age. An important caveat: There are potentially innumerable variations of metamorphic bytecode, which makes detecting all varieties difficult. By scanning for well-known instances though, the detector eliminates low-hanging fruit for attackers who are merely copying and pasting existing examples.

2. **Can the smart contract code self-destruct?** To replace the code in a contract – a key step in creating a metamorphic contract – a developer first needs to delete pre-existing code. The only way to do this is by using the [SELFDESTRUCT opcode](https://docs.soliditylang.org/en/v0.8.13/introduction-to-smart-contracts.html?highlight=selfdestruct#deactivate-and-self-destruct), a command that does exactly what it sounds like; that is, it erase all code and storage at a given contract address. The presence of self-destructing code in a contract does not prove that it is metamorphic; however, it offers a clue that the contract might be metamorphic and it’s worth knowing, anyway, whether contracts you’re relying on can nuke themselves.

3. **Does the smart contract call in code from elsewhere?** If the smart contract in question can't directly self-destruct, it may still be able to erase itself by using the [DELEGATECALL opcode](https://docs.soliditylang.org/en/v0.8.13/introduction-to-smart-contracts.html?highlight=delegatecall#delegatecall-callcode-and-libraries). This opcode allows a smart contract dynamically to load and execute code that lives inside another smart contract. Even if the smart contract doesn't contain the SELFDESTRUCT opcode, it can use DELEGATECALL to load self-destructing code from somewhere else. While the DELEGATECALL functionality does not directly indicate if a smart contract is metamorphic, it is a possible clue – and potential security issue – that’s worth noting. Be warned that this indicator has the potential to raise many false positives. 

4. **Did another contract deploy this contract?** Metamorphic contracts can be deployed only by other smart contracts. This is because metamorphic contracts are enabled by another opcode, usable only by other smart contracts, called CREATE2. (We’ll discuss CREATE2 – how it works and why it matters – more in a later section.) This trait is one of the least conspicuous indicators of possible metamorphism; it is a necessary but insufficient precondition. Scanning for this trait is likely to raise many false positives – but it is valuable information to know as it can raise suspicions and provide a reason to scrutinize a contract further, especially if the smart contract contains the opcode described below.

5. **Does the deployer contract contain the CREATE2 opcode?** As mentioned above, deployment via CREATE2 is an essential precondition for metamorphism. If a deployer contract contains the CREATE2 opcode, that may indicate that it used CREATE2 to deploy the contract in question. If the deployer did indeed use CREATE2 to deploy said contract, while that doesn’t mean the contract is necessarily metamorphic, it does mean that it might be metamorphic and it may be wise to proceed with caution and investigate further. Again, beware false positives; [CREATE2](https://blog.openzeppelin.com/getting-the-most-out-of-create2/) has plenty of [legitimate uses](https://blog.goodaudience.com/one-weird-trick-to-fix-user-on-boarding-d54b7ff9d711), including bolstering [“Layer 2” scaling solutions](https://eips.ethereum.org/EIPS/eip-1014) and making it easier to create smart contract wallets that can improve web3 [user-onboarding](https://blog.openzeppelin.com/getting-the-most-out-of-create2/) and key recovery options.

6. **Did the code change?** This is the most obvious tell, but it will only show up after a metamorphic contract has already morphed. If the smart contract’s code hash – a unique, cryptographic identifier – is different than it was when the contract was initially deployed, then it’s likely the code was removed, replaced, or altered. If the hashes no longer match, then something about the code has changed and the contract might be metamorphic. This flag is the surest indicator of metamorphism, but it won’t help predict or preempt the metamorphosis since it only checks that it already happened.

It’s worth reiterating once again: This detector tool is not fool-proof. The flags it catches aren’t all telltale signs of metamorphic potential, but they do offer clues. Identifying these flags is just the first step in a more thorough inquiry. That’s why we expanded the Detector to search for flags that could easily generate false positives, like the presence of CREATE2 or DELEGATECALL opcodes. If you have suggestions for improving the tool or want to build on or add to this initial work, get in touch with me at mblau@a16z.com.

In addition to building a simple command line tool for the Metamorphic Contract Detector, 
I built some example smart contracts that demonstrate a scam metamorphic contract staking scenario, which I describe in the next section. 
All the code is available in this [GitHub repository](https://github.com/a16z/metamorphic-contract-detector). 
"""

MALICIOUS_EXAMPLE_DROPDOWN = """
Here is how someone might use a metamorphic smart contract as part of a scam. 

First is the setup phase. The attacker deploys a smart contract at a specific address on the blockchain using two tools: metamorphic bytecode and the CREATE2 opcode. (We’ll expand on both of these concepts later.) The metamorphic bytecode then does what its name suggests and “morphs.” Here, it changes into a [staking contract](https://twitter.com/_PorterSmith/status/1508515257777590277) where users can stake ERC-20 tokens. (Again, we’ll discuss the details of this morphing trick later. Promise!)

Next comes the bait and switch. Unsuspecting users stake their tokens in this contract, lured by the possibility of earning a yield or some other perk. The attacker then deletes all the staking code and “state” – blockchain storage or memory – at this smart contract address using the [SELFDESTRUCT opcode](https://docs.soliditylang.org/en/v0.8.13/introduction-to-smart-contracts.html?highlight=selfdestruct#deactivate-and-self-destruct) discussed in the previous section. (It should be noted that the tokens – which exist as part of a separate ERC-20 contract – persist, unaffected by the self-destructed contract.)

Finally, the rug-pull. The attacker reuses the same metamorphic bytecode used in the setup phase to “redeploy” a new contract. This new contract deploys to the same address recently vacated by the self-destructing contract. This time, however, the bytecode “morphs” (again, we’ll explain how later) into a malicious contract that can steal all the tokens staked at the contract address. Scam complete. 

The risks that metamorphic smart contracts pose are by now plainly apparent. But you may still be wondering, how does this metamorphism trick actually work? To understand that, you have to probe deeper, to the bytecode-level. 
"""

CREATE2_DRODOWN_ONE = """
[CREATE2](https://docs.openzeppelin.com/cli/2.8/deploying-with-create2) is an opcode upgrade, [introduced to Ethereum](https://eips.ethereum.org/EIPS/eip-1014) in February 2019, that offers a new way to deploy smart contracts. 

CREATE2 gives developers more control over the deployment of their smart contracts than they previously had. The original CREATE opcode makes it difficult for developers to control the destination address for a to-be-deployed smart contract. With CREATE2, people can control and know the address of a particular smart contract in advance, before actually deploying it to the blockchain. This foreknowledge – plus some clever tricks – is what enables people to create metamorphic smart contracts. 

How can CREATE2 predict the future? The opcode’s calculation is deterministic: as long as the inputs do not change, the address determined by CREATE2 will not change. (Even the smallest change will cause the deployment to happen somewhere else.)

More granularly, CREATE2 is a function that combines and hashes together a few elements. First, it incorporates the address of the deployer (or sender): the initiating smart contract that acts as a parent to the one to be created. Next, it adds an arbitrary number provided by the sender (or “salt”), which allows the developer to deploy the same code to different addresses (by changing the salt) and prevents overwriting existing, identical contracts. Finally, it uses the keccak256 hash of some smart contract initialization (“init”) bytecode, which is the seed that turns into a new smart contract. This hashed-together combination determines an Ethereum address and then deploys the given bytecode to that address. As long as the bytecode remains exactly the same, CREATE2 will always deploy the given bytecode to the same address on the blockchain.

Here’s what the CREATE2 formula looks like. (Note: you’ll notice another element, a “0xFF,” in the example below. This is just a constant CREATE2 uses to [prevent collisions](https://eips.ethereum.org/EIPS/eip-1014) with the preceding CREATE opcode.)
"""

CREATE2_DROPDOWN_TWO = """
Now that we have a way to deploy code to a deterministic address, how is it possible to change the code at that same address? At first, this may seem impossible. If you want to deploy new code using CREATE2, the bytecode must change, and therefore, CREATE2 will deploy to a different address. But what if a developer constructed the bytecode in such a way that it could “morph” into different code when CREATE2 deploys a smart contract?
"""


STEP_BY_STEP_WALKTHROUGH_DROPDOWN_ONE = """
The recipe for turning a smart contract into a metamorphic contract calls for three smart contracts in total, each playing a unique role.

One of these necessary components is the Metamorphic Contract Factory, the brain of the operation. This “Factory” is responsible for deploying the Metamorphic Contract as well as another smart contract called the Implementation Contract, so named because its code eventually becomes implemented inside the Metamorphic Contract. A subtle choreography between these three contracts results in metamorphism, as depicted in the diagram below.
"""

STEP_BY_STEP_WALKTHROUGH_DROPDOWN_TWO = """
Let’s discuss each step, 1-7, in detail to illuminate the operations at work.

##### Step 1: A developer sets everything in motion
A coder designs some smart contract code – the Implementation Contract bytecode – that will eventually end up in the Metamorphic Contract. The developer sends this code to the Metamorphic Contract Factory, a smart contract whose main purpose is to deploy other smart contracts. This action sets the entire Metamorphic Contract creation process in motion. 
Everything that follows is a result of this initial step. Indeed, Steps 1 through 6 happen in one atomic transaction on the blockchain, meaning nearly all at once. These steps can be repeated over and over again, ad infinitum, to replace code inside the Metamorphic Contract and keep it continually morphing.


##### Step 2: Factory deploys Implementation Contract
The first contract the Factory deploys is the Implementation Contract, which contains implementation code. (Creative, we know.) Think of the Implementation Contract as a loading dock, or waypoint, that holds some code before it ships to its final destination, which will be, in this case, inside the Metamorphic Contract. 


##### Step 3: Factory stores Implementation Contract address
After its deployment to the blockchain, the Implementation Contract will necessarily exist at some blockchain address. The Factory stores this contract address in its own memory (to be used later, in Step 5). 


##### Step 4: Factory deploys Metamorphic Contract
The Factory deploys the Metamorphic Contract using CREATE2 and metamorphic bytecode. You can find a technical, in-depth walkthrough of how metamorphic bytecode works in the last dropdown below, but suffice it to say that when metamorphic bytecode executes, it copies code from some other on-chain location – in this case, from the Implementation Contract – into the Metamorphic Contract. As we talked about in the last section, since CREATE2 is deterministic – as long as the same sender, salt, and bytecode are used – then the Metamorphic Contract address stays the same no matter how many times these steps are repeated.

Below is an example of what metamorphic bytecode looks like, from the [metamorphic repo](https://github.com/0age/metamorphic) by 0age. This is just one example of metamorphic bytecode – potentially innumerable variations exist, vastly complicating the detection of metamorphic contracts.
"""

STEP_BY_STEP_WALKTHROUGH_DROPDOWN_THREE = """
##### Step 5: Metamorphic bytecode queries Factory for Implementation Contract address
The metamorphic bytecode asks the Factory for the Implementation Contract address (as stored in Step 3). It doesn’t matter if the address of the Implementation Contract changes as long as the metamorphic bytecode that asks for the address stays the same. Indeed, if the developer later deploys a new Implementation Contract – such as a malicious one designed to steal tokens – it will necessarily deploy at a different blockchain address, per Step 2. This has no impact on the Metamorphic Contract’s creation.


##### Step 6: Implementation Contract code gets copied into the Metamorphic Contract
Using the blockchain address learned in Step 5, the metamorphic bytecode locates the code in the Implementation Contract and copies that code into the Metamorphic Contract’s local storage. This is how the Metamorphic Contract shape-shifts: by copying code from the Implementation Contract. 


##### Step 7: Rinse and repeat
A developer can repeat Steps 1 through 6 over and over again and replace the code in the Metamorphic Contract with whatever they like by way of a new Implementation Contract. All that’s needed is to use the SELFDESTRUCT opcode – or, more deviously, DELEGATECALL opcodes that ultimately result in a SELFDESTRUCT – to remove the pre-existing code in the Metamorphic Contract. By repeating the cycle with new Implementation Contract bytecode, the Metamorphic Contract will, like magic, morph!

Using this technique, a clever developer can constantly shift the ground under web3 users’ feet. Consider, for example, the scam scenario again. A developer might first deploy the Implementation Contract with token-staking code that, through the circuitous path depicted in the graphic and elaborated in the steps above, ends up in the Metamorphic Contract. The scammer could later self-destruct this code and replace it by deploying a new Implementation Contract containing token-stealing code. 

Whatever gets deployed in the Implementation Contract will ultimately end up in the Metamorphic Contract. That’s the essence of the trick. 
"""


NEXT_STEPS = """
The existence of metamorphic contracts means it’s possible for web3 users to enter into contracts that can change at will – that’s why this threat is so important to understand and defend against. My Metamorphic Contract Detector is just a first step toward identifying metamorphic contracts by the sleight of hand they employ. There are several ways the Detector could be improved in the future. For example, by recursively checking the Factory (or deployer contract) that created the Metamorphic Contract, one could see if the Factory is itself metamorphic. This feature would be a useful addition to an upgraded version 2 of the Detector.

It’s worth reiterating once again: This detector tool is not fool-proof. The flags it catches aren’t all telltale signs of metamorphic potential, but they do offer clues. Identifying these flags is just the start for a more thorough inquiry. That’s why we expanded the Detector to search for flags that could easily generate false positives, like the presence of CREATE2 or DELEGATECALL opcodes. If you have suggestions for improving the tool or want to build on or add to this initial work, get in touch with me at mblau@a16z.com.
"""


BYTECODE_BREAKDOWN = """
Here is an opcode by opcode walkthrough of Metamorphic Init Code. This combines my own descriptions with [0age's](https://github.com/0age/metamorphic/blob/master/contracts/MetamorphicContractFactory.sol).

You can load these opcodes and comments directly into evm.codes and step through each opcode one at a time using this [link](<https://www.evm.codes/playground?unit=Wei&codeType=Mnemonic&code='%2F%2F%20ThQB%20opcodQexecuteJcodQthaFliveJaFa%20specified%20%3BJonqblockchain%5Egas%3A%20%C2%82inqcall%20toqspecified%20%3BJ%20~2.%20%3Bs%3AqETH%20%3BJyou%20arQcalling%20to~3.%20argsOffset%3A%20ThQstarting%20%C2%86ofqcalling%20smarF(FthaFcontainsqcall%40to%20send%20along%20i*your%20B~4.%20argSize%3A%20%C2%81qcall%40you%20arQsending%20i*B~5.%20retOffset%3A%20%C2%86wherQyou%20wanFto%20storQany%20%40%7Fby%20B~6.%20retSize%3A%20%C2%81q%7Fdata)~M%2BIniFCode%3A%200x5860208158601c335a63aaf10f428752fa158151803b80938091923cf3)~ThQfirsFsectio*of%20thiJiniFcodQpusheJ%40ontoq~stack%20thaFiJneeded%20for%60B%20toqm%2Bfactory%20(F)~%3C%20SECTION%201%20%3C)~push%600!%20)PCV0%3Eqnumber%2032!%20%7B0x20%20%3D%3D%2032%C2%88sizQof%20%40i*byteJthaF%7CbQ%7Fby%20B~%5C'retSize%23PUSH1%200x20V0j32%3E%600!.~ThiJisqindex%20i*(F%26wherQany%20%7F%40from%20B%20%7CbQstored~%5C'retOffset%23DUP2%20V0j32j0%3E%604!~thiJisq%C2%81qcall%40senFalong%20i*B~NOTE%3A%204%20byteJisqlength%20of%60%24.%20WQ%7CbQcalling%60functio*i*thiJB~%5C'argSize%23PCV0j32j0j4%3E%2028!%20%7B0x1c%20%3D%3D%2028%C2%88positio*ofq%24%20i*(Fmemory~thQreaso*for%2028%20iJbecausQyou%20storQ32%20byteJaFa%20timQi*memory~soqindex%20after%20storing%604%20bytQ%24%20%7CbQ28%20%7B32-4%7D.~seQhowq%40iJpadded%20by%20zeroJi*evm.codes~%5C'argsOffset%23PUSH1%200x1c%20V0j32j0j4j28%3Eqcaller%20%3BJonqstack~thiJwould%20beqfactory%20addesJthaFiJdeployingqm%2B(t~%5C'%3Bs%23CALLER%22%3Eq%C2%82along%20with%20B~%5C'gas%23GAS%22jgas%5D))~pushq%24!~thiJisqfirsF4%20byteJofqKeccak-256%20hash%20ofqfunctio*getI%3Fn%7B%7D%20inqfactory%20(t.~thiJisq%40you%20%7CstorQi*%26using%20MSTORE.)PUSH4%200xaaf10f42%20%22jgasj0xaaf10f42%3E%600!~thiJisqindex%20of%20wherQto%20storeq%24%20i*%26forqnexFMSTORE%20opcode)DUP8%22jgasj0xaaf10f42j0%5D)~storeq%24%20i*memory~againq%C2%86for%20wherQiF%7CbQiJ28%20%7BseQevm.codes%7D)MSTORE%22jgas%5D)~performqB%20using%20several%20valueJyou%20havQpushed!%20up%20until%20thiJpoint~thiJB%20%7Cfetchq(F%3BJthaFcontains~thQi%3F*codQyou%20%7Clater%20storQinqm%2B(t.%20)BV0j1%20%7Bif%20successful%7D%5D)))~%3C%20SECTION%202%20%3C~now%20thaFyou%20haveqi%3F*%3BJi*memory~copyq%C2%83FthaF%3BJintoqcurrenF(F%7BthQm%2B(t%7D~two%20mai*opcodeJi*thiJsectio*arQ%C2%84%20and%20%25)~ThQ%C2%84%20opcodQtakeJaJinpuFa%20(F%3BJand%20returnsqbytQsizQofqcodQaFthaF%3Bs~ThiJ%40iJneeded%20for%20%25)~ThQ%25%20opcodQcopiesqruntimQ%C2%83Fa%20specific%20%3BJand%20storeJiFi*memory%5E%3Bs%3A%2020-bytQ%3BJofq(FwhosQcodQyou%20wanFto%20copy%20into%20%26~2.%20destO%C2%87*%26whereqresulF%7CbQcopied.%20ThiJisq%26ofqm%2B(t.~3.%20o%C2%87nq%C2%85ofq%3BJwQarQcopying%20codQfrom~%20%20%20ThQ%C2%85isqarea%20of%20general%20Ethereum%20accounFstoragQwhereqruntimQcodQof%60smarF(FiJlocated.~%20%20%20Lear*morQhere%3A%20https%3A%2F%2Fwww.evm.codes%2Fabout~4.%20size%3A%20bytQsizQofqcodQto%20copy%20%7Byou%20geFthiJfrom%20%C2%84%7D))~flip%20succesJbiF%7Bo*top%20ofqstack%7D%20to%200)ISZEROV0j0%3E%20another%200!~thiJisqpositio*ofq%3BJfetched%20from%20B%20i*memory)DUP2V0j0j0%5D)~load%2032%20byteJof%20%40from%20index%200%20i*memory~thiJwould%20containq(F%3BJ%7FbyqB)MLOADV0j0j_%3Eq_!%20agai*for%20%25%20to%20consume)DUP1V0j0j_j_%5D)~retur*%C2%81%20%C2%83tq_~and%20push%20thiJvaluQontoqstack)%C2%84V0j0j_j(Fsize%5D)~manipulatQ%C2%89usQbyqRETURN%20opcodQatqend%20of%20thiJiniFcode)DUP1)SWAP4V(Fsizej0j_j(Fsizej0%5D%20%20%20)~push%200!~ThiJ0%20representsq%5C'o%C2%80%20and%20iFiJreferencingq%5C'code%5C'~regio*ofq_.~nextjreorder%20%C2%89%25)DUP1)SWAP2)SWAP3V(Fsizej0j(Fsizej0j0j_%5D%20)~executeq%25%20opcodQwhich%20clonesqruntimQcodQofqi%3F*(t~into%20%26aFpositio*0%20orq%5C'destO%C2%80)%25V(Fsizej0%5D%20)~RETURN%20to%20deployqfinal%20codQthaFiJcurrently%20i*%26~and%20effectively%20storeqi%3F*(FcodQatqm%2B(F%3Bs)RETURN'~)%2F%2F%20q%20thQj%2C%20_i%3F*(F%3BsV~STACK%3A%20%5BQe%20Js%20Ft%20BSTATICCALL*n%20)%5Cn(contrac!%20ontoqstack%22V0j32j0j4j28jfactory%20%3Bs%23%5C'%20inpuFto%20B)%24functio*selector%25EXTCODECOPY%26memory%20%2Betamorphic%20%3Baddres%3C%3D%3D%3D%3D%3D%3D%3D%3E%5D)~push%3Fmplementatio%40data%20%5E.~IFtakeJa%20few%20parameterJaJinput~1.%20%60%20a%20%7Cwill%20%7Freturned%20%C2%80ffset%5C'%20parameter%20of%20%25%C2%81sizQi*byteJof%C2%82amounFof%20gaJto%20send%20%C2%83codQstored%20a%C2%84EXTCODESIZE%C2%85%5C'code%5C'%20regio*%C2%86index%20i*%26%C2%87ffset%3AqbytQoffseFi%C2%88%20i*hex%7D.~thiJisq%C2%89stack%20itemJfor%20%01%C2%89%C2%88%C2%87%C2%86%C2%85%C2%84%C2%83%C2%82%C2%81%C2%80%7F%7C%60%5E%40%3F%3E%3C%3B%2B%26%25%24%23%22!()*BFJQV_jq~_>).

```c
// The STATICCALL opcode executes code that lives at a specified address on the blockchain.
// It takes a few parameters as input
// 1. gas: amount of gas to send in the call to the specified address  
// 2. address: the ETH address you are calling to
// 3. argsOffset: The starting index in memory of the calling smart contract that contains the calldata to send along in your STATICCALL
// 4. argSize: size in bytes of the calldata you are sending in STATICCALL
// 5. retOffset: index in memory where you want to store any data returned by STATICCALL
// 6. retSize: size in bytes of the returned data

// Metamorphic Init Code: 0x5860208158601c335a63aaf10f428752fa158151803b80938091923cf3

// The first section of this init code pushes data onto the 
// stack that is needed for a STATICCALL to the metamorphic factory contract 

// ======= SECTION 1 =======

// push a 0 onto the stack 
PC
// STACK: [0]

// push the number 32 onto the stack (0x20 == 32 in hex).
// this is the size of data in bytes that will be returned by STATICCALL
// "retSize" input to STATICCALL
PUSH1 0x20
// STACK: [0, 32]

// push a 0 onto the stack.
// This is the index in contract memory where any returned data from STATICCALL will be stored
// "retOffset" input to STATICCALL
DUP2 
// STACK: [0, 32, 0]

// push a 4 onto the stack
// this is the size in bytes of the calldata sent along in STATICCALL
// NOTE: 4 bytes is the length of a function selector. We will be calling a function in this STATICCALL
// "argSize" input to STATICCALL
PC
// STACK: [0, 32, 0, 4]

// push 28 onto the stack (0x1c == 28 in hex).
// this is the position of the function selector in contract memory
// the reason for 28 is because you store 32 bytes at a time in memory
// so the index after storing a 4 byte function selector will be 28 (32-4).
// see how the data is padded by zeros in evm.codes
// "argsOffset" input to STATICCALL
PUSH1 0x1c 
// STACK: [0, 32, 0, 4, 28]

// push the caller address on the stack
// this would be the factory addess that is deploying the metamorphic contract
// "address" input to STATICCALL
CALLER
// STACK: [0, 32, 0, 4, 28, factory address]

// push the amount of gas to send along with STATICCALL
// "gas" input to STATICCALL
GAS
// STACK: [0, 32, 0, 4, 28, factory address, gas]


// push the function selector onto the stack
// this is the first 4 bytes of the Keccak-256 hash of the function getImplementation() in the factory contract.
// this is the data you will store in memory using MSTORE.
PUSH4 0xaaf10f42 
// STACK: [0, 32, 0, 4, 28, factory address, gas, 0xaaf10f42]

// push a 0 onto the stack
// this is the index of where to store the function selector in memory for the next MSTORE opcode
DUP8
// STACK: [0, 32, 0, 4, 28, factory address, gas, 0xaaf10f42, 0]

// store the function selector in memory
// again the index in memory for where it will be is 28 (see evm.codes)
MSTORE
// STACK: [0, 32, 0, 4, 28, factory address, gas]

// perform the STATICCALL using several values you have pushed onto the stack up until this point
// this STATICCALL will fetch the contract address that contains
// the implementation code you will later store in the metamorphic contract. 
STATICCALL
// STACK: [0, 1 (if successful)]



// ======= SECTION 2 =======
// now that you have the implementation address in memory
// copy the code stored at that address into the current contract (the metamorphic contract)
// two main opcodes in this section are EXTCODESIZE and EXTCODECOPY

// The EXTCODESIZE opcode takes as input a contract address and returns the byte size of the code at that address
// This data is needed for EXTCODECOPY

// The EXTCODECOPY opcode copies the runtime code stored at a specific address and stores it in memory.
// It takes a few parameters as input
// 1. address: 20-byte address of the contract whose code you want to copy into memory 
// 2. destOffset: the byte offset in memory where the result will be copied. This is the memory of the metamorphic contract.
// 3. offset: the byte offset in the "code" region of the address we are copying code from
//    The "code" region is the area of general Ethereum account storage where the runtime code of a smart contract is located.
//    Learn more here: https://www.evm.codes/about
// 4. size: byte size of the code to copy (you get this from EXTCODESIZE)


// flip success bit (on top of the stack) to 0
ISZERO
// STACK: [0, 0]

// push another 0 onto the stack
// this is the position of the address fetched from STATICCALL in memory
DUP2
// STACK: [0, 0, 0]

// load 32 bytes of data from index 0 in memory
// this would contain the contract address returned by the STATICCALL
MLOAD
// STACK: [0, 0, implementation contract address]

// push the implementation contract address onto the stack again for EXTCODECOPY to consume
DUP1
// STACK: [0, 0, implementation contract address, implementation contract address]

// return size in bytes of code stored at the implementation contract address
// and push this value onto the stack
EXTCODESIZE
// STACK: [0, 0, implementation contract address, contract size]

// manipulate stack items for use by the RETURN opcode at the end of this init code
DUP1
SWAP4
// STACK: [contract size, 0, implementation contract address, contract size, 0]   

// push 0 onto the stack
// This 0 represents the "offset" parameter of EXTCODECOPY and it is referencing the "code"
// region of the implementation contract address.
// next, reorder stack items for EXTCODECOPY
DUP1
SWAP2
SWAP3
// STACK: [contract size, 0, contract size, 0, 0, implementation contract address] 

// execute the EXTCODECOPY opcode which clones the runtime code of the implementation contract
// into memory at position 0 or the "destOffset" parameter of EXTCODECOPY
EXTCODECOPY
// STACK: [contract size, 0] 

// RETURN to deploy the final code that is currently in memory 
// and effectively store the implementation contract code at the metamorphic contract address
RETURN
```
"""
