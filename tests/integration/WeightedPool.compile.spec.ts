
import { TezosToolkit } from '@taquito/taquito';
import { char2Bytes } from '@taquito/utils';
import { tas } from '../types/type-aliases';
import { InMemorySigner, importKey } from '@taquito/signer';
import { WeightedPoolCompileContractType as ContractType } from '../types/WeightedPool.compile.types';
import { WeightedPoolCompileCode as ContractCode } from '../types/WeightedPool.compile.code';

jest.setTimeout(20000)

describe('WeightedPool.compile', () => {
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
                        balances: tas.bigMap([{ 
                            key: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'), 
                            value: {
                            approvals: tas.map([{ 
                                key: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'), 
                                value: tas.nat('42'),
                            }]),
                            balance: tas.nat('42'),
                        },
                        }]),
                        entries: tas.bigMap({ 
                            'VALUE': tas.nat('42'),
                        }),
                        exemptFromYieldFees: true,
                        feeCache: {
                            aumFee: tas.nat('42'),
                            swapFee: tas.nat('42'),
                            yieldFee: tas.nat('42'),
                        },
                        fixedPoint: tas.bigMap({ 
                            'VALUE': tas.lambda([]),
                        }),
                        getTokenValue: tas.lambda([]),
                        initialized: true,
                        metadata: tas.bigMap({ 
                            'VALUE': tas.bytes(char2Bytes('DATA')),
                        }),
                        normalizedWeights: tas.map([{ 
                            key: tas.nat('42'), 
                            value: tas.nat('42'),
                        }]),
                        poolId: tas.bytes(char2Bytes('DATA')),
                        protocolFeesCollector: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                        rateProviders: tas.map([{ 
                            key: tas.nat('42'), 
                            value: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                        }]),
                        scalingFactors: tas.map([{ 
                            key: tas.nat('42'), 
                            value: tas.nat('42'),
                        }]),
                        token_metadata: tas.bigMap([{ 
                            key: tas.nat('42'), 
                            value: {
                            token_id: tas.nat('42'),
                            token_info: tas.map({ 
                                'VALUE': tas.bytes(char2Bytes('DATA')),
                            }),
                        },
                        }]),
                        tokens: tas.map([{ 
                            key: tas.nat('42'), 
                            value: {
                            FA2: true,
                            address: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                            id: tas.nat('42'),
                        },
                        }]),
                        totalSupply: tas.nat('42'),
                        vault: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                        weightedMathLib: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                        18: tas.bigMap([{ 
                            key: tas.nat('42'), 
                            value: tas.lambda([]),
                        }]),
                    },
            });
            const newContractResult = await newContractOrigination.contract();
            const newContractAddress = newContractResult.address;
            contract = await Tezos.contract.at<ContractType>(newContractAddress);
            
    });


    it('should call initialize', async () => {
        
        const getStorageValue = async () => {
            const storage = await contract.storage();
            const value = storage;
            return value;
        };

        const storageValueBefore = await getStorageValue();
        
        const initializeRequest = await contract.methodsObject.initialize({
                normalizedWeights: tas.map([{ 
                    key: tas.nat('42'), 
                    value: tas.nat('42'),
                }]),
                rateProviders: tas.map([{ 
                    key: tas.nat('42'), 
                    value: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                }]),
                swapFeePercentage: tas.nat('42'),
                tokenDecimals: tas.map([{ 
                    key: tas.nat('42'), 
                    value: tas.nat('42'),
                }]),
                tokens: tas.map([{ 
                    key: tas.nat('42'), 
                    value: {
                    FA2: true,
                    address: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                    id: tas.nat('42'),
                },
                }]),
            }).send();
        await initializeRequest.confirmation(3);
        
        const storageValueAfter = await getStorageValue();

        expect(storageValueAfter.toString()).toBe('');
    });

    it('should call approve', async () => {
        
        const getStorageValue = async () => {
            const storage = await contract.storage();
            const value = storage;
            return value;
        };

        const storageValueBefore = await getStorageValue();
        
        const approveRequest = await contract.methodsObject.approve({
                spender: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                value: tas.nat('42'),
            }).send();
        await approveRequest.confirmation(3);
        
        const storageValueAfter = await getStorageValue();

        expect(storageValueAfter.toString()).toBe('');
    });

    it('should call onExitPool', async () => {
        
        const getStorageValue = async () => {
            const storage = await contract.storage();
            const value = storage;
            return value;
        };

        const storageValueBefore = await getStorageValue();
        
        const onExitPoolRequest = await contract.methodsObject.onExitPool({
                balances: tas.map([{ 
                    key: tas.nat('42'), 
                    value: tas.nat('42'),
                }]),
                sender: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
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
            }).send();
        await onExitPoolRequest.confirmation(3);
        
        const storageValueAfter = await getStorageValue();

        expect(storageValueAfter.toString()).toBe('');
    });

    it('should call onJoinPool', async () => {
        
        const getStorageValue = async () => {
            const storage = await contract.storage();
            const value = storage;
            return value;
        };

        const storageValueBefore = await getStorageValue();
        
        const onJoinPoolRequest = await contract.methodsObject.onJoinPool({
                balances: tas.map([{ 
                    key: tas.nat('42'), 
                    value: tas.nat('42'),
                }]),
                recipient: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
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
            }).send();
        await onJoinPoolRequest.confirmation(3);
        
        const storageValueAfter = await getStorageValue();

        expect(storageValueAfter.toString()).toBe('');
    });

    it('should call transfer', async () => {
        
        const getStorageValue = async () => {
            const storage = await contract.storage();
            const value = storage;
            return value;
        };

        const storageValueBefore = await getStorageValue();
        
        const transferRequest = await contract.methodsObject.transfer({
                from: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                to: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                value: tas.nat('42'),
            }).send();
        await transferRequest.confirmation(3);
        
        const storageValueAfter = await getStorageValue();

        expect(storageValueAfter.toString()).toBe('');
    });
});
