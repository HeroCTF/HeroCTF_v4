pragma solidity ^0.8.13;

/*
    Ok so i met this guy, he's got a nuke and he wants to sell it to the highest bidder.
    So I made it possible to buy it there !
*/
contract NukeAuction 
{
    uint public maxAmount = 10 ether;
    address public winner;

    function deposit() public payable 
    {
        require(msg.value == 1 ether, "You can only send 1 Ether");

        uint balance = address(this).balance;
        require(balance <= maxAmount, "Auction is over");

        if (balance == maxAmount) 
        {
            winner = msg.sender;
        }
    }

    function claimAuction() public 
    {
        require(msg.sender == winner, "Not winner");

        (bool sent, ) = msg.sender.call{value: address(this).balance}("");
        require(sent, "Failed to send Ether");
    }

    function isAuctionSane() external view returns (bool)
    {
        return (address(this).balance < 10 ether);
    }

        // Helper function to check the balance of this contract
    function getBalance() public view returns (uint) 
    {
        return address(this).balance;
    }
}