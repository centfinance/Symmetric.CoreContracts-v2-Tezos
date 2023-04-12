/* istanbul ignore next */
/* eslint-disable */

// This file was generated.
// It should NOT be modified manually rather it should be regenerated.
// Contract: KT1DSsMYr3n7C1ecYSgZimtFkDXdEQbxULFw
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
    /** Simple boolean. */
    FA2: boolean;

    /** Tezos address. */
    address: string;

    /** Nat - arbitrary big integer >= 0. */
    id: BigNumber;
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

    /** Bytes. */
    poolId: string;
}

export interface VaultExitPoolParameter {
    /** Bytes. */
    poolId: string;

    /** Tezos address. */
    recipient: string;

    request: VaultExitPoolParameterRequest;

    /** Tezos address. */
    sender: string;
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
    /** Simple boolean. */
    FA2: boolean;

    /** Tezos address. */
    address: string;

    /** Nat - arbitrary big integer >= 0. */
    id: BigNumber;
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
    /** Bytes. */
    poolId: string;

    /** Tezos address. */
    recipient: string;

    request: VaultJoinPoolParameterRequest;

    /** Tezos address. */
    sender: string;
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
    /** Simple boolean. */
    FA2: boolean;

    /** Tezos address. */
    address: string;

    /** Nat - arbitrary big integer >= 0. */
    id: BigNumber;
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

/** Nat - arbitrary big integer >= 0. */
export type VaultRegisterPoolParameter = BigNumber;

export interface VaultRegisterTokensParameter {
    /**
     * In-memory map.
     * 
     * Key of `BigNumber`: Nat - arbitrary big integer >= 0.
     * 
     * Value of `string`: Tezos address.
     */
    assetManagers: MichelsonMap<BigNumber, string> | null;

    /** Bytes. */
    poolId: string;

    /**
     * In-memory map.
     * 
     * Key of `BigNumber`: Nat - arbitrary big integer >= 0.
     * 
     * Value of `VaultRegisterTokensParameterTokensValue`.
     */
    tokens: MichelsonMap<BigNumber, VaultRegisterTokensParameterTokensValue>;
}

export interface VaultRegisterTokensParameterTokensValue {
    /** Simple boolean. */
    FA2: boolean;

    /** Tezos address. */
    address: string;

    /** Nat - arbitrary big integer >= 0. */
    id: BigNumber;
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

    /** Bytes. */
    poolId: string;
}

export interface VaultSwapParameterSingleSwapAssetIn {
    /** Simple boolean. */
    FA2: boolean;

    /** Tezos address. */
    address: string;

    /** Nat - arbitrary big integer >= 0. */
    id: BigNumber;
}

export interface VaultSwapParameterSingleSwapAssetOut {
    /** Simple boolean. */
    FA2: boolean;

    /** Tezos address. */
    address: string;

    /** Nat - arbitrary big integer >= 0. */
    id: BigNumber;
}

/** Tezos address. */
export type VaultTransferAdminParameter = string;

export interface VaultCurrentStorage {
    /** Tezos address. */
    admin: string;

    /**
     * Big map.
     * 
     * Key of `string`: Bytes.
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
     * Key of `string`: Bytes.
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
     * Key of `string`: Bytes.
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

export interface VaultCurrentStoragePoolsBalancesValueKey {
    /** Simple boolean. */
    FA2: boolean;

    /** Tezos address. */
    address: string;

    /** Nat - arbitrary big integer >= 0. */
    id: BigNumber;
}

export interface VaultCurrentStoragePoolsBalancesValueValue {
    /** Nat - arbitrary big integer >= 0. */
    cash: BigNumber;

    /** Nat - arbitrary big integer >= 0. */
    lastChangeBlock: BigNumber;

    /** Nat - arbitrary big integer >= 0. */
    managed: BigNumber;
}

export interface VaultCurrentStoragePoolsTokensValueValue {
    /** Simple boolean. */
    FA2: boolean;

    /** Tezos address. */
    address: string;

    /** Nat - arbitrary big integer >= 0. */
    id: BigNumber;
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
     * Key of `string`: Bytes.
     * 
     * Value of `typeof UnitValue`: An empty result.
     */
    isPoolRegistered: MichelsonMap<string, typeof UnitValue>;

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
     * Key of `string`: Bytes.
     * 
     * Value of `MichelsonMap<VaultInitialStoragePoolsBalancesValueKey, VaultInitialStoragePoolsBalancesValueValue>`:
     * In-memory map.
     * 
     * Key of `VaultInitialStoragePoolsBalancesValueKey`.
     * 
     * Value of `VaultInitialStoragePoolsBalancesValueValue`.
     */
    poolsBalances: MichelsonMap<string, MichelsonMap<VaultInitialStoragePoolsBalancesValueKey, VaultInitialStoragePoolsBalancesValueValue>>;

    /**
     * Big map initial values.
     * 
     * Key of `string`: Bytes.
     * 
     * Value of `MichelsonMap<BigNumber, VaultInitialStoragePoolsTokensValueValue>`:
     * In-memory map.
     * 
     * Key of `BigNumber`: Nat - arbitrary big integer >= 0.
     * 
     * Value of `VaultInitialStoragePoolsTokensValueValue`.
     */
    poolsTokens: MichelsonMap<string, MichelsonMap<BigNumber, VaultInitialStoragePoolsTokensValueValue>>;

    /** Tezos address. */
    proposed_admin: string | null;

    /** Simple boolean. */
    settings: boolean;
}

export interface VaultInitialStoragePoolsBalancesValueKey {
    /** Simple boolean. */
    FA2: boolean;

    /** Tezos address. */
    address: string;

