import BigNumber from 'bignumber.js';
import { Pool, Token } from '../entities';
import { TezosToolkit } from '@taquito/taquito';
import { WeightedPoolFactoryInitialStorage } from '../weighted-pool-factory-indexer-interfaces.generated';

const ZERO_BD = '0';

export function newPoolEntity(poolId: string): Pool {
  let pool = new Pool();
  pool.id = poolId;
  pool.vaultID = '1';
  pool.tokensList = [];
  pool.totalWeight = ZERO_BD;
  pool.totalSwapVolume = ZERO_BD;
  pool.totalSwapFee = ZERO_BD;
  pool.totalLiquidity = ZERO_BD;
  pool.totalShares = ZERO_BD;
  pool.swapsCount = BigInt(0);
  pool.holdersCount = BigInt(0);

  return pool;
}

export function scaleDown(num: BigNumber, decimals: number): string {
  return (num.div(10 ** decimals)).toString()
}

export async function getStorage(poolAddress: string) {
  const tezos = new TezosToolkit('http:localhost:20000');
  const contract = await tezos.contract.at(poolAddress);
  return await contract.storage() as WeightedPoolFactoryInitialStorage;
}