import {
  Entity,
  Column,
  PrimaryColumn,
  OneToMany,
} from "typeorm";
import { Pool } from "./Pool";

@Entity()
export class Symmetric {
  @PrimaryColumn("varchar")
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