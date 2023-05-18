import { InMemorySigner } from "@taquito/signer";
import { PollingSubscribeProvider, TezosToolkit } from "@taquito/taquito";
import { encodePubKey } from "@taquito/utils";
import { tas } from "../../../types/type-aliases";
import { VaultContractType } from "../../../types/Vault.types";

const Tezos = new TezosToolkit("https://ghostnet.smartpy.io");

const config = require("../../../.taq/config.local.testing.json");

const tokenAddress = "KT1JA3UQ6R4C84mH3FqS3G5mKFeEdLumrDc3";

function addMinutes(date: Date, minutes: number) {
  return new Date(date.getTime() + minutes * 60000);
}

InMemorySigner.fromSecretKey(config.accounts.taqOperatorAccount.privateKey)
  .then((theSigner) => {
    Tezos.setProvider({ signer: theSigner });
  })
  .then(async () => {
    const contract = await Tezos.contract.at(config.contracts.Vault.address);
    // const funds = {
    //   recipient: tas.address(config.accounts.bob.publicKeyHash),
    //   sender: tas.address(config.accounts.bob.publicKeyHash),
    // };

    const singleSwap = {
      amount: tas.nat(1 * 10 ** 18),
      assetIn: {
        0: tas.address(tokenAddress),
        1: tas.nat("5"),
      },
      assetOut: {
        0: tas.address(tokenAddress),
        1: tas.nat("0"),
      },
      kind: "GIVEN_OUT",
      poolId: {
        0: tas.address("KT1ADiYeVqgr4xmVpcBatTQG3eopRRNGZj8k"),
        1: tas.nat("1"),
      },
    };

    const swapRequest = await contract.methods
      .swap(
        tas.timestamp(addMinutes(new Date(), 30).toISOString()),
        tas.address("tz1UGWQQ5YFkZqWgE3gqmPyuwy2R5VGpMM9B"),
        tas.address("tz1UGWQQ5YFkZqWgE3gqmPyuwy2R5VGpMM9B"),
        tas.nat(2 * 10 ** 18),
        singleSwap.amount,
        singleSwap.assetIn[0],
        singleSwap.assetIn[1],
        singleSwap.assetOut[0],
        singleSwap.assetOut[1],
        singleSwap.kind,
        singleSwap.poolId[0],
        singleSwap.poolId[1]
      )
      .send();
    // const estimate = await Tezos.estimate.transfer(swapRequest);
    // console.log(estimate);
    await swapRequest.confirmation(1);
  })
  .catch((error) => console.table(`Error: ${JSON.stringify(error, null, 2)}`));
