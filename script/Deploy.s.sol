// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {Script} from "forge-std/Script.sol";
import {SovereignDeed} from "../src/SovereignDeed.sol";

contract DeployScript is Script {
    function run() external {
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");
        vm.startBroadcast(deployerPrivateKey);

        SovereignDeed deed = new SovereignDeed();
        
        vm.stopBroadcast();
    }
}
