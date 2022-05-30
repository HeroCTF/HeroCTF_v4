pragma solidity ^0.8.10;

contract onChainLotterySecuredx20000
{
   /*
    Ok, so everyone wants this "super onChain PRNG". I think i might've found a way
    */ 
    bool hasWon = false;
    mapping (address => uint256) secured_HasH2GueSs;

    constructor () payable {}

    function getPrizePool() external view returns (uint256)
    {
        return address(this).balance;
    }

    function setupMaHash() external
    {
        require(secured_HasH2GueSs[msg.sender] == 0, "Already played, think i'm a fool ?");
        uint256 shuffler = block.timestamp % 25;
        uint256 val = uint256(blockhash(block.number - shuffler)) % block.gaslimit
                      + gasleft();

        secured_HasH2GueSs[msg.sender] = val;
    }

    function trynaGuessMyhash(uint256 guessed) external
    {
        require(secured_HasH2GueSs[msg.sender] != 0, "Really...");
        require(secured_HasH2GueSs[msg.sender] == guessed);
        hasWon = true;

    }

    function verify() external view returns (bool)
    {
        return hasWon;
    }
}