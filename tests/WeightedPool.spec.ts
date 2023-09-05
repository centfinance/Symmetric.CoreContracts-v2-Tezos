import { TezosToolkit } from "@taquito/taquito";
import { char2Bytes } from "@taquito/utils";
import { tas } from "./types/type-aliases";
import { InMemorySigner, importKey } from "@taquito/signer";
import { WeightedPoolContractType as ContractType } from "./types/WeightedPool.types";
import { WeightedPoolCode as ContractCode } from "./types/WeightedPool.code";

jest.setTimeout(20000);

describe("WeightedPool", () => {
  const config = require("../.taq/config.json");
  const Tezos = new TezosToolkit(config.sandbox.local.rpcUrl);
  const key = config.sandbox.local.accounts.bob.secretKey.replace(
    "unencrypted:",
    ""
  );
  Tezos.setProvider({
    signer: new InMemorySigner(key),
  });
  let contract: ContractType = undefined as unknown as ContractType;
  beforeAll(async () => {
    const newContractOrigination = await Tezos.contract.originate<ContractType>(
      {
        code: ContractCode.code,
        storage: {
          admin: tas.address("tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456"),
          balances: tas.bigMap([
            {
              key: tas.address("tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456"),
              value: {
                approvals: tas.map([
                  {
                    key: tas.address("tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456"),
                    value: tas.nat("42"),
                  },
                ]),
                balance: tas.nat("42"),
              },
            },
          ]),
          entries: tas.bigMap({
            VALUE: tas.nat("42"),
          }),
          exemptFromYieldFees: true,
          feeCache: {
            0: tas.nat("42"),
            1: tas.nat("42"),
          },
          fixedPoint: tas.bigMap({
            VALUE: tas.lambda([]),
          }),
          getTokenValue: tas.lambda([]),
          initialized: true,
          metadata: tas.bigMap({
            VALUE: tas.bytes(char2Bytes("DATA")),
          }),
          normalizedWeights: tas.map([
            {
              key: tas.nat("42"),
              value: tas.nat("42"),
            },
          ]),
          poolId: {
            0: tas.address("tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456"),
            1: tas.nat("42"),
          },
          proposed_admin: tas.address("tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456"),
          protocolFeesCollector: tas.address(
            "tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456"
          ),
          rateProviders: tas.map([
            {
              key: tas.nat("42"),
              value: tas.address("tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456"),
            },
          ]),
          recoveryMode: true,
          scalingFactors: tas.map([
            {
              key: tas.nat("42"),
              value: tas.nat("42"),
            },
          ]),
          scaling_helpers: tas.bigMap({
            VALUE: tas.lambda([]),
          }),
          settings: true,
          token_metadata: tas.bigMap([
            {
              key: tas.nat("42"),
              value: {
                token_id: tas.nat("42"),
                token_info: tas.map({
                  VALUE: tas.bytes(char2Bytes("DATA")),
                }),
              },
            },
          ]),
          tokens: tas.map([
            {
              key: tas.nat("42"),
              value: {
                0: tas.address("tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456"),
                1: tas.nat("42"),
              },
            },
          ]),
          totalSupply: tas.nat("42"),
          vault: tas.address("tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456"),
          weightedMathLib: tas.address("tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456"),
          weightedProtocolFeesLib: tas.address(
            "tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456"
          ),
        },
      }
    );
    const newContractResult = await newContractOrigination.contract();
    const newContractAddress = newContractResult.address;
    contract = await Tezos.contract.at<ContractType>(newContractAddress);
  });

  it("should call accept_admin", async () => {
    const getStorageValue = async () => {
      const storage = await contract.storage();
      const value = storage;
      return value;
    };

    const storageValueBefore = await getStorageValue();

    const accept_adminRequest = await contract.methodsObject
      .accept_admin()
      .send();
    await accept_adminRequest.confirmation(3);

    const storageValueAfter = await getStorageValue();

    expect(storageValueAfter.toString()).toBe("");
  });

  it("should call afterExitPool", async () => {
    const getStorageValue = async () => {
      const storage = await contract.storage();
      const value = storage;
      return value;
    };

    const storageValueBefore = await getStorageValue();

    const afterExitPoolRequest = await contract.methodsObject
      .afterExitPool({
        amountsOut: tas.map([
          {
            key: tas.nat("42"),
            value: tas.nat("42"),
          },
        ]),
        balances: tas.map([
          {
            key: tas.nat("42"),
            value: tas.nat("42"),
          },
        ]),
        invariant: tas.nat("42"),
        poolId: {
          0: tas.address("tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456"),
          1: tas.nat("42"),
        },
        recoveryModeExit: true,
        sender: tas.address("tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456"),
        sptAmountIn: tas.nat("42"),
      })
      .send();
    await afterExitPoolRequest.confirmation(3);

    const storageValueAfter = await getStorageValue();

    expect(storageValueAfter.toString()).toBe("");
  });

  it("should call afterJoinPool", async () => {
    const getStorageValue = async () => {
      const storage = await contract.storage();
      const value = storage;
      return value;
    };

    const storageValueBefore = await getStorageValue();

    const afterJoinPoolRequest = await contract.methodsObject
      .afterJoinPool({
        amountsIn: tas.map([
          {
            key: tas.nat("42"),
            value: tas.nat("42"),
          },
        ]),
        balances: tas.map([
          {
            key: tas.nat("42"),
            value: tas.nat("42"),
          },
        ]),
        invariant: tas.nat("42"),
        poolId: {
          0: tas.address("tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456"),
          1: tas.nat("42"),
        },
        recipient: tas.address("tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456"),
        sptAmountOut: tas.nat("42"),
      })
      .send();
    await afterJoinPoolRequest.confirmation(3);

    const storageValueAfter = await getStorageValue();

    expect(storageValueAfter.toString()).toBe("");
  });

  it("should call approve", async () => {
    const getStorageValue = async () => {
      const storage = await contract.storage();
      const value = storage;
      return value;
    };

    const storageValueBefore = await getStorageValue();

    const approveRequest = await contract.methodsObject
      .approve({
        spender: tas.address("tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456"),
        value: tas.nat("42"),
      })
      .send();
    await approveRequest.confirmation(3);

    const storageValueAfter = await getStorageValue();

    expect(storageValueAfter.toString()).toBe("");
  });

  it("should call initializePool", async () => {
    const getStorageValue = async () => {
      const storage = await contract.storage();
      const value = storage;
      return value;
    };

    const storageValueBefore = await getStorageValue();

    const initializePoolRequest = await contract.methodsObject
      .initializePool()
      .send();
    await initializePoolRequest.confirmation(3);

    const storageValueAfter = await getStorageValue();

    expect(storageValueAfter.toString()).toBe("");
  });

  it("should call set_paused", async () => {
    const getStorageValue = async () => {
      const storage = await contract.storage();
      const value = storage;
      return value;
    };

    const storageValueBefore = await getStorageValue();

    const set_pausedRequest = await contract.methodsObject
      .set_paused(true)
      .send();
    await set_pausedRequest.confirmation(3);

    const storageValueAfter = await getStorageValue();

    expect(storageValueAfter.toString()).toBe("");
  });

  it("should call transfer", async () => {
    const getStorageValue = async () => {
      const storage = await contract.storage();
      const value = storage;
      return value;
    };

    const storageValueBefore = await getStorageValue();

    const transferRequest = await contract.methodsObject
      .transfer({
        from: tas.address("tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456"),
        to: tas.address("tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456"),
        value: tas.nat("42"),
      })
      .send();
    await transferRequest.confirmation(3);

    const storageValueAfter = await getStorageValue();

    expect(storageValueAfter.toString()).toBe("");
  });

  it("should call transfer_admin", async () => {
    const getStorageValue = async () => {
      const storage = await contract.storage();
      const value = storage;
      return value;
    };

    const storageValueBefore = await getStorageValue();

    const transfer_adminRequest = await contract.methodsObject
      .transfer_admin(tas.address("tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456"))
      .send();
    await transfer_adminRequest.confirmation(3);

    const storageValueAfter = await getStorageValue();

    expect(storageValueAfter.toString()).toBe("");
  });

  it("should call updateProtocolFeePercentageCache", async () => {
    const getStorageValue = async () => {
      const storage = await contract.storage();
      const value = storage;
      return value;
    };

    const storageValueBefore = await getStorageValue();

    const updateProtocolFeePercentageCacheRequest = await contract.methodsObject
      .updateProtocolFeePercentageCache()
      .send();
    await updateProtocolFeePercentageCacheRequest.confirmation(3);

    const storageValueAfter = await getStorageValue();

    expect(storageValueAfter.toString()).toBe("");
  });
});
