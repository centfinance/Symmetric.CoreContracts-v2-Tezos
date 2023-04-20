import { TezosToolkit } from '@taquito/taquito';
import { Tzip12Module, tzip12 } from '@taquito/tzip12';
import { DbContext } from '@tezos-dappetizer/database';
import BigNumber from 'bignumber.js';
import { Pool, PoolSnapshot, PoolToken, Token } from '../entities';
import { WeightedPoolContractType } from '../types/weighted-pool-types';
import { WeightedPoolFactoryCreateParameterTokensValue, WeightedPoolFactoryInitialStorage } from '../weighted-pool-factory-indexer-interfaces.generated';
import { getPoolTokenId } from './pools';

const tezos = new TezosToolkit('http://localhost:20000');
tezos.addExtension(new Tzip12Module());

export const ZERO_BD = '0';

const DAY = 24 * 60 * 60;

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

export async function getToken(tokenAddress: string, tokenId: number, dbContext: DbContext ): Promise<Token> {
  let token = await dbContext.transaction.findOneBy(Token,{id: tokenAddress});
  if (token == null) {
    token = await createToken(tokenAddress, tokenId, dbContext);
  }
  return token;
}

export async function createToken(tokenAddress: string, tokenId: number, dbContext: DbContext): Promise<Token> {
  let token = new Token();
  token.id = tokenAddress.concat(tokenId.toString());

  // let pool = WeightedPool.bind(tokenAddress);
  // let isPoolCall = pool.try_getPoolId();
  // if (!isPoolCall.reverted) {
  //   let poolId = isPoolCall.value;
  //   token.poolId = poolId.toHexString();
  // }

  let metadata = await getTokenMetadata(tokenAddress, tokenId);

  token.name = metadata.name;
  token.symbol = metadata.symbol;
  token.decimals = metadata.decimals;
  token.totalBalanceUSD = ZERO_BD;
  token.totalBalanceNotional = ZERO_BD;
  token.totalSwapCount = BigInt(0);
  token.totalVolumeUSD = ZERO_BD;
  token.totalVolumeNotional = ZERO_BD;
  token.address = tokenAddress;
  token.tokenId = tokenId;
  dbContext.transaction.save(Token, token);
  return token;
}

export async function createPoolTokenEntity(
  pool: Pool,
  tokenAddress: string,
  tokenId: BigNumber | null,
  tokenIndex: number,
  dbContext: DbContext,
): Promise<void> {
  let poolTokenId = getPoolTokenId(pool.id, tokenAddress, tokenId ? tokenId : BigNumber(0));

  let token = await getTokenMetadata(tokenAddress, tokenId ? tokenId.toNumber() : 0);
  let symbol = token.symbol!;
  let name = token.name!;
  let decimals = 18;

  let poolToken = new PoolToken();
  poolToken.id = poolTokenId;
  // ensures token entity is created
  let _token = await getToken(tokenAddress, tokenId ? tokenId.toNumber() : 0, dbContext);
  
  poolToken.poolId = pool;
  poolToken.address = tokenAddress;
  poolToken.tokenId = tokenId ? tokenId.toString() : null;
  poolToken.name = name;
  poolToken.symbol = symbol;
  poolToken.decimals = decimals;
  poolToken.balance = ZERO_BD;
  poolToken.cashBalance = ZERO_BD;
  poolToken.managedBalance = ZERO_BD;
  poolToken.priceRate = '1';
  poolToken.oldPriceRate = '1';
  poolToken.token = _token;
  poolToken.index = tokenIndex;

  await dbContext.transaction.save(PoolToken, poolToken);
}

export async function loadPoolToken(poolId: string, tokenAddress: string, tokenId: BigNumber | null, dbContext: DbContext): Promise<PoolToken | null> {
  return await dbContext.transaction.findOneBy(PoolToken, {id: getPoolTokenId(poolId, tokenAddress, tokenId ? tokenId : BigNumber(0))});
}

export async function createPoolSnapshot(pool: Pool, timestamp: number, dbContext: DbContext): Promise<void> {
  let dayTimestamp = timestamp - (timestamp % DAY); // Todays Timestamp

  let poolId = pool.id;
  if (pool == null || !pool.tokensList) return;

  let snapshotId = poolId + '-' + dayTimestamp.toString();
  let snapshot = await dbContext.transaction.findOneBy(PoolSnapshot, { id: snapshotId });

  if (!snapshot) {
    snapshot = new PoolSnapshot();
    snapshot.id = snapshotId;
  }

  let tokens = pool.tokensList;
  let amounts = new Array<string>(tokens.length);
  for (let i = 0; i < tokens.length; i++) {
    let token = JSON.parse(tokens[i]) as WeightedPoolFactoryCreateParameterTokensValue;
    let tokenAddress = token[0];
    let tokenId = token[1];
    let poolToken = await loadPoolToken(poolId, tokenAddress, tokenId ? tokenId : BigNumber(0), dbContext);
    if (poolToken == null) continue;

    amounts[i] = poolToken.balance;
  }

  snapshot.pool = pool;
  snapshot.amounts = amounts;
  snapshot.totalShares = pool.totalShares;
  snapshot.swapVolume = pool.totalSwapVolume;
  snapshot.swapFees = pool.totalSwapFee;
  snapshot.liquidity = pool.totalLiquidity;
  snapshot.swapsCount = pool.swapsCount;
  snapshot.holdersCount = pool.holdersCount;
  snapshot.timestamp = dayTimestamp;
  dbContext.transaction.save(PoolSnapshot, snapshot);
}