
import { TezosToolkit } from '@taquito/taquito';
import { char2Bytes } from '@taquito/utils';
import { tas } from '../types/type-aliases';
import { InMemorySigner, importKey } from '@taquito/signer';
import { WeightedPoolFactoryCompileContractType as ContractType } from '../types/WeightedPoolFactory.compile.types';
import { WeightedPoolFactoryCompileCode as ContractCode } from '../types/WeightedPoolFactory.compile.code';

jest.setTimeout(20000)

describe('WeightedPoolFactory.compile', () => {
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
                        fixedPoint: tas.bigMap({ 
                            'VALUE': tas.lambda([]),
                        }),
                        isPoolFromFactory: tas.bigMap([{ 
                            key: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'), 
                            value: tas.unit(),
                        }]),
                        protocolFeeProvider: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                        vault: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                        weightedMathLib: tas.address('tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456'),
                    },
            });
            const newContractResult = await newContractOrigination.contract();
            const newContractAddress = newContractResult.address;
            contract = await Tezos.contract.at<ContractType>(newContractAddress);
            
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
                token_metadata: tas.map({ 
                    'VALUE': tas.bytes(char2Bytes('DATA')),
                }),
            }).send();
        await createRequest.confirmation(3);
        
        const storageValueAfter = await getStorageValue();

        expect(storageValueAfter.toString()).toBe('');
    });
});