    /** Nat - arbitrary big integer >= 0. */
    id: BigNumber;
}

export interface VaultInitialStoragePoolsBalancesValueValue {
    /** Nat - arbitrary big integer >= 0. */
    cash: BigNumber;

    /** Nat - arbitrary big integer >= 0. */
    lastChangeBlock: BigNumber;

    /** Nat - arbitrary big integer >= 0. */
    managed: BigNumber;
}

export interface VaultInitialStoragePoolsTokensValueValue {
    /** Simple boolean. */
    FA2: boolean;

    /** Tezos address. */
    address: string;

    /** Nat - arbitrary big integer >= 0. */
    id: BigNumber;
}

/** Bytes. */
export type VaultIsPoolRegisteredKey = string;

/** An empty result. */
export type VaultIsPoolRegisteredValue = typeof UnitValue;

/** Arbitrary string. */
export type VaultMetadataKey = string;

/** Bytes. */
export type VaultMetadataValue = string;

/** Bytes. */
export type VaultPoolsBalancesKey = string;

/**
 * In-memory map.
 * 
 * Key of `VaultPoolsBalancesValueKey`.
 * 
 * Value of `VaultPoolsBalancesValueValue`.
 */
export type VaultPoolsBalancesValue = MichelsonMap<VaultPoolsBalancesValueKey, VaultPoolsBalancesValueValue>;

export interface VaultPoolsBalancesValueKey {
    /** Simple boolean. */
    FA2: boolean;

    /** Tezos address. */
    address: string;

    /** Nat - arbitrary big integer >= 0. */
    id: BigNumber;
}

export interface VaultPoolsBalancesValueValue {
    /** Nat - arbitrary big integer >= 0. */
    cash: BigNumber;

    /** Nat - arbitrary big integer >= 0. */
    lastChangeBlock: BigNumber;

    /** Nat - arbitrary big integer >= 0. */
    managed: BigNumber;
}

/** Bytes. */
export type VaultPoolsTokensKey = string;

/**
 * In-memory map.
 * 
 * Key of `BigNumber`: Nat - arbitrary big integer >= 0.
 * 
 * Value of `VaultPoolsTokensValueValue`.
 */
export type VaultPoolsTokensValue = MichelsonMap<BigNumber, VaultPoolsTokensValueValue>;

export interface VaultPoolsTokensValueValue {
    /** Simple boolean. */
    FA2: boolean;

    /** Tezos address. */
    address: string;

    /** Nat - arbitrary big integer >= 0. */
    id: BigNumber;
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

    /** Bytes. */
    poolId: string;

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

export interface VaultPoolBalanceChangedPayload1TokensValue {
    /** Simple boolean. */
    FA2: boolean;

    /** Tezos address. */
    address: string;

    /** Nat - arbitrary big integer >= 0. */
    id: BigNumber;
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

    /** Bytes. */
    poolId: string;

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

export interface VaultPoolBalanceChangedPayload2TokensValue {
    /** Simple boolean. */
    FA2: boolean;

    /** Tezos address. */
    address: string;

    /** Nat - arbitrary big integer >= 0. */
    id: BigNumber;
}

export type VaultPoolBalanceChangedPayload = VaultPoolBalanceChangedPayload1 | VaultPoolBalanceChangedPayload2;

export interface VaultPoolRegisteredPayload {
    /** Tezos address. */
    pool: string;

    /** Bytes. */
    poolId: string;

    /** Nat - arbitrary big integer >= 0. */
    specialization: BigNumber;
}

export interface VaultSwapPayload1 {
    /** Nat - arbitrary big integer >= 0. */
    amountIn: BigNumber;

    /** Nat - arbitrary big integer >= 0. */
    amountOut: BigNumber;

    /** Bytes. */
    poolId: string;

    tokenIn: VaultSwapPayload1TokenIn;

    tokenOut: VaultSwapPayload1TokenOut;
}

export interface VaultSwapPayload1TokenIn {
    /** Tezos address. */
    '3': string;

    /** Nat - arbitrary big integer >= 0. */
    '4': BigNumber;
}

export interface VaultSwapPayload1TokenOut {
    /** Tezos address. */
    '5': string;

    /** Nat - arbitrary big integer >= 0. */
    '6': BigNumber;
}

export interface VaultSwapPayload2 {
    /** Nat - arbitrary big integer >= 0. */
    amountIn: BigNumber;

    /** Nat - arbitrary big integer >= 0. */
    amountOut: BigNumber;

    /** Bytes. */
    poolId: string;

    tokenIn: VaultSwapPayload2TokenIn;

    tokenOut: VaultSwapPayload2TokenOut;
}

export interface VaultSwapPayload2TokenIn {
    /** Tezos address. */
    '3': string;

    /** Nat - arbitrary big integer >= 0. */
    '4': BigNumber;
}

export interface VaultSwapPayload2TokenOut {
    /** Tezos address. */
    '5': string;

    /** Nat - arbitrary big integer >= 0. */
    '6': BigNumber;
}

export type VaultSwapPayload = VaultSwapPayload1 | VaultSwapPayload2;

export interface VaultTokensRegisteredPayload {
    /** Bytes. */
    poolId: string;

    /** Nat - arbitrary big integer >= 0. */
    specialization: BigNumber;

    /**
     * In-memory map.
     * 
     * Key of `BigNumber`: Nat - arbitrary big integer >= 0.
     * 
     * Value of `VaultTokensRegisteredPayloadTokensValue`.
     */
    tokens: MichelsonMap<BigNumber, VaultTokensRegisteredPayloadTokensValue>;
}

export interface VaultTokensRegisteredPayloadTokensValue {
    /** Simple boolean. */
    FA2: boolean;

    /** Tezos address. */
    address: string;

    /** Nat - arbitrary big integer >= 0. */
    id: BigNumber;
}
