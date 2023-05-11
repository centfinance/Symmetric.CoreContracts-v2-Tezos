import { Entity, Column, PrimaryColumn, ManyToOne } from "typeorm";
import { Pool } from "./Pool";

@Entity()
export class TokenPrice {
  @PrimaryColumn("varchar")
  id!: string;

  @ManyToOne(() => Pool, (pool) => pool.tokenPrices)
  pool!: Pool;

  @Column("varchar")
  asset!: string;

  @Column("decimal")
  amount!: string;

  @Column("varchar")
  pricingAsset!: string;

  @Column("decimal")
  price!: string;

  @Column("numeric")
  block!: number;

  @Column("numeric")
  timestamp!: number;
}
