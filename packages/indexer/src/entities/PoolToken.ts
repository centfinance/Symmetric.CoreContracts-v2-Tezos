import { Entity, Column, PrimaryColumn, OneToMany, ManyToOne } from "typeorm";
import { Pool } from "./Pool";
import { Token } from "./Token";

@Entity()
export class PoolToken {
  @PrimaryColumn("varchar")
  id!: string;

  @Column("varchar")
  poolId!: string;

  @ManyToOne(() => Pool, (pool) => pool.tokens)
  pool?: Pool;

  @ManyToOne(() => Token, (token) => token.poolTokens)
  token!: Token;

  @Column("varchar", { length: 36, nullable: true })
  assetManager!: string;

  @Column("varchar")
  symbol!: string;

  @Column("varchar")
  name!: string;

  @Column("int")
  decimals!: number;

  @Column("int", { nullable: true })
  index?: number;

  @Column("varchar", { length: 36 })
  address!: string;

  @Column("numeric")
  tokenId!: string | null;

  @Column("decimal", { precision: 40, scale: 18, nullable: true })
  oldPriceRate?: string;

  @Column("decimal", { precision: 40, scale: 18 })
  priceRate!: string;

  @Column("decimal", { precision: 40, scale: 18 })
  balance!: string;

  @Column("decimal", { precision: 40, scale: 18 })
  cashBalance!: string;

  @Column("decimal", { precision: 40, scale: 18 })
  managedBalance!: string;

  // @OneToMany(() => ManagementOperation, (managementOperation) => managementOperation.poolTokenId)
  // managements!: ManagementOperation[];

  // WeightedPool Only
  @Column("decimal", { precision: 40, scale: 18, nullable: true })
  weight?: string;

  // // ComposableStablePool Only
  // @Column("boolean", { nullable: true })
  // isExemptFromYieldProtocolFee?: boolean;
}
