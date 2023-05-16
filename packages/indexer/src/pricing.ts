import { DbContext } from "@tezos-dappetizer/database";
import BigNumber from "bignumber.js";
import { SimpleConsoleLogger } from "typeorm";
// import { LatestPrice, Pool, PoolHistoricalLiquidity, PoolToken, Symmetric, Token, TokenPrice } from "./entities";
import {
  MAX_NEG_PRICE_CHANGE,
  MAX_POS_PRICE_CHANGE,
  MAX_TIME_DIFF_FOR_PRICING,
  PRICING_ASSETS,
  USD_STABLE_ASSETS,
} from "./helpers/constants";
import {
  createPoolSnapshot,
  getSymmetricSnapshot,
  getToken,
  loadPoolToken,
  ZERO_BD,
} from "./helpers/misc";
import { isComposableStablePool } from "./helpers/pools";
import { WeightedPoolFactoryCreateParameterTokensValue } from "./weighted-pool-factory-indexer-interfaces.generated";
import { Pool } from "./entities/Pool";
import { LatestPrice } from "./entities/LatestPrice";
import { PoolHistoricalLiquidity } from "./entities/PoolHistoricalLiquidity";
import { PoolToken } from "./entities/PoolToken";
import { Symmetric } from "./entities/Symmetric";
import { Token } from "./entities/Token";
import { TokenPrice } from "./entities/TokenPrice";

export async function updatePoolLiquidity(
  poolId: string,
  timestamp: number,
  dbContext: DbContext
): Promise<boolean> {
  const pool = await dbContext.transaction.findOneBy(Pool, { id: poolId });
  if (pool == null) return false;
  const tokensList = pool.tokensList;
  let newPoolLiquidity: BigNumber = BigNumber(ZERO_BD);

  for (let j: number = 0; j < tokensList.length; j++) {
    const tokenAddress = tokensList[j].slice(0, 36);
    const tokenId = BigNumber(tokensList[j].slice(36));
    // Exclude virtual supply from pool value
    if (isComposableStablePool(pool) && pool.address === tokenAddress) {
      continue;
    }

    const poolToken = await dbContext.transaction.findOneBy(PoolToken, {
      poolId: pool.id,
      address: tokenAddress,
      poolTokenId: tokenId ? tokenId.toString() : undefined,
    });
    console.log("poolToken: ", poolToken);
    if (poolToken == null) continue;

    const poolTokenQuantity: BigNumber = BigNumber(poolToken.balance);
    const poolTokenValue = await valueInUSD(
      poolTokenQuantity,
      tokenAddress,
      tokenId,
      dbContext
    );
    console.log("poolTokenValue: ", poolTokenValue);
    newPoolLiquidity = newPoolLiquidity.plus(poolTokenValue);
    console.log("newPoolLiquidity: ", newPoolLiquidity);
  }

  const oldPoolLiquidity: BigNumber = BigNumber(pool.totalLiquidity);
  const liquidityChange: BigNumber = newPoolLiquidity.minus(oldPoolLiquidity);

  // Update pool stats
  pool.totalLiquidity = newPoolLiquidity.toString();
  await dbContext.transaction.save(Pool, pool);

  // We want to avoid too frequently calling setWrappedTokenPrice because it makes a call to the rate provider
  // Doing it here allows us to do it only once, when the MIN_POOL_LIQUIDITY threshold is crossed
  // if (oldPoolLiquidity < MIN_POOL_LIQUIDITY) {
  //   setWrappedTokenPrice(pool, poolId, block_number, timestamp);
  // }

  // update SPT price
  await updateSptPrice(pool, dbContext);

  // Create or update pool daily snapshot
  await createPoolSnapshot(pool, timestamp, dbContext);

  // Update global stats
  const vault = await dbContext.transaction.findOneBy(Symmetric, { id: "1" });
  vault!.totalLiquidity = BigNumber(vault!.totalLiquidity)
    .plus(liquidityChange)
    .toString();
  await dbContext.transaction.save(Symmetric, vault!);

  const vaultSnapshot = await getSymmetricSnapshot(
    vault!.id,
    timestamp,
    dbContext
  );

  vaultSnapshot.totalLiquidity = vault!.totalLiquidity;
  await dbContext.transaction.save(Symmetric, vaultSnapshot);
  return true;
}

