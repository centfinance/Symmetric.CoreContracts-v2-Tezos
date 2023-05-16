import { MichelsonMap } from "@taquito/michelson-encoder";
import { DbContext } from "@tezos-dappetizer/database";
import {
  contractFilter,
  indexEvent,
  indexOrigination,
} from "@tezos-dappetizer/decorators";
import {
  EventIndexingContext,
  OriginationIndexingContext,
} from "@tezos-dappetizer/indexer";
import BigNumber from "bignumber.js";
import { Pool } from "./entities/Pool";
import { Symmetric } from "./entities/Symmetric";
// import { Pool, Symmetric, Token } from './entities';
import {
  createPoolTokenEntity,
  getStorage,
  getTokenMetadata,
  newPoolEntity,
  scaleDown,
} from "./helpers/misc";
import { setPriceRateProviders } from "./helpers/pools";
import { address, nat } from "./types/type-aliases";

import {
  WeightedPoolFactoryCreateParameter,
  WeightedPoolFactoryCreateParameterTokensValue,
  WeightedPoolFactoryInitialStorage,
  WeightedPoolFactoryIsPoolFromFactoryKey,
  WeightedPoolFactoryIsPoolFromFactoryValue,
  WeightedPoolFactoryPoolCreatedPayload,
} from "./weighted-pool-factory-indexer-interfaces.generated";

@contractFilter({ name: "WeightedPoolFactory" })
export class WeightedPoolFactoryIndexer {
  @indexOrigination()
  async indexOrigination(
    initialStorage: WeightedPoolFactoryInitialStorage,
    dbContext: DbContext,
    indexingContext: OriginationIndexingContext
  ): Promise<void> {
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

  @indexEvent("PoolCreated")
  async indexPoolCreatedEvent(
    payload: WeightedPoolFactoryPoolCreatedPayload,
    dbContext: DbContext,
    indexingContext: EventIndexingContext
  ): Promise<void> {
    // Implement your indexing logic here or delete the method if not needed.
    await createWeightedLikePool(payload, indexingContext, dbContext);
  }
}

async function handleNewPool(
  poolAddress: string,
  poolId:
    | {
        0: address;
        1: nat;
      }
    | undefined,
  params: WeightedPoolFactoryCreateParameter,
  indexingContext: EventIndexingContext,
  dbContext: DbContext
) {
  const pool = await newPoolEntity(poolAddress, dbContext);
  pool.swapFee = scaleDown(params.swapFeePercentage, 18);

  pool.createTime = indexingContext.block.timestamp.getTime();
  pool.address = poolAddress;
  pool.factory = indexingContext.contract.address;
  pool.oracleEnabled = false;
  // pool.tx = event.transaction.hash;
  pool.swapEnabled = true;
  pool.isPaused = false;

  // const metadata = await getTokenMetadata(poolAddress, 0)
  // pool.name = metadata.name!;
  // pool.symbol = metadata.symbol!;

  pool.name = "Symm LP Token";
  pool.symbol = "SYMMLP";

  // await dbContext.transaction.save(Pool, pool)

  const vault = await dbContext.transaction.findOneOrFail(Symmetric, {
    where: {
      id: "1",
    },
  });

  vault.poolCount += 1;
  await dbContext.transaction.save(Symmetric, vault);

  // let vaultSnapshot = getSymmetricSnapshot(vault.id, event.block.timestamp.toI32());
  // vaultSnapshot.poolCount += 1;
  // vaultSnapshot.save();

  // let poolContract = PoolContract.load(poolAddress.toHexString());
  // if (poolContract == null) {
  //   poolContract = new PoolContract(poolAddress.toHexString());
  //   poolContract.pool = poolId.toHexString();
  //   poolContract.save();
  // }
  return pool;
}

async function createWeightedLikePool(
  poolAddress: string,
  indexingContext: EventIndexingContext,
  dbContext: DbContext
): Promise<void> {
  const params =
    indexingContext.transactionParameter?.value.convert() as WeightedPoolFactoryCreateParameter;
  const poolStorage = await getStorage(poolAddress);

  const pool = await handleNewPool(
    poolAddress,
    poolStorage.poolId,
    params,
    indexingContext,
    dbContext
  );
  pool.poolType = "Weighted";
  pool.poolTypeVersion = 1;
  pool.owner = poolStorage.admin;
  pool.tokensList = [...params.tokens.values()].map((t) =>
    t[0].concat(t[1] ? t[1].toString() : "0")
  );
  pool.totalWeight = "100";
  pool.holdersCount = BigInt(0);

  await dbContext.transaction.save(Pool, pool);

  await handleNewPoolTokens(
    pool,
    params.tokens,
    params.normalizedWeights,
    dbContext
  );

  // rome-ignore lint/style/noNonNullAssertion: <explanation>
  await setPriceRateProviders(
    JSON.stringify(poolStorage.poolId),
    params.rateProviders!,
    pool.tokensList,
    dbContext
  );
}

async function handleNewPoolTokens(
  pool: Pool,
  tokens: MichelsonMap<
    BigNumber,
    WeightedPoolFactoryCreateParameterTokensValue
  >,
  weights: MichelsonMap<BigNumber, BigNumber>,
  dbContext: DbContext
): Promise<void> {
  for (let i: number = 0; i < tokens.size; i++) {
    const tokenData = tokens.get(BigNumber(i))!;
    const weight = weights.get(BigNumber(i))!;
    await createPoolTokenEntity(
      pool,
      tokenData?.[0],
      tokenData?.[1],
      weight,
      i,
      dbContext
    );
  }
}
