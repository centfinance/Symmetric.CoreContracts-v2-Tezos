import { TezosToolkit } from '@taquito/taquito';
import { InMemorySigner } from '@taquito/signer';

import { WeightedPoolFactoryCode } from '../../../types/WeightedPoolFactory.code';
import { Storage } from '../../../types/WeightedPoolFactory.types';
import { tas } from '../../../types/type-aliases';

const config = require('../../../.taq/config.local.development.json');

const tezos = new TezosToolkit('http://localhost:20000');

export async function deployWeightedPoolFactory(
    adminAddress: string,
    protocolFeeProviderAddress: string,
    vaultAddress: string,
    weightedMathLibAddress: string,
    weightedProtocolFeesLibAddress: string
) {
    try {
        // Replace with the private key of the account you want to deploy the contract with
        const signer = await InMemorySigner.fromSecretKey(config.accounts.bob.secretKey.slice(12));
        tezos.setProvider({ signer });

        // Replace with the Michelson code of the WeightedPoolFactory contract
        const weightedPoolFactoryCode = WeightedPoolFactoryCode.code;

        const storage: Storage = {
            admin: tas.address(adminAddress),
            feeCache: { 0: tas.nat(400000000000000000), 1: tas.nat(400000000000000000)},
            isPoolFromFactory: tas.bigMap([{
              key: tas.address(adminAddress),
              value: tas.unit()
            }]),
            metadata: tas.bigMap([{
              key: 'name',
              value: tas.bytes(''),
            }]),
            proposed_admin: undefined,
            protocolFeeProvider: tas.address(protocolFeeProviderAddress),
            vault: tas.address(vaultAddress),
            weightedMathLib: tas.address(weightedMathLibAddress),
            weightedProtocolFeesLib: tas.address(weightedProtocolFeesLibAddress),
        };

        const originationOp = await tezos.contract.originate({
            code: weightedPoolFactoryCode,
            storage: storage,
        });

        console.log('Awaiting confirmation...');
        await originationOp.confirmation();

        const weightedPoolFactoryContract = await originationOp.contract();
        console.log('WeightedPoolFactory contract deployed at address:', weightedPoolFactoryContract.address);
    } catch (error) {
        console.error('Error deploying WeightedPoolFactory contract:', error);
    }
}

// Replace with the appropriate addresses for each parameter
const adminAddress = '<your_admin_address>';
const protocolFeeProviderAddress = '<your_protocol_fee_provider_address>';
const vaultAddress = '<your_vault_address>';
const weightedMathLibAddress = '<your_weighted_math_lib_address>';
const weightedProtocolFeesLibAddress = '<your_weighted_protocol_fees_lib_address>';

// deployWeightedPoolFactory(
//     adminAddress,
//     protocolFeeProviderAddress,
//     vaultAddress,
//     weightedMathLibAddress,
//     weightedProtocolFeesLibAddress
// );
