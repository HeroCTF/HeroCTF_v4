pragma solidity 0.4.16;

contract PrivateENS
{
    bool public locked;
    address owner;

    function PrivateENS() public
    {
        locked = true;
        owner = msg.sender;
    }
    
    
    struct NameRecord 
    {
        bytes32 name;  
        address mappedAddress;
    }

    mapping(address => NameRecord) public registeredNameRecord; // records who registered names 
    mapping(bytes32 => address) public resolve; // resolves hashes to addresses
    
    function register(bytes32 _name, address _mappedAddress) public 
    {
        // set up the new NameRecord
        NameRecord newRecord;
        newRecord.name = _name;
        require(!locked);
        newRecord.mappedAddress = _mappedAddress; 
        resolve[_name] = _mappedAddress;
        registeredNameRecord[msg.sender] = newRecord; 

    }

    function get_registrar(bytes32 _name) external view returns (address)
    {
        return resolve[_name];
    }

    function switchStatus() external 
    {
        require(msg.sender == owner);
        if (locked)
        {
            locked = false;
        }
        else
        {
            locked = true;
        }
    }


}
