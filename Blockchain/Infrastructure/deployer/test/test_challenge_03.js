const { expect } = require("chai");
const { ethers } = require("hardhat");


describe("Challenge 03", function () 
{
  it("Should deploy the contract, read the storage and be equal to the verif flag on test contract", async function ()
  {
    const challenge02 = await ethers.getContractFactory("onChainLotterySecuredx20000");
    const challenge02_contract = await challenge02.deploy();
    await challenge02_contract.deployed();

    console.log("Contract deployed to ", challenge02_contract.address);

    const setupHash = await challenge02_contract.setupMaHash();
    // wait until the transaction is mined
    await setupHash.wait();

    [owner] = await ethers.getSigners();
    let key = "0x" + "0".repeat(24) + owner.address.toString().toLowerCase().slice(2);
    var slot = "0".repeat(63)  + "1";
    let storageat = web3.utils.soliditySha3(key+slot);
    let flag = await web3.eth.getStorageAt(challenge02_contract.address, storageat, web3.eth.defaultBlock, console.log);

    let flag_verif = await challenge02_contract.getmaHash();

    console.log('Flag ->', flag, "verif ->", flag_verif);
    expect(ethers.BigNumber.from(flag)).to.equal(flag_verif);
  });
});
