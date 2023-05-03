import {
  Entity,
  Column,
  PrimaryColumn,
  ManyToOne,
} from "typeorm";
import { TradePair } from "./TradePair";

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