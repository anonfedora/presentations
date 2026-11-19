## Core idea 5 — Native assets in contracts

- Every classic Stellar asset (XLM, USDC, …) can be wrapped by the built-in Stellar Asset Contract (SAC).
- The SAC implements the SEP-41 token interface (similar to ERC-20).
- Contracts move real issued assets — no bridges, no wrapped tokens.
- Issuer controls and trustline rules still apply.
