import {
  Entity,
  Column,
  PrimaryColumn,
  OneToMany,
  ManyToOne,
} from "typeorm";
import { Pool } from "./Pool";

@Entity()
export class PoolHistoricalLiquidity {
  @PrimaryColumn('varchar')
  id!: string;

  @ManyToOne(() => Pool, (pool) => pool.historicalValues, { onDelete: 'CASCADE' })
  poolId!: Pool;

  @Column('decimal')
  poolTotalShares!: string;

  @Column('decimal')
  poolLiquidity!: string;

  @Column('decimal')
  poolShareValue!: string;

  @Column('varchar')
  pricingAsset!: string;

  @Column('bigint')
  block!: BigInt;
}