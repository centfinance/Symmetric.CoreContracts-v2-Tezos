import { InMemorySigner } from "@taquito/signer";
import { TezosToolkit } from "@taquito/taquito";
import { tas } from "../../../types/type-aliases";
import { VaultContractType as ContractType } from "../../../types/Vault.types";

const Tezos = new TezosToolkit("https://ghostnet.smartpy.io");

const config = require("../../../.taq/config.local.testing.json");

const tokenAddress = "KT1JA3UQ6R4C84mH3FqS3G5mKFeEdLumrDc3";

InMemorySigner.fromSecretKey(config.accounts.taqOperatorAccount.privateKey)
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
          0: tas.address("KT1VHbP2ska1R5goBCER1W8n1CNDKRPXSpn1"),
          1: tas.nat("1"),
        },
        recipient: tas.address("tz1UGWQQ5YFkZqWgE3gqmPyuwy2R5VGpMM9B"),
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
                1: tas.nat("0"),
              },
            },
          ]),
          limits: tas.map([
            {
              key: tas.nat("0"),
              value: tas.nat(1),
            },
            {
              key: tas.nat("1"),
              value: tas.nat(1),
            },
          ]),
          userData: {
            amountsOut: undefined,
            maxSPTAmountIn: undefined,
            sptAmountIn: tas.nat(10000000000000000000),
            tokenIndex: undefined,
            kind: "EXACT_SPT_IN_FOR_TOKENS_OUT",
            recoveryModeExit: false,
          },
        },
        sender: tas.address("tz1UGWQQ5YFkZqWgE3gqmPyuwy2R5VGpMM9B"),
      })
      .send();
    // const estimate = await Tezos.estimate.transfer(exitPoolRequest);
    // console.log(estimate);
    await exitPoolRequest.confirmation(1);
  })
  .catch((error) => console.table(`Error: ${JSON.stringify(error, null, 2)}`));
