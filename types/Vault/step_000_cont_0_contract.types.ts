
import { ContractAbstractionFromContractType, WalletContractAbstractionFromContractType } from '../type-utils';
import { address, BigMap, bytes, int, MMap, nat, timestamp, unit } from '../type-aliases';

export type Storage = {
    admin: address;
    isPoolRegistered: BigMap<{
        0: address;
        1: nat;
    }, unit>;
    metadata: BigMap<string, bytes>;
    nextPoolNonce: nat;
    poolsBalances: BigMap<{
        0: address;
        1: nat;
    }, MMap<{
        0: address;
        1?: nat;
    }, {
        0: nat;
        1: nat;
    }>>;
    poolsTokens: BigMap<{
        0: address;
        1: nat;
    }, MMap<nat, {
        0: address;
        1?: nat;
    }>>;
    proposed_admin?: address;
    settings: boolean;
};

type Methods = {
    accept_admin: () => Promise<void>;
    batchSwap: (
        assets: MMap<nat, {
            0: address;
            1?: nat;
        }>,
        deadline: timestamp,
        funds: {
            recipient: address;
            sender: address;
        },
        kind: string,
        limits: MMap<nat, int>,
        swaps: MMap<nat, {
            amount: nat;
            assetInIndex: nat;
            assetOutIndex: nat;
            poolId: {
                0: address;
                1: nat;
            };
        }>,
    ) => Promise<void>;
    exitPool: (
        poolId: {
            0: address;
            1: nat;
        },
        recipient: address,
        request: {
            assets: MMap<nat, {
                0: address;
                1?: nat;
            }>;
            limits: MMap<nat, nat>;
            userData: {
                amountsOut?: MMap<nat, nat>;
                kind: string;
                maxSPTAmountIn?: nat;
                recoveryModeExit: boolean;
                sptAmountIn?: nat;
                tokenIndex?: nat;
            };
        },
        sender: address,
    ) => Promise<void>;
    joinPool: (
        poolId: {
            0: address;
            1: nat;
        },
        recipient: address,
        request: {
            assets: MMap<nat, {
                0: address;
                1?: nat;
            }>;
            limits: MMap<nat, nat>;
            userData: {
                allT?: nat;
                amountsIn?: MMap<nat, nat>;
                kind: string;
                minSPTAmountOut?: nat;
                sptAmountOut?: nat;
                tokenIndex?: nat;
            };
        },
        sender: address,
    ) => Promise<void>;
    registerPool: () => Promise<void>;
    registerTokens: (
        assetManagers?: MMap<nat, address>,
        poolId: {
            0: address;
            1: nat;
        },
        tokens: MMap<nat, {
            0: address;
            1?: nat;
        }>,
    ) => Promise<void>;
    set_paused: (param: boolean) => Promise<void>;
    swap: (
        deadline: timestamp,
        funds: {
            recipient: address;
            sender: address;
        },
        limit: nat,
        singleSwap: {
            amount: nat;
            assetIn: {
                0: address;
                1?: nat;
            };
            assetOut: {
                0: address;
                1?: nat;
            };
            kind: string;
            poolId: {
                0: address;
                1: nat;
            };
        },
    ) => Promise<void>;
    transfer_admin: (param: address) => Promise<void>;
};

type MethodsObject = {
    accept_admin: () => Promise<void>;
    batchSwap: (params: {
        assets: MMap<nat, {
            0: address;
            1?: nat;
        }>,
        deadline: timestamp,
        funds: {
            recipient: address;
            sender: address;
        },
        kind: string,
        limits: MMap<nat, int>,
        swaps: MMap<nat, {
            amount: nat;
            assetInIndex: nat;
            assetOutIndex: nat;
            poolId: {
                0: address;
                1: nat;
            };
        }>,
    }) => Promise<void>;
    exitPool: (params: {
        poolId: {
            0: address;
            1: nat;
        },
        recipient: address,
        request: {
            assets: MMap<nat, {
                0: address;
                1?: nat;
            }>;
            limits: MMap<nat, nat>;
            userData: {
                amountsOut?: MMap<nat, nat>;
                kind: string;
                maxSPTAmountIn?: nat;
                recoveryModeExit: boolean;
                sptAmountIn?: nat;
                tokenIndex?: nat;
            };
        },
        sender: address,
    }) => Promise<void>;
    joinPool: (params: {
        poolId: {
            0: address;
            1: nat;
        },
        recipient: address,
        request: {
            assets: MMap<nat, {
                0: address;
                1?: nat;
            }>;
            limits: MMap<nat, nat>;
            userData: {
                allT?: nat;
                amountsIn?: MMap<nat, nat>;
                kind: string;
                minSPTAmountOut?: nat;
                sptAmountOut?: nat;
                tokenIndex?: nat;
            };
        },
        sender: address,
    }) => Promise<void>;
    registerPool: () => Promise<void>;
    registerTokens: (params: {
        assetManagers?: MMap<nat, address>,
        poolId: {
            0: address;
            1: nat;
        },
        tokens: MMap<nat, {
            0: address;
            1?: nat;
        }>,
    }) => Promise<void>;
    set_paused: (param: boolean) => Promise<void>;
    swap: (params: {
        deadline: timestamp,
        funds: {
            recipient: address;
            sender: address;
        },
        limit: nat,
        singleSwap: {
            amount: nat;
            assetIn: {
                0: address;
                1?: nat;
            };
            assetOut: {
                0: address;
                1?: nat;
            };
            kind: string;
            poolId: {
                0: address;
                1: nat;
            };
        },
    }) => Promise<void>;
    transfer_admin: (param: address) => Promise<void>;
};

type contractTypes = { methods: Methods, methodsObject: MethodsObject, storage: Storage, code: { __type: 'VaultStep000Cont0ContractCode', protocol: string, code: object[] } };
export type VaultStep000Cont0ContractContractType = ContractAbstractionFromContractType<contractTypes>;
export type VaultStep000Cont0ContractWalletType = WalletContractAbstractionFromContractType<contractTypes>;
