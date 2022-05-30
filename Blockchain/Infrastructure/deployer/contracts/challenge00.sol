// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

// @dev : iHuggsy
contract Introduction
{
    
    
    /**
        Before going into the source code, make sure you visited http://blockchain.heroctf.fr:22000/help if you need it !

        THERE IS ONE (1) RULE :
            - The whole node system and mining system (and machines that are part of this system) 
              does not belong to ANY of the challenges, any attempt to use them in a 
              way that is not considered normal in a blockchain environment, pentest them 
              or even scan them WILL result in a ban of your entire team without any notice.

        By interacting with the `accept_rules` function that follows, you are signing a contract 
        that you agree with the rule.
        (Even if you don't interact with it, you agree to it lol)

        Have a good one !

        If you run into any problem, feel free to DM me on the Discord 
        @dev : iHuggsy
    **/

    bytes32 flags;
    mapping (address => bool) accepted_rules;

    constructor (bytes32 _flagz)
    {
        flags = _flagz;
    }

    function get_flag_part_one() external view returns (bytes32)
    {
        require(accepted_rules[msg.sender] == true);
        return flags;
    }

    function accept_rules() external
    {
        accepted_rules[msg.sender] = true;
    }
}