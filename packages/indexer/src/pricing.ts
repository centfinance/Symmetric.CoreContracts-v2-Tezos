import { DbContext } from "@tezos-dappetizer/database";
import { getToken, ZERO_BD } from "./helpers/misc";

export async function valueInUSD(value: BigDecimal, asset: string, assetId: number, dbContext: DbContext): BigDecimal {
  let usdValue = ZERO_BD;

  if (isUSDStable(asset)) {
    usdValue = value;
  } else {
    // convert to USD
    let token = await getToken(asset, assetId, dbContext);

    if (token.latestUSDPrice) {
      const latestUSDPrice = token.latestUSDPrice as BigDecimal;
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

