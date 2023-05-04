import {
  Entity,
  Column,
  PrimaryColumn,
  OneToMany,
  ManyToOne,
} from "typeorm";
import { Pool } from "./Pool";

@Entity()
export class LatestPrice {
  @PrimaryColumn('varchar')
  id!: string;

  @Column('varchar')
  asset!: string;

  @Column('varchar')
  pricingAsset!: string;

  @ManyToOne(() => Pool)
  poolId!: Pool;

  @Column('decimal')
  price!: string;

  @Column('numeric')
  block!: number;
}