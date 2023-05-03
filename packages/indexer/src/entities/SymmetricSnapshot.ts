import {
  Entity,
  Column,
  PrimaryColumn,
  ManyToOne,
} from "typeorm";
import { Symmetric } from "./Symmetric";

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