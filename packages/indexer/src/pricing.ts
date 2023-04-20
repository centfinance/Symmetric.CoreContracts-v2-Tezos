import { DbContext } from "@tezos-dappetizer/database";
import BigNumber from "bignumber.js";
import { Pool, PoolToken, Symmetric, Token } from "./entities";
import { USD_STABLE_ASSETS } from "./helpers/constants";
import { createPoolSnapshot, getSymmetricSnapshot, getToken, ZERO_BD } from "./helpers/misc";
import { isComposableStablePool } from "./helpers/pools";
import { WeightedPoolFactoryCreateParameterTokensValue } from "./weighted-pool-factory-indexer-interfaces.generated";


export async function updatePoolLiquidity(poolId: string, timestamp: number, dbContext: DbContext): Promise<boolean> {
  let pool = await dbContext.transaction.findOneBy(Pool,  { id: poolId });
  if (pool == null) return false;
  let tokensList = pool.tokensList;
  let newPoolLiquidity: BigNumber = BigNumber(ZERO_BD);

  for (let j: number = 0; j < tokensList.length; j++) {
    let token = JSON.parse(tokensList[j]) as WeightedPoolFactoryCreateParameterTokensValue;
    let tokenAddress = token[0];
    let tokenId = token[1];
    // Exclude virtual supply from pool value
    if (isComposableStablePool(pool) && pool.address == tokenAddress) {
      continue;
    }

    let poolToken = await dbContext.transaction.findOneBy(PoolToken, { poolId: pool.id,  address: tokenAddress, tokenId: tokenId ? tokenId.toString() : undefined });
    if (poolToken == null) continue;

    let poolTokenQuantity: BigNumber = BigNumber(poolToken.balance);
    let poolTokenValue = await valueInUSD(poolTokenQuantity, tokenAddress, tokenId, dbContext);
    newPoolLiquidity = newPoolLiquidity.plus(poolTokenValue);
  }

  let oldPoolLiquidity: BigNumber = BigNumber(pool.totalLiquidity);
  let liquidityChange: BigNumber = newPoolLiquidity.minus(oldPoolLiquidity);

  // Update pool stats
  pool.totalLiquidity = newPoolLiquidity.toString();
  await dbContext.transaction.save(Pool, pool);

  // We want to avoid too frequently calling setWrappedTokenPrice because it makes a call to the rate provider
  // Doing it here allows us to do it only once, when the MIN_POOL_LIQUIDITY threshold is crossed
  // if (oldPoolLiquidity < MIN_POOL_LIQUIDITY) {
  //   setWrappedTokenPrice(pool, poolId, block_number, timestamp);
  // }

  // update BPT price
  await updateSptPrice(pool, dbContext);

  // Create or update pool daily snapshot
  await createPoolSnapshot(pool, timestamp, dbContext);

  // Update global stats
  let vault = await dbContext.transaction.findOneBy(Symmetric,  { id: '1' });
  vault!.totalLiquidity = BigNumber(vault!.totalLiquidity).plus(liquidityChange).toString();
  await dbContext.transaction.save(Symmetric, vault!);

  let vaultSnapshot = await getSymmetricSnapshot(vault!.id, timestamp, dbContext);
  vaultSnapshot.totalLiquidity = vault!.totalLiquidity;
  await dbContext.transaction.save(Symmetric, vaultSnapshot);
  return true;
}

export async function valueInUSD(value: BigNumber, asset: string, assetId: BigNumber | null, dbContext: DbContext): Promise<BigNumber>  {
  let usdValue = BigNumber(ZERO_BD);

  if (isUSDStable(asset)) {
    usdValue = value;
  } else {
    // convert to USD
    let token = await getToken(asset, assetId ? assetId.toNumber() : 0, dbContext);

    if (token.latestUSDPrice) {
      const latestUSDPrice = BigNumber(token.latestUSDPrice);
      usdValue = value.times(latestUSDPrice);
    }
  }

  return usdValue;
}

export function isUSDStable(asset: string): boolean {
  for (let i: number = 0; i < USD_STABLE_ASSETS.length; i++) {
    if (USD_STABLE_ASSETS[i] == asset) return true;
  }
  return false;
}

export async function updateSptPrice(pool: Pool, dbContext: DbContext): Promise<void> {
  if (BigNumber(pool.totalShares).isEqualTo(ZERO_BD)) return;

  const sptAddress = pool.address;
  let sptToken = await getToken(sptAddress, 0, dbContext);
  sptToken.latestUSDPrice = BigNumber(pool.totalLiquidity).div(pool.totalShares).toString();
  dbContext.transaction.save(Token, sptToken);
}


// export function setWrappedTokenPrice(pool: Pool, poolId: string, block_number: BigInt, timestamp: BigInt): void {
//   if (isLinearPool(pool)) {
//     if (pool.totalLiquidity.gt(MIN_POOL_LIQUIDITY)) {
//       const poolAddress = bytesToAddress(pool.address);
//       let poolContract = AaveLinearPool.bind(poolAddress);
//       let rateCall = poolContract.try_getWrappedTokenRate();
//       if (rateCall.reverted) {
//         log.info('getWrappedTokenRate reverted', []);
//       } else {
//         const rate = rateCall.value;
//         const amount = BigDecimal.fromString('1');
//         const asset = bytesToAddress(pool.tokensList[pool.wrappedIndex]);
//         const pricingAsset = bytesToAddress(pool.tokensList[pool.mainIndex]);
//         const price = scaleDown(rate, 18);
//         let tokenPriceId = getTokenPriceId(poolId, asset, pricingAsset, block_number);
//         let tokenPrice = new TokenPrice(tokenPriceId);
//         tokenPrice.poolId = poolId;
//         tokenPrice.block = block_number;
//         tokenPrice.timestamp = timestamp.toI32();
//         tokenPrice.asset = asset;
//         tokenPrice.pricingAsset = pricingAsset;
//         tokenPrice.amount = amount;
//         tokenPrice.price = price;
//         tokenPrice.save();
//         updateLatestPrice(tokenPrice, timestamp);
//       }
//     }
//   }
// }