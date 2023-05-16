import { deployAll } from './contracts/deployments/helpers/deployAll';

const adminAddress = 'tz1UGWQQ5YFkZqWgE3gqmPyuwy2R5VGpMM9B';

if (adminAddress) {
  deployAll(adminAddress, 'local').catch((error) => {
    console.error('Error deploying contract:', error);
    process.exit(1);
  });
} else {
  console.error('Admin address is required.');
  process.exit(1);
}