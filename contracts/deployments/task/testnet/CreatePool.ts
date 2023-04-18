import { InMemorySigner  } from '@taquito/signer';
import { char2Bytes } from '@taquito/utils';
import { TezosToolkit } from '@taquito/taquito';
import { tas } from '../../../../types/type-aliases';
import { WeightedPoolFactoryContractType as ContractType } from '../../../../types/WeightedPoolFactory.types';

const Tezos = new TezosToolkit("http://localhost:20000");

const config = require('../../../../.taq/config.local.development.json');

InMemorySigner.fromSecretKey(config.accounts.bob.secretKey.slice(12))
  .then((theSigner) => {
    Tezos.setProvider({ signer: theSigner });
  })
  .then( async () => {
    const contract = await Tezos.contract.at<ContractType>('KT1Ewux3ZjVaGnowHo9sVu7wzGhDbq3he65o');
    const createRequest = await contract.methodsObject.create({
      metadata: tas.bytes(
        char2Bytes('SYMMLP')),
      token_metadata: tas.map({
        "name": tas.bytes(char2Bytes('8 Token Pool')),
        "symbol": tas.bytes(char2Bytes('SYMMLP')),
        "decimals": tas.bytes(char2Bytes('18')),
        "thumbnailUri":tas.bytes(char2Bytes('https://assets.coingecko.com/coins/images/18525/small/SYMM-Coin-2.png?1632276841')),
        }),
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
              0: tas.address('KT1JA3UQ6R4C84mH3FqS3G5mKFeEdLumrDc3'),
              1: tas.nat('0'),
          }},
          {
            key: tas.nat('1'),
            value: {
              0: tas.address('KT1JA3UQ6R4C84mH3FqS3G5mKFeEdLumrDc3'),
              1: tas.nat('1'),
          }},
          {
            key: tas.nat('2'),
            value: {
              0: tas.address('KT1JA3UQ6R4C84mH3FqS3G5mKFeEdLumrDc3'),
              1: tas.nat('2'),
          }},
          {
            key: tas.nat('3'),
            value: {
              0: tas.address('KT1JA3UQ6R4C84mH3FqS3G5mKFeEdLumrDc3'),
              1: tas.nat('3'),
          }},
          {
            key: tas.nat('4'),
            value: {
              0: tas.address('KT1JA3UQ6R4C84mH3FqS3G5mKFeEdLumrDc3'),
              1: tas.nat('4'),
          }},
          {
            key: tas.nat('5'),
            value: {
              0: tas.address('KT1JA3UQ6R4C84mH3FqS3G5mKFeEdLumrDc3'),
              1: tas.nat('5'),
          }},
          {
            key: tas.nat('6'),
            value: {
              0: tas.address('KT1JA3UQ6R4C84mH3FqS3G5mKFeEdLumrDc3'),
              1: tas.nat('6'),
          }},
          {
            key: tas.nat('7'),
            value: {
              0: tas.address('KT1JA3UQ6R4C84mH3FqS3G5mKFeEdLumrDc3'),
              1: tas.nat('7'),
          }},
        ]),
  }).send();
    await createRequest.confirmation(1);
  })
  .catch((error) => console.table(`Error: ${JSON.stringify(error, null, 2)}`));