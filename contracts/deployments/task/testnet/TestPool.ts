import { InMemorySigner  } from '@taquito/signer';
import { TezosToolkit } from '@taquito/taquito';
import { tas } from '../../../../types/type-aliases';
import { WeightedPoolCompileContractType as ContractType } from '../../../../types/WeightedPool.compile.types';

const Tezos = new TezosToolkit("https://ghostnet.ecadinfra.com");

const config = require('../../../../.taq/config.local.testing.json')

InMemorySigner.fromSecretKey(config.accounts.taqOperatorAccount.privateKey)
  .then((theSigner) => {
    Tezos.setProvider({ signer: theSigner });
  })
  .then( async () => {
    const contract = await Tezos.contract.at<ContractType>('KT1MPScnKibWNrpDqmBioNoZ3Koj55Z4mpHa');
    const initializeRequest = await contract.methodsObject.initialize({
      normalizedWeights: tas.map([{ 
          key: tas.nat('0'), 
          value: tas.nat('500000000000000000'),
      },
      { 
        key: tas.nat('1'), 
        value: tas.nat('500000000000000000'),
      }
    ]),
      rateProviders: tas.map([{ 
          key: tas.nat('0'), 
          value: tas.address('tz1UGWQQ5YFkZqWgE3gqmPyuwy2R5VGpMM9B'),
      },
      { 
        key: tas.nat('1'), 
        value: tas.address('tz1UGWQQ5YFkZqWgE3gqmPyuwy2R5VGpMM9B'),
    }]),
      swapFeePercentage: tas.nat('1000000000000'),
      tokenDecimals: tas.map([{ 
          key: tas.nat('0'), 
          value: tas.nat('18'),
      },
      { 
        key: tas.nat('1'), 
        value: tas.nat('18'),
      }]),
      tokens: tas.map([{ 
          key: tas.nat('0'), 
          value: {
            FA2: true,
            address: tas.address('KT1VvQ6azTcyj5otVciTicuFS1gVhcHD56Kr'),
            id: tas.nat('0'),
          },
      },
      { 
        key: tas.nat('1'), 
        value: {
          FA2: true,
          address: tas.address('KT1VvQ6azTcyj5otVciTicuFS1gVhcHD56Kr'),
          id: tas.nat('1'),
        },
    }]),
  }).toTransferParams({});
  await Tezos.estimate.transfer(initializeRequest)
  // await initializeRequest.confirmation(0);
  })
  .catch((error) => console.table(`Error: ${JSON.stringify(error, null, 2)}`));