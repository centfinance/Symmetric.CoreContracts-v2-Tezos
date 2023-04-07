import {
  Entity,
  Column,
  PrimaryColumn,
  OneToMany,
  ManyToOne,
  ManyToMany,
  JoinTable,
} from "typeorm";

// Balancer
@Entity()
export class Symmetric {
  @PrimaryColumn("varchar", { length: 42 })
  id!: string;

  @Column("int")
  poolCount!: number;

  @OneToMany(() => Pool, (pool) => pool.vault)
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

  @Column("int")
  strategyType!: number;

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

  @ManyToOne(() => Symmetric, (symmetric) => symmetric.pools)
  vault!: Symmetric;

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

  @ManyToOne(() => Pool, (pool) => pool.tokens)
  poolId!: Pool;

  @ManyToOne(() => Token, (token) => token.poolTokens)
  token!: Token;

  // ... other columns and relations for the PoolToken entity
}

// Token
@Entity()
export class Token {
  @PrimaryColumn("varchar", { length: 42 })
  id!: string;

  // ... other columns for the Token entity

  @OneToMany(() => PoolToken, (poolToken) => poolToken.token)
  poolTokens!: PoolToken[];

  @ManyToOne(() => Pool, (pool) => pool.tokensList)
  pool!: Pool;
}

// PriceRateProvider
@Entity()
export class PriceRateProvider {
  @PrimaryColumn("varchar", { length: 42 })
  id!: string;

  @ManyToOne(() => Pool, (pool) => pool.priceRateProviders)
  poolId!: Pool;

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

  // ... other relations for the User entity
}

// ... other TypeORM entities for the remaining schema

