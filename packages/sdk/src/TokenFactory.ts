import { MichelsonMap, TezosToolkit } from "@taquito/taquito";
import { InMemorySigner } from "@taquito/signer";
import { char2Bytes } from "@taquito/utils";
import { fa2TokenFactory } from "./data/fa2-token-factory";

const config = require("../../../.taq/config.local.development.json");

const provider = "http://localhost:20000";

async function example() {
  const owner = config.accounts.bob.publicKeyHash;
  const vault = config.contracts.Vault.address;

  const signer = new InMemorySigner(config.accounts.bob.secretKey.slice(12));
  const tezos = new TezosToolkit(provider);
  tezos.setSignerProvider(signer);

  try {
    console.log("Deploying Tzip12BigMapsTokenMetadata contract...");

    const ledger = new MichelsonMap();
    ledger.set(
      {
        owner: owner,
        token_id: 1,
      },
      (1000000 * 10 ** 18).toString()
    );
    ledger.set(
      {
        owner: owner,
        token_id: 2,
      },
      (1000000 * 10 ** 18).toString()
    );
    ledger.set(
      {
        owner: owner,
        token_id: 3,
      },
      (1000000 * 10 ** 18).toString()
    );
    ledger.set(
      {
        owner: owner,
        token_id: 4,
      },
      (1000000 * 10 ** 18).toString()
    );
    ledger.set(
      {
        owner: owner,
        token_id: 5,
      },
      (1000000 * 10 ** 18).toString()
    );
    ledger.set(
      {
        owner: owner,
        token_id: 6,
      },
      (1000000 * 10 ** 18).toString()
    );
    ledger.set(
      {
        owner: owner,
        token_id: 7,
      },
      (1000000 * 10 ** 18).toString()
    );
    ledger.set(
      {
        owner: owner,
        token_id: 8,
      },
      (1000000 * 10 ** 18).toString()
    );

    const url = "https://storage.googleapis.com/tzip-16/fa2-token-factory.json";
    const bytesUrl = char2Bytes(url);
    const metadata = new MichelsonMap();
    metadata.set("", bytesUrl);

    const operators = new MichelsonMap();
    operators.set(
      {
        owner: owner,
        operator: vault,
        token_id: "0",
      },
      [["unit"]]
    );
    operators.set(
      {
        owner: owner,
        operator: vault,
        token_id: "1",
      },
      [["unit"]]
    );
    operators.set(
      {
        owner: owner,
        operator: vault,
        token_id: "2",
      },
      [["unit"]]
    );
    operators.set(
      {
        owner: owner,
        operator: vault,
        token_id: "3",
      },
      [["unit"]]
    );
    operators.set(
      {
        owner: owner,
        operator: vault,
        token_id: "4",
      },
      [["unit"]]
    );
    operators.set(
      {
        owner: owner,
        operator: vault,
        token_id: "5",
      },
      [["unit"]]
    );
    operators.set(
      {
        owner: owner,
        operator: vault,
        token_id: "6",
      },
      [["unit"]]
    );
    operators.set(
      {
        owner: owner,
        operator: vault,
        token_id: "7",
      },
      [["unit"]]
    );
    operators.set(
      {
        owner: owner,
        operator: vault,
        token_id: "8",
      },
      [["unit"]]
    );

    const token_admins = new MichelsonMap();
    token_admins.set("0", {
      0: owner,
      1: true,
    });
    token_admins.set("1", {
      0: owner,
      1: true,
    });
    token_admins.set("2", {
      0: owner,
      1: true,
    });
    token_admins.set("3", {
      0: owner,
      1: true,
    });
    token_admins.set("4", {
      0: owner,
      1: true,
    });
    token_admins.set("5", {
      0: owner,
      1: true,
    });
    token_admins.set("6", {
      0: owner,
      1: true,
    });
    token_admins.set("7", {
      0: owner,
      1: true,
    });
    token_admins.set("8", {
      0: owner,
      1: true,
    });

    const token_metadata = new MichelsonMap();
    const token0 = new MichelsonMap();
    token0.set("name", char2Bytes("wToken"));
    token0.set("symbol", char2Bytes("wTK"));
    token0.set("decimals", "18");
    const token1 = new MichelsonMap();
    token1.set("name", char2Bytes("wToken"));
    token1.set("symbol", char2Bytes("wTK"));
    token1.set("decimals", "18");
    const token2 = new MichelsonMap();
    token2.set("name", char2Bytes("AliceToken"));
    token2.set("symbol", char2Bytes("ALC"));
    token2.set("decimals", "18");
    const token3 = new MichelsonMap();
    token3.set("name", char2Bytes("wToken"));
    token3.set("symbol", char2Bytes("wTK"));
    token3.set("decimals", "18");
    const token4 = new MichelsonMap();
    token4.set("name", char2Bytes("AliceToken"));
    token4.set("symbol", char2Bytes("ALC"));
    token4.set("decimals", "18");
    const token5 = new MichelsonMap();
    token5.set("name", char2Bytes("wToken"));
    token5.set("symbol", char2Bytes("wTK"));
    token5.set("decimals", "18");
    const token6 = new MichelsonMap();
    token6.set("name", char2Bytes("AliceToken"));
    token6.set("symbol", char2Bytes("ALC"));
    token6.set("decimals", "18");
    const token7 = new MichelsonMap();
    token7.set("name", char2Bytes("wToken"));
    token7.set("symbol", char2Bytes("wTK"));
    token7.set("decimals", "18");
    const token8 = new MichelsonMap();
    token8.set("name", char2Bytes("AliceToken"));
    token8.set("symbol", char2Bytes("ALC"));
    token8.set("decimals", "18");

    token_metadata.set("0", {
      token_id: "0",
      token_info: token1,
    });
    token_metadata.set("1", {
      token_id: "1",
      token_info: token1,
    });
    token_metadata.set("2", {
      token_id: "2",
      token_info: token2,
    });
    token_metadata.set("3", {
      token_id: "3",
      token_info: token3,
    });
    token_metadata.set("4", {
      token_id: "4",
      token_info: token4,
    });
    token_metadata.set("5", {
      token_id: "5",
      token_info: token5,
    });
    token_metadata.set("6", {
      token_id: "6",
      token_info: token6,
    });
    token_metadata.set("7", {
      token_id: "7",
      token_info: token7,
    });
    token_metadata.set("8", {
      token_id: "8",
      token_info: token8,
    });

    const token_total_supply = new MichelsonMap();
    token_total_supply.set("0", (1000000 * 10 ** 18).toString());
    token_total_supply.set("1", (1000000 * 10 ** 18).toString());
    token_total_supply.set("2", (1000000 * 10 ** 18).toString());
    token_total_supply.set("3", (1000000 * 10 ** 18).toString());
    token_total_supply.set("4", (1000000 * 10 ** 18).toString());
    token_total_supply.set("5", (1000000 * 10 ** 18).toString());
    token_total_supply.set("6", (1000000 * 10 ** 18).toString());
    token_total_supply.set("7", (1000000 * 10 ** 18).toString());
    token_total_supply.set("8", (1000000 * 10 ** 18).toString());

    const op = await tezos.contract.originate({
      code: fa2TokenFactory,
      storage: {
        admin: await tezos.signer.publicKeyHash(),
        exchange_address: "KT1DGRPQUwLJyCZnM8WKtwDGiKDSMv4hftk4",
        last_token_id: "8",
        ledger,
        metadata,
        operators,
        token_admins,
        token_metadata,
        token_total_supply,
      },
    });

    console.log("Awaiting confirmation...");
    const contract = await op.contract();
    console.log(
      "Tzip12BigMapsTokenMetadata Contract address",
      contract.address
    );
    console.log("Gas Used", op.consumedGas);
    console.log("Storage Paid", op.storageDiff);
    console.log("Storage Size", op.storageSize);
    console.log("Storage", await contract.storage());
    console.log(
      "Operation hash:",
      op.hash,
      "Included in block level:",
      op.includedInBlock
    );
  } catch (ex) {
    console.error(ex);
  }
}

example();
// KT1SLJQqS6Qk6FJ4qUq8eyney7Q5VU31zktB
