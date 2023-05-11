import { TezosToolkit } from "@taquito/taquito";
import { Tzip12Module, tzip12 } from "@taquito/tzip12";
import { DbContext } from "@tezos-dappetizer/database";
import BigNumber from "bignumber.js";
import { Pool } from "../entities/Pool";
import { PoolToken } from "../entities/PoolToken";
import { Symmetric } from "../entities/Symmetric";
import { Token } from "../entities/Token";
// import { Pool,
//   PoolSnapshot,
//   PoolToken,
//   Symmetric,
//   SymmetricSnapshot,
//   Token,
//   TokenSnapshot,
//   TradePair,
//   TradePairSnapshot } from '../entities';
import { valueInUSD } from "../pricing";
import { WeightedPoolContractType } from "../types/weighted-pool-types";
import {
  WeightedPoolFactoryCreateParameterTokensValue,
  WeightedPoolFactoryInitialStorage,
} from "../weighted-pool-factory-indexer-interfaces.generated";
import { getPoolTokenId } from "./pools";
import { PoolSnapshot } from "../entities/PoolSnapshot";
import { SymmetricSnapshot } from "../entities/SymmetricSnapshot";
import { TokenSnapshot } from "../entities/TokenSnapshot";
import { TradePair } from "../entities/TradePair";
import { TradePairSnapshot } from "../entities/TradePairSnapshot";

const tezos = new TezosToolkit("http://localhost:20000");
tezos.addExtension(new Tzip12Module());

export const ZERO_BD = "0";

const DAY = 24 * 60 * 60;

export async function newPoolEntity(
  poolId: string,
  dbContext: DbContext
): Promise<Pool> {
  const pool = new Pool();
  pool.id = poolId;

  let vault = await dbContext.transaction.findOne(Symmetric, {
    where: {
      id: "1",
    },
  });

  if (!vault) {
    vault = new Symmetric();
    vault.id = "1";
    vault.poolCount = 0;
    vault.pools = [];
    vault.totalLiquidity = "0";
    vault.totalSwapCount = BigInt("0");
    vault.totalSwapVolume = "0";
    vault.totalSwapFee = "0";
    await dbContext.transaction.save(Symmetric, vault);
  }

  pool.vault = vault;
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
  return num.div(10 ** decimals).toString();
}

export async function getStorage(poolAddress: string) {
  const contract = await tezos.contract.at<WeightedPoolContractType>(
    poolAddress
  );
  return await contract.storage();
}

export async function getTokenMetadata(tokenAddress: string, tokenId: number) {
  try {
    const contract = await tezos.contract.at(tokenAddress, tzip12);
    return await contract.tzip12().getTokenMetadata(tokenId);
  } catch (e) {
    return {
      name: "Symm LP Token",
      symbol: "SYMMLP",
      decimals: 18,
    };
  }
}

export async function getToken(
  tokenAddress: string,
  tokenId: BigNumber | null,
  dbContext: DbContext
): Promise<Token> {
  let token = await dbContext.transaction.findOneBy(Token, {
    id: tokenAddress.concat(tokenId ? tokenId.toString() : "0"),
  });
  if (token == null) {
    token = await createToken(tokenAddress, tokenId, dbContext);
  }
  return token;
}

export async function createToken(
  tokenAddress: string,
  tokenId: BigNumber | null,
  dbContext: DbContext
): Promise<Token> {
  let token = new Token();
  token.id = tokenAddress.concat(tokenId ? tokenId.toString() : "0");

  // let pool = WeightedPool.bind(tokenAddress);
  // let isPoolCall = pool.try_getPoolId();
  // if (!isPoolCall.reverted) {
  //   let poolId = isPoolCall.value;
  //   token.poolId = poolId.toHexString();
  // }

  let metadata = await getTokenMetadata(
    tokenAddress,
    tokenId ? tokenId.toNumber() : 0
  );

  token.name = metadata.name;
  token.symbol = metadata.symbol;
  token.decimals = Number.isNaN(metadata.decimals) ? 18 : metadata.decimals;
  token.totalBalanceUSD = ZERO_BD;
  token.totalBalanceNotional = ZERO_BD;
  token.totalSwapCount = BigInt(0);
  token.totalVolumeUSD = ZERO_BD;
  token.totalVolumeNotional = ZERO_BD;
  token.address = tokenAddress;
  token.tokenId = tokenId ? tokenId.toNumber() : 0;
  token.FA2 = tokenId ? true : false;

  await dbContext.transaction.save(Token, token);
  return token;
}

