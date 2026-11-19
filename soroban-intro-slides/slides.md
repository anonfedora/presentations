# Introduction to Soroban

### Smart contracts on the Stellar network

Rust · WebAssembly · Stellar

<!--
Notes: Opening slide. Soroban is Stellar's native smart contract platform.
-->

---

## What is Soroban?

- **Stellar's smart contract platform** — built into the core protocol, not a sidechain.
- **Live on mainnet** — since February 20, 2024 (Protocol 20); opened to public dApp deployment in March 2024.
- **Rust → WASM** — contracts are written in Rust, compiled to WebAssembly and executed by Stellar Core.
- **Beyond payments** — extends a payments-first network to DeFi and other financial services.

> **Note:** Not EVM-compatible: it is a separate design, so Solidity habits do not carry over directly.

<!--
Notes: Sources: eco.com Soroban overview (launch dates), The Block (March 2024 launch coverage).
-->

---

## Core idea 1 — Rust → WASM

- Write contracts with the soroban-sdk crate.
- Compile to a small WASM binary with: stellar contract build
- Target is wasm32v1-none; do not build contracts with plain cargo build.
- The SDK tracks protocol versions (e.g. SDK v28 shipped alongside Protocol 28).

<!--
Notes: docs.rs/soroban-sdk explicitly recommends stellar contract build over cargo build.
-->

---

## Core idea 2 — The Env

Every contract function receives an Env handle — your gateway to the host.

- Storage, events, auth, crypto and ledger info all go through Env.
- Contracts are #![no_std].
- Use SDK types: Symbol, Vec, Map, Address, String, Bytes.

---

## Core idea 3 — Storage tiers & state archival

| Tier | Use it for | When the TTL runs out |
| --- | --- | --- |
| Instance | Small contract config (admin, token name) | Archived together with the contract instance |
| Persistent | Data that must not be lost (balances) | Archived — must be restored before use |
| Temporary | Cheap, short-lived data (nonces, allowances) | Deleted permanently |

> **Heads up:** State has rent: extend TTLs with extend_ttl(). Living forever is not free.

<!--
Notes: This is the biggest difference from Ethereum. Accessed via env.storage().instance() / .persistent() / .temporary().
-->

---

## Core idea 4 — Authorization

- Call address.require_auth() — the host verifies the signature.
- Works for classic Stellar accounts and contract accounts alike.
- Contracts request specific, limited permissions instead of blanket approvals.
- No hand-rolled msg.sender checks.

<!--
Notes: Source: SDF blog, 'Soroban: the smart contract platform designed for developers'.
-->

---

## Core idea 5 — Native assets in contracts

- Every classic Stellar asset (XLM, USDC, …) can be wrapped by the built-in Stellar Asset Contract (SAC).
- The SAC implements the SEP-41 token interface (similar to ERC-20).
- Contracts move real issued assets — no bridges, no wrapped tokens.
- Issuer controls and trustline rules still apply.

---

## Core idea 6 — Resource-based fees

1. **Simulate** — RPC simulateTransaction estimates CPU, memory, reads/writes and ledger footprint.
2. **Declare** — The transaction declares exactly those resources.
3. **Pay** — Fees are charged for the declared resources — predictable costs.

<!--
Notes: Simulation is a required step in any client flow.
-->

---

## A minimal contract

```rust {12,13,15,16}
#![no_std]
use soroban_sdk::{contract, contractimpl, symbol_short, Address, Env, Symbol};

const COUNTER: Symbol = symbol_short!("COUNTER");

#[contract]
pub struct CounterContract;

#[contractimpl]
impl CounterContract {
    pub fn increment(env: Env, caller: Address) -> u32 {
        caller.require_auth();
        let mut count: u32 = env.storage().instance().get(&COUNTER).unwrap_or(0);
        count += 1;
        env.storage().instance().set(&COUNTER, &count);
        env.storage().instance().extend_ttl(100, 1000);
        count
    }
}
```

<!--
Notes: Line 12: require_auth. Lines 13-16: read, write and extend the TTL of instance storage.
-->

---

## Workflow with the Stellar CLI

