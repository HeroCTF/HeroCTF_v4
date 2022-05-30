const { expect } = require("chai");
const { ethers, waffle } = require("hardhat");
                         


describe("Challenge 02", function () {
    it("Should deploy the contract, check the balance, and exploit it by deploying the attack contract", async function ()
    {
    
        const challenge01 = await ethers.getContractFactory("WMEL");
        const challenge01_contract = await challenge01.deploy();
        await challenge01_contract.deployed();

        console.log("Contract deployed to ", challenge01_contract.address);

        overrides = { value : ethers.utils.parseEther("20.0") };

        let tx = await challenge01_contract.deposit(overrides);
        await tx.wait();


        let provider = await ethers.getDefaultProvider();


        let bal = await challenge01_contract.getBalance();
        console.log("bal :", bal);

        const challenge01pwn = await ethers.getContractFactory("Attack");
        const challenge01pwn_contract = await challenge01pwn.deploy(challenge01_contract.address);
        await challenge01pwn_contract.deployed();
        overrides = { value : ethers.utils.parseEther("1.0") };
        let pwntx = await challenge01pwn_contract.attack(overrides);
        await pwntx.wait();
        bal = await challenge01pwn_contract.getBalance();
        console.log("bal:", bal);

    });
});
