import {
  Entity,
  Column,
  PrimaryColumn,
  OneToMany,
} from "typeorm";
import { PoolToken } from "./PoolToken";

@Entity()
export class Token {
  @PrimaryColumn("varchar")
  id!: string;

  @Column("varchar", { nullable: true })
  symbol?: string;

  @Column("varchar", { nullable: true })
  name?: string;

  @Column("int")
  decimals!: number;

  @Column("varchar", { length: 36 })
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

  // @OneToOne(() => LatestPrice, { nullable: true })
  // latestPrice?: LatestPrice;

  @Column("decimal", { precision: 40, scale: 18, nullable: true })
  latestUSDPrice?: string;

  @Column("numeric", { nullable: true })
  latestUSDPriceTimestamp?: number;

  @Column("decimal", { precision: 40, scale: 18, nullable: true })
  latestFXPrice?: string;

  @OneToMany(() => PoolToken, (poolToken) => poolToken.token)
  poolTokens!: PoolToken[];

  @Column("varchar")
  poolId!: string;

  // @ManyToOne(() => Pool, (pool) => pool.tokensList)
  // pool!: Pool;

  // @OneToMany(() => TokenSnapshot, (snapshot) => snapshot.token)
  // snapshots!: TokenSnapshot[];

  // @OneToMany(() => TradePair, (pair) => pair.token0 || pair.token1)
  // tradePairs!: TradePair[];
}