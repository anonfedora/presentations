## Core idea 4 — Authorization

- Call address.require_auth() — the host verifies the signature.
- Works for classic Stellar accounts and contract accounts alike.
- Contracts request specific, limited permissions instead of blanket approvals.
- No hand-rolled msg.sender checks.

<!--
Notes: Source: SDF blog, 'Soroban: the smart contract platform designed for developers'.
-->