export async function valueInUSD(
  value: BigNumber,
  asset: string,
  assetId: BigNumber | null,
  dbContext: DbContext
): Promise<BigNumber> {
  let usdValue = BigNumber(ZERO_BD);
  console.log(assetId);
  console.log(isUSDStable(asset, assetId ? assetId : BigNumber(0)));
  if (isUSDStable(asset, assetId ? assetId : BigNumber(0))) {
    usdValue = value;
  } else {
    // convert to USD
    const token = await getToken(asset, assetId, dbContext);

    if (token.latestUSDPrice) {
      const latestUSDPrice = BigNumber(token.latestUSDPrice);
      usdValue = value.times(latestUSDPrice);
    }
  }

  return usdValue;
}

export async function swapValueInUSD(
  tokenInAddress: string,
  tokenInId: BigNumber | null,
  tokenAmountIn: BigNumber,
  tokenOutAddress: string,
  tokenOutId: BigNumber | null,
  tokenAmountOut: BigNumber,
  dbContext: DbContext
): Promise<BigNumber> {
  let swapValueUSD = BigNumber(ZERO_BD);

  if (isUSDStable(tokenOutAddress, tokenOutId)) {
    // if one of the tokens is a stable, it takes precedence
    swapValueUSD = await valueInUSD(
      tokenAmountOut,
      tokenOutAddress,
      tokenOutId,
      dbContext
    );
    return swapValueUSD;
  } else if (isUSDStable(tokenInAddress, tokenInId)) {
    // if one of the tokens is a stable, it takes precedence
    console.log("isStable");
    swapValueUSD = await valueInUSD(
      tokenAmountIn,
      tokenInAddress,
      tokenInId,
      dbContext
    );
    return swapValueUSD;
  }

  if (
    isPricingAsset(tokenInAddress, tokenInId) &&
    !isPricingAsset(tokenOutAddress, tokenOutId)
  ) {
    // if only one of the tokens is a pricing asset, it takes precedence
    swapValueUSD = await valueInUSD(
      tokenAmountIn,
      tokenInAddress,
      tokenInId,
      dbContext
    );
    if (swapValueUSD.gt(ZERO_BD)) return swapValueUSD;
  }

  if (
    isPricingAsset(tokenOutAddress, tokenOutId) &&
    !isPricingAsset(tokenInAddress, tokenInId)
  ) {
    // if only one of the tokens is a pricing asset, it takes precedence
    swapValueUSD = await valueInUSD(
      tokenAmountOut,
      tokenOutAddress,
      tokenOutId,
      dbContext
    );
    if (swapValueUSD.gt(ZERO_BD)) return swapValueUSD;
  }

  // if none or both tokens are pricing assets, take the average of the known prices
  let tokenInSwapValueUSD = await valueInUSD(
    tokenAmountIn,
    tokenInAddress,
    tokenInId,
    dbContext
  );
  let tokenOutSwapValueUSD = await valueInUSD(
    tokenAmountOut,
    tokenOutAddress,
    tokenOutId,
    dbContext
  );
  let divisor =
    tokenInSwapValueUSD.gt(ZERO_BD) && tokenOutSwapValueUSD.gt(ZERO_BD)
      ? BigNumber("2")
      : BigNumber("1");
  swapValueUSD = tokenInSwapValueUSD.plus(tokenOutSwapValueUSD).div(divisor);

  return swapValueUSD;
}

export function isUSDStable(
  asset: string,
  id: BigNumber | null = null
): boolean {
  for (let i: number = 0; i < USD_STABLE_ASSETS.length; i++) {
    if (
      USD_STABLE_ASSETS[i].address === asset &&
      USD_STABLE_ASSETS[i].id.toNumber() === (id ? id.toNumber() : 0)
    )
      return true;
  }
  return false;
}

export async function updateSptPrice(
  pool: Pool,
  dbContext: DbContext
): Promise<void> {
  if (BigNumber(pool.totalShares).isEqualTo(ZERO_BD)) return;

  const sptAddress = pool.address;
  const sptToken = await getToken(sptAddress, null, dbContext);
  sptToken.latestUSDPrice = BigNumber(pool.totalLiquidity)
    .div(pool.totalShares)
    .toString();
  dbContext.transaction.save(Token, sptToken);
}

