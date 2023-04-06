import { TezosToolkit } from '@taquito/taquito';
import { InMemorySigner } from '@taquito/signer';
import { ExternalWeightedMathCompileCode } from '../../../types/ExternalWeightedMath.compile.code';
import { ExternalWeightedProtocolFeesCompileCode } from '../../../types/ExternalWeightedProtocolFees.compile.code';
const config = require('../../../../.taq/config.local.testing.json')

const tezos = new TezosToolkit(config.environments.development.rpcUrl);


const signer = await InMemorySigner.fromSecretKey(config.accounts.taqOperatorAccount.privateKey);
tezos.setProvider({ signer });

const externalWeightedMathCode = ExternalWeightedMathCompileCode.code;
const externalWeightedProtocolFeesCode = ExternalWeightedProtocolFeesCompileCode.code;

async function deployContracts() {
  try {
    const batch = await tezos.contract.batch()
      .withOrigination({
        code: externalWeightedMathCode,
        storage: { prim: 'Unit' },
      })
      .withOrigination({
        code: externalWeightedProtocolFeesCode,
        storage: { prim: 'Unit' },
      })
      .send();

    console.log('Sending batch operation...');
    console.log('Awaiting confirmation...');
    await batch.confirmation();

    const contracts = batch.getOriginatedContractAddresses();

    console.log('ExternalWeightedMath contract deployed at address:', contracts[0]);
    console.log('ExternalWeightedProtocolFees contract deployed at address:', contracts[1]);
  } catch (error) {
    console.error('Error deploying contracts:', error);
  }
}


deployContracts();
