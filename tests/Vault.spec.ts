import { TezosToolkit } from "@taquito/taquito";
import { char2Bytes } from "@taquito/utils";
import { tas } from "./types/type-aliases";
import { InMemorySigner, importKey } from "@taquito/signer";
import { VaultContractType as ContractType } from "./types/Vault.types";
import { VaultCode as ContractCode } from "./types/Vault.code";

const config = require("../.taq/config.json");
const Tezos = new TezosToolkit(config.sandbox.local.rpcUrl);
const key = config.sandbox.local.accounts.bob.secretKey.replace(
  "unencrypted:",
  ""
);
Tezos.setProvider({
  signer: new InMemorySigner(key),
});

export async function vaultOrigination() {
  const newContractOrigination = await Tezos.contract.originate<ContractType>({
    code: ContractCode.code,
    storage: {
      admin: tas.address("tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456"),
      isPoolRegistered: tas.bigMap([]),
      metadata: tas.bigMap({
        VALUE: tas.bytes(char2Bytes("DATA")),
      }),
      nextPoolNonce: tas.nat("1"),
      poolsBalances: tas.bigMap([]),
      poolsTokens: tas.bigMap([]),
      proposed_admin: tas.address("tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456"),
      settings: true,
    },
  });
  const newContractResult = await newContractOrigination.contract();
  const newContractAddress = newContractResult.address;
  const contract = await Tezos.contract.at<ContractType>(newContractAddress);
  return contract;
}

jest.setTimeout(20000);

