## Core idea 1 — Rust → WASM

- Write contracts with the soroban-sdk crate.
- Compile to a small WASM binary with: stellar contract build
- Target is wasm32v1-none; do not build contracts with plain cargo build.
- The SDK tracks protocol versions (e.g. SDK v28 shipped alongside Protocol 28).

<!--
Notes: docs.rs/soroban-sdk explicitly recommends stellar contract build over cargo build.
-->
