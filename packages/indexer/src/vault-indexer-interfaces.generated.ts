/* istanbul ignore next */
/* eslint-disable */

// This file was generated.
// It should NOT be modified manually rather it should be regenerated.
// Contract: KT1GQ1ZkB6CFfyjrfWddvfJA5VRwEYnR26Xu
// Tezos network: mainnet

import { UnitValue } from '@taquito/michelson-encoder';
import { BigMapAbstraction, MichelsonMap } from '@taquito/taquito';
import { BigNumber } from 'bignumber.js';

export type VaultParameter =
    | { entrypoint: 'accept_admin'; value: VaultAcceptAdminParameter }
    | { entrypoint: 'batchSwap'; value: VaultBatchSwapParameter }
    | { entrypoint: 'exitPool'; value: VaultExitPoolParameter }
    | { entrypoint: 'joinPool'; value: VaultJoinPoolParameter }
    | { entrypoint: 'registerPool'; value: VaultRegisterPoolParameter }
    | { entrypoint: 'registerTokens'; value: VaultRegisterTokensParameter }
    | { entrypoint: 'set_paused'; value: VaultSetPausedParameter }
    | { entrypoint: 'swap'; value: VaultSwapParameter }
    | { entrypoint: 'transfer_admin'; value: VaultTransferAdminParameter };

/** An empty result. */
export type VaultAcceptAdminParameter = typeof UnitValue;

export interface VaultBatchSwapParameter {
    /**
     * In-memory map.
     * 
     * Key of `BigNumber`: Nat - arbitrary big integer >= 0.
     * 
     * Value of `VaultBatchSwapParameterAssetsValue`.
     */
    assets: MichelsonMap<BigNumber, VaultBatchSwapParameterAssetsValue>;

    /** Date ISO 8601 string. */
    deadline: string;

    funds: VaultBatchSwapParameterFunds;

    /** Arbitrary string. */
    kind: string;

    /**
     * In-memory map.
     * 
     * Key of `BigNumber`: Nat - arbitrary big integer >= 0.
     * 
     * Value of `BigNumber`: Integer from -2^31-1 to 2^31.
     */
    limits: MichelsonMap<BigNumber, BigNumber>;

    /**
     * In-memory map.
     * 
     * Key of `BigNumber`: Nat - arbitrary big integer >= 0.
     * 
     * Value of `VaultBatchSwapParameterSwapsValue`.
     */
    swaps: MichelsonMap<BigNumber, VaultBatchSwapParameterSwapsValue>;
}

export interface VaultBatchSwapParameterAssetsValue {
    /** Tezos address. */
    '0': string;

    /** Nat - arbitrary big integer >= 0. */
    '1': BigNumber | null;
}

export interface VaultBatchSwapParameterFunds {
    /** Simple boolean. */
    fromInternalBalance: boolean;

    /** Tezos address. */
    recipient: string;

    /** Tezos address. */
    sender: string;

    /** Simple boolean. */
    toInternalBalance: boolean;
}

export interface VaultBatchSwapParameterSwapsValue {
    /** Nat - arbitrary big integer >= 0. */
    amount: BigNumber;

    /** Nat - arbitrary big integer >= 0. */
    assetInIndex: BigNumber;

    /** Nat - arbitrary big integer >= 0. */
    assetOutIndex: BigNumber;

    poolId: VaultBatchSwapParameterSwapsValuePoolId;
}

export interface VaultBatchSwapParameterSwapsValuePoolId {
    /** Tezos address. */
    '3': string;

    /** Nat - arbitrary big integer >= 0. */
    '4': BigNumber;
}

export interface VaultExitPoolParameter {
    poolId: VaultExitPoolParameterPoolId;

    /** Tezos address. */
    recipient: string;

    request: VaultExitPoolParameterRequest;

    /** Tezos address. */
    sender: string;
}

export interface VaultExitPoolParameterPoolId {
    /** Tezos address. */
    '0': string;

    /** Nat - arbitrary big integer >= 0. */
    '1': BigNumber;
}

export interface VaultExitPoolParameterRequest {
    /**
     * In-memory map.
     * 
     * Key of `BigNumber`: Nat - arbitrary big integer >= 0.
     * 
     * Value of `VaultExitPoolParameterRequestAssetsValue`.
     */
    assets: MichelsonMap<BigNumber, VaultExitPoolParameterRequestAssetsValue>;

