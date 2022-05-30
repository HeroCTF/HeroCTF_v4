const { expect } = require("chai");
const { ethers, waffle } = require("hardhat");



describe("Challenge 01", function () {
  it("Should deploy the contract, make a transaction, and query the flag", async function ()
  {
    
    const challenge00 = await ethers.getContractFactory("Introduction");
    const challenge00_contract = await challenge00.deploy(ethers.utils.formatBytes32String("Hero{SomeFlagz}"));
    await challenge00_contract.deployed();

    console.log("Contract deployed to ", challenge00_contract.address);

    const acceptRulesTx = await challenge00_contract.accept_rules();
    // wait until the transaction is mined
    await acceptRulesTx.wait();
    const flag = await challenge00_contract.get_flag_part_one();

    console.log('Flag ->', await flag);
    expect(flag).to.equal(ethers.utils.formatBytes32String("Hero{SomeFlagz}"));
  });
});
