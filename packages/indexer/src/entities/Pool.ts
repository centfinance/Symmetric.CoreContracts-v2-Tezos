import {
  Entity,
  Column,
  PrimaryColumn,
  OneToMany,
  ManyToOne,
} from "typeorm";
import { PoolToken } from "./PoolToken";
import { Symmetric } from "./Symmetric";
import { PoolSnapshot } from "./PoolSnapshot";

@Entity()
export class Pool {
  @PrimaryColumn("varchar")
  id!: string;

  @Column("varchar", { length: 36 })
  address!: string;

  @Column("text")
  poolType!: string;

  @Column("int")
  poolTypeVersion!: number;

  @Column("varchar", { length: 36 })
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

  @Column("varchar", { length: 36 })
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

  @Column("numeric")
  createTime!: number;

  @Column("bigint")
  swapsCount!: bigint;

  @Column("bigint")
  holdersCount!: bigint;

  @ManyToOne(() => Symmetric, (symmetric) => symmetric.pools)
  vault!: Symmetric;

  @Column("simple-array")
  tokensList!: string[];

  @OneToMany(() => PoolToken, (poolToken) => poolToken.pool)
  tokens!: PoolToken[];

  // @OneToMany(() => Swap, (swap) => swap.poolId)
  // swaps!: Swap[];

  // @OneToMany(() => PoolShare, (poolShare) => poolShare.poolId)
  // shares!: PoolShare[];

  @OneToMany(() => PoolSnapshot, (poolSnapshot) => poolSnapshot.pool)
  snapshots!: PoolSnapshot[];

  // @OneToMany(() => PoolHistoricalLiquidity, (poolHistoricalLiquidity) => poolHistoricalLiquidity.poolId)
  // historicalValues!: PoolHistoricalLiquidity[];
  
  // @OneToMany(() => TokenPrice, (tokenPrice) => tokenPrice.pool)
  // tokenPrices!: TokenPrice[];

  priceRateProviders: any;

  // ... other columns and relations for the Pool entity
}