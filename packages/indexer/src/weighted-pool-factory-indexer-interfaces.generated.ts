/* istanbul ignore next */
/* eslint-disable */

// This file was generated.
// It should NOT be modified manually rather it should be regenerated.
// Contract: KT1Ewux3ZjVaGnowHo9sVu7wzGhDbq3he65o
// Tezos network: mainnet

import { UnitValue } from '@taquito/michelson-encoder';
import { BigMapAbstraction, MichelsonMap } from '@taquito/taquito';

export type WeightedPoolFactoryParameter =
    | { entrypoint: 'create'; value: WeightedPoolFactoryCreateParameter };

export interface WeightedPoolFactoryCreateParameter {
    /** Bytes. */
    metadata: string;

    /**
     * In-memory map.
     * 
     * Key of `string`: Arbitrary string.
     * 
     * Value of `string`: Bytes.
     */
    token_metadata: MichelsonMap<string, string>;
}

export interface WeightedPoolFactoryCurrentStorage {
    /** Tezos address. */
    admin: string;

    /**
     * Big map.
     * 
     * Key of `string`: Arbitrary string.
     * 
     * Value of `unknown`: Lambda.
     */
    fixedPoint: BigMapAbstraction;

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
    protocolFeeProvider: string;

    /** Tezos address. */
    vault: string;

    /** Tezos address. */
    weightedMathLib: string;

    /** Tezos address. */
    weightedProtocolFeesLib: string;
}

export interface WeightedPoolFactoryChangedStorage {
    /** Tezos address. */
    admin: string;

    /** Big map ID - string with arbitrary big integer, negative if temporary. */
    fixedPoint: string;

    /** Big map ID - string with arbitrary big integer, negative if temporary. */
    isPoolFromFactory: string;

    /** Big map ID - string with arbitrary big integer, negative if temporary. */
    metadata: string;

    /** Tezos address. */
    protocolFeeProvider: string;

    /** Tezos address. */
    vault: string;

    /** Tezos address. */
    weightedMathLib: string;

    /** Tezos address. */
    weightedProtocolFeesLib: string;
}

export interface WeightedPoolFactoryInitialStorage {
    /** Tezos address. */
    admin: string;

    /**
     * Big map initial values.
     * 
     * Key of `string`: Arbitrary string.
     * 
     * Value of `unknown`: Lambda.
     */
    fixedPoint: MichelsonMap<string, unknown>;

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
    protocolFeeProvider: string;

    /** Tezos address. */
    vault: string;

    /** Tezos address. */
    weightedMathLib: string;

    /** Tezos address. */
    weightedProtocolFeesLib: string;
}

/** Arbitrary string. */
export type WeightedPoolFactoryFixedPointKey = string;

/** Lambda. */
export type WeightedPoolFactoryFixedPointValue = unknown;

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
