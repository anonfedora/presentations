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
