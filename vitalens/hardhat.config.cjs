require("@nomicfoundation/hardhat-toolbox");
require("dotenv").config({ path: "./backend/.env" });

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: "0.8.20",
  networks: {
    sepolia: {
      url: process.env.BLOCKCHAIN_RPC || "",
      accounts: process.env.WALLET_PRIVATE_KEY ? [process.env.WALLET_PRIVATE_KEY] : [],
    },
  },
};
