import { DbContext } from '@tezos-dappetizer/database';
import {
    contractFilter,
    indexBigMapUpdate,
    indexEntrypoint,
    indexEvent,
    indexOrigination,
    indexStorageChange,
} from '@tezos-dappetizer/decorators';
import {
    BigMapUpdateIndexingContext,
    EventIndexingContext,
    OriginationIndexingContext,
    StorageChangeIndexingContext,
    TransactionIndexingContext,
} from '@tezos-dappetizer/indexer';
import BigNumber from 'bignumber.js';
import { InvestType, JoinExit, Pool, PoolToken, Swap, Symmetric, Token, TokenSnapshot, User } from './entities';
import { getSymmetricSnapshot, getToken, getTokenSnapshot, loadPoolToken, scaleDown, tokenToDecimal, ZERO_BD } from './helpers/misc';
import { addHistoricalPoolLiquidityRecord, isPricingAsset, updatePoolLiquidity, valueInUSD } from './pricing';

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
} from './vault-indexer-interfaces.generated';
import { WeightedPoolFactoryCreateParameterTokensValue } from './weighted-pool-factory-indexer-interfaces.generated';

@contractFilter({ name: 'Vault' })
export class VaultIndexer {
    @indexOrigination()
    async indexOrigination(
        initialStorage: VaultInitialStorage,
        dbContext: DbContext,
        indexingContext: OriginationIndexingContext,
    ): Promise<void> {
        // Implement your indexing logic here or delete the method if not needed.
    }

    @indexEntrypoint('accept_admin')
    async indexAcceptAdmin(
        parameter: VaultAcceptAdminParameter,
        dbContext: DbContext,
        indexingContext: TransactionIndexingContext,
    ): Promise<void> {
        // Implement your indexing logic here or delete the method if not needed.
    }

    @indexEntrypoint('batchSwap')
    async indexBatchSwap(
        parameter: VaultBatchSwapParameter,
        dbContext: DbContext,
        indexingContext: TransactionIndexingContext,
    ): Promise<void> {
        // Implement your indexing logic here or delete the method if not needed.
    }

    @indexEntrypoint('exitPool')
    async indexExitPool(
        parameter: VaultExitPoolParameter,
        dbContext: DbContext,
        indexingContext: TransactionIndexingContext,
    ): Promise<void> {
        // Implement your indexing logic here or delete the method if not needed.
    }

    @indexEntrypoint('joinPool')
    async indexJoinPool(
      parameter: VaultJoinPoolParameter,
      dbContext: DbContext,
      indexingContext: TransactionIndexingContext,
    ): Promise<void> {
      // const poolId: string = parameter.poolId;
      // const amounts = parameter.request.assets.map((_, key) => parameter.request.limits.get(key));
      // const blockTimestamp = indexingContext.timestamp.toI32();
      // const logIndex = indexingContext.logIndex;
      // const transactionHash = indexingContext.transaction.hash;
  
      // const pool = await dbContext.poolRepository.findOne(poolId);
      // if (pool === undefined) {
      //   console.warn('Pool not found in indexJoinPool: {} {}', [poolId, transactionHash.toHexString()]);
      //   return;
      // }
  
      // const tokenAddresses = pool.tokensList;
  
      // const joinId = transactionHash.toHexString().concat(logIndex.toString());

      // const joinAmounts: string[] = [];
      // let valueUSD = '0';
  
      // for (let i = 0; i < tokenAddresses.length; i++) {
      //   const tokenAddress = tokenAddresses[i];
      //   const poolToken = await dbContext.poolTokenRepository.findOne({ pool: pool, token: tokenAddress });
      //   if (poolToken === undefined) {
      //     throw new Error('poolToken not found');
      //   }
  
      //   // You'll need to implement the scaleDown function
      //   const joinAmount = scaleDown(amounts[i], poolToken.decimals);
      //   joinAmounts[i] = joinAmount.toString();
      //   const tokenJoinAmountInUSD = valueInUSD(joinAmount, tokenAddress); // You'll need to implement the valueInUSD function
      //   valueUSD = (parseFloat(valueUSD) + parseFloat(tokenJoinAmountInUSD)).toString();
      // }
      // const join = {
      //   id: joinId,
      //   sender: parameter.sender,
      //   type: 'Join',
      //   amounts: joinAmounts,
      //   pool: pool,
      //   user: await dbContext.userRepository.findOne(parameter.sender) ?? new User(parameter.sender), // Assuming that User has a constructor taking the user address as the only argument
      //   timestamp: blockTimestamp,
      //   tx: transactionHash,
      //   valueUSD: valueUSD,
      // }


      // await dbContext.transaction.insert(JoinExit, join);
  
      // The rest of the function depends on functions and data structures that are specific to the Balancer v2 subgraph
      // You may need to adjust or implement these functions and data structures accordingly
      // Also, note that some of the entity updates should be adjusted to work with your dbContext and TypeORM
  
      // ...
  
    }