    /**
     * In-memory map.
     * 
     * Key of `BigNumber`: Nat - arbitrary big integer >= 0.
     * 
     * Value of `BigNumber`: Nat - arbitrary big integer >= 0.
     */
    limits: MichelsonMap<BigNumber, BigNumber>;

    /** Simple boolean. */
    useInternalBalance: boolean;

    userData: VaultExitPoolParameterRequestUserData;
}

export interface VaultExitPoolParameterRequestAssetsValue {
    /** Tezos address. */
    '0': string;

    /** Nat - arbitrary big integer >= 0. */
    '1': BigNumber | null;
}

export interface VaultExitPoolParameterRequestUserData {
    /**
     * In-memory map.
     * 
     * Key of `BigNumber`: Nat - arbitrary big integer >= 0.
     * 
     * Value of `BigNumber`: Nat - arbitrary big integer >= 0.
     */
    amountsOut: MichelsonMap<BigNumber, BigNumber> | null;

    /** Arbitrary string. */
    kind: string;

    /** Nat - arbitrary big integer >= 0. */
    maxSPTAmountIn: BigNumber | null;

    /** Simple boolean. */
    recoveryModeExit: boolean;

    /** Nat - arbitrary big integer >= 0. */
    sptAmountIn: BigNumber | null;

    /** Nat - arbitrary big integer >= 0. */
    tokenIndex: BigNumber | null;
}

export interface VaultJoinPoolParameter {
    poolId: VaultJoinPoolParameterPoolId;

    /** Tezos address. */
    recipient: string;

    request: VaultJoinPoolParameterRequest;

    /** Tezos address. */
    sender: string;
}

export interface VaultJoinPoolParameterPoolId {
    /** Tezos address. */
    '0': string;

    /** Nat - arbitrary big integer >= 0. */
    '1': BigNumber;
}

export interface VaultJoinPoolParameterRequest {
    /**
     * In-memory map.
     * 
     * Key of `BigNumber`: Nat - arbitrary big integer >= 0.
     * 
     * Value of `VaultJoinPoolParameterRequestAssetsValue`.
     */
    assets: MichelsonMap<BigNumber, VaultJoinPoolParameterRequestAssetsValue>;

    /**
     * In-memory map.
     * 
     * Key of `BigNumber`: Nat - arbitrary big integer >= 0.
     * 
     * Value of `BigNumber`: Nat - arbitrary big integer >= 0.
     */
    limits: MichelsonMap<BigNumber, BigNumber>;

    /** Simple boolean. */
    useInternalBalance: boolean;

    userData: VaultJoinPoolParameterRequestUserData;
}

export interface VaultJoinPoolParameterRequestAssetsValue {
    /** Tezos address. */
    '0': string;

    /** Nat - arbitrary big integer >= 0. */
    '1': BigNumber | null;
}

export interface VaultJoinPoolParameterRequestUserData {
    /** Nat - arbitrary big integer >= 0. */
    allT: BigNumber | null;

    /**
     * In-memory map.
     * 
     * Key of `BigNumber`: Nat - arbitrary big integer >= 0.
     * 
     * Value of `BigNumber`: Nat - arbitrary big integer >= 0.
     */
    amountsIn: MichelsonMap<BigNumber, BigNumber> | null;

    /** Arbitrary string. */
    kind: string;

    /** Nat - arbitrary big integer >= 0. */
    minSPTAmountOut: BigNumber | null;

    /** Nat - arbitrary big integer >= 0. */
    sptAmountOut: BigNumber | null;

    /** Nat - arbitrary big integer >= 0. */
    tokenIndex: BigNumber | null;
}

/** An empty result. */
export type VaultRegisterPoolParameter = typeof UnitValue;

export interface VaultRegisterTokensParameter {
    /**
     * In-memory map.
     * 
     * Key of `BigNumber`: Nat - arbitrary big integer >= 0.
     * 
     * Value of `string`: Tezos address.
     */
    assetManagers: MichelsonMap<BigNumber, string> | null;

    poolId: VaultRegisterTokensParameterPoolId;

