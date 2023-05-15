import BigNumber from "bignumber.js";

const tokenAddress = "KT19SwoUtpqsJrKFkJHiDQkXBNU8qXKoUZp4";
export const stableAssets = [
  { address: tokenAddress, id: BigNumber(2) },
  { address: tokenAddress, id: BigNumber(5) },
  { address: tokenAddress, id: BigNumber(6) },
  { address: tokenAddress, id: BigNumber(8) },
];

export const pricingAssets = [
  { address: tokenAddress, id: BigNumber(0) },
  { address: tokenAddress, id: BigNumber(1) },
  { address: tokenAddress, id: BigNumber(3) },
  { address: tokenAddress, id: BigNumber(4) },
];
