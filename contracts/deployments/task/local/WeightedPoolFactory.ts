import { InMemorySigner  } from '@taquito/signer';
import { TezosToolkit } from '@taquito/taquito';

const weightedPoolFactory = require('../../../../artifacts/WeightedPoolFactory.compile.json')
const weightedPoolFactoryStorage = require('../../../../artifacts/WeightedPoolFactory.compile.default_storage.json')
const Tezos = new TezosToolkit('http://localhost:20000');

InMemorySigner.fromSecretKey(process.env.TEST_KEY as string)
  .then((theSigner) => {
    Tezos.setProvider({ signer: theSigner });
  })
  .then(() => {
    Tezos.contract.originate({
      code: weightedPoolFactory,
      init: weightedPoolFactoryStorage,
      storageLimit: 60000,
    })
    .then((originationOp) => {
      console.log(`Waiting for confirmation of origination for ${originationOp.contractAddress}...`);
      return originationOp.contract();
    })
    .then((contract) => {
      console.log(`Origination completed.`);
    })
  })
  .catch((error) => console.log(`Error: ${error} ${JSON.stringify(error, null, 2)}`));
