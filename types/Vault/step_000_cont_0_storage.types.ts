
import { ContractAbstractionFromContractType, WalletContractAbstractionFromContractType } from '../type-utils';
import {  } from '../type-aliases';

export type Storage = {
    
};

type Methods = {
    
};

type MethodsObject = {
    
};

type contractTypes = { methods: Methods, methodsObject: MethodsObject, storage: Storage, code: { __type: 'VaultStep000Cont0StorageCode', protocol: string, code: object[] } };
export type VaultStep000Cont0StorageContractType = ContractAbstractionFromContractType<contractTypes>;
export type VaultStep000Cont0StorageWalletType = WalletContractAbstractionFromContractType<contractTypes>;