export async function addHistoricalPoolLiquidityRecord(
  poolId: string,
  block: number,
  pricingAsset: string,
  pricingAssetId: BigNumber | null,
  dbContext: DbContext
): Promise<boolean> {
  const pool = await dbContext.transaction.findOneBy(Pool, { id: poolId });
  if (pool == null) return false;
  const tokensList = pool.tokensList;
  if (tokensList.length < 2) return false;
  // if (hasVirtualSupply(pool) && pool.address == pricingAsset) return false;

  let poolValue = BigNumber(ZERO_BD);

  for (let j: number = 0; j < tokensList.length; j++) {
    const tokenAddress = tokensList[j].slice(0, 36);
    const tokenId = BigNumber(tokensList[j].slice(36));

    const poolToken = await loadPoolToken(
      poolId,
      tokenAddress,
      tokenId,
      dbContext
    );
    if (poolToken == null) continue;

    if (tokenAddress === pricingAsset && tokenId === pricingAssetId) {
      poolValue = poolValue.plus(poolToken.balance);
      continue;
    }
    const poolTokenQuantity = BigNumber(poolToken.balance);

    let price = BigNumber(ZERO_BD);
    const tokenAsset = tokenAddress.concat(tokenId ? tokenId.toString() : "0");
    const pricing = pricingAsset.concat(
      pricingAssetId ? pricingAssetId.toString() : "0"
    );
    const latestPriceId = getLatestPriceId(tokenAsset, pricing);
    const latestPrice = await dbContext.transaction.findOneBy(LatestPrice, {
      id: latestPriceId,
    });

    // note that we can only meaningfully report liquidity once assets are traded with
    // the pricing asset
    if (latestPrice) {
      // value in terms of priceableAsset
      price = BigNumber(latestPrice.price);
    }
    // else if (pool.poolType == PoolType.StablePhantom || isComposableStablePool(pool)) {
    //   // try to estimate token price in terms of pricing asset
    //   let pricingAssetInUSD = await valueInUSD(BigNumber('1'), pricingAsset);
    //   let currentTokenInUSD = await valueInUSD(BigNumber('1'), tokenAddress, tokenId, dbContext);

    //   if (pricingAssetInUSD.isEqualTo(ZERO_BD) || currentTokenInUSD.isEqualTo(ZERO_BD)) {
    //     continue;
    //   }

    //   price = currentTokenInUSD.div(pricingAssetInUSD);
    // }

    // Exclude virtual supply from pool value
    // if (hasVirtualSupply(pool) && pool.address == tokenAddress) {
    //   continue;
    // }

    if (price.gt(ZERO_BD)) {
      const poolTokenValue = price.times(poolTokenQuantity);
      poolValue = poolValue.plus(poolTokenValue);
    }
  }

  const newPoolLiquidity =
    (await valueInUSD(poolValue, pricingAsset, pricingAssetId, dbContext)) ||
    ZERO_BD;

  // If the pool isn't empty but we have a zero USD value then it's likely that we have a bad pricing asset
  // Don't commit any changes and just report the failure.
  if (poolValue.gt(ZERO_BD) !== newPoolLiquidity.gt(ZERO_BD)) {
    return false;
  }

  // Take snapshot of pool state
  const phlId = getPoolHistoricalLiquidityId(
    poolId,
    pricingAsset,
    pricingAssetId,
    block
  );
  const phl = new PoolHistoricalLiquidity();
  phl.id = phlId;
  phl.poolId = pool;
  phl.pricingAsset = pricingAsset;
  phl.block = BigInt(block);
  phl.poolTotalShares = pool.totalShares;
  phl.poolLiquidity = poolValue.toString();
  phl.poolShareValue = BigNumber(pool.totalShares).gt(ZERO_BD)
    ? poolValue.div(pool.totalShares).toString()
    : ZERO_BD;
  await dbContext.transaction.save(PoolHistoricalLiquidity, phl);

  return true;
}

export function getLatestPriceId(
  tokenAsset: string,
  pricingAsset: string
): string {
  return tokenAsset.concat("-").concat(pricingAsset);
}

export function getPoolHistoricalLiquidityId(
  poolId: string,
  tokenAddress: string,
  tokenId: BigNumber | null,
  block: number
): string {
  return poolId
    .concat("-")
    .concat(tokenAddress)
    .concat(tokenId ? tokenId.toString() : "")
    .concat("-")
    .concat(block.toString());
}

export function isPricingAsset(
  asset: string,
  id: BigNumber | null = null
): boolean {
  for (let i: number = 0; i < PRICING_ASSETS.length; i++) {
    if (
      PRICING_ASSETS[i].address == asset &&
      PRICING_ASSETS[i].id.toNumber() == (id ? id.toNumber() : 0)
    ) {
      return true;
    }
  }
  return false;
}

