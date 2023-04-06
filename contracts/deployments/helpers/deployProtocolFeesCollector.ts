import { TezosToolkit } from '@taquito/taquito';
import { InMemorySigner } from '@taquito/signer';
import { ProtocolFeesCollectorCompileCode } from '../../../types/ProtocolFeesCollector.compile.code';
import { Storage } from '../../../types/ProtocolFeesCollector.compile.types';
import { tas } from '../../../types/type-aliases';

const config = require('../../../.taq/config.local.development.json');

const tezos = new TezosToolkit('http://localhost:20000');

export async function deployProtocolFeesCollector(adminAddress: string, vaultAddress: string, flashLoanFeePercentage: string, swapFeePercentage: string) {
    try {
        const signer = await InMemorySigner.fromSecretKey(config.accounts.bob.secretKey.slice(12));
        tezos.setProvider({ signer });

        const protocolFeesCollectorCode = ProtocolFeesCollectorCompileCode.code;

        const storage: Storage = {
            admin: tas.address(adminAddress),
            flashLoanFeePercentage: tas.nat(flashLoanFeePercentage),
            swapFeePercentage: tas.nat(swapFeePercentage),
            vault: tas.address(vaultAddress),
        };

        const originationOp = await tezos.contract.originate({
            code: protocolFeesCollectorCode,
            storage: storage,
        });

        console.log('Awaiting confirmation...');
        await originationOp.confirmation();

        const protocolFeesCollectorContract = await originationOp.contract();
        console.log('ProtocolFeesCollector contract deployed at address:', protocolFeesCollectorContract.address);
        return protocolFeesCollectorContract;
      } catch (error) {
        console.error('Error deploying ProtocolFeesCollector contract:', error);
    }
}

const adminAddress = '<your_admin_address>';
const vaultAddress = '<your_vault_address>';
const flashLoanFeePercentage = '1000000000000000';
const swapFeePercentage = '400000000000000000';

deployProtocolFeesCollector(adminAddress, vaultAddress, flashLoanFeePercentage, swapFeePercentage);
