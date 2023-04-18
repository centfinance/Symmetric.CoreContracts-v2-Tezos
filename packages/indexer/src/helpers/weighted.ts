import { MichelsonMap } from "@taquito/michelson-encoder";
import { DbContext } from "@tezos-dappetizer/database";
import BigNumber from "bignumber.js";
import { Pool } from "../entities";
import { scaleDown } from "./misc";


// export async function updatePoolWeights(
//   poolId: string, 
//   weights:MichelsonMap<BigNumber, BigNumber>,
//   dbContext: DbContext
// ): Promise<void> {

//   const pool = await dbContext.transaction.findOneOrFail(Pool, {
//     where: {
//       id: poolId,
//     }
//   })
//   if (pool == null) return;

//   const tokensList = pool.tokensList;
//   if (weights.size == tokensList.length) {
//       let totalWeight = ZERO_BD;

//       for (let i = 0; i < tokensList.length; i++) {
//         const weight = weights.get(BigNumber(i));

//         // let poolToken = loadPoolToken(poolId, tokenAddress);
//         // if (poolToken != null) {
//         //   poolToken.weight = scaleDown(weight, 18);
//         //   poolToken.save();
//         // }

//         totalWeight = totalWeight.plus(scaleDown(weight, 18));
//       }

//       pool.totalWeight = totalWeight;
//     }
  

//     dbContext.transaction.save(Pool, pool)
// }