describe("Vault", () => {
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
    const vault = await vaultOrigination();
    contract = vault;
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

  it("should call batchSwap", async () => {
    const getStorageValue = async () => {
      const storage = await contract.storage();
      const value = storage;
      return value;
    };

    const storageValueBefore = await getStorageValue();

    const batchSwapRequest = await contract.methodsObject
      .batchSwap({
        assets: tas.map([
          {
            key: tas.nat("42"),
            value: {
              0: tas.address("tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456"),
              1: tas.nat("42"),
            },
          },
        ]),
        deadline: tas.timestamp(new Date()),
        funds: {
          recipient: tas.address("tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456"),
          sender: tas.address("tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456"),
        },
        kind: tas.nat("42"),
        limits: tas.map([
          {
            key: tas.nat("42"),
            value: tas.int("42"),
          },
        ]),
        swaps: tas.map([
          {
            key: tas.nat("42"),
            value: {
              amount: tas.nat("42"),
              assetInIndex: tas.nat("42"),
              assetOutIndex: tas.nat("42"),
              poolId: {
                0: tas.address("tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456"),
                1: tas.nat("42"),
              },
            },
          },
        ]),
      })
      .send();
    await batchSwapRequest.confirmation(3);

    const storageValueAfter = await getStorageValue();

    expect(storageValueAfter.toString()).toBe("");
  });

  it("should call exitPool", async () => {
    const getStorageValue = async () => {
      const storage = await contract.storage();
      const value = storage;
      return value;
    };

    const storageValueBefore = await getStorageValue();

    const exitPoolRequest = await contract.methodsObject
      .exitPool({
        poolId: {
          0: tas.address("tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456"),
          1: tas.nat("42"),
        },
        recipient: tas.address("tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456"),
        request: {
          assets: tas.map([
            {
              key: tas.nat("42"),
              value: {
                0: tas.address("tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456"),
                1: tas.nat("42"),
              },
            },
          ]),
          limits: tas.map([
            {
              key: tas.nat("42"),
              value: tas.nat("42"),
            },
          ]),
          userData: {
            amountsOut: tas.map([
              {
                key: tas.nat("42"),
                value: tas.nat("42"),
              },
            ]),
            kind: tas.nat("42"),
            maxSPTAmountIn: tas.nat("42"),
            recoveryModeExit: true,
            sptAmountIn: tas.nat("42"),
            tokenIndex: tas.nat("42"),
          },
        },
        sender: tas.address("tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456"),
      })
      .send();
    await exitPoolRequest.confirmation(3);

    const storageValueAfter = await getStorageValue();

    expect(storageValueAfter.toString()).toBe("");
  });

  it("should call joinPool", async () => {
    const getStorageValue = async () => {
      const storage = await contract.storage();
      const value = storage;
      return value;
    };

    const storageValueBefore = await getStorageValue();

    const joinPoolRequest = await contract.methodsObject
      .joinPool({
        poolId: {
          0: tas.address("tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456"),
          1: tas.nat("42"),
        },
        recipient: tas.address("tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456"),
        request: {
          assets: tas.map([
            {
              key: tas.nat("42"),
              value: {
                0: tas.address("tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456"),
                1: tas.nat("42"),
              },
            },
          ]),
          limits: tas.map([
            {
              key: tas.nat("42"),
              value: tas.nat("42"),
            },
          ]),
          userData: {
            allT: tas.nat("42"),
            amountsIn: tas.map([
              {
                key: tas.nat("42"),
                value: tas.nat("42"),
              },
            ]),
            kind: tas.nat("42"),
            minSPTAmountOut: tas.nat("42"),
            sptAmountOut: tas.nat("42"),
            tokenIndex: tas.nat("42"),
          },
        },
        sender: tas.address("tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456"),
      })
      .send();
    await joinPoolRequest.confirmation(3);

    const storageValueAfter = await getStorageValue();

    expect(storageValueAfter.toString()).toBe("");
  });

  it("should call registerPool", async () => {
    const getStorageValue = async () => {
      const storage = await contract.storage();
      const value = storage;
      return value;
    };

    const storageValueBefore = await getStorageValue();

    const registerPoolRequest = await contract.methodsObject
      .registerPool()
      .send();
    await registerPoolRequest.confirmation(3);

    const storageValueAfter = await getStorageValue();

    expect(storageValueAfter.toString()).toBe("");
  });

  it("should call registerTokens", async () => {
    const getStorageValue = async () => {
      const storage = await contract.storage();
      const value = storage;
      return value;
    };

    const storageValueBefore = await getStorageValue();

    const registerTokensRequest = await contract.methodsObject
      .registerTokens({
        assetManagers: tas.map([
          {
            key: tas.nat("42"),
            value: tas.address("tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456"),
          },
        ]),
        poolId: {
          0: tas.address("tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456"),
          1: tas.nat("42"),
        },
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
    await registerTokensRequest.confirmation(3);

    const storageValueAfter = await getStorageValue();

    expect(storageValueAfter.toString()).toBe("");
  });

  // it("should call run_lambda", async () => {
  //   const getStorageValue = async () => {
  //     const storage = await contract.storage();
  //     const value = storage;
  //     return value;
  //   };

  //   const storageValueBefore = await getStorageValue();

  //   const run_lambdaRequest = await contract.methodsObject
  //     .run_lambda(tas.lambda([]))
  //     .send();
  //   await run_lambdaRequest.confirmation(3);

  //   const storageValueAfter = await getStorageValue();

  //   expect(storageValueAfter.toString()).toBe("");
  // });

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

  it("should call swap", async () => {
    const getStorageValue = async () => {
      const storage = await contract.storage();
      const value = storage;
      return value;
    };

    const storageValueBefore = await getStorageValue();

    const swapRequest = await contract.methodsObject
      .swap({
        deadline: tas.timestamp(new Date()),
        funds: {
          recipient: tas.address("tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456"),
          sender: tas.address("tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456"),
        },
        limit: tas.nat("42"),
        singleSwap: {
          amount: tas.nat("42"),
          assetIn: {
            0: tas.address("tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456"),
            1: tas.nat("42"),
          },
          assetOut: {
            0: tas.address("tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456"),
            1: tas.nat("42"),
          },
          kind: tas.nat("42"),
          poolId: {
            0: tas.address("tz1ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456"),
            1: tas.nat("42"),
          },
        },
      })
      .send();
    await swapRequest.confirmation(3);

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
});
