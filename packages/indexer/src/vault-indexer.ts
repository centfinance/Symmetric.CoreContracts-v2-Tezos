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
import { InvestType, JoinExit, Pool, PoolToken, Token } from './entities';
import { getToken, loadPoolToken, scaleDown, ZERO_BD } from './helpers/misc';
import { addHistoricalPoolLiquidityRecord, updatePoolLiquidity, valueInUSD } from './pricing';

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


export async function handlePoolJoined(event: VaultPoolBalanceChangedPayload1, indexingContext: EventIndexingContext, dbContext: DbContext): void {
  let poolId: string = event.poolId;
  let amounts: BigNumber[] = [...event.amountsInOrOut.values()];
  let protocolFeeAmounts: BigInt[] = event.params.protocolFeeAmounts;
  let blockTimestamp = indexingContext.block.timestamp.getTime();
  let logIndex = event.logIndex;
  let transactionHash = event.transaction.hash;
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

  let joinId = transactionHash.toHexString().concat(logIndex.toString());
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
  join.pool = poolId
  join.user = event.sender;
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
    let amountIn = amounts[i].minus(protocolFeeAmounts[i]);
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

    let tokenSnapshot = await getTokenSnapshot(tokenAddress, event);
    tokenSnapshot.totalBalanceNotional = tokenTotalBalanceNotional;
    tokenSnapshot.totalBalanceUSD = tokenTotalBalanceUSD;
    tokenSnapshot.save();
  }

  for (let i: number = 0; i < tokens.length; i++) {
    const t = JSON.parse(tokens[i]) as WeightedPoolFactoryCreateParameterTokensValue;
    let tokenAddress = t[0];
    let tokenId = t[1];    
    
    if (isPricingAsset(tokenAddress)) {
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