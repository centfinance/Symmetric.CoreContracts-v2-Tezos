import { TezosToolkit } from '@taquito/taquito';
import { InMemorySigner } from '@taquito/signer';
import { ExternalWeightedMathCode } from '../../../types/ExternalWeightedMath.code';
import { ExternalWeightedProtocolFeesCode } from '../../../types/ExternalWeightedProtocolFees.code';

const externalWeightedMathStorage = require('../../../artifacts/ExternalWeightedMath.default_storage.json')
const externalWeightedProtocolFeesStorage = require('../../../artifacts/ExternalWeightedMath.default_storage.json')

const config = require('../../../.taq/config.local.development.json');

const tezos = new TezosToolkit('http://localhost:20000');

export async function deployExternalContracts(tezos: TezosToolkit) {
  try {
    // const signer = await InMemorySigner.fromSecretKey(config.accounts.bob.secretKey.slice(12));
    // tezos.setProvider({ signer });
  
    const externalWeightedMathCode = ExternalWeightedMathCode.code;
    const externalWeightedProtocolFeesCode = ExternalWeightedProtocolFeesCode.code;
    const batch = await tezos.contract.batch()
      .withOrigination({
        code: externalWeightedMathCode,
        init: externalWeightedMathStorage,
      })
      .send();
      await batch.confirmation();
      
      const contract1 = batch.getOriginatedContractAddresses();
      
      const batch2 = await tezos.contract.batch()
      .withOrigination({
        code: externalWeightedProtocolFeesCode,
        init: externalWeightedProtocolFeesStorage,
      })
      .send();

    console.log('Sending batch operation...');
    console.log('Awaiting confirmation...');

    await batch2.confirmation();

    const contract2 = batch2.getOriginatedContractAddresses();

    console.log('ExternalWeightedMath contract deployed at address:', contract1[0]);
    console.log('ExternalWeightedProtocolFees contract deployed at address:', contract2[0]);
    
    return [contract1[0], contract2[0]];
  } catch (error) {
    console.error('Error deploying contracts:', error);
  }
}


// deployExternalContracts();
