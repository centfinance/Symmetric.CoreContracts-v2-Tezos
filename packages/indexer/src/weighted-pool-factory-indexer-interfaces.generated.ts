/* istanbul ignore next */
/* eslint-disable */

// This file was generated.
// It should NOT be modified manually rather it should be regenerated.
// Contract: KT1QmzwyMArWDrEkhHDHBtM4sh39xfVinqoE
// Tezos network: mainnet

import { UnitValue } from '@taquito/michelson-encoder';
import { BigMapAbstraction, MichelsonMap } from '@taquito/taquito';
import { BigNumber } from 'bignumber.js';

export type WeightedPoolFactoryParameter =
    | { entrypoint: 'accept_admin'; value: WeightedPoolFactoryAcceptAdminParameter }
    | { entrypoint: 'create'; value: WeightedPoolFactoryCreateParameter }
    | { entrypoint: 'transfer_admin'; value: WeightedPoolFactoryTransferAdminParameter };

/** An empty result. */
export type WeightedPoolFactoryAcceptAdminParameter = typeof UnitValue;

export interface WeightedPoolFactoryCreateParameter {
    /** Bytes. */
    metadata: string;

    /**
     * In-memory map.
     * 
     * Key of `BigNumber`: Nat - arbitrary big integer >= 0.
     * 
     * Value of `BigNumber`: Nat - arbitrary big integer >= 0.
     */
    normalizedWeights: MichelsonMap<BigNumber, BigNumber>;

    /**
     * In-memory map.
     * 
     * Key of `BigNumber`: Nat - arbitrary big integer >= 0.
     * 
     * Value of `string | null`: Tezos address.
     */
    rateProviders: MichelsonMap<BigNumber, string | null> | null;

    /** Nat - arbitrary big integer >= 0. */
    swapFeePercentage: BigNumber;

    /**
     * In-memory map.
     * 
     * Key of `BigNumber`: Nat - arbitrary big integer >= 0.
     * 
     * Value of `BigNumber`: Nat - arbitrary big integer >= 0.
     */
    tokenDecimals: MichelsonMap<BigNumber, BigNumber>;

    /**
     * In-memory map.
     * 
     * Key of `string`: Arbitrary string.
     * 
     * Value of `string`: Bytes.
     */
    token_metadata: MichelsonMap<string, string>;

    /**
     * In-memory map.
     * 
     * Key of `BigNumber`: Nat - arbitrary big integer >= 0.
     * 
     * Value of `WeightedPoolFactoryCreateParameterTokensValue`.
     */
    tokens: MichelsonMap<BigNumber, WeightedPoolFactoryCreateParameterTokensValue>;
}

export interface WeightedPoolFactoryCreateParameterTokensValue {
    /** Tezos address. */
    '0': string;

    /** Nat - arbitrary big integer >= 0. */
    '1': BigNumber | null;
}

/** Tezos address. */
export type WeightedPoolFactoryTransferAdminParameter = string;

export interface WeightedPoolFactoryCurrentStorage {
    /** Tezos address. */
    admin: string;

    feeCache: WeightedPoolFactoryCurrentStorageFeeCache;

    /**
     * Big map.
     * 
     * Key of `string`: Tezos address.
     * 
     * Value of `typeof UnitValue`: An empty result.
     */
    isPoolFromFactory: BigMapAbstraction;

    /**
     * Big map.
     * 
     * Key of `string`: Arbitrary string.
     * 
     * Value of `string`: Bytes.
     */
    metadata: BigMapAbstraction;

    /** Tezos address. */
    proposed_admin: string | null;

    /** Tezos address. */
    protocolFeeProvider: string;

    /** Tezos address. */
    vault: string;

    /** Tezos address. */
    weightedMathLib: string;

    /** Tezos address. */
    weightedProtocolFeesLib: string;
}

export interface WeightedPoolFactoryCurrentStorageFeeCache {
    /** Nat - arbitrary big integer >= 0. */
    '1': BigNumber;

    /** Nat - arbitrary big integer >= 0. */
    '2': BigNumber;
}

export interface WeightedPoolFactoryChangedStorage {
    /** Tezos address. */
    admin: string;

    feeCache: WeightedPoolFactoryChangedStorageFeeCache;

    /** Big map ID - string with arbitrary big integer, negative if temporary. */
    isPoolFromFactory: string;

    /** Big map ID - string with arbitrary big integer, negative if temporary. */
    metadata: string;

    /** Tezos address. */
    proposed_admin: string | null;

    /** Tezos address. */
    protocolFeeProvider: string;

    /** Tezos address. */
    vault: string;

    /** Tezos address. */
    weightedMathLib: string;

    /** Tezos address. */
    weightedProtocolFeesLib: string;
}

export interface WeightedPoolFactoryChangedStorageFeeCache {
    /** Nat - arbitrary big integer >= 0. */
    '1': BigNumber;

    /** Nat - arbitrary big integer >= 0. */
    '2': BigNumber;
}

export interface WeightedPoolFactoryInitialStorage {
    /** Tezos address. */
    admin: string;

    feeCache: WeightedPoolFactoryInitialStorageFeeCache;

    /**
     * Big map initial values.
     * 
     * Key of `string`: Tezos address.
     * 
     * Value of `typeof UnitValue`: An empty result.
     */
    isPoolFromFactory: MichelsonMap<string, typeof UnitValue>;

    /**
     * Big map initial values.
     * 
     * Key of `string`: Arbitrary string.
     * 
     * Value of `string`: Bytes.
     */
    metadata: MichelsonMap<string, string>;

    /** Tezos address. */
    proposed_admin: string | null;

    /** Tezos address. */
    protocolFeeProvider: string;

    /** Tezos address. */
    vault: string;

    /** Tezos address. */
    weightedMathLib: string;

    /** Tezos address. */
    weightedProtocolFeesLib: string;
}

export interface WeightedPoolFactoryInitialStorageFeeCache {
    /** Nat - arbitrary big integer >= 0. */
    '1': BigNumber;

    /** Nat - arbitrary big integer >= 0. */
    '2': BigNumber;
}

/** Tezos address. */
export type WeightedPoolFactoryIsPoolFromFactoryKey = string;

/** An empty result. */
export type WeightedPoolFactoryIsPoolFromFactoryValue = typeof UnitValue;

/** Arbitrary string. */
export type WeightedPoolFactoryMetadataKey = string;

/** Bytes. */
export type WeightedPoolFactoryMetadataValue = string;

/** Tezos address. */
export type WeightedPoolFactoryPoolCreatedPayload = string;
