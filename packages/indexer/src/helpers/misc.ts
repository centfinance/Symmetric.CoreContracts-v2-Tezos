import { TezosToolkit } from '@taquito/taquito';
import { Tzip12Module, tzip12 } from '@taquito/tzip12';
import BigNumber from 'bignumber.js';
import { Pool, Token } from '../entities';
import { WeightedPoolContractType } from '../types/weighted-pool-types';
import { WeightedPoolFactoryInitialStorage } from '../weighted-pool-factory-indexer-interfaces.generated';

const tezos = new TezosToolkit('http://localhost:20000');
tezos.addExtension(new Tzip12Module());

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
  const contract = await tezos.contract.at<WeightedPoolContractType>(poolAddress);
  return await contract.storage();
}

export async function getTokenMetadata(tokenAddress: string, tokenId: number) {
  const contract = await tezos.contract.at(tokenAddress, tzip12);
  return await contract.tzip12().getTokenMetadata(tokenId);
}