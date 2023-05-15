import { DbContext } from "@tezos-dappetizer/database";
import {
  contractFilter,
  indexBigMapUpdate,
  indexEntrypoint,
  indexEvent,
  indexOrigination,
  indexStorageChange,
} from "@tezos-dappetizer/decorators";
import {
  BigMapUpdateIndexingContext,
  EventIndexingContext,
  OriginationIndexingContext,
  StorageChangeIndexingContext,
  TransactionIndexingContext,
} from "@tezos-dappetizer/indexer";
import BigNumber from "bignumber.js";
// import { InvestType, JoinExit, Pool, PoolToken, Swap, Symmetric, SymmetricSnapshot, Token, TokenPrice, TokenSnapshot, TradePair, TradePairSnapshot, User } from './entities';
import { MIN_POOL_LIQUIDITY, MIN_SWAP_VALUE_USD } from "./helpers/constants";
import {
  getSymmetricSnapshot,
  getToken,
  getTokenPriceId,
  getTokenSnapshot,
  getTradePair,
  getTradePairSnapshot,
  loadPoolToken,
  scaleDown,
  tokenToDecimal,
  updateTokenBalances,
  uptickSwapsForToken,
  ZERO_BD,
} from "./helpers/misc";
import {
  addHistoricalPoolLiquidityRecord,
  getPreferentialPricingAsset,
  isPricingAsset,
  swapValueInUSD,
  updateLatestPrice,
  updatePoolLiquidity,
  valueInUSD,
} from "./pricing";

import {
  VaultAcceptAdminParameter,
  VaultBatchSwapParameter,
  VaultChangedStorage,
  VaultExitPoolParameter,
  VaultInitialStorage,
  VaultIsPoolRegisteredKey,
  VaultIsPoolRegisteredValue,
  VaultJoinPoolParameter,
  VaultMetadataKey,
  VaultMetadataValue,
  VaultPoolBalanceChangedPayload,
  VaultPoolBalanceChangedPayload1,
  VaultPoolBalanceChangedPayload2,
  VaultPoolRegisteredPayload,
  VaultPoolsBalancesKey,
  VaultPoolsBalancesValue,
  VaultPoolsTokensKey,
  VaultPoolsTokensValue,
  VaultRegisterPoolParameter,
  VaultRegisterTokensParameter,
  VaultSetPausedParameter,
  VaultSwapParameter,
  VaultSwapPayload,
  VaultTokensRegisteredPayload,
  VaultTransferAdminParameter,
} from "./vault-indexer-interfaces.generated";
import { WeightedPoolFactoryCreateParameterTokensValue } from "./weighted-pool-factory-indexer-interfaces.generated";
import { Symmetric } from "./entities/Symmetric";
import { Pool } from "./entities/Pool";
import { PoolToken } from "./entities/PoolToken";
import { TokenSnapshot } from "./entities/TokenSnapshot";
import { Token } from "./entities/Token";
import { SymmetricSnapshot } from "./entities/SymmetricSnapshot";
import { TradePair } from "./entities/TradePair";
import { TradePairSnapshot } from "./entities/TradePairSnapshot";
import { InvestType, JoinExit } from "./entities/JoinExit";
import { User } from "./entities/User";
import { TokenPrice } from "./entities/TokenPrice";
import { Swap } from "./entities/Swap";

@contractFilter({ name: "Vault" })
export class VaultIndexer {
  @indexOrigination()
  async indexOrigination(
    initialStorage: VaultInitialStorage,
    dbContext: DbContext,
    indexingContext: OriginationIndexingContext
  ): Promise<void> {
    // Implement your indexing logic here or delete the method if not needed.
    const vault = new Symmetric();
    vault.id = "1";
    vault.poolCount = 0;
    vault.pools = [];
    vault.totalLiquidity = "0";
    vault.totalSwapCount = BigInt("0");
    vault.totalSwapVolume = "0";
    vault.totalSwapFee = "0";

    await dbContext.transaction.save(Symmetric, vault);
  }

