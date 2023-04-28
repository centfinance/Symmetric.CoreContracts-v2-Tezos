import {
  Entity,
  Column,
  PrimaryColumn,
} from "typeorm";

@Entity()
export class PriceRateProvider {
  @PrimaryColumn('text')
  id!: string;

  @Column('text')
  poolId!: string;

  @Column('text')
  address!: string | undefined | null;

  @Column('text')
  token!: string;


  // ... other columns and relations for the PriceRateProvider entity
}