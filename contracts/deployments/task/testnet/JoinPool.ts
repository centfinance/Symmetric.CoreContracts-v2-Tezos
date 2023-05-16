import { InMemorySigner } from "@taquito/signer";
import { TezosToolkit } from "@taquito/taquito";
import { tas } from "../../../../types/type-aliases";
import { VaultContractType as ContractType } from "../../../../types/Vault.types";

const Tezos = new TezosToolkit("https://rpc.tzkt.io/ghostnet");

const config = require("../../../../.taq/config.local.testing.json");

InMemorySigner.fromSecretKey(config.accounts.taqOperatorAccount.privateKey)
  .then((theSigner) => {
    Tezos.setProvider({ signer: theSigner });
  })
  .then(async () => {
    const contract = await Tezos.contract.at<ContractType>(
      "KT1XV3C2twmrgVaHv2jNtUpymQZ39C6mM7Kp"
    );
    const joinPoolRequest = contract.methodsObject
      .joinPool({
        poolId: {
          0: tas.address("tz1UGWQQ5YFkZqWgE3gqmPyuwy2R5VGpMM9B"),
          1: tas.nat(1),
        },
        recipient: tas.address("tz1UGWQQ5YFkZqWgE3gqmPyuwy2R5VGpMM9B"),
        request: {
          assets: tas.map([
            {
              key: tas.nat("0"),
              value: {
                0: tas.address("KT1VvQ6azTcyj5otVciTicuFS1gVhcHD56Kr"),
                1: tas.nat("0"),
              },
            },
            {
              key: tas.nat("1"),
              value: {
                0: tas.address("KT1VvQ6azTcyj5otVciTicuFS1gVhcHD56Kr"),
                1: tas.nat("1"),
              },
            },
          ]),
          limits: tas.map([
            {
              key: tas.nat("0"),
              value: tas.nat("100000000000000000000"),
            },
            {
              key: tas.nat("1"),
              value: tas.nat("100000000000000000000"),
            },
          ]),
          useInternalBalance: false,
          userData: {
            allT: undefined,
            amountsIn: tas.map([
              {
                key: tas.nat("0"),
                value: tas.nat("100000000000000000000"),
              },
              {
                key: tas.nat("1"),
                value: tas.nat("100000000000000000000"),
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
      .toTransferParams();
    const estimate = await Tezos.estimate.transfer(joinPoolRequest);
    console.log(estimate);
    // await joinPoolRequest.confirmation(0);
  })
  .catch((error) => console.table(`Error: ${JSON.stringify(error, null, 2)}`));
