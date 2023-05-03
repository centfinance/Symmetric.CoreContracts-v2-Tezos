import {
  Entity,
  Column,
  PrimaryColumn,
  ManyToOne,
  OneToMany,
} from "typeorm";
import { Pool } from "./Pool";
import { User } from "./User";

export enum InvestType {
  Join = 'Join',
  Exit = 'Exit',
}

@Entity()
export class JoinExit {
  @PrimaryColumn('varchar')
  id!: string;

  @Column({ type: 'enum', enum: InvestType })
  type!: InvestType;

  @Column('varchar')
  sender!: string;

  @Column('simple-array')
  amounts!: string[];

  @Column('decimal', { nullable: true })
  valueUSD?: string;

  @ManyToOne(() => Pool)
  pool!: Pool;

  @ManyToOne(() => User)
  user!: User;

  @Column('int')
  timestamp!: number;

  @Column('varchar')
  tx!: string;
}