    /**
     * In-memory map.
     * 
     * Key of `BigNumber`: Nat - arbitrary big integer >= 0.
     * 
     * Value of `VaultRegisterTokensParameterTokensValue`.
     */
    tokens: MichelsonMap<BigNumber, VaultRegisterTokensParameterTokensValue>;
}

export interface VaultRegisterTokensParameterPoolId {
    /** Tezos address. */
    '1': string;

    /** Nat - arbitrary big integer >= 0. */
    '2': BigNumber;
}

export interface VaultRegisterTokensParameterTokensValue {
    /** Tezos address. */
    '0': string;

    /** Nat - arbitrary big integer >= 0. */
    '1': BigNumber | null;
}

/** Simple boolean. */
export type VaultSetPausedParameter = boolean;

export interface VaultSwapParameter {
    /** Date ISO 8601 string. */
    deadline: string;

    funds: VaultSwapParameterFunds;

    /** Nat - arbitrary big integer >= 0. */
    limit: BigNumber;

    singleSwap: VaultSwapParameterSingleSwap;
}

export interface VaultSwapParameterFunds {
    /** Simple boolean. */
    fromInternalBalance: boolean;

    /** Tezos address. */
    recipient: string;

    /** Tezos address. */
    sender: string;

    /** Simple boolean. */
    toInternalBalance: boolean;
}

export interface VaultSwapParameterSingleSwap {
    /** Nat - arbitrary big integer >= 0. */
    amount: BigNumber;

    assetIn: VaultSwapParameterSingleSwapAssetIn;

    assetOut: VaultSwapParameterSingleSwapAssetOut;

    /** Arbitrary string. */
    kind: string;

    poolId: VaultSwapParameterSingleSwapPoolId;
}

export interface VaultSwapParameterSingleSwapAssetIn {
    /** Tezos address. */
    '4': string;

    /** Nat - arbitrary big integer >= 0. */
    '5': BigNumber | null;
}

export interface VaultSwapParameterSingleSwapAssetOut {
    /** Tezos address. */
    '5': string;

    /** Nat - arbitrary big integer >= 0. */
    '6': BigNumber | null;
}

export interface VaultSwapParameterSingleSwapPoolId {
    /** Tezos address. */
    '8': string;

    /** Nat - arbitrary big integer >= 0. */
    '9': BigNumber;
}

/** Tezos address. */
export type VaultTransferAdminParameter = string;

export interface VaultCurrentStorage {
    /** Tezos address. */
    admin: string;

    /**
     * Big map.
     * 
     * Key of `VaultCurrentStorageIsPoolRegisteredKey`.
     * 
     * Value of `typeof UnitValue`: An empty result.
     */
    isPoolRegistered: BigMapAbstraction;

    /**
     * Big map.
     * 
     * Key of `string`: Arbitrary string.
     * 
     * Value of `string`: Bytes.
     */
    metadata: BigMapAbstraction;

    /** Nat - arbitrary big integer >= 0. */
    nextPoolNonce: BigNumber;

    /**
     * Big map.
     * 
     * Key of `VaultCurrentStoragePoolsBalancesKey`.
     * 
     * Value of `MichelsonMap<VaultCurrentStoragePoolsBalancesValueKey, VaultCurrentStoragePoolsBalancesValueValue>`:
     * In-memory map.
     * 
     * Key of `VaultCurrentStoragePoolsBalancesValueKey`.
     * 
     * Value of `VaultCurrentStoragePoolsBalancesValueValue`.
     */
    poolsBalances: BigMapAbstraction;

    /**
     * Big map.
     * 
     * Key of `VaultCurrentStoragePoolsTokensKey`.
     * 
     * Value of `MichelsonMap<BigNumber, VaultCurrentStoragePoolsTokensValueValue>`:
     * In-memory map.
     * 
     * Key of `BigNumber`: Nat - arbitrary big integer >= 0.
     * 
     * Value of `VaultCurrentStoragePoolsTokensValueValue`.
     */
    poolsTokens: BigMapAbstraction;

    /** Tezos address. */
    proposed_admin: string | null;

    /** Simple boolean. */
    settings: boolean;
}

export interface VaultCurrentStorageIsPoolRegisteredKey {
    /** Tezos address. */
    '0': string;

    /** Nat - arbitrary big integer >= 0. */
    '1': BigNumber;
}

