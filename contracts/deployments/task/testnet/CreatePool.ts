import { InMemorySigner  } from '@taquito/signer';
import { char2Bytes } from '@taquito/utils';
import { TezosToolkit } from '@taquito/taquito';
import { tas } from '../../../../types/type-aliases';
import { WeightedPoolFactoryCompileContractType as ContractType } from '../../../../types/WeightedPoolFactory.compile.types';

const Tezos = new TezosToolkit("https://ghostnet.ecadinfra.com");

const config = require('../../../../.taq/config.local.testing.json')

InMemorySigner.fromSecretKey(config.accounts.taqOperatorAccount.privateKey)
  .then((theSigner) => {
    Tezos.setProvider({ signer: theSigner });
  })
  .then( async () => {
    const contract = await Tezos.contract.at<ContractType>('KT1Ewux3ZjVaGnowHo9sVu7wzGhDbq3he65o');
    const createRequest = await contract.methodsObject.default({
      metadata: tas.bytes(
        char2Bytes('SYMMLP')),
      token_metadata: tas.map({
        "name": tas.bytes(char2Bytes('8 Token Pool')),
        "symbol": tas.bytes(char2Bytes('SYMMLP')),
        "decimals": tas.bytes(char2Bytes('18')),
        "thumbnailUri":tas.bytes(char2Bytes('https://assets.coingecko.com/coins/images/18525/small/SYMM-Coin-2.png?1632276841')),
        }),
  }).send();
    await createRequest.confirmation(1);
  })
  .catch((error) => console.table(`Error: ${JSON.stringify(error, null, 2)}`));