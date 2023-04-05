import { TezosToolkit } from '@taquito/taquito';
import { InMemorySigner } from '@taquito/signer';

import { VaultCompileCode } from '../../../types/Vault.compile.code';
import { Storage } from '../../../types/Vault.compile.types';
import { tas } from '../../../types/type-aliases';

const config = require('../../../../.taq/config.local.testing.json')

const tezos = new TezosToolkit('<rpc_url>');

async function deployVault(adminAddress: string) {
    try {
        // Replace with the private key of the account you want to deploy the contract with
        const signer = await InMemorySigner.fromSecretKey(config.accounts.taqOperatorAccount.privateKey);
        tezos.setProvider({ signer });

        // Replace with the Michelson code of the Vault contract
        const vaultCode = VaultCompileCode.code;

        const storage: Storage = {
          admin: tas.address(adminAddress),
          isPoolRegistered: tas.bigMap([]),
          metadata: tas.bigMap([]),
          nextPoolNonce: tas.nat(0),
          poolsBalances: tas.bigMap([]),
          poolsTokens: tas.bigMap([]),
          settings: false,
      };

        const originationOp = await tezos.contract.originate({
            code: vaultCode,
            storage: storage,
        });

        console.log('Awaiting confirmation...');
        await originationOp.confirmation();

        const vaultContract = await originationOp.contract();
        console.log('Vault contract deployed at address:', vaultContract.address);
    } catch (error) {
        console.error('Error deploying Vault contract:', error);
    }
}

// Replace with the admin address you want to set for the Vault contract
const adminAddress = '<your_admin_address>';
deployVault(adminAddress);