export async function updateLatestPrice(
  tokenPrice: TokenPrice,
  blockTimestamp: number,
  dbContext: DbContext
): Promise<void> {
  let tokenAsset = tokenPrice.asset;
  let pricingAsset = tokenPrice.pricingAsset;

  let latestPriceId = getLatestPriceId(tokenAsset, pricingAsset);
  let latestPrice = (await dbContext.transaction.findOneBy(LatestPrice, {
    id: latestPriceId,
  })) as LatestPrice;

  if (latestPrice == null) {
    latestPrice = new LatestPrice();
    latestPrice.id = latestPriceId;
    latestPrice.asset = tokenPrice.asset;
    latestPrice.assetId = tokenPrice.assetId;
    latestPrice.pricingAsset = tokenPrice.pricingAsset;
    latestPrice.pricingAssetId = tokenPrice.pricingAssetId;
  }

  latestPrice.block = tokenPrice.block;
  latestPrice.poolId = tokenPrice.pool;
  latestPrice.price = tokenPrice.price;
  await dbContext.transaction.save(LatestPrice, latestPrice);

  let token = await getToken(
    tokenAsset.slice(0, 36),
    BigNumber(tokenAsset.slice(36)),
    dbContext
  );
  const currentUSDPrice = await valueInUSD(
    BigNumber(tokenPrice.price),
    tokenPrice.pricingAsset,
    BigNumber(tokenPrice.pricingAssetId),
    dbContext
  );

  if (currentUSDPrice == BigNumber(ZERO_BD)) return;

  let oldUSDPrice = BigNumber(token.latestUSDPrice!);
  if (!oldUSDPrice || oldUSDPrice.isEqualTo(ZERO_BD)) {
    token.latestUSDPriceTimestamp = blockTimestamp;
    token.latestUSDPrice = currentUSDPrice.toString();
    token.latestPrice = latestPrice;
    await dbContext.transaction.save(Token, token);
    return;
  }

  let change = currentUSDPrice.minus(oldUSDPrice).div(oldUSDPrice);
  if (
    !token.latestUSDPriceTimestamp ||
    (change.lt(MAX_POS_PRICE_CHANGE) && change.gt(MAX_NEG_PRICE_CHANGE)) ||
    // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
    BigNumber(blockTimestamp)
      .minus(token.latestUSDPriceTimestamp!)
      .gt(MAX_TIME_DIFF_FOR_PRICING)
  ) {
    token.latestUSDPriceTimestamp = blockTimestamp;
    token.latestUSDPrice = currentUSDPrice.toString();
    token.latestPrice = latestPrice;
    await dbContext.transaction.save(Token, token);
  }
}

export function getPreferentialPricingAsset(assets: string[]): string {
  // Assumes PRICING_ASSETS are sorted by order of preference
  for (let i: number = 0; i < PRICING_ASSETS.length; i++) {
    if (
      assets.includes(
        PRICING_ASSETS[i].address.concat(PRICING_ASSETS[i].id.toString())
      )
    )
      return PRICING_ASSETS[i].address;
  }
  return "0";
}

// // export function setWrappedTokenPrice(pool: Pool, poolId: string, block_number: BigInt, timestamp: BigInt): void {
// //   if (isLinearPool(pool)) {
// //     if (pool.totalLiquidity.gt(MIN_POOL_LIQUIDITY)) {
// //       const poolAddress = bytesToAddress(pool.address);
// //       let poolContract = AaveLinearPool.bind(poolAddress);
// //       let rateCall = poolContract.try_getWrappedTokenRate();
// //       if (rateCall.reverted) {
// //         log.info('getWrappedTokenRate reverted', []);
// //       } else {
// //         const rate = rateCall.value;
// //         const amount = BigDecimal.fromString('1');
// //         const asset = bytesToAddress(pool.tokensList[pool.wrappedIndex]);
// //         const pricingAsset = bytesToAddress(pool.tokensList[pool.mainIndex]);
// //         const price = scaleDown(rate, 18);
// //         let tokenPriceId = getTokenPriceId(poolId, asset, pricingAsset, block_number);
// //         let tokenPrice = new TokenPrice(tokenPriceId);
// //         tokenPrice.poolId = poolId;
// //         tokenPrice.block = block_number;
// //         tokenPrice.timestamp = timestamp.toI32();
// //         tokenPrice.asset = asset;
// //         tokenPrice.pricingAsset = pricingAsset;
// //         tokenPrice.amount = amount;
// //         tokenPrice.price = price;
// //         tokenPrice.save();
// //         updateLatestPrice(tokenPrice, timestamp);
// //       }
// //     }
// //   }
// // }
