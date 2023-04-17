import { deployAll } from './contracts/deployments/helpers/deployAll';

const adminAddress = 'tz1VSUr8wwNhLAzempoch5d6hLRiTh8Cjcjb';

if (adminAddress) {
  deployAll(adminAddress).catch((error) => {
    console.error('Error deploying contract:', error);
    process.exit(1);
  });
} else {
  console.error('Admin address is required.');
  process.exit(1);
}