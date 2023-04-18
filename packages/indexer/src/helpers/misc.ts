import { TezosToolkit } from '@taquito/taquito';
import { Tzip12Module, tzip12 } from '@taquito/tzip12';
import { DbContext } from '@tezos-dappetizer/database';
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

export function getToken(tokenAddress: string, dbContext: DbContext ): Token {
  let token = dbContext.transaction.findOneBy(Token,{id: tokenAddress});
  if (token == null) {
    token = createToken(tokenAddress);
  }
  return token;
}

export function createToken(tokenAddress: Address): Token {
  let erc20token = ERC20.bind(tokenAddress);
  let token = new Token(tokenAddress.toHexString());
  let name = '';
  let symbol = '';
  let decimals = 0;

  // attempt to retrieve erc20 values
  let maybeName = erc20token.try_name();
  let maybeSymbol = erc20token.try_symbol();
  let maybeDecimals = erc20token.try_decimals();

  if (!maybeName.reverted) name = maybeName.value;
  if (!maybeSymbol.reverted) symbol = maybeSymbol.value;
  if (!maybeDecimals.reverted) decimals = maybeDecimals.value;

  let pool = WeightedPool.bind(tokenAddress);
  let isPoolCall = pool.try_getPoolId();
  if (!isPoolCall.reverted) {
    let poolId = isPoolCall.value;
    token.poolId = poolId.toHexString();
  }

  token.name = name;
  token.symbol = symbol;
  token.decimals = decimals;
  token.totalBalanceUSD = ZERO_BD;
  token.totalBalanceNotional = ZERO_BD;
  token.totalSwapCount = ZERO;
  token.totalVolumeUSD = ZERO_BD;
  token.totalVolumeNotional = ZERO_BD;
  token.address = tokenAddress.toHexString();
  token.save();
  return token;
}