  @indexEvent("PoolBalanceChanged")
  async indexPoolBalanceChangedEvent(
    payload: VaultPoolBalanceChangedPayload,
    dbContext: DbContext,
    indexingContext: EventIndexingContext
  ): Promise<void> {
    const amounts = [...payload.amountsInOrOut.values()];
    if (amounts.length === 0) {
      return;
    }
    const total: BigNumber = amounts.reduce<BigNumber>(
      (sum, amount) => sum.plus(amount),
      BigNumber(0)
    );
    if (total.gt(0)) {
      await handlePoolJoined(payload, indexingContext, dbContext);
    } else {
      await handlePoolExited(payload, indexingContext, dbContext);
    }
  }

  @indexEvent("Swap")
  async indexSwapEvent(
    payload: VaultSwapPayload,
    dbContext: DbContext,
    indexingContext: EventIndexingContext
  ): Promise<void> {
    await handleSwapEvent(payload, indexingContext, dbContext);
  }
}

export async function handlePoolJoined(
  event: VaultPoolBalanceChangedPayload1,
  indexingContext: EventIndexingContext,
  dbContext: DbContext
): Promise<void> {
  const poolId: string = event.poolId[1];
  const amounts: BigNumber[] = [...event.amountsInOrOut.values()];
  const blockTimestamp = indexingContext.block.timestamp.getTime();
  const logIndex = indexingContext.mainOperation.uid;
  const transactionHash = indexingContext.operationGroup.hash;
  const block = indexingContext.block.level;
  const pool = await dbContext.transaction.findOneBy(Pool, { id: poolId });
  if (pool == null) {
    return;
  }

  // if a pool that was paused is joined, it means it's pause has expired
  // TODO: fix this for when pool.isPaused is null
  // TODO: handle the case where the pool's actual swapEnabled is false
  // if (pool.isPaused) {
  //   pool.isPaused = false;
  //   pool.swapEnabled = true;
  // }

  const tokens = pool.tokensList;

  const joinId = transactionHash.concat(logIndex);
  const join = new JoinExit();
  join.id = joinId;
  join.sender = event.sender;
  const joinAmounts = new Array<string>(amounts.length);
  let valueUSD = BigNumber(ZERO_BD);
  for (let i: number = 0; i < tokens.length; i++) {
    const tokenAddress = tokens[i].slice(0, 36);
    const tokenId = BigNumber(tokens[i].slice(36));

    const poolToken = await loadPoolToken(
      poolId,
      tokenAddress,
      tokenId,
      dbContext
    );
    if (poolToken == null) {
      throw new Error("poolToken not found");
    }
    const joinAmount = scaleDown(amounts[i], poolToken.decimals);
    joinAmounts[i] = joinAmount;
    const tokenJoinAmountInUSD = await valueInUSD(
      BigNumber(joinAmount),
      tokenAddress,
      tokenId,
      dbContext
    );
    valueUSD = valueUSD.plus(tokenJoinAmountInUSD);
  }
  join.type = InvestType.Join;
  join.amounts = joinAmounts;
  join.pool = pool;
  let user = await dbContext.transaction.findOneBy(User, { id: event.sender });
  if (!user) {
    user = new User();
    user.id = event.sender;
    await dbContext.transaction.save(User, user);
  }

  join.userId = user.id;
  join.timestamp = blockTimestamp;

  join.tx = transactionHash;
  join.valueUSD = valueUSD.toString();
  await dbContext.transaction.save(JoinExit, join);

  for (let i: number = 0; i < tokens.length; i++) {
    const tokenAddress = tokens[i].slice(0, 36);
    const tokenId = BigNumber(tokens[i].slice(36));
    const poolToken = await loadPoolToken(
      poolId,
      tokenAddress,
      tokenId,
      dbContext
    );

    // adding initial liquidity
    if (poolToken == null) {
      throw new Error("poolToken not found");
    }
    const amountIn = amounts[i];
    const tokenAmountIn = tokenToDecimal(amountIn, poolToken.decimals);
    const newBalance = BigNumber(poolToken.balance).plus(tokenAmountIn);
    poolToken.balance = newBalance.toString();
    await dbContext.transaction.save(PoolToken, poolToken);

    const token = await getToken(tokenAddress, tokenId, dbContext);
    const tokenTotalBalanceNotional = BigNumber(
      token.totalBalanceNotional
    ).plus(tokenAmountIn);
    const tokenTotalBalanceUSD = await valueInUSD(
      tokenTotalBalanceNotional,
      tokenAddress,
      tokenId,
      dbContext
    );
    token.totalBalanceNotional = tokenTotalBalanceNotional.toString();
    token.totalBalanceUSD = tokenTotalBalanceUSD.toString();
    await dbContext.transaction.save(Token, token);

    const tokenSnapshot = await getTokenSnapshot(
      tokenAddress,
      tokenId,
      indexingContext.block.timestamp.getTime(),
      dbContext
    );
    tokenSnapshot.totalBalanceNotional = tokenTotalBalanceNotional.toString();
    tokenSnapshot.totalBalanceUSD = tokenTotalBalanceUSD.toString();
    await dbContext.transaction.save(TokenSnapshot, tokenSnapshot);
  }

  for (let i: number = 0; i < tokens.length; i++) {
    const tokenAddress = tokens[i].slice(0, 36);
    const tokenId = BigNumber(tokens[i].slice(36));

    if (isPricingAsset(tokenAddress, tokenId)) {
      const success = await addHistoricalPoolLiquidityRecord(
        poolId,
        block,
        tokenAddress,
        tokenId,
        dbContext
      );
      // Some pricing assets may not have a route back to USD yet
      // so we keep trying until we find one
      if (success) {
        break;
      }
    }
  }

  // StablePhantom and ComposableStable pools only emit the PoolBalanceChanged event
  // with a non-zero value for the BPT amount when the pool is initialized,
  // when the amount of BPT informed in the event corresponds to the "excess" BPT that was preminted
  // and therefore must be subtracted from totalShares
  // if (pool.poolType == PoolType.StablePhantom || isComposableStablePool(pool)) {
  //   let preMintedBpt = ZERO_BD;
  //   for (let i: i32 = 0; i < tokenAddresses.length; i++) {
  //     if (tokenAddresses[i] == pool.address) {
  //       preMintedBpt = scaleDown(amounts[i], 18);
  //     }
  //   }
  //   pool.totalShares = pool.totalShares.minus(preMintedBpt);
  //   pool.save();
  // }

  await updatePoolLiquidity(poolId, blockTimestamp, dbContext);
}

