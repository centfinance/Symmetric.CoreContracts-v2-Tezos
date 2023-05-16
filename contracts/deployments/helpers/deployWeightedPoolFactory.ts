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
    weightedProtocolFeesLibAddress: string,
    tezos: TezosToolkit,
) {
    try {
        // Replace with the private key of the account you want to deploy the contract with
        // const signer = await InMemorySigner.fromSecretKey(config.accounts.bob.secretKey.slice(12));
        // tezos.setProvider({ signer });

        // Replace with the Michelson code of the WeightedPoolFactory contract
        const weightedPoolFactoryCode = WeightedPoolFactoryCode.code;

        const storage: Storage = {
            admin: tas.address(adminAddress),
            feeCache: { 0: tas.nat('400000000000000000'), 1: tas.nat('400000000000000000')},
            isPoolFromFactory: tas.bigMap([{
              key: tas.address(adminAddress),
              value: tas.unit()
            }]),
            metadata: tas.bigMap([{
              key: "",
              value: tas.bytes('0x68747470733a2f2f7261772e67697468756275736572636f6e74656e742e636f6d2f63656e7466696e616e63652f53796d6d65747269632e436f7265436f6e7472616374732d76322d54657a6f732f6d61696e2f6d657461646174612f746573746e65742f5765696768746564506f6f6c466163746f72792e6a736f6e'),
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
