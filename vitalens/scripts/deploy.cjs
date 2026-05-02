const hre = require("hardhat");

async function main() {
  const PatientRecord = await hre.ethers.getContractFactory("PatientRecord");
  console.log("Deploying PatientRecord...");
  const contract = await PatientRecord.deploy();

  await contract.waitForDeployment();

  console.log("PatientRecord deployed to:", await contract.getAddress());
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
