import { DbContext } from "@tezos-dappetizer/database";
import { getToken } from "./helpers/misc";

export function valueInUSD(value: BigDecimal, asset: string, dbContext: DbContext): BigDecimal {
  let usdValue = ZERO_BD;

  if (isUSDStable(asset)) {
    usdValue = value;
  } else {
    // convert to USD
    let token = getToken(asset, dbContext);

    if (token.latestUSDPrice) {
      const latestUSDPrice = token.latestUSDPrice as BigDecimal;
      usdValue = value.times(latestUSDPrice);
    }
  }

  return usdValue;
}

export function isUSDStable(asset: Address): boolean {
  for (let i: i32 = 0; i < USD_STABLE_ASSETS.length; i++) {
    if (USD_STABLE_ASSETS[i] == asset) return true;
  }
  return false;
}

