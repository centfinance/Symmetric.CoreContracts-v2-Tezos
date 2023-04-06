import { deployExternalContracts } from './deployExternalContracts';
import { deployVault } from './deployVault';
import { deployProtocolFeesCollector } from './deployProtocolFeesCollector';
import { deployWeightedPoolFactory } from './deployWeightedPoolFactory';


export async function deployAll(adminAddress: string) {
    try {
      const contracts = await deployExternalContracts() as string[];

      const vault = await deployVault(adminAddress)

      const protocolFeeProvider = await deployProtocolFeesCollector(
        adminAddress, 
        vault?.address as string, 
        '1000000000000000', 
        '400000000000000000'
      )

      await deployWeightedPoolFactory(
        adminAddress,
        protocolFeeProvider?.address as string,
        vault?.address as string,
        contracts[0],
        contracts[1],
      )

      console.log('All contracts deployed')

    } catch (error) {
        console.error('Error deploying contract:', error);
    }
}