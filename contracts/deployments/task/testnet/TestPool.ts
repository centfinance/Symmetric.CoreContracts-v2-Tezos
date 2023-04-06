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
    const contract = await Tezos.contract.at<ContractType>('KT1PR7ZHamLMhqcnHKgnKvuE6udHJJwCHKRE');
    const tokens = tas.map([
      {
        key: tas.nat('0'),
        value: {
          FA2: true,
          address: tas.address('KT1JA3UQ6R4C84mH3FqS3G5mKFeEdLumrDc3'),
          id: tas.nat('0'),
      }},
      {
        key: tas.nat('1'),
        value: {
          FA2: true,
          address: tas.address('KT1JA3UQ6R4C84mH3FqS3G5mKFeEdLumrDc3'),
          id: tas.nat('1'),
      }},
      {
        key: tas.nat('2'),
        value: {
          FA2: true,
          address: tas.address('KT1JA3UQ6R4C84mH3FqS3G5mKFeEdLumrDc3'),
          id: tas.nat('2'),
      }},
      {
        key: tas.nat('3'),
        value: {
          FA2: true,
          address: tas.address('KT1JA3UQ6R4C84mH3FqS3G5mKFeEdLumrDc3'),
          id: tas.nat('3'),
      }},
      {
        key: tas.nat('4'),
        value: {
          FA2: true,
          address: tas.address('KT1JA3UQ6R4C84mH3FqS3G5mKFeEdLumrDc3'),
          id: tas.nat('4'),
      }},
      {
        key: tas.nat('5'),
        value: {
          FA2: true,
          address: tas.address('KT1JA3UQ6R4C84mH3FqS3G5mKFeEdLumrDc3'),
          id: tas.nat('5'),
      }},
      {
        key: tas.nat('6'),
        value: {
          FA2: true,
          address: tas.address('KT1JA3UQ6R4C84mH3FqS3G5mKFeEdLumrDc3'),
          id: tas.nat('6'),
      }},
      {
        key: tas.nat('7'),
        value: {
          FA2: true,
          address: tas.address('KT1JA3UQ6R4C84mH3FqS3G5mKFeEdLumrDc3'),
          id: tas.nat('7'),
      }},
    ])
    
    const weights = tas.map([
      { 
        key: tas.nat('0'), 
        value: tas.nat('125000000000000000'),
      },
      { 
        key: tas.nat('1'), 
        value: tas.nat('125000000000000000'),
      },
      { 
        key: tas.nat('2'), 
        value: tas.nat('125000000000000000'),
      },
      { 
        key: tas.nat('3'), 
        value: tas.nat('125000000000000000'),
      },
      { 
        key: tas.nat('4'), 
        value: tas.nat('125000000000000000'),
      },
      { 
        key: tas.nat('5'), 
        value: tas.nat('125000000000000000'),
      },
      { 
        key: tas.nat('6'), 
        value: tas.nat('125000000000000000'),
      },
      { 
        key: tas.nat('7'), 
        value: tas.nat('125000000000000000'),
      },
    ])
    const rateProviders = tas.map([
      { 
        key: tas.nat('0'), 
        value: null,
      },
      { 
        key: tas.nat('1'), 
        value: null,
      },
      { 
        key: tas.nat('2'), 
        value: null,
      },
      { 
        key: tas.nat('3'), 
        value: null,
      },
      { 
        key: tas.nat('4'), 
        value: null,
      },
      { 
        key: tas.nat('5'), 
        value: null,
      },
      { 
        key: tas.nat('6'), 
        value: null,
      },
      { 
        key: tas.nat('7'), 
        value: null,
      },
    ])
    
    const decimals = tas.map([
      { 
        key: tas.nat('0'), 
        value: tas.nat('18'),
      },
      { 
        key: tas.nat('1'), 
        value: tas.nat('18'),
      },
      { 
        key: tas.nat('2'), 
        value: tas.nat('18'),
      },
      { 
        key: tas.nat('3'), 
        value: tas.nat('18'),
      },
      { 
        key: tas.nat('4'), 
        value: tas.nat('18'),
      },
      { 
        key: tas.nat('5'), 
        value: tas.nat('18'),
      },
      { 
        key: tas.nat('6'), 
        value: tas.nat('18'),
      },
      { 
        key: tas.nat('7'), 
        value: tas.nat('18'),
      },
    ])
    
    const initializeRequest = await contract.methodsObject.initialize({
      normalizedWeights: tas.map([
        { 
          key: tas.nat('0'), 
          value: tas.nat('125000000000000000'),
        },
        { 
          key: tas.nat('1'), 
          value: tas.nat('125000000000000000'),
        },
        { 
          key: tas.nat('2'), 
          value: tas.nat('125000000000000000'),
        },
        { 
          key: tas.nat('3'), 
          value: tas.nat('125000000000000000'),
        },
        { 
          key: tas.nat('4'), 
          value: tas.nat('125000000000000000'),
        },
        { 
          key: tas.nat('5'), 
          value: tas.nat('125000000000000000'),
        },
        { 
          key: tas.nat('6'), 
          value: tas.nat('125000000000000000'),
        },
        { 
          key: tas.nat('7'), 
          value: tas.nat('125000000000000000'),
        },
      ]),
      rateProviders: tas.map([
        { 
          key: tas.nat('0'), 
          value: null,
        },
        { 
          key: tas.nat('1'), 
          value: null,
        },
        { 
          key: tas.nat('2'), 
          value: null,
        },
        { 
          key: tas.nat('3'), 
          value: null,
        },
        { 
          key: tas.nat('4'), 
          value: null,
        },
        { 
          key: tas.nat('5'), 
          value: null,
        },
        { 
          key: tas.nat('6'), 
          value: null,
        },
        { 
          key: tas.nat('7'), 
          value: null,
        },
      ]),
      swapFeePercentage: tas.nat('1000000000000'),
      tokenDecimals: tas.map([
        { 
          key: tas.nat('0'), 
          value: tas.nat('18'),
        },
        { 
          key: tas.nat('1'), 
          value: tas.nat('18'),
        },
        { 
          key: tas.nat('2'), 
          value: tas.nat('18'),
        },
        { 
          key: tas.nat('3'), 
          value: tas.nat('18'),
        },
        { 
          key: tas.nat('4'), 
          value: tas.nat('18'),
        },
        { 
          key: tas.nat('5'), 
          value: tas.nat('18'),
        },
        { 
          key: tas.nat('6'), 
          value: tas.nat('18'),
        },
        { 
          key: tas.nat('7'), 
          value: tas.nat('18'),
        },
      ]),
      tokens: tas.map([
        {
          key: tas.nat('0'),
          value: {
            FA2: true,
            address: tas.address('KT1JA3UQ6R4C84mH3FqS3G5mKFeEdLumrDc3'),
            id: tas.nat('0'),
        }},
        {
          key: tas.nat('1'),
          value: {
            FA2: true,
            address: tas.address('KT1JA3UQ6R4C84mH3FqS3G5mKFeEdLumrDc3'),
            id: tas.nat('1'),
        }},
        {
          key: tas.nat('2'),
          value: {
            FA2: true,
            address: tas.address('KT1JA3UQ6R4C84mH3FqS3G5mKFeEdLumrDc3'),
            id: tas.nat('2'),
        }},
        {
          key: tas.nat('3'),
          value: {
            FA2: true,
            address: tas.address('KT1JA3UQ6R4C84mH3FqS3G5mKFeEdLumrDc3'),
            id: tas.nat('3'),
        }},
        {
          key: tas.nat('4'),
          value: {
            FA2: true,
            address: tas.address('KT1JA3UQ6R4C84mH3FqS3G5mKFeEdLumrDc3'),
            id: tas.nat('4'),
        }},
        {
          key: tas.nat('5'),
          value: {
            FA2: true,
            address: tas.address('KT1JA3UQ6R4C84mH3FqS3G5mKFeEdLumrDc3'),
            id: tas.nat('5'),
        }},
        {
          key: tas.nat('6'),
          value: {
            FA2: true,
            address: tas.address('KT1JA3UQ6R4C84mH3FqS3G5mKFeEdLumrDc3'),
            id: tas.nat('6'),
        }},
        {
          key: tas.nat('7'),
          value: {
            FA2: true,
            address: tas.address('KT1JA3UQ6R4C84mH3FqS3G5mKFeEdLumrDc3'),
            id: tas.nat('7'),
        }},
      ]),
      feeCache: {
        swapFee: tas.nat('400000000000000000'),
        yieldFee: tas.nat('400000000000000000'),
        aumFee: tas.nat('0')
      }
  }).send();
  // const estimate = await Tezos.estimate.transfer(initializeRequest)
  // console.log(estimate)
    await initializeRequest.confirmation(1);
  })
  .catch((error) => console.table(`Error: ${JSON.stringify(error, null, 2)}`));