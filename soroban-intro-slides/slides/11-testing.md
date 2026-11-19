## Testing & client integration

- **Unit tests** — cargo test runs natively against a mocked Env.
- **Auth in tests** — env.mock_all_auths() makes auth paths easy to exercise.
- **TypeScript** — stellar contract bindings typescript generates a typed client from the contract spec.
- **Network access** — talk to the chain through Stellar RPC.
