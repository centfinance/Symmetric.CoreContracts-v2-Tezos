import { TezosToolkit } from "@taquito/taquito";
import { InMemorySigner } from "@taquito/signer";
import { encodePubKey } from "@taquito/utils";
import { WeightedPoolFactoryContractType as ContractType } from "../../../types/WeightedPoolFactory.types";

const tezos = new TezosToolkit("https://ghostnet.smartpy.io");

const config = require("../../../.taq/config.local.testing.json");
// const secretKey = config.accounts[config.accountDefault].secretKey.slice(12);

// const signer = await InMemorySigner.fromSecretKey(secretKey);
// tezos.setProvider({ signer });

InMemorySigner.fromSecretKey(config.accounts.taqOperatorAccount.privateKey)
  .then((theSigner) => {
    tezos.setProvider({ signer: theSigner });
  })
  .then(async () => {
    const contract = await tezos.contract.at<ContractType>(
      config.contracts.WeightedPoolFactory.address
    );
    const initRequest = await contract.methods.initialize().send();
    await initRequest.confirmation(1);
  })
  .catch((error) => console.table(`Error: ${JSON.stringify(error, null, 2)}`));

try {
  const sub = tezos.stream.subscribeEvent({
    tag: "PoolRegistered",
    address: config.contracts.Vault.address,
  });

  // rome-ignore lint/suspicious/noExplicitAny: <explanation>
  function getPoolId(data: any) {
    console.log("Pool ID: ", {
      0: encodePubKey(data.payload.args[0].bytes),
      1: data.payload.args[1].args[1].int,
    });
    sub.close();
  }

  sub.on("data", getPoolId);
} catch (e) {
  console.log(e);
}
