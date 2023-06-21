import { InMemorySigner } from "@taquito/signer";
import { char2Bytes } from "@taquito/utils";
import { PollingSubscribeProvider, TezosToolkit } from "@taquito/taquito";
import { encodePubKey } from "@taquito/utils";
import { tas } from "../../../types/type-aliases";
import { WeightedPoolFactoryContractType as ContractType } from "../../../types/WeightedPoolFactory.types";

const Tezos = new TezosToolkit("https://ghostnet.smartpy.io");

const config = require("../../../.taq/config.local.testing.json");

const tokenAddress = "KT1JA3UQ6R4C84mH3FqS3G5mKFeEdLumrDc3";

InMemorySigner.fromSecretKey(config.accounts.taqOperatorAccount.privateKey)
  .then((theSigner) => {
    Tezos.setProvider({ signer: theSigner });
  })
  .then(async () => {
    const contract = await Tezos.contract.at<ContractType>(
      config.contracts.WeightedPoolFactory.address
    );
    const createRequest = await contract.methodsObject
      .create({
        metadata: tas.bytes(
          char2Bytes(
            "https://raw.githubusercontent.com/centfinance/Symmetric.CoreContracts-v2-Tezos/main/metadata/testnet/pools/SYMM-CTEZ/50-50.json"
          )
        ),
        token_metadata: tas.map({
          name: tas.bytes(char2Bytes("SYMM / CTEZ 50/50")),
          symbol: tas.bytes(char2Bytes("SYMMLP")),
          decimals: tas.bytes(char2Bytes("18")),
          thumbnailUri: tas.bytes(
            char2Bytes(
              "https://assets.coingecko.com/coins/images/18525/small/SYMM-Coin-2.png?1632276841"
            )
          ),
        }),
        normalizedWeights: tas.map([
          {
            key: tas.nat("0"),
            value: tas.nat("500000000000000000"),
          },
          {
            key: tas.nat("1"),
            value: tas.nat("500000000000000000"),
          },
        ]),
        swapFeePercentage: tas.nat("10000000000000000"),
        tokenDecimals: tas.map([
          {
            key: tas.nat("0"),
            value: tas.nat("18"),
          },
          {
            key: tas.nat("1"),
            value: tas.nat("18"),
          },
        ]),
        tokens: tas.map([
          {
            key: tas.nat("0"),
            value: {
              0: tas.address(tokenAddress),
              1: tas.nat("6"),
            },
          },
          {
            key: tas.nat("1"),
            value: {
              0: tas.address(tokenAddress),
              1: tas.nat("7"),
            },
          },
        ]),
      })
      .send();
    await createRequest.confirmation(1);
  })
  .catch((error) => console.table(`Error: ${JSON.stringify(error, null, 2)}`));

Tezos.setStreamProvider(
  Tezos.getFactory(PollingSubscribeProvider)({
    shouldObservableSubscriptionRetry: true,
    pollingIntervalMilliseconds: 1500,
  })
);

try {
  const sub = Tezos.stream.subscribeEvent({
    tag: "PoolCreated",
    address: config.contracts.WeightedPoolFactory.address,
  });

  // rome-ignore lint/suspicious/noExplicitAny: <explanation>
  function getAddressFromEvent(data: any) {
    console.log("pool address: ", encodePubKey(data.payload.bytes));
    sub.close();
  }

  sub.on("data", getAddressFromEvent);
} catch (e) {
  console.log(e);
}
