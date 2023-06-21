
import { ContractAbstractionFromContractType, WalletContractAbstractionFromContractType } from './type-utils';
import { address, BigMap, bytes, Instruction, MMap, nat } from './type-aliases';

export type Storage = {
    admin: address;
    balances: BigMap<address, {
        approvals: MMap<address, nat>;
        balance: nat;
    }>;
    entries: BigMap<string, nat>;
    exemptFromYieldFees: boolean;
    feeCache: {
        0: nat;
        1: nat;
    };
    fixedPoint: BigMap<string, Instruction[]>;
    getTokenValue: Instruction[];
    initialized: boolean;
    metadata: BigMap<string, bytes>;
    normalizedWeights: MMap<nat, nat>;
    poolId?: {
        0: address;
        1: nat;
    };
    proposed_admin?: address;
    protocolFeesCollector: address;
    rateProviders?: MMap<nat, address>;
    recoveryMode: boolean;
    scalingFactors: MMap<nat, nat>;
    scaling_helpers: BigMap<string, Instruction[]>;
    settings: boolean;
    token_metadata: BigMap<nat, {
        token_id: nat;
        token_info: MMap<string, bytes>;
    }>;
    tokens: MMap<nat, {
        0: address;
        1?: nat;
    }>;
    totalSupply: nat;
    vault: address;
    weightedMathLib: address;
    weightedProtocolFeesLib: address;
};

type Methods = {
    accept_admin: () => Promise<void>;
    afterExitPool: (
        amountsOut: MMap<nat, nat>,
        balances: MMap<nat, nat>,
        invariant: nat,
        poolId: {
            0: address;
            1: nat;
        },
        recoveryModeExit: boolean,
        sender: address,
        sptAmountIn: nat,
    ) => Promise<void>;
    afterJoinPool: (
        amountsIn: MMap<nat, nat>,
        balances: MMap<nat, nat>,
        invariant: nat,
        poolId: {
            0: address;
            1: nat;
        },
        recipient: address,
        sptAmountOut: nat,
    ) => Promise<void>;
    approve: (
        spender: address,
        value: nat,
    ) => Promise<void>;
    initializePool: () => Promise<void>;
    set_paused: (param: boolean) => Promise<void>;
    transfer: (
        from: address,
        to: address,
        value: nat,
    ) => Promise<void>;
    transfer_admin: (param: address) => Promise<void>;
    updateProtocolFeePercentageCache: () => Promise<void>;
};

type MethodsObject = {
    accept_admin: () => Promise<void>;
    afterExitPool: (params: {
        amountsOut: MMap<nat, nat>,
        balances: MMap<nat, nat>,
        invariant: nat,
        poolId: {
            0: address;
            1: nat;
        },
        recoveryModeExit: boolean,
        sender: address,
        sptAmountIn: nat,
    }) => Promise<void>;
    afterJoinPool: (params: {
        amountsIn: MMap<nat, nat>,
        balances: MMap<nat, nat>,
        invariant: nat,
        poolId: {
            0: address;
            1: nat;
        },
        recipient: address,
        sptAmountOut: nat,
    }) => Promise<void>;
    approve: (params: {
        spender: address,
        value: nat,
    }) => Promise<void>;
    initializePool: () => Promise<void>;
    set_paused: (param: boolean) => Promise<void>;
    transfer: (params: {
        from: address,
        to: address,
        value: nat,
    }) => Promise<void>;
    transfer_admin: (param: address) => Promise<void>;
    updateProtocolFeePercentageCache: () => Promise<void>;
};

type contractTypes = { methods: Methods, methodsObject: MethodsObject, storage: Storage, code: { __type: 'WeightedPoolCode', protocol: string, code: object[] } };
export type WeightedPoolContractType = ContractAbstractionFromContractType<contractTypes>;
export type WeightedPoolWalletType = WalletContractAbstractionFromContractType<contractTypes>;
