import {
  Entity,
  Column,
  PrimaryColumn,
  OneToOne,
  OneToMany,
  ManyToOne,
  ManyToMany,
  JoinColumn,
} from "typeorm";

// Balancer
@Entity()
export class Symmetric {
  @PrimaryColumn("varchar", { length: 42 })
  id!: string;

  @Column("int")
  poolCount!: number;

  @OneToMany(() => Pool, (pool) => pool.vaultID)
  pools!: Pool[];

  @Column("numeric")
  totalLiquidity!: string;

  @Column("bigint")
  totalSwapCount!: bigint;

  @Column("numeric")
  totalSwapVolume!: string;

  @Column("numeric")
  totalSwapFee!: string;
}

// Pool
@Entity()
export class Pool {
  @PrimaryColumn("varchar", { length: 42 })
  id!: string;

  @Column("varchar", { length: 42 })
  address!: string;

  @Column("text")
  poolType!: string;

  @Column("int")
  poolTypeVersion!: number;

  @Column("varchar", { length: 42 })
  factory!: string;

  // @Column("int")
  // strategyType!: number;

  @Column("boolean")
  oracleEnabled!: boolean;

  @Column("text")
  symbol!: string;

  @Column("text")
  name!: string;

  @Column("boolean")
  swapEnabled!: boolean;

  @Column("numeric")
  swapFee!: string;

  @Column("varchar", { length: 42 })
  owner!: string;

  @Column("boolean")
  isPaused!: boolean;

  @Column("numeric", { nullable: true })
  totalWeight?: string;

  @Column("numeric")
  totalSwapVolume!: string;

  @Column("numeric")
  totalSwapFee!: string;

  @Column("numeric")
  totalLiquidity!: string;

  @Column("numeric")
  totalShares!: string;

  @Column("int")
  createTime!: number;

  @Column("bigint")
  swapsCount!: bigint;

  @Column("bigint")
  holdersCount!: bigint;

  // @ManyToOne(() => Symmetric, (symmetric) => symmetric.pools)
  @Column("numeric")
  vaultID!: string;

  @Column("simple-array")
  tokensList!: string[];

  @OneToMany(() => PoolToken, (poolToken) => poolToken.poolId)
  tokens!: PoolToken[];

  @OneToMany(() => Swap, (swap) => swap.poolId)
  swaps!: Swap[];

  @OneToMany(() => PoolShare, (poolShare) => poolShare.poolId)
  shares!: PoolShare[];

  @OneToMany(() => PoolSnapshot, (poolSnapshot) => poolSnapshot.pool)
  snapshots!: PoolSnapshot[];

  @OneToMany(() => PoolHistoricalLiquidity, (poolHistoricalLiquidity) => poolHistoricalLiquidity.poolId)
  historicalValues!: PoolHistoricalLiquidity[];
  
  @OneToMany(() => TokenPrice, (tokenPrice) => tokenPrice.pool)
  tokenPrices!: TokenPrice[];

  priceRateProviders: any;

  // ... other columns and relations for the Pool entity
}

// PoolContract
@Entity()
export class PoolContract {
  @PrimaryColumn("varchar", { length: 42 })
  id!: string;

  @OneToOne(() => Pool)
  pool!: Pool;
}

// PoolToken
@Entity()
export class PoolToken {
  @PrimaryColumn("varchar", { length: 42 })
  id!: string;

  @Column("varchar")
  poolId?: string;

  @ManyToOne(() => Token, (token) => token.poolTokens)
  token!: Token;

  @Column("varchar", { length: 42 })
  assetManager!: string;

  @Column("varchar")
  symbol!: string;

  @Column("varchar")
  name!: string;

  @Column("int")
  decimals!: number;

  @Column("int", { nullable: true })
  index?: number;

  @Column("varchar", { length: 42 })
  address!: string;

  @Column("numeric")
  tokenId!: string | null;

  @Column("decimal", { precision: 40, scale: 18, nullable: true })
  oldPriceRate?: string;

  @Column("decimal", { precision: 40, scale: 18 })
  priceRate!: string;

  @Column("decimal", { precision: 40, scale: 18 })
  balance!: string;

  @Column("decimal", { precision: 40, scale: 18 })
  cashBalance!: string;

  @Column("decimal", { precision: 40, scale: 18 })
  managedBalance!: string;

  // @OneToMany(() => ManagementOperation, (managementOperation) => managementOperation.poolTokenId)
  // managements!: ManagementOperation[];

  // WeightedPool Only
  @Column("decimal", { precision: 40, scale: 18, nullable: true })
  weight?: string;

  // // ComposableStablePool Only
  // @Column("boolean", { nullable: true })
  // isExemptFromYieldProtocolFee?: boolean;
}

