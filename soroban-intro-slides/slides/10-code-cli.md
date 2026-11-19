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
