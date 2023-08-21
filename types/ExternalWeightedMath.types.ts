
import { ContractAbstractionFromContractType, WalletContractAbstractionFromContractType } from './type-utils';
import { BigMap, Instruction, nat } from './type-aliases';

export type Storage = BigMap<nat, Instruction[]>;

type Methods = {
    
};

type MethodsObject = {
    
};

type contractTypes = { methods: Methods, methodsObject: MethodsObject, storage: Storage, code: { __type: 'ExternalWeightedMathCode', protocol: string, code: object[] } };
export type ExternalWeightedMathContractType = ContractAbstractionFromContractType<contractTypes>;
export type ExternalWeightedMathWalletType = WalletContractAbstractionFromContractType<contractTypes>;