export interface VaultCurrentStoragePoolsBalancesKey {
    /** Tezos address. */
    '0': string;

    /** Nat - arbitrary big integer >= 0. */
    '1': BigNumber;
}

export interface VaultCurrentStoragePoolsBalancesValueKey {
    /** Tezos address. */
    '0': string;

    /** Nat - arbitrary big integer >= 0. */
    '1': BigNumber | null;
}

export interface VaultCurrentStoragePoolsBalancesValueValue {
    /** Nat - arbitrary big integer >= 0. */
    '0': BigNumber;

    /** Nat - arbitrary big integer >= 0. */
    '1': BigNumber;
}

export interface VaultCurrentStoragePoolsTokensKey {
    /** Tezos address. */
    '0': string;

    /** Nat - arbitrary big integer >= 0. */
    '1': BigNumber;
}

export interface VaultCurrentStoragePoolsTokensValueValue {
    /** Tezos address. */
    '0': string;

    /** Nat - arbitrary big integer >= 0. */
    '1': BigNumber | null;
}

export interface VaultChangedStorage {
    /** Tezos address. */
    admin: string;

    /** Big map ID - string with arbitrary big integer, negative if temporary. */
    isPoolRegistered: string;

    /** Big map ID - string with arbitrary big integer, negative if temporary. */
    metadata: string;

    /** Nat - arbitrary big integer >= 0. */
    nextPoolNonce: BigNumber;

    /** Big map ID - string with arbitrary big integer, negative if temporary. */
    poolsBalances: string;

    /** Big map ID - string with arbitrary big integer, negative if temporary. */
    poolsTokens: string;

    /** Tezos address. */
    proposed_admin: string | null;

    /** Simple boolean. */
    settings: boolean;
}

export interface VaultInitialStorage {
    /** Tezos address. */
    admin: string;

    /**
     * Big map initial values.
     * 
     * Key of `VaultInitialStorageIsPoolRegisteredKey`.
     * 
     * Value of `typeof UnitValue`: An empty result.
     */
    isPoolRegistered: MichelsonMap<VaultInitialStorageIsPoolRegisteredKey, typeof UnitValue>;

    /**
     * Big map initial values.
     * 
     * Key of `string`: Arbitrary string.
     * 
     * Value of `string`: Bytes.
     */
    metadata: MichelsonMap<string, string>;

    /** Nat - arbitrary big integer >= 0. */
    nextPoolNonce: BigNumber;

    /**
     * Big map initial values.
     * 
     * Key of `VaultInitialStoragePoolsBalancesKey`.
     * 
     * Value of `MichelsonMap<VaultInitialStoragePoolsBalancesValueKey, VaultInitialStoragePoolsBalancesValueValue>`:
     * In-memory map.
     * 
     * Key of `VaultInitialStoragePoolsBalancesValueKey`.
     * 
     * Value of `VaultInitialStoragePoolsBalancesValueValue`.
     */
    poolsBalances: MichelsonMap<VaultInitialStoragePoolsBalancesKey, MichelsonMap<VaultInitialStoragePoolsBalancesValueKey, VaultInitialStoragePoolsBalancesValueValue>>;

    /**
     * Big map initial values.
     * 
     * Key of `VaultInitialStoragePoolsTokensKey`.
     * 
     * Value of `MichelsonMap<BigNumber, VaultInitialStoragePoolsTokensValueValue>`:
     * In-memory map.
     * 
     * Key of `BigNumber`: Nat - arbitrary big integer >= 0.
     * 
     * Value of `VaultInitialStoragePoolsTokensValueValue`.
     */
    poolsTokens: MichelsonMap<VaultInitialStoragePoolsTokensKey, MichelsonMap<BigNumber, VaultInitialStoragePoolsTokensValueValue>>;

    /** Tezos address. */
    proposed_admin: string | null;

    /** Simple boolean. */
    settings: boolean;
}

export interface VaultInitialStorageIsPoolRegisteredKey {
    /** Tezos address. */
    '0': string;

    /** Nat - arbitrary big integer >= 0. */
    '1': BigNumber;
}

export interface VaultInitialStoragePoolsBalancesKey {
    /** Tezos address. */
    '0': string;

    /** Nat - arbitrary big integer >= 0. */
    '1': BigNumber;
}