```bash
# 1. Scaffold a workspace
stellar contract init my-project

# 2. Compile to .wasm
stellar contract build

# 3. Create and fund a testnet identity
stellar keys generate alice --network testnet --fund

# 4. Deploy
stellar contract deploy \
  --wasm target/wasm32v1-none/release/counter.wasm \
  --source alice --network testnet

# 5. Invoke
stellar contract invoke --id <CONTRACT_ID> \
  --source alice --network testnet \
  -- increment --caller alice
```

<!--
Notes: keys generate --fund uses Friendbot on testnet to fund the new account.
-->

---

## Testing & client integration

- **Unit tests** — cargo test runs natively against a mocked Env.
- **Auth in tests** — env.mock_all_auths() makes auth paths easy to exercise.
- **TypeScript** — stellar contract bindings typescript generates a typed client from the contract spec.
- **Network access** — talk to the chain through Stellar RPC.

---

## Resources — Start here

- [Smart contracts overview](https://developers.stellar.org/docs/build/smart-contracts) — Main hub: SDK, host environment, FAQs
- [Getting Started](https://developers.stellar.org/docs/build/smart-contracts/getting-started) — Official step-by-step track
- [Setup](https://developers.stellar.org/docs/build/smart-contracts/getting-started/setup) — Install Rust and the Stellar CLI
- [1. Hello World](https://developers.stellar.org/docs/build/smart-contracts/getting-started/hello-world)
- [2. Deploy to Testnet](https://developers.stellar.org/docs/build/smart-contracts/getting-started/deploy-to-testnet)
- [Scaffold Stellar](https://developers.stellar.org/docs/tools/scaffold-stellar) — Fastest path to a full-stack dApp

---

## Resources — SDK & tooling

- [soroban-sdk (docs.rs)](https://docs.rs/soroban-sdk) — API reference
- [stellar/rs-soroban-sdk](https://github.com/stellar/rs-soroban-sdk) — SDK source
- [stellar/stellar-cli](https://github.com/stellar/stellar-cli) — brew install stellar-cli
- [stellar/stellar-rpc](https://github.com/stellar/stellar-rpc) — RPC server
- [RPC docs](https://developers.stellar.org/docs/data/apis/rpc)
- [Stellar Lab](https://lab.stellar.org) — Build, simulate, submit transactions
- [Stellar Expert](https://stellar.expert) — Block explorer

---

## Resources — Example contracts

- [Example contracts (docs)](https://developers.stellar.org/docs/build/smart-contracts/example-contracts)
- [stellar/soroban-examples](https://github.com/stellar/soroban-examples) — Token, atomic swap, auth, timelock…
- [OpenZeppelin Stellar Contracts](https://docs.openzeppelin.com/stellar-contracts) — Audited building blocks
- [OpenZeppelin on Stellar docs](https://developers.stellar.org/docs/tools/openzeppelin-contracts)

---

## Resources — Storage & tokens

- [State archival: concepts](https://developers.stellar.org/docs/learn/fundamentals/contract-development/storage/state-archival)
- [State archival how-tos](https://developers.stellar.org/docs/build/guides/archival)
- [State archival in dApps](https://developers.stellar.org/docs/build/guides/dapps/state-archival) — Client-side restore
- [Stellar Asset Contract](https://developers.stellar.org/docs/tokens/stellar-asset-contract)
- [SAC how-to guide](https://developers.stellar.org/docs/build/guides/tokens/stellar-asset-contract)
- [Token interface](https://developers.stellar.org/docs/tokens/token-interface)
- [SEP-41 spec](https://github.com/stellar/stellar-protocol/blob/master/ecosystem/sep-0041.md)
- [Anatomy of an asset](https://developers.stellar.org/docs/tokens/anatomy-of-an-asset) — Asset models compared

---

## Resources — Community & funding

- [Stellar Developer Discord](https://discord.gg/stellardev)
- [Stellar Community Fund](https://communityfund.stellar.org) — Grants for builders
- [Docs index (llms.txt)](https://developers.stellar.org/llms.txt) — Every docs page in one list
- [Build hub](https://developers.stellar.org/docs/build) — Includes payment apps without contracts (Wallet SDK, JS SDK)

<!--
Notes: Payments-only apps may not need contracts at all — see the Wallet SDK and JS SDK payment tutorials linked from the Build hub.
-->

---

# Thank you

### Questions?

Start building: developers.stellar.org/docs/build/smart-contracts