export async function handlePoolExited(
  event: VaultPoolBalanceChangedPayload2,
  indexingContext: EventIndexingContext,
  dbContext: DbContext
): Promise<void> {
  let poolId: string = event.poolId[1];
  let amounts: BigNumber[] = [...event.amountsInOrOut.values()];
  let blockTimestamp = indexingContext.block.timestamp.getTime();
  let logIndex = indexingContext.mainOperation.uid;
  let transactionHash = indexingContext.operationGroup.hash;
  let block = indexingContext.block.level;
  let pool = await dbContext.transaction.findOneBy(Pool, { id: poolId });
  if (pool == null) {
    return;
  }

  // if a pool that was paused is joined, it means it's pause has expired
  // TODO: fix this for when pool.isPaused is null
  // TODO: handle the case where the pool's actual swapEnabled is false
  // if (pool.isPaused) {
  //   pool.isPaused = false;
  //   pool.swapEnabled = true;
  // }

  const tokens = pool.tokensList;

  let exitId = transactionHash.concat(logIndex);
  let exit = new JoinExit();
  exit.id = exitId;
  exit.sender = event.sender;
  let exitAmounts = new Array<string>(amounts.length);
  let valueUSD = BigNumber(ZERO_BD);
  for (let i: number = 0; i < tokens.length; i++) {
    const tokenAddress = tokens[i].slice(0, 36);
    const tokenId = BigNumber(tokens[i].slice(36));

    let poolToken = await loadPoolToken(
      poolId,
      tokenAddress,
      tokenId,
      dbContext
    );
    if (poolToken == null) {
      throw new Error("poolToken not found");
    }
    let exitAmount = scaleDown(amounts[i].negated(), poolToken.decimals);
    exitAmounts[i] = exitAmount;
    let tokenExitAmountInUSD = await valueInUSD(
      BigNumber(exitAmount),
      tokenAddress,
      tokenId,
      dbContext
    );
    valueUSD = valueUSD.plus(tokenExitAmountInUSD);
  }
  exit.type = InvestType.Exit;
  exit.amounts = exitAmounts;
  exit.pool = pool;
  console.log(event.sender);
  exit.userId = event.sender;
  exit.timestamp = blockTimestamp;
  exit.tx = transactionHash;
  exit.valueUSD = valueUSD.toString();
  await dbContext.transaction.save(JoinExit, exit);

  for (let i: number = 0; i < tokens.length; i++) {
    const tokenAddress = tokens[i].slice(0, 36);
    const tokenId = BigNumber(tokens[i].slice(36));

    let poolToken = await loadPoolToken(
      poolId,
      tokenAddress,
      tokenId,
      dbContext
    );

    // adding initial liquidity
    if (poolToken == null) {
      throw new Error("poolToken not found");
    }
    let amountOut = amounts[i].negated();
    let tokenAmountOut = tokenToDecimal(amountOut, poolToken.decimals);
    let newBalance = BigNumber(poolToken.balance).minus(tokenAmountOut);
    poolToken.balance = newBalance.toString();
    await dbContext.transaction.save(PoolToken, poolToken);

    let token = await getToken(tokenAddress, tokenId, dbContext);
    const tokenTotalBalanceNotional = BigNumber(
      token.totalBalanceNotional
    ).minus(tokenAmountOut);
    const tokenTotalBalanceUSD = await valueInUSD(
      tokenTotalBalanceNotional,
      tokenAddress,
      tokenId,
      dbContext
    );
    token.totalBalanceNotional = tokenTotalBalanceNotional.toString();
    token.totalBalanceUSD = tokenTotalBalanceUSD.toString();
    await dbContext.transaction.save(Token, token);

    let tokenSnapshot = await getTokenSnapshot(
      tokenAddress,
      tokenId,
      indexingContext.block.timestamp.getTime(),
      dbContext
    );
    tokenSnapshot.totalBalanceNotional = tokenTotalBalanceNotional.toString();
    tokenSnapshot.totalBalanceUSD = tokenTotalBalanceUSD.toString();
    await dbContext.transaction.save(TokenSnapshot, tokenSnapshot);
  }

  for (let i: number = 0; i < tokens.length; i++) {
    const tokenAddress = tokens[i].slice(0, 36);
    const tokenId = BigNumber(tokens[i].slice(36));

    if (isPricingAsset(tokenAddress, tokenId)) {
      let success = await addHistoricalPoolLiquidityRecord(
        poolId,
        block,
        tokenAddress,
        tokenId,
        dbContext
      );
      // Some pricing assets may not have a route back to USD yet
      // so we keep trying until we find one
      if (success) {
        break;
      }
    }
  }

  // StablePhantom and ComposableStable pools only emit the PoolBalanceChanged event
  // with a non-zero value for the BPT amount when the pool is initialized,
  // when the amount of BPT informed in the event corresponds to the "excess" BPT that was preminted
  // and therefore must be subtracted from totalShares
  // if (pool.poolType == PoolType.StablePhantom || isComposableStablePool(pool)) {
  //   let preMintedBpt = ZERO_BD;
  //   for (let i: i32 = 0; i < tokenAddresses.length; i++) {
  //     if (tokenAddresses[i] == pool.address) {
  //       preMintedBpt = scaleDown(amounts[i], 18);
  //     }
  //   }
  //   pool.totalShares = pool.totalShares.minus(preMintedBpt);
  //   pool.save();
  // }

  await updatePoolLiquidity(poolId, blockTimestamp, dbContext);
}

