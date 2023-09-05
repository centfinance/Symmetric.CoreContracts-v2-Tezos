
import { ContractAbstractionFromContractType, WalletContractAbstractionFromContractType } from './type-utils';
import { address, BigMap, bytes, MMap, nat, unit } from './type-aliases';

export type Storage = {
    admin: address;
    feeCache: {
        0: nat;
        1: nat;
    };
    isPoolFromFactory: BigMap<address, unit>;
    lastPool: address;
    metadata: BigMap<string, bytes>;
    proposed_admin?: address;
    protocolFeeProvider: address;
    vault: address;
    weightedMathLib: address;
    weightedProtocolFeesLib: address;
};

type Methods = {
    accept_admin: () => Promise<void>;
    create: (
        metadata: bytes,
        normalizedWeights: MMap<nat, nat>,
        rateProviders?: MMap<nat, address>,
        swapFeePercentage: nat,
        tokenDecimals: MMap<nat, nat>,
        token_metadata: MMap<string, bytes>,
        tokens: MMap<nat, {
            0: address;
            1?: nat;
        }>,
    ) => Promise<void>;
    initialize: () => Promise<void>;
    transfer_admin: (param: address) => Promise<void>;
};

type MethodsObject = {
    accept_admin: () => Promise<void>;
    create: (params: {
        metadata: bytes,
        normalizedWeights: MMap<nat, nat>,
        rateProviders?: MMap<nat, address>,
        swapFeePercentage: nat,
        tokenDecimals: MMap<nat, nat>,
        token_metadata: MMap<string, bytes>,
        tokens: MMap<nat, {
            0: address;
            1?: nat;
        }>,
    }) => Promise<void>;
    initialize: () => Promise<void>;
    transfer_admin: (param: address) => Promise<void>;
};

type contractTypes = { methods: Methods, methodsObject: MethodsObject, storage: Storage, code: { __type: 'WeightedPoolFactoryCode', protocol: string, code: object[] } };
export type WeightedPoolFactoryContractType = ContractAbstractionFromContractType<contractTypes>;
export type WeightedPoolFactoryWalletType = WalletContractAbstractionFromContractType<contractTypes>;
