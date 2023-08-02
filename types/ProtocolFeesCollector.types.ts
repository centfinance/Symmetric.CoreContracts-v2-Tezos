
import { ContractAbstractionFromContractType, WalletContractAbstractionFromContractType } from './type-utils';
import { address, MMap, nat } from './type-aliases';

export type Storage = {
    admin: address;
    flashLoanFeePercentage: nat;
    proposed_admin?: address;
    swapFeePercentage: nat;
    vault: address;
};

type Methods = {
    accept_admin: () => Promise<void>;
    setFlashLoanFeePercentage: (param: nat) => Promise<void>;
    setSwapFeePercentage: (param: nat) => Promise<void>;
    transfer_admin: (param: address) => Promise<void>;
    withdrawCollectedFees: (
        amounts: MMap<nat, nat>,
        recipient: address,
        tokens: MMap<nat, {
            0: address;
            1?: nat;
        }>,
    ) => Promise<void>;
};

type MethodsObject = {
    accept_admin: () => Promise<void>;
    setFlashLoanFeePercentage: (param: nat) => Promise<void>;
    setSwapFeePercentage: (param: nat) => Promise<void>;
    transfer_admin: (param: address) => Promise<void>;
    withdrawCollectedFees: (params: {
        amounts: MMap<nat, nat>,
        recipient: address,
        tokens: MMap<nat, {
            0: address;
            1?: nat;
        }>,
    }) => Promise<void>;
};

type contractTypes = { methods: Methods, methodsObject: MethodsObject, storage: Storage, code: { __type: 'ProtocolFeesCollectorCode', protocol: string, code: object[] } };
export type ProtocolFeesCollectorContractType = ContractAbstractionFromContractType<contractTypes>;
export type ProtocolFeesCollectorWalletType = WalletContractAbstractionFromContractType<contractTypes>;
