import { Entity, Column, PrimaryColumn, ManyToOne, OneToMany } from "typeorm";
import { JoinExit } from "./JoinExit";

@Entity()
export class User {
  @PrimaryColumn("varchar", { length: 36 })
  id!: string;

  // @ManyToOne(() => Swap)
  // swaps: Swap[];

  // ... other relations for the User entity
}
