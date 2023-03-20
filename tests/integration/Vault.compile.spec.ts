
import { TezosToolkit } from '@taquito/taquito';
import { char2Bytes } from '@taquito/utils';
import { tas } from '../types/type-aliases';
import { InMemorySigner, importKey } from '@taquito/signer';
import { VaultCompileContractType as ContractType } from '../types/Vault.compile.types';
import { VaultCompileCode as ContractCode } from '../types/Vault.compile.code';

jest.setTimeout(20000)

describe('Vault.compile', () => {
	const config = require('../.taq/config.json')
    const Tezos = new TezosToolkit(config.sandbox.local.rpcUrl);
	const key = config.sandbox.local.accounts.bob.secretKey.replace('unencrypted:', '')
	Tezos.setProvider({
		signer: new InMemorySigner(key),
	  });
    let contract: ContractType = undefined as unknown as ContractType;
    beforeAll(async () => {
        
            const newContractOrigination = await Tezos.contract.originate<ContractType>({
                code: ContractCode.code,
                storage: {
                        _isPoolRegistered: tas.bigMap([{ 
                            key: tas.bytes(char2Bytes('DATA')), 
                            value: tas.unit(),
                        }]),
                        _minimalSwapInfoPoolsBalances: tas.bigMap([{ 
                            key: tas.bytes(char2Bytes('DATA')), 
                            value: tas.map([{ 
                            key: {
                            FA2: true,
                            address: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                            id: tas.nat('42'),
                        }, 
                            value: {
                            cash: tas.nat('42'),
                            lastChangeBlock: tas.nat('42'),
                            managed: tas.nat('42'),
                        },
                        }]),
                        }]),
                        _minimalSwapInfoPoolsTokens: tas.bigMap([{ 
                            key: tas.bytes(char2Bytes('DATA')), 
                            value: tas.map([{ 
                            key: tas.nat('42'), 
                            value: {
                            FA2: true,
                            address: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                            id: tas.nat('42'),
                        },
                        }]),
                        }]),
                        nextPoolNonce: tas.nat('42'),
                        // 6: tas.bigMap([{ 
                        //     key: tas.nat('42'), 
                        //     value: tas.lambda([]),
                        // }]),
                    },
            });
            const newContractResult = await newContractOrigination.contract();
            const newContractAddress = newContractResult.address;
            contract = await Tezos.contract.at<ContractType>(newContractAddress);
            
    });


    it('should call batchSwap', async () => {
        
        const getStorageValue = async () => {
            const storage = await contract.storage();
            const value = storage;
            return value;
        };

        const storageValueBefore = await getStorageValue();
        
        const batchSwapRequest = await contract.methodsObject.batchSwap({
                assets: tas.map([{ 
                    key: tas.nat('42'), 
                    value: {
                    FA2: true,
                    address: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                    id: tas.nat('42'),
                },
                }]),
                deadline: tas.timestamp(new Date()),
                funds: {
                    fromInternalBalance: true,
                    recipient: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                    sender: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                    toInternalBalance: true,
                },
                kind: 'VALUE',
                limits: tas.map([{ 
                    key: tas.nat('42'), 
                    value: tas.int('42'),
                }]),
                swaps: tas.map([{ 
                    key: tas.nat('42'), 
                    value: {
                    amount: tas.nat('42'),
                    assetInIndex: tas.nat('42'),
                    assetOutIndex: tas.nat('42'),
                    poolId: tas.bytes(char2Bytes('DATA')),
                },
                }]),
            }).send();
        await batchSwapRequest.confirmation(3);
        
        const storageValueAfter = await getStorageValue();

        expect(storageValueAfter.toString()).toBe('');
    });

    it('should call registerPool', async () => {
        
        const getStorageValue = async () => {
            const storage = await contract.storage();
            const value = storage;
            return value;
        };

        const storageValueBefore = await getStorageValue();
        
        const registerPoolRequest = await contract.methodsObject.registerPool(tas.nat('42')).send();
        await registerPoolRequest.confirmation(3);
        
        const storageValueAfter = await getStorageValue();

        expect(storageValueAfter.toString()).toBe('');
    });

    it('should call registerTokens', async () => {
        
        const getStorageValue = async () => {
            const storage = await contract.storage();
            const value = storage;
            return value;
        };

        const storageValueBefore = await getStorageValue();
        
        const registerTokensRequest = await contract.methodsObject.registerTokens({
                assetManagers: [tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456')],
                poolId: tas.bytes(char2Bytes('DATA')),
                tokens: tas.map([{ 
                    key: tas.nat('42'), 
                    value: {
                    FA2: true,
                    address: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                    id: tas.nat('42'),
                },
                }]),
            }).send();
        await registerTokensRequest.confirmation(3);
        
        const storageValueAfter = await getStorageValue();

        expect(storageValueAfter.toString()).toBe('');
    });

    it('should call swap', async () => {
        
        const getStorageValue = async () => {
            const storage = await contract.storage();
            const value = storage;
            return value;
        };

        const storageValueBefore = await getStorageValue();
        
        const swapRequest = await contract.methodsObject.swap({
                deadline: tas.timestamp(new Date()),
                funds: {
                    fromInternalBalance: true,
                    recipient: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                    sender: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                    toInternalBalance: true,
                },
                limit: tas.nat('42'),
                singleSwap: {
                    amount: tas.nat('42'),
                    assetIn: {
                        FA2: true,
                        address: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                        id: tas.nat('42'),
                    },
                    assetOut: {
                        FA2: true,
                        address: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                        id: tas.nat('42'),
                    },
                    kind: 'VALUE',
                    poolId: tas.bytes(char2Bytes('DATA')),
                },
            }).send();
        await swapRequest.confirmation(3);
        
        const storageValueAfter = await getStorageValue();

        expect(storageValueAfter.toString()).toBe('');
    });

    it('should call exitPool', async () => {
        
        const getStorageValue = async () => {
            const storage = await contract.storage();
            const value = storage;
            return value;
        };

        const storageValueBefore = await getStorageValue();
        
        const exitPoolRequest = await contract.methodsObject.exitPool({
                poolId: tas.bytes(char2Bytes('DATA')),
                recipient: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                request: {
                    assets: tas.map([{ 
                        key: tas.nat('42'), 
                        value: {
                        FA2: true,
                        address: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                        id: tas.nat('42'),
                    },
                    }]),
                    limits: tas.map([{ 
                        key: tas.nat('42'), 
                        value: tas.nat('42'),
                    }]),
                    useInternalBalance: true,
                    userData: {
                        amountsOut: tas.map([{ 
                            key: tas.nat('42'), 
                            value: tas.nat('42'),
                        }]),
                        kind: 'VALUE',
                        maxSPTAmountIn: tas.nat('42'),
                        recoveryModeExit: true,
                        sptAmountIn: tas.nat('42'),
                        tokenIndex: tas.nat('42'),
                    },
                },
                sender: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
            }).send();
        await exitPoolRequest.confirmation(3);
        
        const storageValueAfter = await getStorageValue();

        expect(storageValueAfter.toString()).toBe('');
    });

    it('should call joinPool', async () => {
        
        const getStorageValue = async () => {
            const storage = await contract.storage();
            const value = storage;
            return value;
        };

        const storageValueBefore = await getStorageValue();
        
        const joinPoolRequest = await contract.methodsObject.joinPool({
                poolId: tas.bytes(char2Bytes('DATA')),
                recipient: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                request: {
                    assets: tas.map([{ 
                        key: tas.nat('42'), 
                        value: {
                        FA2: true,
                        address: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                        id: tas.nat('42'),
                    },
                    }]),
                    limits: tas.map([{ 
                        key: tas.nat('42'), 
                        value: tas.nat('42'),
                    }]),
                    useInternalBalance: true,
                    userData: {
                        allT: tas.nat('42'),
                        amountsIn: tas.map([{ 
                            key: tas.nat('42'), 
                            value: tas.nat('42'),
                        }]),
                        kind: 'VALUE',
                        minSPTAmountOut: tas.nat('42'),
                        sptAmountOut: tas.nat('42'),
                        tokenIndex: tas.nat('42'),
                    },
                },
                sender: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
            }).send();
        await joinPoolRequest.confirmation(3);
        
        const storageValueAfter = await getStorageValue();

        expect(storageValueAfter.toString()).toBe('');
    });
});
