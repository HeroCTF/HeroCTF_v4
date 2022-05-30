const { expect } = require("chai");
const { ethers, waffle } = require("hardhat");
require("@nomiclabs/hardhat-waffle");
require("@nomiclabs/hardhat-web3");

[owner, nonOwner] = [0, 0];
[trader1, trader2] = [0, 0];

const deploy = async(contract_name, params=[]) =>
{
  const factory = await ethers.getContractFactory(contract_name);
  const contract = await factory.deploy(...params);
  await contract.deployed();

  return contract;
}

async function main()
{
    let challenge02 = await deploy("PrivateENS");

    console.log(challenge02.address);
}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
