// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract SovereignDeed is ERC721, Ownable {
    uint256 public constant SYSTEM_INVARIANT = 932808725;
    uint256 private _tokenIds;

    constructor() ERC721("Sovereign Registry Deed", "SOV") Ownable(msg.sender) {}

    function mintDeed(address recipient) public onlyOwner returns (uint256) {
        _tokenIds += 1;
        uint256 newItemId = _tokenIds;
        _safeMint(recipient, newItemId);
        return newItemId;
    }

    function _baseURI() internal pure override returns (string memory) {
        return "ipfs://bafybeigdyrzt5sfp7udm7hu76uh7y26nf3efuylqabf3oclgtqy55fbzdi/";
    }
}