    @indexEntrypoint('registerPool')
    async indexRegisterPool(
        parameter: VaultRegisterPoolParameter,
        dbContext: DbContext,
        indexingContext: TransactionIndexingContext,
    ): Promise<void> {
        // Implement your indexing logic here or delete the method if not needed.
        
    }

    @indexEntrypoint('registerTokens')
    async indexRegisterTokens(
        parameter: VaultRegisterTokensParameter,
        dbContext: DbContext,
        indexingContext: TransactionIndexingContext,
    ): Promise<void> {
        // Implement your indexing logic here or delete the method if not needed.
    }

    @indexEntrypoint('set_paused')
    async indexSetPaused(
        parameter: VaultSetPausedParameter,
        dbContext: DbContext,
        indexingContext: TransactionIndexingContext,
    ): Promise<void> {
        // Implement your indexing logic here or delete the method if not needed.
    }

    @indexEntrypoint('swap')
    async indexSwap(
        parameter: VaultSwapParameter,
        dbContext: DbContext,
        indexingContext: TransactionIndexingContext,
    ): Promise<void> {
        // Implement your indexing logic here or delete the method if not needed.
    }

    @indexEntrypoint('transfer_admin')
    async indexTransferAdmin(
        parameter: VaultTransferAdminParameter,
        dbContext: DbContext,
        indexingContext: TransactionIndexingContext,
    ): Promise<void> {
        // Implement your indexing logic here or delete the method if not needed.
    }

    @indexStorageChange()
    async indexStorageChange(
        newStorage: VaultChangedStorage,
        dbContext: DbContext,
        indexingContext: StorageChangeIndexingContext,
    ): Promise<void> {
        // Implement your indexing logic here or delete the method if not needed.
    }

    @indexBigMapUpdate({ path: ['isPoolRegistered'] })
    async indexIsPoolRegisteredUpdate(
        key: VaultIsPoolRegisteredKey,
        value: VaultIsPoolRegisteredValue | undefined, // Undefined represents a removal.
        dbContext: DbContext,
        indexingContext: BigMapUpdateIndexingContext,
    ): Promise<void> {
        // Implement your indexing logic here or delete the method if not needed.
    }

    @indexBigMapUpdate({ path: ['metadata'] })
    async indexMetadataUpdate(
        key: VaultMetadataKey,
        value: VaultMetadataValue | undefined, // Undefined represents a removal.
        dbContext: DbContext,
        indexingContext: BigMapUpdateIndexingContext,
    ): Promise<void> {
        // Implement your indexing logic here or delete the method if not needed.
    }

    @indexBigMapUpdate({ path: ['poolsBalances'] })
    async indexPoolsBalancesUpdate(
        key: VaultPoolsBalancesKey,
        value: VaultPoolsBalancesValue | undefined, // Undefined represents a removal.
        dbContext: DbContext,
        indexingContext: BigMapUpdateIndexingContext,
    ): Promise<void> {
        // Implement your indexing logic here or delete the method if not needed.
    }

