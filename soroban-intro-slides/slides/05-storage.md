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
