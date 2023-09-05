
import { TezosToolkit } from '@taquito/taquito';
import { char2Bytes } from '@taquito/utils';
import { tas } from './types/type-aliases';
import { InMemorySigner, importKey } from '@taquito/signer';
import { WeightedPoolFactoryContractType as ContractType } from './types/WeightedPoolFactory.types';
import { WeightedPoolFactoryCode as ContractCode } from './types/WeightedPoolFactory.code';

jest.setTimeout(20000)

describe('WeightedPoolFactory', () => {
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
                        admin: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                        feeCache: {
                            0: tas.nat('42'),
                            1: tas.nat('42'),
                        },
                        isPoolFromFactory: tas.bigMap([{ 
                            key: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'), 
                            value: tas.unit(),
                        }]),
                        lastPool: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                        metadata: tas.bigMap({ 
                            'VALUE': tas.bytes(char2Bytes('DATA')),
                        }),
                        proposed_admin: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                        protocolFeeProvider: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                        vault: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                        weightedMathLib: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                        weightedProtocolFeesLib: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                    },
            });
            const newContractResult = await newContractOrigination.contract();
            const newContractAddress = newContractResult.address;
            contract = await Tezos.contract.at<ContractType>(newContractAddress);
            
    });


    it('should call accept_admin', async () => {
        
        const getStorageValue = async () => {
            const storage = await contract.storage();
            const value = storage;
            return value;
        };

        const storageValueBefore = await getStorageValue();
        
        const accept_adminRequest = await contract.methodsObject.accept_admin().send();
        await accept_adminRequest.confirmation(3);
        
        const storageValueAfter = await getStorageValue();

        expect(storageValueAfter.toString()).toBe('');
    });

    it('should call create', async () => {
        
        const getStorageValue = async () => {
            const storage = await contract.storage();
            const value = storage;
            return value;
        };

        const storageValueBefore = await getStorageValue();
        
        const createRequest = await contract.methodsObject.create({
                metadata: tas.bytes(char2Bytes('DATA')),
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
                token_metadata: tas.map({ 
                    'VALUE': tas.bytes(char2Bytes('DATA')),
                }),
                tokens: tas.map([{ 
                    key: tas.nat('42'), 
                    value: {
                    0: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                    1: tas.nat('42'),
                },
                }]),
            }).send();
        await createRequest.confirmation(3);
        
        const storageValueAfter = await getStorageValue();

        expect(storageValueAfter.toString()).toBe('');
    });

    it('should call initialize', async () => {
        
        const getStorageValue = async () => {
            const storage = await contract.storage();
            const value = storage;
            return value;
        };

        const storageValueBefore = await getStorageValue();
        
        const initializeRequest = await contract.methodsObject.initialize().send();
        await initializeRequest.confirmation(3);
        
        const storageValueAfter = await getStorageValue();

        expect(storageValueAfter.toString()).toBe('');
    });

    it('should call transfer_admin', async () => {
        
        const getStorageValue = async () => {
            const storage = await contract.storage();
            const value = storage;
            return value;
        };

        const storageValueBefore = await getStorageValue();
        
        const transfer_adminRequest = await contract.methodsObject.transfer_admin(tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456')).send();
        await transfer_adminRequest.confirmation(3);
        
        const storageValueAfter = await getStorageValue();

        expect(storageValueAfter.toString()).toBe('');
    });
});
