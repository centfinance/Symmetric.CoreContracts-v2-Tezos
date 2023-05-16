import { Entity, Column, PrimaryColumn, ManyToOne } from "typeorm";
import { Pool } from "./Pool";
import { User } from "./User";

@Entity()
export class Swap {
  @PrimaryColumn("varchar")
  id!: string;

  @Column("varchar", { length: 36 })
  caller!: string;

  @Column("varchar", { length: 36 })
  tokenIn!: string;

  @Column()
  tokenInSym!: string;

  @Column("varchar", { length: 42 })
  tokenOut!: string;

  @Column()
  tokenOutSym!: string;

  @Column("decimal", { precision: 40, scale: 18 })
  tokenAmountIn!: string;

  @Column("decimal", { precision: 40, scale: 18 })
  tokenAmountOut!: string;

  @Column("decimal", { precision: 40, scale: 18 })
  valueUSD!: string;

  @ManyToOne(() => Pool, (pool) => pool.swaps)
  poolId!: Pool;

  @Column("varchar", { length: 36 })
  userAddress!: string;

  @Column("numeric")
  timestamp!: number;

  @Column("varchar", { length: 66 })
  tx!: string;
}
