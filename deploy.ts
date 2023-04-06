import { deployAll } from './contracts/deployments/helpers/deployAll';

const adminAddress = process.argv[2];

if (adminAddress) {
  deployAll(adminAddress).catch((error) => {
    console.error('Error deploying contract:', error);
    process.exit(1);
  });
} else {
  console.error('Admin address is required.');
  process.exit(1);
}