    @indexBigMapUpdate({ path: ['poolsTokens'] })
    async indexPoolsTokensUpdate(
        key: VaultPoolsTokensKey,
        value: VaultPoolsTokensValue | undefined, // Undefined represents a removal.
        dbContext: DbContext,
        indexingContext: BigMapUpdateIndexingContext,
    ): Promise<void> {
        // Implement your indexing logic here or delete the method if not needed.
    }


    @indexEvent('PoolBalanceChanged')
    async indexPoolBalanceChangedEvent(
        payload: VaultPoolBalanceChangedPayload,
        dbContext: DbContext,
        indexingContext: EventIndexingContext,
    ): Promise<void> {
        // Implement your indexing logic here or delete the method if not needed.

    }

    @indexEvent('PoolRegistered')
    async indexPoolRegisteredEvent(
        payload: VaultPoolRegisteredPayload,
        dbContext: DbContext,
        indexingContext: EventIndexingContext,
    ): Promise<void> {
        // Implement your indexing logic here or delete the method if not needed.
    }

    @indexEvent('Swap')
    async indexSwapEvent(
        payload: VaultSwapPayload,
        dbContext: DbContext,
        indexingContext: EventIndexingContext,
    ): Promise<void> {
        // Implement your indexing logic here or delete the method if not needed.
    }

    @indexEvent('TokensRegistered')
    async indexTokensRegisteredEvent(
        payload: VaultTokensRegisteredPayload,
        dbContext: DbContext,
        indexingContext: EventIndexingContext,
    ): Promise<void> {
        // Implement your indexing logic here or delete the method if not needed.
    }
}


