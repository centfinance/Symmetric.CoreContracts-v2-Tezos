import { InMemorySigner } from "@taquito/signer";
import { PollingSubscribeProvider, TezosToolkit } from "@taquito/taquito";
import { encodePubKey } from "@taquito/utils";
import { tas } from "../../../types/type-aliases";
import { VaultContractType } from "../../../types/Vault.types";

const Tezos = new TezosToolkit("http://localhost:20000");

const config = require("../../../../.taq/config.local.development.json");

const contract = await Tezos.contract.at<VaultContractType>(
  config.contracts.WeightedPoolFactory.address
);

const swapRequest = await contract.methodsObject.swap({
  deadline: tas.timestamp(new Date()),
  funds: {
    fromInternalBalance: false,
    recipient: "",
    sender: "",
    toInternalBalance: false,
  },
  limit: "",
  singleSwap: {
    amount: nat,
    assetIn: {
      0: address,
      1: nat | undefined,
    },
    assetOut: {
      0: address,
      1: nat | undefined,
    },
    kind: "string",
    poolId: {
      0: "address",
      1: "nat",
    },
  },
});
