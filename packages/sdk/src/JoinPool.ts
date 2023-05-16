import { InMemorySigner } from "@taquito/signer";
import { TezosToolkit } from "@taquito/taquito";
import { tas } from "../../../types/type-aliases";
import { VaultContractType as ContractType } from "../../../types/Vault.types";

const config = require("../../../.taq/config.local.testing.json");

const Tezos = new TezosToolkit("https://ghostnet.ecadinfra.com");

const tokenAddress = "KT1JA3UQ6R4C84mH3FqS3G5mKFeEdLumrDc3";

InMemorySigner.fromSecretKey(config.accounts.taqOperatorAccount.privateKey)
  .then((theSigner) => {
    Tezos.setProvider({ signer: theSigner });
  })
  .then(async () => {
    const contract = await Tezos.contract.at<ContractType>(
      config.contracts.Vault.address
    );
    const joinPoolRequest = await contract.methodsObject
      .joinPool({
        poolId: {
          0: tas.address("KT1ADiYeVqgr4xmVpcBatTQG3eopRRNGZj8k"),
          1: tas.nat("1"),
        },
        recipient: tas.address("tz1UGWQQ5YFkZqWgE3gqmPyuwy2R5VGpMM9B"),
        request: {
          assets: tas.map([
            {
              key: tas.nat("0"),
              value: {
                0: tas.address(tokenAddress),
                1: tas.nat("0"),
              },
            },
            {
              key: tas.nat("1"),
              value: {
                0: tas.address(tokenAddress),
                1: tas.nat("1"),
              },
            },
            {
              key: tas.nat("2"),
              value: {
                0: tas.address(tokenAddress),
                1: tas.nat("2"),
              },
            },
            {
              key: tas.nat("3"),
              value: {
                0: tas.address(tokenAddress),
                1: tas.nat("3"),
              },
            },
            {
              key: tas.nat("4"),
              value: {
                0: tas.address(tokenAddress),
                1: tas.nat("4"),
              },
            },
            {
              key: tas.nat("5"),
              value: {
                0: tas.address(tokenAddress),
                1: tas.nat("5"),
              },
            },
            {
              key: tas.nat("6"),
              value: {
                0: tas.address(tokenAddress),
                1: tas.nat("6"),
              },
            },
            {
              key: tas.nat("7"),
              value: {
                0: tas.address(tokenAddress),
                1: tas.nat("7"),
              },
            },
          ]),
          limits: tas.map([
            {
              key: tas.nat("0"),
              value: tas.nat(200 * 10 ** 18),
            },
            {
              key: tas.nat("1"),
              value: tas.nat(200 * 10 ** 18),
            },
            {
              key: tas.nat("2"),
              value: tas.nat(200 * 10 ** 18),
            },
            {
              key: tas.nat("3"),
              value: tas.nat(200 * 10 ** 18),
            },
            {
              key: tas.nat("4"),
              value: tas.nat(200 * 10 ** 18),
            },
            {
              key: tas.nat("5"),
              value: tas.nat(200 * 10 ** 18),
            },
            {
              key: tas.nat("6"),
              value: tas.nat(200 * 10 ** 18),
            },
            {
              key: tas.nat("7"),
              value: tas.nat(200 * 10 ** 18),
            },
          ]),
          userData: {
            allT: undefined,
            amountsIn: tas.map([
              {
                key: tas.nat("0"),
                value: tas.nat(200 * 10 ** 18),
              },
              {
                key: tas.nat("1"),
                value: tas.nat(200 * 10 ** 18),
              },
              {
                key: tas.nat("2"),
                value: tas.nat(200 * 10 ** 18),
              },
              {
                key: tas.nat("3"),
                value: tas.nat(200 * 10 ** 18),
              },
              {
                key: tas.nat("4"),
                value: tas.nat(200 * 10 ** 18),
              },
              {
                key: tas.nat("5"),
                value: tas.nat(200 * 10 ** 18),
              },
              {
                key: tas.nat("6"),
                value: tas.nat(200 * 10 ** 18),
              },
              {
                key: tas.nat("7"),
                value: tas.nat(200 * 10 ** 18),
              },
            ]),
            kind: "INIT",
            minSPTAmountOut: undefined,
            sptAmountOut: undefined,
            tokenIndex: undefined,
          },
        },
        sender: tas.address("tz1UGWQQ5YFkZqWgE3gqmPyuwy2R5VGpMM9B"),
      })
      .send();
    await joinPoolRequest.confirmation(1);
  })
  .catch((error) => console.table(`Error: ${JSON.stringify(error, null, 2)}`));

try {
  const sub = Tezos.stream.subscribeEvent({
    tag: "PoolBalanceChanged",
    address: config.contracts.Vault.address,
  });

  // rome-ignore lint/suspicious/noExplicitAny: <explanation>
  // function getAddressFromEvent(data: any) {
  //   console.log("pool address: ", encodePubKey(data.payload.bytes));
  //   sub.close();
  // }

  sub.on("data", console.log);
} catch (e) {
  console.log(e);
}
