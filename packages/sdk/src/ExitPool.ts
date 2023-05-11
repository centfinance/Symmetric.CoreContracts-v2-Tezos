import { InMemorySigner } from "@taquito/signer";
import { TezosToolkit } from "@taquito/taquito";
import { tas } from "../../../types/type-aliases";
import { VaultContractType as ContractType } from "../../../types/Vault.types";

const config = require("../../../.taq/config.local.development.json");

const Tezos = new TezosToolkit(config.rpcUrl);

const poolAddress = "KT1ELPXpfFSpk1AJVQ9m8t5uudGvVrvCgVHU";

const tokenAddress = "KT1HV453GKwd6M2PKkxHy7Tnajdorisv268q";

InMemorySigner.fromSecretKey(config.accounts.bob.secretKey.slice(12))
  .then((theSigner) => {
    Tezos.setProvider({ signer: theSigner });
  })
  .then(async () => {
    const contract = await Tezos.contract.at<ContractType>(
      config.contracts.Vault.address
    );
    const exitPoolRequest = await contract.methodsObject
      .exitPool({
        poolId: {
          0: tas.address(poolAddress),
          1: tas.nat(1),
        },
        recipient: tas.address("tz1aSkwEot3L2kmUvcoxzjMomb9mvBNuzFK6"),
        request: {
          assets: tas.map([
            {
              key: tas.nat("0"),
              value: {
                0: tas.address(tokenAddress),
                1: tas.nat("1"),
              },
            },
            {
              key: tas.nat("1"),
              value: {
                0: tas.address(tokenAddress),
                1: tas.nat("2"),
              },
            },
            {
              key: tas.nat("2"),
              value: {
                0: tas.address(tokenAddress),
                1: tas.nat("3"),
              },
            },
            {
              key: tas.nat("3"),
              value: {
                0: tas.address(tokenAddress),
                1: tas.nat("4"),
              },
            },
            {
              key: tas.nat("4"),
              value: {
                0: tas.address(tokenAddress),
                1: tas.nat("5"),
              },
            },
            {
              key: tas.nat("5"),
              value: {
                0: tas.address(tokenAddress),
                1: tas.nat("6"),
              },
            },
            {
              key: tas.nat("6"),
              value: {
                0: tas.address(tokenAddress),
                1: tas.nat("7"),
              },
            },
            {
              key: tas.nat("7"),
              value: {
                0: tas.address(tokenAddress),
                1: tas.nat("8"),
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
          useInternalBalance: false,
          userData: {
            amountsOut: tas.map([
              {
                key: tas.nat("0"),
                value: tas.nat(20 * 10 ** 18),
              },
              {
                key: tas.nat("1"),
                value: tas.nat(20 * 10 ** 18),
              },
              {
                key: tas.nat("2"),
                value: tas.nat(20 * 10 ** 18),
              },
              {
                key: tas.nat("3"),
                value: tas.nat(20 * 10 ** 18),
              },
              {
                key: tas.nat("4"),
                value: tas.nat(20 * 10 ** 18),
              },
              {
                key: tas.nat("5"),
                value: tas.nat(20 * 10 ** 18),
              },
              {
                key: tas.nat("6"),
                value: tas.nat(20 * 10 ** 18),
              },
              {
                key: tas.nat("7"),
                value: tas.nat(20 * 10 ** 18),
              },
            ]),
            maxSPTAmountIn: tas.nat("0"),
            kind: "SPT_IN_FOR_EXACT_TOKENS_OUT",
            recoveryModeExit: false,
          },
        },
        sender: tas.address("tz1aSkwEot3L2kmUvcoxzjMomb9mvBNuzFK6"),
      })
      .send();
    // const estimate = await Tezos.estimate.transfer(exitPoolRequest);
    // console.log(estimate);
    await exitPoolRequest.confirmation(1);
  })
  .catch((error) => console.table(`Error: ${JSON.stringify(error, null, 2)}`));
