import { InMemorySigner } from "@taquito/signer";
import { PollingSubscribeProvider, TezosToolkit } from "@taquito/taquito";
import { encodePubKey } from "@taquito/utils";
import { tas } from "../../../types/type-aliases";
import { VaultContractType } from "../../../types/Vault.types";

const Tezos = new TezosToolkit("http://localhost:20000");

const config = require("../../../.taq/config.local.development.json");

const tokenAddress = "KT19SwoUtpqsJrKFkJHiDQkXBNU8qXKoUZp4";

function addMinutes(date: Date, minutes: number) {
  return new Date(date.getTime() + minutes * 60000);
}

InMemorySigner.fromSecretKey(config.accounts.bob.secretKey.slice(12))
  .then((theSigner) => {
    Tezos.setProvider({ signer: theSigner });
  })
  .then(async () => {
    const contract = await Tezos.contract.at(config.contracts.Vault.address);
    const funds = {
      fromInternalBalance: false,
      recipient: tas.address(config.accounts.bob.publicKeyHash),
      sender: tas.address(config.accounts.bob.publicKeyHash),
      toInternalBalance: false,
    };

    const singleSwap = {
      amount: tas.nat(1 * 10 ** 18),
      assetIn: {
        0: tas.address(tokenAddress),
        1: tas.nat("2"),
      },
      assetOut: {
        0: tas.address(tokenAddress),
        1: tas.nat("3"),
      },
      kind: "GIVEN_OUT",
      poolId: {
        0: tas.address("KT1HNE3uYR1XxLzfMFP65DC7nJqVSvhpgaV7"),
        1: tas.nat("4"),
      },
    };

    const swapRequest = await contract.methods
      .swap(
        tas.timestamp(addMinutes(new Date(), 30).toISOString()),
        false,
        tas.address(config.accounts.bob.publicKeyHash),
        tas.address(config.accounts.bob.publicKeyHash),
        false,
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