@Entity()
export class PoolSnapshot {
  @PrimaryColumn('varchar', { length: 255 })
  id!: string;

  @ManyToOne(() => Pool, (pool) => pool.snapshots, { onDelete: 'CASCADE' })
  @JoinColumn({ name: 'poolId' })
  pool!: Pool;

  @Column('decimal', { array: true })
  amounts!: string[];

  @Column('decimal')
  totalShares!: string;

  @Column('decimal')
  swapVolume!: string;

  @Column('decimal')
  swapFees!: string;

  @Column('decimal')
  liquidity!: string;

  @Column('bigint')
  swapsCount!: BigInt;

  @Column('bigint')
  holdersCount!: BigInt;

  @Column('int')
  timestamp!: number;
}

@Entity()
export class PoolHistoricalLiquidity {
  @PrimaryColumn('varchar', { length: 255 })
  id!: string;

  @ManyToOne(() => Pool, (pool) => pool.historicalValues, { onDelete: 'CASCADE' })
  @JoinColumn({ name: 'poolId' })
  poolId!: Pool;

  @Column('decimal')
  poolTotalShares!: string;

  @Column('decimal')
  poolLiquidity!: string;

  @Column('decimal')
  poolShareValue!: string;

  @Column('varchar', { length: 255 })
  pricingAsset!: string;

  @Column('bigint')
  block!: BigInt;
}

@Entity()
export class TokenPrice {
  @PrimaryColumn('varchar')
  id!: string;

  @ManyToOne(() => Pool, (pool) => pool.tokenPrices)
  pool!: Pool;

  @Column('varchar')
  asset!: string;
  
  @Column('decimal')
  amount!: string;

  @Column('varchar')
  pricingAsset!: string;
  
  @Column('decimal')
  price!: string;
  
  @Column('numeric')
  block!: number;
  
  @Column('numeric')
  timestamp!: number
}

// Token
@Entity()
export class Token {
  @PrimaryColumn("varchar", { length: 42 })
  id!: string;

  @Column("varchar", { nullable: true })
  symbol?: string;

  @Column("varchar", { nullable: true })
  name?: string;

  @Column("int")
  decimals!: number;

  @Column("varchar", { length: 42 })
  address!: string;

  @Column("numeric")
  tokenId!: number;

  @Column("boolean")
  FA2!: boolean;

  @Column("decimal", { precision: 40, scale: 18 })
  totalBalanceUSD!: string;

  @Column("decimal", { precision: 40, scale: 18 })
  totalBalanceNotional!: string;

  @Column("decimal", { precision: 40, scale: 18 })
  totalVolumeUSD!: string;

  @Column("decimal", { precision: 40, scale: 18 })
  totalVolumeNotional!: string;

  @Column("bigint")
  totalSwapCount!: bigint;

  @OneToOne(() => LatestPrice, { nullable: true })
  latestPrice?: LatestPrice;

  @Column("decimal", { precision: 40, scale: 18, nullable: true })
  latestUSDPrice?: string;

  @Column("numeric", { nullable: true })
  latestUSDPriceTimestamp?: number;

  @Column("decimal", { precision: 40, scale: 18, nullable: true })
  latestFXPrice?: string;

  @OneToMany(() => PoolToken, (poolToken) => poolToken.token)
  poolTokens!: PoolToken[];

  @Column("varchar", { length: 42 })
  poolId!: string;

  @ManyToOne(() => Pool, (pool) => pool.tokensList)
  pool!: Pool;

  @OneToMany(() => TokenSnapshot, (snapshot) => snapshot.token)
  snapshots!: TokenSnapshot[];

  @OneToMany(() => TradePair, (pair) => pair.token0 || pair.token1)
  tradePairs!: TradePair[];
}

@Entity()
export class TokenSnapshot {
  @PrimaryColumn("varchar", { length: 42 })
  id!: string;

  @ManyToOne(() => Token, (token) => token.snapshots)
  token!: Token;

  @Column("int")
  timestamp!: number;

  @Column("decimal", { precision: 40, scale: 18 })
  totalBalanceUSD!: string;

  @Column("decimal", { precision: 40, scale: 18 })
  totalBalanceNotional!: string;

  @Column("decimal", { precision: 40, scale: 18 })
  totalVolumeUSD!: string;

  @Column("decimal", { precision: 40, scale: 18 })
  totalVolumeNotional!: string;

  @Column("bigint")
  totalSwapCount!: bigint;
}

// PriceRateProvider
@Entity()
export class PriceRateProvider {
  @PrimaryColumn('text')
  id!: string;

  @Column('text')
  poolId!: string;

  @Column('text')
  address!: string | undefined | null;

  @Column('text')
  token!: string;


  // ... other columns and relations for the PriceRateProvider entity
}

