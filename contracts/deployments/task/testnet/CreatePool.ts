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
    const contract = await Tezos.contract.at<ContractType>('KT1B3DinmvQp2eWNZhVXWUveBeaty2Kx24rF');
    const createRequest = await contract.methodsObject.default({
      metadata: tas.bytes(
        "697066733a2f2f516d527a593459644842465565754750686d50524155576b564e39716848337057313465743556366b5a71465a4d"),
      token_metadata: tas.map({
        "name": tas.bytes("53594d4d2f4354455a2035303a3530"),
        "symbol": tas.bytes("53594d4d4c50"),
        "decimals": tas.bytes("3138"),
        "thumbnailUri":tas.bytes("697066733a2f2f516d527a593459644842465565754750686d50524155576b564e39716848337057313465743556366b5a71465a4d"),
        }),
  }).send();
    await createRequest.confirmation(1);
  })
  .catch((error) => console.table(`Error: ${JSON.stringify(error, null, 2)}`));