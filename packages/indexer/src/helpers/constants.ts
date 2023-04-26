import BigNumber from 'bignumber.js';
import * as assets from  './assets';

export const USD_STABLE_ASSETS = assets.stableAssets;

export const PRICING_ASSETS = assets.pricingAssets;

export const MAX_TIME_DIFF_FOR_PRICING = BigNumber(600); // 10min

export let MAX_POS_PRICE_CHANGE = BigNumber('1'); // +100%
export let MAX_NEG_PRICE_CHANGE = BigNumber('-0.5'); // -50%%

export const MIN_POOL_LIQUIDITY = BigNumber('2000');
export const MIN_SWAP_VALUE_USD = BigNumber('1');