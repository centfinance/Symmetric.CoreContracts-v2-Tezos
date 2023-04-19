import { DbContext } from "@tezos-dappetizer/database";
import BigNumber from "bignumber.js";
import { USD_STABLE_ASSETS } from "./helpers/constants";
import { getToken, ZERO_BD } from "./helpers/misc";

export async function valueInUSD(value: BigNumber, asset: string, assetId: number, dbContext: DbContext): Promise<BigNumber>  {
  let usdValue = BigNumber(ZERO_BD);

  if (isUSDStable(asset)) {
    usdValue = value;
  } else {
    // convert to USD
    let token = await getToken(asset, assetId, dbContext);

    if (token.latestUSDPrice) {
      const latestUSDPrice = BigNumber(token.latestUSDPrice);
      usdValue = value.times(latestUSDPrice);
    }
  }

  return usdValue;
}

export function isUSDStable(asset: string): boolean {
  for (let i: number = 0; i < USD_STABLE_ASSETS.length; i++) {
    if (USD_STABLE_ASSETS[i] == asset) return true;
  }
  return false;
}