// PoolShare
@Entity()
export class PoolShare {
  @PrimaryColumn("varchar", { length: 42 })
  id!: string;

  @ManyToOne(() => User, (user) => user.sharesOwned)
  userAddress!: User;

  @ManyToOne(() => Pool, (pool) => pool.shares)
  poolId!: Pool;

  // ... other columns for the PoolShare entity
}

// User
@Entity()
export class User {
  @PrimaryColumn("varchar", { length: 42 })
  id!: string;

  @OneToMany(() => PoolShare, (poolShare) => poolShare.userAddress)
  sharesOwned!: PoolShare[];
  swaps: any;

  // ... other relations for the User entity
}

@Entity()
export class Swap {
  @PrimaryColumn("varchar", { length: 42 })
  id!: string;

  @Column("varchar", { length: 42 })
  caller!: string;

  @Column("varchar", { length: 42 })
  tokenIn!: string;

  @Column()
  tokenInSym!: string;

  @Column("varchar", { length: 42 })
  tokenOut!: string;

  @Column()
  tokenOutSym!: string;

  @Column("decimal", { precision: 40, scale: 18 })
  tokenAmountIn!: string;

  @Column("decimal", { precision: 40, scale: 18 })
  tokenAmountOut!: string;

  @Column("decimal", { precision: 40, scale: 18 })
  valueUSD!: string;

  @ManyToOne(() => Pool, (pool) => pool.swaps)
  @JoinColumn({ name: "poolId" })
  poolId!: Pool;

  @ManyToOne(() => User, (user) => user.swaps)
  @JoinColumn({ name: "userAddress" })
  userAddress!: User;

  @Column("int")
  timestamp!: number;

  @Column("varchar", { length: 66 })
  tx!: string;
}

export enum InvestType {
  Join = 'Join',
  Exit = 'Exit',
}

@Entity()
export class JoinExit {
  @PrimaryColumn('varchar', { length: 255 })
  id!: string;

  @Column({ type: 'enum', enum: InvestType })
  type!: InvestType;

  @Column('varchar', { length: 255 })
  sender!: string;

  @Column('simple-array')
  amounts!: string[];

  @Column('decimal', { nullable: true })
  valueUSD?: string;

  @ManyToOne(() => Pool)
  @JoinColumn({ name: 'poolId' })
  pool!: Pool;

  @ManyToOne(() => User)
  @JoinColumn({ name: 'userId' })
  user!: User;

  @Column('int')
  timestamp!: number;

  @Column('varchar', { length: 255 })
  tx!: string;
}

@Entity()
export class LatestPrice {
  @PrimaryColumn('varchar', { length: 255 })
  id!: string;

  @Column('varchar', { length: 255 })
  asset!: string;

  @Column('varchar', { length: 255 })
  pricingAsset!: string;

  @ManyToOne(() => Pool)
  @JoinColumn({ name: 'poolId' })
  poolId!: Pool;

  @Column('decimal')
  price!: string;

  @Column('numeric')
  block!: number;
}

// ... other TypeORM entities for the remaining schema

@Entity()
export class SymmetricSnapshot {
  @PrimaryColumn("varchar", { length: 42 })
  id!: string;

  @ManyToOne(() => Symmetric, (symmetric) => symmetric)
  vault!: Symmetric;

  @Column("int")
  timestamp!: number;

  @Column("int")
  poolCount!: number;

  @Column("decimal", { precision: 40, scale: 18 })
  totalLiquidity!: string;

  @Column("bigint")
  totalSwapCount!: bigint;

  @Column("decimal", { precision: 40, scale: 18 })
  totalSwapVolume!: string;

  @Column("decimal", { precision: 40, scale: 18 })
  totalSwapFee!: string;
}

@Entity()
export class TradePair {
  @PrimaryColumn("varchar")
  id!: string;

  @ManyToOne(() => Token, (token) => token.tradePairs)
  token0!: Token;

  @ManyToOne(() => Token, (token) => token.tradePairs)
  token1!: Token;

  @Column("decimal", { precision: 40, scale: 18 })
  totalSwapVolume!: string;

  @Column("decimal", { precision: 40, scale: 18 })
  totalSwapFee!: string;

  @OneToMany(() => TradePairSnapshot, (snapshot) => snapshot.pair)
  snapshots!: TradePairSnapshot[];
}

@Entity()
export class TradePairSnapshot {
  @PrimaryColumn("varchar")
  id!: string;

  @ManyToOne(() => TradePair, (pair) => pair.snapshots)
  pair!: TradePair;

  @Column("int")
  timestamp!: number;

  @Column("decimal", { precision: 40, scale: 18 })
  totalSwapVolume!: string;

  @Column("decimal", { precision: 40, scale: 18 })
  totalSwapFee!: string;
}