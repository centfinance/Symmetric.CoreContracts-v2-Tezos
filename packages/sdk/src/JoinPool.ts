import { InMemorySigner } from "@taquito/signer";
import { TezosToolkit } from "@taquito/taquito";
import { tas } from "../../../types/type-aliases";
import { VaultContractType as ContractType } from "../../../types/Vault.types";

const config = require("../../../.taq/config.local.development.json");

const Tezos = new TezosToolkit(config.rpcUrl);

InMemorySigner.fromSecretKey(config.accounts.bob.secretKey.slice(12))
  .then((theSigner) => {
    Tezos.setProvider({ signer: theSigner });
  })
  .then(async () => {
    const contract = await Tezos.contract.at<ContractType>(
      config.contracts.Vault.address
    );
    const joinPoolRequest = contract.methodsObject
      .joinPool({
        poolId: {
          0: tas.address("KT1EHBAZxvw5FsPvnQpiFCcbNPh5NXNx1Zrd"),
          1: tas.nat(7),
        },
        recipient: tas.address("tz1aSkwEot3L2kmUvcoxzjMomb9mvBNuzFK6"),
        request: {
          assets: tas.map([
            {
              key: tas.nat("0"),
              value: {
                0: tas.address("KT1SLJQqS6Qk6FJ4qUq8eyney7Q5VU31zktB"),
                1: tas.nat("0"),
              },
            },
            {
              key: tas.nat("1"),
              value: {
                0: tas.address("KT1SLJQqS6Qk6FJ4qUq8eyney7Q5VU31zktB"),
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
        sender: tas.address("tz1aSkwEot3L2kmUvcoxzjMomb9mvBNuzFK6"),
      })
      .toTransferParams();
    const estimate = await Tezos.estimate.transfer(joinPoolRequest);
    console.log(estimate);
    // await joinPoolRequest.confirmation(0);
  })
  .catch((error) => console.table(`Error: ${JSON.stringify(error, null, 2)}`));