export interface VaultInitialStoragePoolsBalancesValueKey {
    /** Tezos address. */
    '0': string;

    /** Nat - arbitrary big integer >= 0. */
    '1': BigNumber | null;
}

export interface VaultInitialStoragePoolsBalancesValueValue {
    /** Nat - arbitrary big integer >= 0. */
    '0': BigNumber;

    /** Nat - arbitrary big integer >= 0. */
    '1': BigNumber;
}

export interface VaultInitialStoragePoolsTokensKey {
    /** Tezos address. */
    '0': string;

    /** Nat - arbitrary big integer >= 0. */
    '1': BigNumber;
}

export interface VaultInitialStoragePoolsTokensValueValue {
    /** Tezos address. */
    '0': string;

    /** Nat - arbitrary big integer >= 0. */
    '1': BigNumber | null;
}

export interface VaultIsPoolRegisteredKey {
    /** Tezos address. */
    '0': string;

    /** Nat - arbitrary big integer >= 0. */
    '1': BigNumber;
}

/** An empty result. */
export type VaultIsPoolRegisteredValue = typeof UnitValue;

/** Arbitrary string. */
export type VaultMetadataKey = string;

/** Bytes. */
export type VaultMetadataValue = string;

export interface VaultPoolsBalancesKey {
    /** Tezos address. */
    '0': string;

    /** Nat - arbitrary big integer >= 0. */
    '1': BigNumber;
}

/**
 * In-memory map.
 * 
 * Key of `VaultPoolsBalancesValueKey`.
 * 
 * Value of `VaultPoolsBalancesValueValue`.
 */
export type VaultPoolsBalancesValue = MichelsonMap<VaultPoolsBalancesValueKey, VaultPoolsBalancesValueValue>;

export interface VaultPoolsBalancesValueKey {
    /** Tezos address. */
    '0': string;

    /** Nat - arbitrary big integer >= 0. */
    '1': BigNumber | null;
}

export interface VaultPoolsBalancesValueValue {
    /** Nat - arbitrary big integer >= 0. */
    '0': BigNumber;

    /** Nat - arbitrary big integer >= 0. */
    '1': BigNumber;
}

export interface VaultPoolsTokensKey {
    /** Tezos address. */
    '0': string;

    /** Nat - arbitrary big integer >= 0. */
    '1': BigNumber;
}

/**
 * In-memory map.
 * 
 * Key of `BigNumber`: Nat - arbitrary big integer >= 0.
 * 
 * Value of `VaultPoolsTokensValueValue`.
 */
export type VaultPoolsTokensValue = MichelsonMap<BigNumber, VaultPoolsTokensValueValue>;

export interface VaultPoolsTokensValueValue {
    /** Tezos address. */
    '0': string;

    /** Nat - arbitrary big integer >= 0. */
    '1': BigNumber | null;
}

export interface VaultPoolBalanceChangedPayload1 {
    /**
     * In-memory map.
     * 
     * Key of `BigNumber`: Nat - arbitrary big integer >= 0.
     * 
     * Value of `BigNumber`: Integer from -2^31-1 to 2^31.
     */
    amountsInOrOut: MichelsonMap<BigNumber, BigNumber>;

    poolId: VaultPoolBalanceChangedPayload1PoolId;

    /** Tezos address. */
    sender: string;

    /**
     * In-memory map.
     * 
     * Key of `BigNumber`: Nat - arbitrary big integer >= 0.
     * 
     * Value of `VaultPoolBalanceChangedPayload1TokensValue`.
     */
    tokens: MichelsonMap<BigNumber, VaultPoolBalanceChangedPayload1TokensValue>;
}

export interface VaultPoolBalanceChangedPayload1PoolId {
    /** Tezos address. */
    '1': string;

    /** Nat - arbitrary big integer >= 0. */
    '2': BigNumber;
}

export interface VaultPoolBalanceChangedPayload1TokensValue {
    /** Tezos address. */
    '0': string;

    /** Nat - arbitrary big integer >= 0. */
    '1': BigNumber | null;
}

export interface VaultPoolBalanceChangedPayload2 {
    /**
     * In-memory map.
     * 
     * Key of `BigNumber`: Nat - arbitrary big integer >= 0.
     * 
     * Value of `BigNumber`: Integer from -2^31-1 to 2^31.
     */
    amountsInOrOut: MichelsonMap<BigNumber, BigNumber>;

