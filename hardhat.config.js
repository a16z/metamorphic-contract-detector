require("@nomiclabs/hardhat-ethers");
require("@nomiclabs/hardhat-etherscan");

const dotenv = require("dotenv");
dotenv.config();

module.exports = {
  solidity: "0.8.7",
  defaultNetwork: "hardhat",
};
