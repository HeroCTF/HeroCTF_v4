// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

/*
    This contract implements "WMEL" (Wrapped MEL). You get an ERC20 version of Melcoin where 1WMEL == 1MEL at all times.
    This is a beta version !
*/

// @dev : iHuggsy
contract WMEL
{
    mapping(address => uint) public balances;

    constructor () payable {}

    function deposit() external payable 
    {
        balances[msg.sender] += msg.value;
    }

    function withdraw() public 
    {
        uint bal = balances[msg.sender];
        require(bal > 0);
        (bool sent, ) = msg.sender.call{value: bal}("");
        require(sent, "Failed to send Ether");
        balances[msg.sender] = 0;
    }

    // Helper function to check the balance of this contract
    function getBalance() public view returns (uint) 
    {
        return address(this).balance;
    }
}