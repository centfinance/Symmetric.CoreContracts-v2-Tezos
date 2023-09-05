import { TezosToolkit } from "@taquito/taquito";
import { char2Bytes } from "@taquito/utils";
import { tas } from "./types/type-aliases";
import { InMemorySigner, importKey } from "@taquito/signer";
import { WeightedPoolFactoryNoAdminContractType as ContractType } from "./types/WeightedPoolFactoryNoAdmin.types";
import { WeightedPoolFactoryNoAdminCode as ContractCode } from "./types/WeightedPoolFactoryNoAdmin.code";

const config = require("../.taq/config.json");
const Tezos = new TezosToolkit(config.sandbox.local.rpcUrl);
const key = config.sandbox.local.accounts.bob.secretKey.replace(
  "unencrypted:",
  ""
);
Tezos.setProvider({
  signer: new InMemorySigner(key),
});
export async function factoryOrigination() {
  const newContractOrigination = await Tezos.contract.originate<ContractType>({
    code: ContractCode.code,
    storage: {
      admin: tas.address(config.sandbox.local.accounts.bob),
      feeCache: {
        0: tas.nat("400000000000000000"),
        1: tas.nat("400000000000000000"),
      },
      isPoolFromFactory: tas.bigMap([]),
      lastPool: tas.address("tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456"),
      metadata: tas.bigMap({
        VALUE: tas.bytes(char2Bytes("DATA")),
      }),
      protocolFeeProvider: tas.address("tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456"),
      vault: tas.address("tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456"),
      weightedMathLib: tas.address("tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456"),
      weightedProtocolFeesLib: tas.address(
        "tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456"
      ),
    },
  });
  const newContractResult = await newContractOrigination.contract();
  const newContractAddress = newContractResult.address;
  const contract = await Tezos.contract.at<ContractType>(newContractAddress);
  return contract;
}
jest.setTimeout(20000);

describe("WeightedPoolFactoryNoAdmin", () => {
  let contract: ContractType = undefined as unknown as ContractType;
  beforeAll(async () => {
    contract = await factoryOrigination();
  });

  it("should call create", async () => {
    const getStorageValue = async () => {
      const storage = await contract.storage();
      const value = storage;
      return value;
    };

    const storageValueBefore = await getStorageValue();

    const createRequest = await contract.methodsObject
      .create({
        metadata: tas.bytes(char2Bytes("DATA")),
        normalizedWeights: tas.map([
          {
            key: tas.nat("0"),
            value: tas.nat("500000000000000000"),
          },
          {
            key: tas.nat("1"),
            value: tas.nat("500000000000000000"),
          },
        ]),
        rateProviders: tas.map([
          {
            key: tas.nat("42"),
            value: tas.address("tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456"),
          },
        ]),
        swapFeePercentage: tas.nat("42"),
        tokenDecimals: tas.map([
          {
            key: tas.nat("42"),
            value: tas.nat("42"),
          },
        ]),
        token_metadata: tas.map({
          VALUE: tas.bytes(char2Bytes("DATA")),
        }),
        tokens: tas.map([
          {
            key: tas.nat("42"),
            value: {
              0: tas.address("tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456"),
              1: tas.nat("42"),
            },
          },
        ]),
      })
      .send();
    await createRequest.confirmation(3);

    const storageValueAfter = await getStorageValue();

    expect(storageValueAfter.toString()).toBe("");
  });

  it("should call initialize", async () => {
    const getStorageValue = async () => {
      const storage = await contract.storage();
      const value = storage;
      return value;
    };

    const storageValueBefore = await getStorageValue();

    const initializeRequest = await contract.methodsObject.initialize().send();
    await initializeRequest.confirmation(3);

    const storageValueAfter = await getStorageValue();

    expect(storageValueAfter.toString()).toBe("");
  });
});
