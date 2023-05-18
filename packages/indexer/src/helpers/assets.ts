import BigNumber from "bignumber.js";

const tokenAddress = "KT1JA3UQ6R4C84mH3FqS3G5mKFeEdLumrDc3";
export const stableAssets = [
  { address: tokenAddress, id: BigNumber(5) },
  { address: tokenAddress, id: BigNumber(7) },
];

export const pricingAssets = [
  { address: tokenAddress, id: BigNumber(0) },
  { address: tokenAddress, id: BigNumber(1) },
  { address: tokenAddress, id: BigNumber(3) },
  { address: tokenAddress, id: BigNumber(6) },
];