export async function handlePoolJoined(event: VaultPoolBalanceChangedPayload1, indexingContext: EventIndexingContext, dbContext: DbContext): Promise<void> {
  let poolId: string = event.poolId;
  let amounts: BigNumber[] = [...event.amountsInOrOut.values()];
  let blockTimestamp = indexingContext.block.timestamp.getTime();
  let logIndex = indexingContext.mainOperation.uid;
  let transactionHash = indexingContext.operationGroup.hash;
  let block = indexingContext.block.level
  let pool = await dbContext.transaction.findOneBy(Pool, {id: poolId});
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

  let joinId = transactionHash.concat(logIndex);
  let join = new JoinExit();
  join.id = joinId
  join.sender = event.sender;
  let joinAmounts = new Array<string>(amounts.length);
  let valueUSD = BigNumber(ZERO_BD);
  for (let i: number = 0; i < tokens.length; i++) {
    const token = JSON.parse(tokens[i]) as WeightedPoolFactoryCreateParameterTokensValue;
    let tokenAddress = token[0];
    let tokenId = token[1];
    let poolToken = await loadPoolToken(poolId, tokenAddress, tokenId, dbContext);
    if (poolToken == null) {
      throw new Error('poolToken not found');
    }
    let joinAmount = scaleDown(amounts[i], poolToken.decimals);
    joinAmounts[i] = joinAmount;
    let tokenJoinAmountInUSD = await valueInUSD(BigNumber(joinAmount), tokenAddress, tokenId, dbContext);
    valueUSD = valueUSD.plus(tokenJoinAmountInUSD);
  }
  join.type = InvestType.Join;
  join.amounts = joinAmounts;
  join.pool = pool
  let user  = await dbContext.transaction.findOneBy(User, {id: event.sender});
  if (!user) {
    user  = new User();
    user.id = event.sender;
  }
  join.user = user, 
  join.timestamp = blockTimestamp;
  join.tx = transactionHash;
  join.valueUSD = valueUSD.toString();
  await dbContext.transaction.save(JoinExit, join);

  for (let i: number = 0; i < tokens.length; i++) {
    const t = JSON.parse(tokens[i]) as WeightedPoolFactoryCreateParameterTokensValue;
    let tokenAddress = t[0];
    let tokenId = t[1];
    let poolToken = await loadPoolToken(poolId, tokenAddress, tokenId, dbContext);

    // adding initial liquidity
    if (poolToken == null) {
      throw new Error('poolToken not found');
    }
    let amountIn = amounts[i];
    let tokenAmountIn = tokenToDecimal(amountIn, poolToken.decimals);
    let newBalance = BigNumber(poolToken.balance).plus(tokenAmountIn);
    poolToken.balance = newBalance.toString();
    await dbContext.transaction.save(PoolToken, poolToken);
    
    let token = await getToken(tokenAddress, tokenId ? tokenId.toNumber() : 0, dbContext);
    const tokenTotalBalanceNotional = BigNumber(token.totalBalanceNotional).plus(tokenAmountIn);
    const tokenTotalBalanceUSD = await valueInUSD(tokenTotalBalanceNotional, tokenAddress, tokenId, dbContext);
    token.totalBalanceNotional = tokenTotalBalanceNotional.toString();
    token.totalBalanceUSD = tokenTotalBalanceUSD.toString();
    await dbContext.transaction.save(Token, token);

    let tokenSnapshot = await getTokenSnapshot(tokenAddress, tokenId, indexingContext.block.timestamp.getTime(), dbContext);
    tokenSnapshot.totalBalanceNotional = tokenTotalBalanceNotional.toString();
    tokenSnapshot.totalBalanceUSD = tokenTotalBalanceUSD.toString();
    await dbContext.transaction.save(TokenSnapshot, tokenSnapshot);
  }

  for (let i: number = 0; i < tokens.length; i++) {
    const t = JSON.parse(tokens[i]) as WeightedPoolFactoryCreateParameterTokensValue;
    let tokenAddress = t[0];
    let tokenId = t[1];    
    
    if (isPricingAsset(tokens[i])) {
      let success = await addHistoricalPoolLiquidityRecord(poolId, block, tokenAddress, tokenId, dbContext);
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

export async function handlePoolExited(event: VaultPoolBalanceChangedPayload2, indexingContext: EventIndexingContext, dbContext: DbContext): Promise<void> {
  let poolId: string = event.poolId;
  let amounts: BigNumber[] = [...event.amountsInOrOut.values()];
  let blockTimestamp = indexingContext.block.timestamp.getTime();
  let logIndex = indexingContext.mainOperation.uid;
  let transactionHash = indexingContext.operationGroup.hash;
  let block = indexingContext.block.level
  let pool = await dbContext.transaction.findOneBy(Pool, {id: poolId});
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
  exit.id = exitId
  exit.sender = event.sender;
  let exitAmounts = new Array<string>(amounts.length);
  let valueUSD = BigNumber(ZERO_BD);
  for (let i: number = 0; i < tokens.length; i++) {
    const token = JSON.parse(tokens[i]) as WeightedPoolFactoryCreateParameterTokensValue;
    let tokenAddress = token[0];
    let tokenId = token[1];
    let poolToken = await loadPoolToken(poolId, tokenAddress, tokenId, dbContext);
    if (poolToken == null) {
      throw new Error('poolToken not found');
    }
    let exitAmount = scaleDown(amounts[i].negated(), poolToken.decimals);
    exitAmounts[i] = exitAmount;
    let tokenExitAmountInUSD = await valueInUSD(BigNumber(exitAmount), tokenAddress, tokenId, dbContext);
    valueUSD = valueUSD.plus(tokenExitAmountInUSD);
  }
  exit.type = InvestType.Exit;
  exit.amounts = exitAmounts;
  exit.pool = pool
  let user  = await dbContext.transaction.findOneBy(User, {id: event.sender});
  exit.user = user!, 
  exit.timestamp = blockTimestamp;
  exit.tx = transactionHash;
  exit.valueUSD = valueUSD.toString();
  await dbContext.transaction.save(JoinExit, exit);

  for (let i: number = 0; i < tokens.length; i++) {
    const t = JSON.parse(tokens[i]) as WeightedPoolFactoryCreateParameterTokensValue;
    let tokenAddress = t[0];
    let tokenId = t[1];
    let poolToken = await loadPoolToken(poolId, tokenAddress, tokenId, dbContext);

    // adding initial liquidity
    if (poolToken == null) {
      throw new Error('poolToken not found');
    }
    let amountOut = amounts[i].negated();
    let tokenAmountOut = tokenToDecimal(amountOut, poolToken.decimals);
    let newBalance = BigNumber(poolToken.balance).minus(tokenAmountOut);
    poolToken.balance = newBalance.toString();
    await dbContext.transaction.save(PoolToken, poolToken);
    
    let token = await getToken(tokenAddress, tokenId ? tokenId.toNumber() : 0, dbContext);
    const tokenTotalBalanceNotional = BigNumber(token.totalBalanceNotional).minus(tokenAmountOut);
    const tokenTotalBalanceUSD = await valueInUSD(tokenTotalBalanceNotional, tokenAddress, tokenId, dbContext);
    token.totalBalanceNotional = tokenTotalBalanceNotional.toString();
    token.totalBalanceUSD = tokenTotalBalanceUSD.toString();
    await dbContext.transaction.save(Token, token);

    let tokenSnapshot = await getTokenSnapshot(tokenAddress, tokenId, indexingContext.block.timestamp.getTime(), dbContext);
    tokenSnapshot.totalBalanceNotional = tokenTotalBalanceNotional.toString();
    tokenSnapshot.totalBalanceUSD = tokenTotalBalanceUSD.toString();
    await dbContext.transaction.save(TokenSnapshot, tokenSnapshot);
  }

  for (let i: number = 0; i < tokens.length; i++) {
    const t = JSON.parse(tokens[i]) as WeightedPoolFactoryCreateParameterTokensValue;
    let tokenAddress = t[0];
    let tokenId = t[1];    
    
    if (isPricingAsset(tokens[i])) {
      let success = await addHistoricalPoolLiquidityRecord(poolId, block, tokenAddress, tokenId, dbContext);
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

export async function handleSwapEvent(event: VaultSwapPayload, indexingContext: EventIndexingContext, dbContext: DbContext): Promise<void> {
  const params = indexingContext.transactionParameter?.value.convert() as VaultSwapParameter | VaultBatchSwapParameter
  let user  = await dbContext.transaction.findOneBy(User, {id: params.funds.sender});
  if (!user) {
    user  = new User();
    user.id = params.funds.sender;
  }
  
  let poolId = event.poolId;

  let pool = await dbContext.transaction.findOneBy(Pool, {id: poolId});
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
  let tokenInAddress: string = event.tokenIn[3];
  let tokenInId:BigNumber = event.tokenIn[4];
  let tokenOutAddress: string = event.tokenOut[5];
  let tokenOutId:BigNumber = event.tokenOut[6];

  let blockTimestamp = indexingContext.block.timestamp.getTime();
  let logIndex = indexingContext.mainOperation.uid;
  let transactionHash = indexingContext.operationGroup.hash;
  let block = indexingContext.block.level

  let poolTokenIn = await loadPoolToken(poolId, tokenInAddress, tokenInId, dbContext);
  let poolTokenOut = await loadPoolToken(poolId, tokenOutAddress, tokenOutId, dbContext);
  if (poolTokenIn == null || poolTokenOut == null) {
    return;
  }

  let tokenAmountIn  = scaleDown(event.amountIn, poolTokenIn.decimals);
  let tokenAmountOut = scaleDown(event.amountOut, poolTokenOut.decimals);

  let swapValueUSD = ZERO_BD;
  let swapFeesUSD = ZERO_BD;

  // Swap events are emitted when joining/exitting from pools with preminted BPT.
  // Since we want this type of swap to register tokens prices but not counting as volume
  // we defined two variables: 1. valueUSD - the value in USD of the transaction;
  // 2. swapValueUSD - equal to valueUSD if trade, zero otherwise, and used to update metrics.
  const valueUSD = swapValueInUSD(tokenInAddress, tokenAmountIn, tokenOutAddress, tokenAmountOut);

  if (poolAddress != tokenInAddress && poolAddress != tokenOutAddress) {
    swapValueUSD = valueUSD;
    let swapFee = pool.swapFee;
    swapFeesUSD = swapValueUSD.times(swapFee);
  }

  let newInAmount = poolTokenIn.balance.plus(tokenAmountIn);
  poolTokenIn.balance = newInAmount;
  await dbContext.transaction.save(PoolToken, poolTokenIn);

  let newOutAmount = poolTokenOut.balance.minus(tokenAmountOut);
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
  swap.id = swapId
  swap.tokenIn = tokenInAddress;
  swap.tokenInSym = poolTokenIn.symbol;
  swap.tokenAmountIn = tokenAmountIn;

  swap.tokenOut = tokenOutAddress;
  swap.tokenOutSym = poolTokenOut.symbol;
  swap.tokenAmountOut = tokenAmountOut;

  swap.valueUSD = valueUSD;

  swap.caller = indexingContext.mainOperation.sourceAddress;
  swap.userAddress = user;
  swap.poolId = pool;

  swap.timestamp = blockTimestamp;
  swap.tx = transactionHash;
  await dbContext.transaction.save(Swap, swap);

  // update pool swapsCount
  // let pool = Pool.load(poolId.toHex());
  pool.swapsCount = pool.swapsCount.plus(BigInt.fromI32(1));
  pool.totalSwapVolume = pool.totalSwapVolume.plus(swapValueUSD);
  pool.totalSwapFee = pool.totalSwapFee.plus(swapFeesUSD);

  await dbContext.transaction.save(Pool, pool);

  // update vault total swap volume
  let vault = await dbContext.transaction.findOneBy(Symmetric, { id: '1'}) as Symmetric;
  vault.totalSwapVolume = BigNumber(vault.totalSwapVolume).plus(swapValueUSD).toString();
  vault.totalSwapFee = BigNumber(vault.totalSwapFee).plus(swapFeesUSD).toString();
  vault.totalSwapCount = vault.totalSwapCount + BigInt(1);
  await dbContext.transaction.save(Symmetric, vault);

  let vaultSnapshot = getSymmetricSnapshot(vault.id, blockTimestamp);
  vaultSnapshot.totalSwapVolume = vault.totalSwapVolume;
  vaultSnapshot.totalSwapFee = vault.totalSwapFee;
  vaultSnapshot.totalSwapCount = vault.totalSwapCount;
  vaultSnapshot.save();

  // update swap counts for token
  // updates token snapshots as well
  uptickSwapsForToken(tokenInAddress, event);
  uptickSwapsForToken(tokenOutAddress, event);

  // update volume and balances for the tokens
  // updates token snapshots as well
  updateTokenBalances(tokenInAddress, swapValueUSD, tokenAmountIn, SWAP_IN, event);
  updateTokenBalances(tokenOutAddress, swapValueUSD, tokenAmountOut, SWAP_OUT, event);

  let tradePair = getTradePair(tokenInAddress, tokenOutAddress);
  tradePair.totalSwapVolume = tradePair.totalSwapVolume.plus(swapValueUSD);
  tradePair.totalSwapFee = tradePair.totalSwapFee.plus(swapFeesUSD);
  tradePair.save();

  let tradePairSnapshot = getTradePairSnapshot(tradePair.id, blockTimestamp);
  tradePairSnapshot.totalSwapVolume = tradePair.totalSwapVolume.plus(swapValueUSD);
  tradePairSnapshot.totalSwapFee = tradePair.totalSwapFee.plus(swapFeesUSD);
  tradePairSnapshot.save();

  if (swap.tokenAmountOut == ZERO_BD || swap.tokenAmountIn == ZERO_BD) {
    return;
  }

  // Capture price
  // TODO: refactor these if statements using a helper function
  let blockNumber = event.block.number;
  let tokenInWeight = poolTokenIn.weight;
  let tokenOutWeight = poolTokenOut.weight;
  if (isPricingAsset(tokenInAddress) && pool.totalLiquidity.gt(MIN_POOL_LIQUIDITY) && valueUSD.gt(MIN_SWAP_VALUE_USD)) {
    let tokenPriceId = getTokenPriceId(poolId.toHex(), tokenOutAddress, tokenInAddress, blockNumber);
    let tokenPrice = new TokenPrice(tokenPriceId);
    //tokenPrice.poolTokenId = getPoolTokenId(poolId, tokenOutAddress);
    tokenPrice.poolId = poolId.toHexString();
    tokenPrice.block = blockNumber;
    tokenPrice.timestamp = blockTimestamp;
    tokenPrice.asset = tokenOutAddress;
    tokenPrice.amount = tokenAmountIn;
    tokenPrice.pricingAsset = tokenInAddress;

    if (tokenInWeight && tokenOutWeight) {
      // As the swap is with a WeightedPool, we can easily calculate the spot price between the two tokens
      // based on the pool's weights and updated balances after the swap.
      tokenPrice.price = newInAmount.div(tokenInWeight).div(newOutAmount.div(tokenOutWeight));
    } else {
      // Otherwise we can get a simple measure of the price from the ratio of amount in vs amount out
      tokenPrice.price = tokenAmountIn.div(tokenAmountOut);
    }

    tokenPrice.save();

    updateLatestPrice(tokenPrice, event.block.timestamp);
  }
  if (
    isPricingAsset(tokenOutAddress) &&
    pool.totalLiquidity.gt(MIN_POOL_LIQUIDITY) &&
    valueUSD.gt(MIN_SWAP_VALUE_USD)
  ) {
    let tokenPriceId = getTokenPriceId(poolId.toHex(), tokenInAddress, tokenOutAddress, blockNumber);
    let tokenPrice = new TokenPrice(tokenPriceId);
    //tokenPrice.poolTokenId = getPoolTokenId(poolId, tokenInAddress);
    tokenPrice.poolId = poolId.toHexString();
    tokenPrice.block = blockNumber;
    tokenPrice.timestamp = blockTimestamp;
    tokenPrice.asset = tokenInAddress;
    tokenPrice.amount = tokenAmountOut;
    tokenPrice.pricingAsset = tokenOutAddress;

    if (tokenInWeight && tokenOutWeight) {
      // As the swap is with a WeightedPool, we can easily calculate the spot price between the two tokens
      // based on the pool's weights and updated balances after the swap.
      tokenPrice.price = newOutAmount.div(tokenOutWeight).div(newInAmount.div(tokenInWeight));
    } else {
      // Otherwise we can get a simple measure of the price from the ratio of amount out vs amount in
      tokenPrice.price = tokenAmountOut.div(tokenAmountIn);
    }

    tokenPrice.save();

    updateLatestPrice(tokenPrice, event.block.timestamp);
  }

  const preferentialToken = getPreferentialPricingAsset([tokenInAddress, tokenOutAddress]);
  if (preferentialToken != ZERO_ADDRESS) {
    await addHistoricalPoolLiquidityRecord(poolId, blockNumber, preferentialToken, preferentialTokenId, dbContext);
  }

  await updatePoolLiquidity(poolId, blockNumber, dbContext);
}