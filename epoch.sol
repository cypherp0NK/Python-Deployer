//SPDX-License-Identifier: Unlicense
pragma solidity 0.8.0;

contract Epoch {

    function check() public returns(uint256){
        return block.timestamp;
    }
}