## Core idea 2 — The Env

Every contract function receives an Env handle — your gateway to the host.

- Storage, events, auth, crypto and ledger info all go through Env.
- Contracts are #![no_std].
- Use SDK types: Symbol, Vec, Map, Address, String, Bytes.
