import { TezosToolkit } from '@taquito/taquito';
import { InMemorySigner } from '@taquito/signer';
import { ExternalWeightedMathCompileCode } from '../../../types/ExternalWeightedMath.compile.code';
import { ExternalWeightedProtocolFeesCompileCode } from '../../../types/ExternalWeightedProtocolFees.compile.code';
const config = require('../../../.taq/config.local.development.json');

const tezos = new TezosToolkit('http://localhost:20000');

export async function deployExternalContracts() {
  try {
    const signer = await InMemorySigner.fromSecretKey(config.accounts.bob.secretKey.slice(12));
    tezos.setProvider({ signer });
  
    const externalWeightedMathCode = ExternalWeightedMathCompileCode.code;
    const externalWeightedProtocolFeesCode = ExternalWeightedProtocolFeesCompileCode.code;
    const batch = await tezos.contract.batch()
      .withOrigination({
        code: externalWeightedMathCode,
        storage: {},
      })
      .withOrigination({
        code: externalWeightedProtocolFeesCode,
        storage: {},
      })
      .send();

    console.log('Sending batch operation...');
    console.log('Awaiting confirmation...');
    await batch.confirmation();

    const contracts = batch.getOriginatedContractAddresses();

    console.log('ExternalWeightedMath contract deployed at address:', contracts[0]);
    console.log('ExternalWeightedProtocolFees contract deployed at address:', contracts[1]);
    
    return contracts;
  } catch (error) {
    console.error('Error deploying contracts:', error);
  }
}


deployExternalContracts();
