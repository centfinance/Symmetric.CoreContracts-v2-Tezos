import {
  Entity,
  Column,
  PrimaryColumn,
  ManyToOne,
  JoinColumn,
} from "typeorm";
import { Pool } from "./Pool";

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