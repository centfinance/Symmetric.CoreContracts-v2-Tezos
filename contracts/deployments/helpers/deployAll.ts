import { deployExternalContracts } from './deployExternalContracts';
import { deployVault } from './deployVault';
import { deployProtocolFeesCollector } from './deployProtocolFeesCollector';
import { deployWeightedPoolFactory } from './deployWeightedPoolFactory';
import { TezosToolkit } from '@taquito/taquito';
import { InMemorySigner } from '@taquito/signer';



export async function deployAll(adminAddress: string, network: string) {
    try {
      const config = require(`../../../.taq/config.local.${network == 'local' ? 'development' : 'testing'}.json`);

      const tezos = new TezosToolkit(config.rpcUrl);
      const secretKey = network == 'local' ? config.accounts[config.accountDefault].secretKey.slice(12) : config.accounts[config.accountDefault].privateKey;
      const signer = await InMemorySigner.fromSecretKey(secretKey);
      tezos.setProvider({ signer });

      await deployExternalContracts(tezos) as string[];

      const vault = await deployVault(adminAddress, tezos)

      await deployProtocolFeesCollector(
        adminAddress, 
        vault?.address as string, 
        '1000000000000000', 
        '400000000000000000',
        tezos,
      )

      // await deployWeightedPoolFactory(
      //   adminAddress,
      //   protocolFeeProvider?.address as string,
      //   vault?.address as string,
      //   contracts[0],
      //   contracts[1],
      //   tezos,
      // )

      console.log('All contracts deployed')

    } catch (error) {
        console.error('Error deploying contract:', error);
    }
}