export async function handleSwapEvent(
  event: VaultSwapPayload,
  indexingContext: EventIndexingContext,
  dbContext: DbContext
): Promise<void> {
  const params = indexingContext.transactionParameter?.value.convert() as
    | VaultSwapParameter
    | VaultBatchSwapParameter;
  let user = await dbContext.transaction.findOneBy(User, {
    id: params.funds.sender,
  });
  if (!user) {
    user = new User();
    user.id = params.funds.sender;
  }

  let poolId = event.poolId[2];

  let pool = await dbContext.transaction.findOneBy(Pool, { id: poolId });
  if (pool == null) {
    return;
  }

  // if a swap happens in a pool that was paused, it means it's pause has expired
  // TODO: fix this for when pool.isPaused is null
  // TODO: handle the case where the pool's actual swapEnabled is false
  // if (pool.isPaused) {
  //   pool.isPaused = false;
  //   pool.swapEnabled = true;
  // }

  // if (isVariableWeightPool(pool)) {
  //   // Some pools' weights update over time so we need to update them after each swap
  //   updatePoolWeights(poolId.toHexString());
  // }
  // } else if (isStableLikePool(pool)) {
  //   // Stablelike pools' amplification factors update over time so we need to update them after each swap
  //   updateAmpFactor(pool);
  // }

  // Update virtual supply
  // if (hasVirtualSupply(pool)) {
  //   if (event.params.tokenIn == pool.address) {
  //     pool.totalShares = pool.totalShares.minus(tokenToDecimal(event.params.amountIn, 18));
  //   }
  //   if (event.params.tokenOut == pool.address) {
  //     pool.totalShares = pool.totalShares.plus(tokenToDecimal(event.params.amountOut, 18));
  //   }
  // }

  let poolAddress = pool.address;
  let tokenInAddress: string = event.tokenIn[4];
  let tokenInId = event.tokenIn[5];
  let tokenOutAddress = event.tokenOut[6];
  let tokenOutId = event.tokenOut[7];

  let tokenIn = (await dbContext.transaction.findOneBy(Token, {
    address: tokenInAddress,
    tokenId: tokenInId ? tokenInId.toNumber() : 0,
  })) as Token;

  let tokenOut = (await dbContext.transaction.findOneBy(Token, {
    address: tokenOutAddress,
    tokenId: tokenOutId ? tokenOutId.toNumber() : 0,
  })) as Token;

  let blockTimestamp = indexingContext.block.timestamp.getTime();
  let logIndex = indexingContext.mainOperation.uid;
  let transactionHash = indexingContext.operationGroup.hash;
  let blockNumber = indexingContext.block.level;

  let poolTokenIn = await loadPoolToken(
    poolId,
    tokenInAddress,
    tokenInId,
    dbContext
  );
  let poolTokenOut = await loadPoolToken(
    poolId,
    tokenOutAddress,
    tokenOutId,
    dbContext
  );
  if (poolTokenIn == null || poolTokenOut == null) {
    return;
  }

  let tokenAmountIn = scaleDown(event.amountIn, poolTokenIn.decimals);
  let tokenAmountOut = scaleDown(event.amountOut, poolTokenOut.decimals);

  let swapValueUSD = ZERO_BD;
  let swapFeesUSD = ZERO_BD;

  // Swap events are emitted when joining/exitting from pools with preminted BPT.
  // Since we want this type of swap to register tokens prices but not counting as volume
  // we defined two variables: 1. valueUSD - the value in USD of the transaction;
  // 2. swapValueUSD - equal to valueUSD if trade, zero otherwise, and used to update metrics.
  const valueUSD = await swapValueInUSD(
    tokenInAddress,
    tokenInId,
    BigNumber(tokenAmountIn),
    tokenOutAddress,
    tokenOutId,
    BigNumber(tokenAmountOut),
    dbContext
  );
  console.log(valueUSD);

  if (poolAddress != tokenInAddress && poolAddress != tokenOutAddress) {
    swapValueUSD = valueUSD.toString();
    let swapFee = pool.swapFee;
    swapFeesUSD = valueUSD.times(swapFee).toString();
  }

  let newInAmount = BigNumber(poolTokenIn.balance)
    .plus(tokenAmountIn)
    .toString();
  poolTokenIn.balance = newInAmount;
  await dbContext.transaction.save(PoolToken, poolTokenIn);

  let newOutAmount = BigNumber(poolTokenOut.balance)
    .minus(tokenAmountOut)
    .toString();
  poolTokenOut.balance = newOutAmount;
  await dbContext.transaction.save(PoolToken, poolTokenOut);

  let swapId = transactionHash.concat(logIndex);

  // if (poolAddress == tokenInAddress || poolAddress == tokenOutAddress) {
  // if (isComposableStablePool(pool)) {
  //   let tokenAddresses = pool.tokensList;
  //   let balances: BigInt[] = [];
  //   for (let i: i32 = 0; i < tokenAddresses.length; i++) {
  //     let tokenAddress: Address = Address.fromString(tokenAddresses[i].toHexString());
  //     if (tokenAddresses[i] == pool.address) {
  //       continue;
  //     }
  //     let poolToken = loadPoolToken(pool.id, tokenAddress);
  //     if (poolToken == null) {
  //       throw new Error('poolToken not found');
  //     }
  //     let balance = scaleUp(poolToken.balance.times(poolToken.priceRate), 18);
  //     balances.push(balance);
  //   }
  //   if (pool.amp) {
  //     // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
  //     let amp = pool.amp!.times(AMP_PRECISION);
  //     let invariantInt = calculateInvariant(amp, balances, swapId);
  //     let invariant = scaleDown(invariantInt, 18);
  //     pool.lastPostJoinExitInvariant = invariant;
  //   }
  // }
  //}

  let swap = new Swap();
  swap.id = swapId;
  swap.tokenIn = tokenInAddress;
  swap.tokenInSym = poolTokenIn.symbol;
  swap.tokenAmountIn = tokenAmountIn;

  swap.tokenOut = tokenOutAddress;
  swap.tokenOutSym = poolTokenOut.symbol;
  swap.tokenAmountOut = tokenAmountOut;

  swap.valueUSD = valueUSD.toString();

  swap.caller = indexingContext.mainOperation.sourceAddress;
  swap.userAddress = user.id;
  swap.poolId = pool;

  swap.timestamp = blockTimestamp;
  swap.tx = transactionHash;
  await dbContext.transaction.save(Swap, swap);

  // update pool swapsCount
  // let pool = Pool.load(poolId.toHex());
  pool.swapsCount = pool.swapsCount++;
  pool.totalSwapVolume = BigNumber(pool.totalSwapVolume)
    .plus(swapValueUSD)
    .toString();
  pool.totalSwapFee = BigNumber(pool.totalSwapFee).plus(swapFeesUSD).toString();

  await dbContext.transaction.save(Pool, pool);

  // update vault total swap volume
  let vault = (await dbContext.transaction.findOneBy(Symmetric, {
    id: "1",
  })) as Symmetric;
  vault.totalSwapVolume = BigNumber(vault.totalSwapVolume)
    .plus(swapValueUSD)
    .toString();
  vault.totalSwapFee = BigNumber(vault.totalSwapFee)
    .plus(swapFeesUSD)
    .toString();
  vault.totalSwapCount = vault.totalSwapCount++;
  await dbContext.transaction.save(Symmetric, vault);

  let vaultSnapshot = await getSymmetricSnapshot(
    vault.id,
    blockTimestamp,
    dbContext
  );
  vaultSnapshot.totalSwapVolume = vault.totalSwapVolume;
  vaultSnapshot.totalSwapFee = vault.totalSwapFee;
  vaultSnapshot.totalSwapCount = vault.totalSwapCount;
  await dbContext.transaction.save(SymmetricSnapshot, vaultSnapshot);

  // update swap counts for token
  // updates token snapshots as well
  await uptickSwapsForToken(
    tokenInAddress,
    tokenInId,
    blockTimestamp,
    dbContext
  );
  await uptickSwapsForToken(
    tokenOutAddress,
    tokenOutId,
    blockTimestamp,
    dbContext
  );
  // update volume and balances for the tokens
  // updates token snapshots as well
  await updateTokenBalances(
    tokenInAddress,
    tokenInId,
    BigNumber(swapValueUSD),
    BigNumber(tokenAmountIn),
    0,
    dbContext
  );
  await updateTokenBalances(
    tokenOutAddress,
    tokenOutId,
    BigNumber(swapValueUSD),
    BigNumber(tokenAmountOut),
    1,
    dbContext
  );

  let tradePair = await getTradePair(
    tokenInAddress,
    tokenInId,
    tokenOutAddress,
    tokenOutId,
    dbContext
  );
  tradePair.totalSwapVolume = BigNumber(tradePair.totalSwapVolume)
    .plus(swapValueUSD)
    .toString();
  tradePair.totalSwapFee = BigNumber(tradePair.totalSwapFee)
    .plus(swapFeesUSD)
    .toString();
  await dbContext.transaction.save(TradePair, tradePair);

  let tradePairSnapshot = await getTradePairSnapshot(
    tradePair.id,
    blockTimestamp,
    dbContext
  );
  tradePairSnapshot.totalSwapVolume = BigNumber(tradePair.totalSwapVolume)
    .plus(swapValueUSD)
    .toString();
  tradePairSnapshot.totalSwapFee = BigNumber(tradePair.totalSwapFee)
    .plus(swapFeesUSD)
    .toString();
  await dbContext.transaction.save(TradePairSnapshot, tradePairSnapshot);

  if (swap.tokenAmountOut == ZERO_BD || swap.tokenAmountIn == ZERO_BD) {
    return;
  }

  // Capture price
  // TODO: refactor these if statements using a helper function
  let tokenInWeight = poolTokenIn.weight;
  let tokenOutWeight = poolTokenOut.weight;
  if (
    isPricingAsset(tokenInAddress, tokenInId) &&
    BigNumber(pool.totalLiquidity).gt(MIN_POOL_LIQUIDITY) &&
    valueUSD.gt(MIN_SWAP_VALUE_USD)
  ) {
    let tokenPriceId = getTokenPriceId(
      poolId,
      tokenOut.id,
      tokenIn.id,
      blockNumber
    );
    let tokenPrice = new TokenPrice();
    tokenPrice.id = tokenPriceId;
    //tokenPrice.poolTokenId = getPoolTokenId(poolId, tokenOutAddress);
    tokenPrice.pool = pool;
    tokenPrice.block = blockNumber;
    tokenPrice.timestamp = blockTimestamp;
    tokenPrice.asset = tokenOutAddress;
    tokenPrice.assetId = tokenOutId ? tokenOutId.toString() : "0";
    tokenPrice.amount = tokenAmountIn;
    tokenPrice.pricingAsset = tokenInAddress;
    tokenPrice.pricingAssetId = tokenInId ? tokenInId.toString() : "0";

    if (tokenInWeight && tokenOutWeight) {
      // As the swap is with a WeightedPool, we can easily calculate the spot price between the two tokens
      // based on the pool's weights and updated balances after the swap.
      tokenPrice.price = BigNumber(newInAmount)
        .div(tokenInWeight)
        .div(BigNumber(newOutAmount).div(tokenOutWeight))
        .toString();
    } else {
      // Otherwise we can get a simple measure of the price from the ratio of amount in vs amount out
      tokenPrice.price = BigNumber(tokenAmountIn)
        .div(tokenAmountOut)
        .toString();
    }

    await dbContext.transaction.save(TokenPrice, tokenPrice);

    await updateLatestPrice(tokenPrice, blockTimestamp, dbContext);
  }
  if (
    isPricingAsset(tokenOutAddress, tokenOutId) &&
    BigNumber(pool.totalLiquidity).gt(MIN_POOL_LIQUIDITY) &&
    valueUSD.gt(MIN_SWAP_VALUE_USD)
  ) {
    let tokenPriceId = getTokenPriceId(
      poolId,
      tokenIn.id,
      tokenOut.id,
      blockNumber
    );
    let tokenPrice = new TokenPrice();
    tokenPrice.id = tokenPriceId;
    //tokenPrice.poolTokenId = getPoolTokenId(poolId, tokenInAddress);
    tokenPrice.pool = pool;
    tokenPrice.block = blockNumber;
    tokenPrice.timestamp = blockTimestamp;
    tokenPrice.asset = tokenInAddress;
    tokenPrice.assetId = tokenInId ? tokenInId.toString() : "0";
    tokenPrice.amount = tokenAmountOut;
    tokenPrice.pricingAsset = tokenOutAddress;
    tokenPrice.pricingAssetId = tokenOutId ? tokenOutId.toString() : "0";

    if (tokenInWeight && tokenOutWeight) {
      // As the swap is with a WeightedPool, we can easily calculate the spot price between the two tokens
      // based on the pool's weights and updated balances after the swap.
      tokenPrice.price = BigNumber(newOutAmount)
        .div(tokenOutWeight)
        .div(BigNumber(newInAmount).div(tokenInWeight))
        .toString();
    } else {
      // Otherwise we can get a simple measure of the price from the ratio of amount out vs amount in
      tokenPrice.price = BigNumber(tokenAmountOut)
        .div(tokenAmountIn)
        .toString();
    }

    await dbContext.transaction.save(TokenPrice, tokenPrice);

    await updateLatestPrice(tokenPrice, blockTimestamp, dbContext);
  }

  const preferentialToken = getPreferentialPricingAsset([
    tokenIn.id,
    tokenOut.id,
  ]);
  if (preferentialToken != "0") {
    await addHistoricalPoolLiquidityRecord(
      poolId,
      blockNumber,
      preferentialToken.slice(0, 36),
      BigNumber(preferentialToken.slice(36)),
      dbContext
    );
  }

  await updatePoolLiquidity(poolId, blockNumber, dbContext);
}