export async function createPoolTokenEntity(
  pool: Pool,
  tokenAddress: string,
  tokenId: BigNumber | null,
  tokenIndex: number,
  dbContext: DbContext
): Promise<void> {
  let poolTokenId = getPoolTokenId(
    pool.id,
    tokenAddress,
    tokenId ? tokenId : BigNumber(0)
  );

  let token = await getTokenMetadata(tokenAddress, 0);
  let symbol = token.symbol || "SYMMLP";
  let name = token.name || "Symmetric Pool Token";
  let decimals = 18;

  let poolToken = new PoolToken();
  poolToken.id = poolTokenId;

  // ensures token entity is created
  let _token = await getToken(tokenAddress, tokenId, dbContext);

  poolToken.poolId = pool.id;
  poolToken.pool = pool;
  poolToken.address = tokenAddress;
  poolToken.tokenId = tokenId ? tokenId.toString() : null;
  poolToken.name = name;
  poolToken.symbol = symbol;
  poolToken.decimals = decimals;
  poolToken.balance = ZERO_BD;
  poolToken.cashBalance = ZERO_BD;
  poolToken.managedBalance = ZERO_BD;
  poolToken.priceRate = "1";
  poolToken.oldPriceRate = "1";
  poolToken.token = _token;
  poolToken.index = tokenIndex;

  await dbContext.transaction.save(PoolToken, poolToken);
}

export async function loadPoolToken(
  poolId: string,
  tokenAddress: string,
  tokenId: BigNumber | null,
  dbContext: DbContext
): Promise<PoolToken | null> {
  return await dbContext.transaction.findOneBy(PoolToken, {
    id: getPoolTokenId(poolId, tokenAddress, tokenId ? tokenId : BigNumber(0)),
  });
}

