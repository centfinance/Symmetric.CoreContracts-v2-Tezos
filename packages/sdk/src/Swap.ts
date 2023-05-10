import { InMemorySigner } from "@taquito/signer";
import { PollingSubscribeProvider, TezosToolkit } from "@taquito/taquito";
import { encodePubKey } from "@taquito/utils";
import { tas } from "../../../types/type-aliases";
import { VaultContractType } from "../../../types/Vault.types";

const Tezos = new TezosToolkit("http://localhost:20000");

const config = require("../../../.taq/config.local.development.json");

const tokenAddress = "KT1TFoy7ikLHYQqhYyvsBjDFTGukPm2jLs9f";

InMemorySigner.fromSecretKey(config.accounts.bob.secretKey.slice(12))
  .then((theSigner) => {
    Tezos.setProvider({ signer: theSigner });
  })
  .then(async () => {
    const contract = await Tezos.contract.at<VaultContractType>(
      config.contracts.Vault.address
    );

    const swapRequest = await contract.methodsObject
      .swap({
        deadline: tas.timestamp(new Date().toISOString()),
        funds: {
          fromInternalBalance: false,
          recipient: tas.address("tz1aSkwEot3L2kmUvcoxzjMomb9mvBNuzFK6"),
          sender: tas.address("tz1aSkwEot3L2kmUvcoxzjMomb9mvBNuzFK6"),
          toInternalBalance: false,
        },
        limit: tas.nat("0"),
        singleSwap: {
          amount: tas.nat(1 * 10 ** 18),
          assetIn: {
            0: tas.address(tokenAddress),
            1: tas.nat("1"),
          },
          assetOut: {
            0: tas.address(tokenAddress),
            1: tas.nat("2"),
          },
          kind: "GIVEN_IN",
          poolId: {
            0: tas.address("KT1Wio8FdY7pWg7KQuAUQxyd9qWV4zBxszHB"),
            1: tas.nat("4"),
          },
        },
      })
      .toTransferParams();
    const estimate = await Tezos.estimate.transfer(swapRequest);
    console.log(estimate);
    // await swapRequest.confirmation(1);
  })
  .catch((error) => console.table(`Error: ${JSON.stringify(error, null, 2)}`));