    poolId: VaultPoolBalanceChangedPayload2PoolId;

    /** Tezos address. */
    sender: string;

    /**
     * In-memory map.
     * 
     * Key of `BigNumber`: Nat - arbitrary big integer >= 0.
     * 
     * Value of `VaultPoolBalanceChangedPayload2TokensValue`.
     */
    tokens: MichelsonMap<BigNumber, VaultPoolBalanceChangedPayload2TokensValue>;
}

export interface VaultPoolBalanceChangedPayload2PoolId {
    /** Tezos address. */
    '1': string;

    /** Nat - arbitrary big integer >= 0. */
    '2': BigNumber;
}

export interface VaultPoolBalanceChangedPayload2TokensValue {
    /** Tezos address. */
    '0': string;

    /** Nat - arbitrary big integer >= 0. */
    '1': BigNumber | null;
}

export type VaultPoolBalanceChangedPayload = VaultPoolBalanceChangedPayload1 | VaultPoolBalanceChangedPayload2;

export interface VaultPoolRegisteredPayload {
    /** Tezos address. */
    pool: string;

    poolId: VaultPoolRegisteredPayloadPoolId;
}

export interface VaultPoolRegisteredPayloadPoolId {
    /** Tezos address. */
    '1': string;

    /** Nat - arbitrary big integer >= 0. */
    '2': BigNumber;
}

export interface VaultSwapPayload1 {
    /** Nat - arbitrary big integer >= 0. */
    amountIn: BigNumber;

    /** Nat - arbitrary big integer >= 0. */
    amountOut: BigNumber;

    poolId: VaultSwapPayload1PoolId;

    tokenIn: VaultSwapPayload1TokenIn;

    tokenOut: VaultSwapPayload1TokenOut;
}

export interface VaultSwapPayload1PoolId {
    /** Tezos address. */
    '2': string;

    /** Nat - arbitrary big integer >= 0. */
    '3': BigNumber;
}

export interface VaultSwapPayload1TokenIn {
    /** Tezos address. */
    '4': string;

    /** Nat - arbitrary big integer >= 0. */
    '5': BigNumber | null;
}

export interface VaultSwapPayload1TokenOut {
    /** Tezos address. */
    '6': string;

    /** Nat - arbitrary big integer >= 0. */
    '7': BigNumber | null;
}

export interface VaultSwapPayload2 {
    /** Nat - arbitrary big integer >= 0. */
    amountIn: BigNumber;

    /** Nat - arbitrary big integer >= 0. */
    amountOut: BigNumber;

    poolId: VaultSwapPayload2PoolId;

    tokenIn: VaultSwapPayload2TokenIn;

    tokenOut: VaultSwapPayload2TokenOut;
}

export interface VaultSwapPayload2PoolId {
    /** Tezos address. */
    '2': string;

    /** Nat - arbitrary big integer >= 0. */
    '3': BigNumber;
}

export interface VaultSwapPayload2TokenIn {
    /** Tezos address. */
    '4': string;

    /** Nat - arbitrary big integer >= 0. */
    '5': BigNumber | null;
}

export interface VaultSwapPayload2TokenOut {
    /** Tezos address. */
    '6': string;

    /** Nat - arbitrary big integer >= 0. */
    '7': BigNumber | null;
}

export type VaultSwapPayload = VaultSwapPayload1 | VaultSwapPayload2;

export interface VaultTokensRegisteredPayload {
    poolId: VaultTokensRegisteredPayloadPoolId;

    /**
     * In-memory map.
     * 
     * Key of `BigNumber`: Nat - arbitrary big integer >= 0.
     * 
     * Value of `VaultTokensRegisteredPayloadTokensValue`.
     */
    tokens: MichelsonMap<BigNumber, VaultTokensRegisteredPayloadTokensValue>;
}

export interface VaultTokensRegisteredPayloadPoolId {
    /** Tezos address. */
    '0': string;

    /** Nat - arbitrary big integer >= 0. */
    '1': BigNumber;
}

export interface VaultTokensRegisteredPayloadTokensValue {
    /** Tezos address. */
    '0': string;

    /** Nat - arbitrary big integer >= 0. */
    '1': BigNumber | null;
}
