import {
  Entity,
  Column,
  PrimaryColumn,
  ManyToOne,
  OneToMany,
} from "typeorm";
import { Token } from "./Token";
import { TradePairSnapshot } from "./TradePairSnapshot";

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