export async function createPoolSnapshot(
  pool: Pool,
  timestamp: number,
  dbContext: DbContext
): Promise<void> {
  let dayTimestamp = timestamp - (timestamp % DAY); // Todays Timestamp

  let poolId = pool.id;
  if (pool == null || !pool.tokensList) return;

  let snapshotId = poolId + "-" + dayTimestamp.toString();
  let snapshot = await dbContext.transaction.findOneBy(PoolSnapshot, {
    id: snapshotId,
  });

  if (!snapshot) {
    snapshot = new PoolSnapshot();
    snapshot.id = snapshotId;
  }

  let tokens = pool.tokensList;
  let amounts = new Array<string>(tokens.length);
  for (let i = 0; i < tokens.length; i++) {
    const tokenAddress = tokens[i].slice(0, 36);
    const tokenId = BigNumber(tokens[i].slice(36));

    let poolToken = await loadPoolToken(
      poolId,
      tokenAddress,
      tokenId ? tokenId : BigNumber(0),
      dbContext
    );
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

export async function getSymmetricSnapshot(
  vaultId: string,
  timestamp: number,
  dbContext: DbContext
): Promise<SymmetricSnapshot> {
  let dayID = timestamp / 86400;
  let id = vaultId + "-" + dayID.toString();
  let snapshot = await dbContext.transaction.findOneBy(SymmetricSnapshot, {
    id: id,
  });

  if (snapshot == null) {
    let dayStartTimestamp = dayID * 86400;
    snapshot = new SymmetricSnapshot();
    snapshot.id = id;
    // we know that the vault should be created by this call
    let vault = (await dbContext.transaction.findOneBy(Symmetric, {
      id: "1",
    })) as Symmetric;

    snapshot.poolCount = vault.poolCount;

    snapshot.totalLiquidity = vault.totalLiquidity;
    snapshot.totalSwapFee = vault.totalSwapFee;
    snapshot.totalSwapVolume = vault.totalSwapVolume;
    snapshot.totalSwapCount = vault.totalSwapCount;
    snapshot.vault = vault;
    snapshot.timestamp = dayStartTimestamp;
    await dbContext.transaction.save(SymmetricSnapshot, snapshot);
  }

  return snapshot;
}

export async function getTokenSnapshot(
  tokenAddress: string,
  tokenId: BigNumber | null,
  timestamp: number,
  dbContext: DbContext
): Promise<TokenSnapshot> {
  let dayID = timestamp / 86400;
  let id =
    tokenAddress +
    (tokenId ? tokenId.toString() : "0") +
    "-" +
    dayID.toString();
  let dayData = await dbContext.transaction.findOneBy(TokenSnapshot, {
    id: id,
  });

  if (dayData == null) {
    let dayStartTimestamp = dayID * 86400;
    let token = await getToken(tokenAddress, tokenId, dbContext);
    dayData = new TokenSnapshot();
    dayData.id = id;
    dayData.timestamp = dayStartTimestamp;
    dayData.totalSwapCount = token.totalSwapCount;
    dayData.totalBalanceUSD = token.totalBalanceUSD;
    dayData.totalBalanceNotional = token.totalBalanceNotional;
    dayData.totalVolumeUSD = token.totalVolumeUSD;
    dayData.totalVolumeNotional = token.totalVolumeNotional;
    dayData.token = token;
    await dbContext.transaction.save(TokenSnapshot, dayData);
  }

  return dayData;
}

export function tokenToDecimal(amount: BigNumber, decimals: number): BigNumber {
  let scale = BigNumber(10).pow(decimals);
  return amount.div(scale);
}

export async function uptickSwapsForToken(
  tokenAddress: string,
  tokenId: BigNumber | null,
  timestamp: number,
  dbContext: DbContext
): Promise<void> {
  let token = await getToken(tokenAddress, tokenId, dbContext);
  // update the overall swap count for the token
  token.totalSwapCount = token.totalSwapCount + BigInt(1);
  await dbContext.transaction.save(Token, token);

  // update the snapshots
  let snapshot = await getTokenSnapshot(
    tokenAddress,
    tokenId,
    timestamp,
    dbContext
  );
  snapshot.totalSwapCount = token.totalSwapCount;
  await dbContext.transaction.save(TokenSnapshot, snapshot);
}

export async function updateTokenBalances(
  tokenAddress: string,
  tokenId: BigNumber | null,
  usdBalance: BigNumber,
  notionalBalance: BigNumber,
  swapDirection: number,
  dbContext: DbContext
): Promise<void> {
  let token = await getToken(tokenAddress, tokenId, dbContext);

  if (swapDirection == 0) {
    const totalBalanceNotional = BigNumber(token.totalBalanceNotional).plus(
      notionalBalance
    );
    token.totalBalanceNotional = totalBalanceNotional.toString();
    token.totalBalanceUSD = (
      await valueInUSD(totalBalanceNotional, tokenAddress, tokenId, dbContext)
    ).toString();
  } else if (swapDirection == 1) {
    const totalBalanceNotional = BigNumber(token.totalBalanceNotional).minus(
      notionalBalance
    );
    token.totalBalanceNotional = totalBalanceNotional.toString();
    token.totalBalanceUSD = (
      await valueInUSD(totalBalanceNotional, tokenAddress, tokenId, dbContext)
    ).toString();
  }

  token.totalVolumeUSD = BigNumber(token.totalVolumeUSD)
    .plus(usdBalance)
    .toString();
  await dbContext.transaction.save(Token, token);
}

export async function getTradePair(
  token0Address: string,
  token0Id: BigNumber | null,
  token1Address: string,
  token1Id: BigNumber | null,
  dbContext: DbContext
): Promise<TradePair> {
  let tradePairId = token0Address
    .concat(token0Id ? token0Id.toString() : "")
    .concat("-")
    .concat(token1Address.concat(token1Id ? token1Id.toString() : ""));
  let tradePair = await dbContext.transaction.findOneBy(TradePair, {
    id: tradePairId,
  });

  if (tradePair == null) {
    tradePair = new TradePair();
    tradePair.id = tradePairId;
    tradePair.token0 = (await dbContext.transaction.findOneBy(Token, {
      id: token0Address.concat(token0Id ? token0Id.toString() : "0"),
    })) as Token;
    tradePair.token1 = (await dbContext.transaction.findOneBy(Token, {
      id: token1Address.concat(token1Id ? token1Id.toString() : "0"),
    })) as Token;
    tradePair.totalSwapFee = ZERO_BD;
    tradePair.totalSwapVolume = ZERO_BD;
    await dbContext.transaction.save(TradePair, tradePair);
  }

  return tradePair;
}

export async function getTradePairSnapshot(
  tradePairId: string,
  timestamp: number,
  dbContext: DbContext
): Promise<TradePairSnapshot> {
  let dayID = timestamp / 86400;
  let id = tradePairId + "-" + dayID.toString();

  let snapshot = await dbContext.transaction.findOneBy(TradePairSnapshot, {
    id: id,
  });
  if (snapshot == null) {
    let dayStartTimestamp = dayID * 86400;
    let tradePair = (await dbContext.transaction.findOneBy(TradePair, {
      id: tradePairId,
    })) as TradePair;

    snapshot = new TradePairSnapshot();
    snapshot.id = id;
    snapshot.pair = tradePair;
    snapshot.timestamp = dayStartTimestamp;
    snapshot.totalSwapVolume =
      tradePair != null ? tradePair.totalSwapVolume : ZERO_BD;
    snapshot.totalSwapFee =
      tradePair != null ? tradePair.totalSwapFee : ZERO_BD;
    await dbContext.transaction.save(TradePairSnapshot, snapshot);
  }
  return snapshot;
}

export function getTokenPriceId(
  poolId: string,
  tokenId: string,
  stableTokenId: string,
  block: number
): string {
  return poolId
    .concat("-")
    .concat(tokenId)
    .concat("-")
    .concat(stableTokenId)
    .concat("-")
    .concat(block.toString());
}
