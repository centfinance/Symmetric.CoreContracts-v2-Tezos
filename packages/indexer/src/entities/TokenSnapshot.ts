import { Entity, Column, PrimaryColumn, ManyToOne } from "typeorm";
import { Token } from "./Token";

@Entity()
export class TokenSnapshot {
  @PrimaryColumn("varchar")
  id!: string;

  @ManyToOne(() => Token, (token) => token.snapshots)
  token!: Token;

  @Column("numeric")
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
