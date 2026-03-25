// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

// VitaLens — PatientRecord.sol
// Immutable health record storage on Ethereum

contract PatientRecord {

    struct Diagnosis {
        string  patientName;
        string  disease;
        uint256 riskScore;
        string  city;
        bytes32 dataHash;
        uint256 timestamp;
        address recordedBy;
    }

    // patientName => list of diagnoses
    mapping(string => Diagnosis[]) private records;

    // Only authorized addresses can write
    mapping(address => bool) public authorizedDoctors;
    address public owner;

    event DiagnosisRecorded(string indexed patientName, string disease, uint256 riskScore, uint256 timestamp);

    constructor() {
        owner = msg.sender;
        authorizedDoctors[msg.sender] = true;
    }

    modifier onlyOwner() { require(msg.sender == owner, "Not owner"); _; }
    modifier onlyAuthorized() { require(authorizedDoctors[msg.sender], "Not authorized"); _; }

    function authorizeDoctor(address doctor) external onlyOwner {
        authorizedDoctors[doctor] = true;
    }

    function recordDiagnosis(
        string memory _name,
        string memory _disease,
        uint256 _riskScore,
        string memory _city,
        bytes32 _dataHash
    ) external {
        records[_name].push(Diagnosis({
            patientName: _name,
            disease:     _disease,
            riskScore:   _riskScore,
            city:        _city,
            dataHash:    _dataHash,
            timestamp:   block.timestamp,
            recordedBy:  msg.sender
        }));
        emit DiagnosisRecorded(_name, _disease, _riskScore, block.timestamp);
    }

    function getRecordCount(string memory _name) external view returns (uint256) {
        return records[_name].length;
    }

    function getRecord(string memory _name, uint256 index) external view
        returns (string memory disease, uint256 riskScore, string memory city, uint256 timestamp, bytes32 dataHash)
    {
        Diagnosis memory d = records[_name][index];
        return (d.disease, d.riskScore, d.city, d.timestamp, d.dataHash);
    }

    function getRecords(string memory _name) external view returns (string[] memory) {
        Diagnosis[] memory ds = records[_name];
        string[] memory result = new string[](ds.length);
        for (uint i = 0; i < ds.length; i++) {
            result[i] = string(abi.encodePacked(ds[i].disease, "|", uint2str(ds[i].riskScore)));
        }
        return result;
    }

    function uint2str(uint256 v) internal pure returns (string memory) {
        if (v == 0) return "0";
        uint256 temp = v; uint256 digits;
        while (temp != 0) { digits++; temp /= 10; }
        bytes memory buf = new bytes(digits);
        while (v != 0) { digits--; buf[digits] = bytes1(uint8(48 + v % 10)); v /= 10; }
        return string(buf);
    }
}
