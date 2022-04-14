require("@nomiclabs/hardhat-ethers");
require("@nomiclabs/hardhat-etherscan")

const dotenv = require('dotenv');
dotenv.config();

/**
 * @type import('hardhat/config').HardhatUserConfig
 */
const DEV_SEED = process.env.DEV_SEED || ""
const RINKEBY_ALCHEMY_URL = process.env.RINKEBY_ALCHEMY_URL || ""

const MAINNET_ALCHEMY_URL = process.env.RPC_ENDPOINT || ""
const ETHERSCAN_API_KEY = process.env.ETHERSCAN_API_KEY || "my etherscan API key"

module.exports = {
  solidity: "0.8.7",
  defaultNetwork: "hardhat",
  networks: {

    local :{
      url: "http://127.0.0.1:8545",
      timeout:0
    },

    hardhat:{
      forking:{
        url: MAINNET_ALCHEMY_URL
      },
      timeout:0
    },

    rinkeby:{
        url: RINKEBY_ALCHEMY_URL,
        accounts: {mnemonic: DEV_SEED},
        gas:100000000,
    },

    mainnet:{
      url: MAINNET_ALCHEMY_URL,
      accounts: {mnemonic:DEV_SEED}
    },

    arbitrum_rinkeby:{
      url: 'https://rinkeby.arbitrum.io/rpc',
      accounts: {mnemonic:DEV_SEED},
      gasPrice: 10000000000,
    },

  },

  etherscan:{
    apiKey: ETHERSCAN_API_KEY
  },
  
  
};