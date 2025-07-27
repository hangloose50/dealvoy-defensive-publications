# Clean Code – Chapter 3: Naming

## Key Principles

1. **Intent Revealing**  
   - Names should describe what something does, not how.  
   - E.g. `fetch_with_retries` is clearer than `fetch`.

2. **Avoid Disinformation**  
   - Don’t reuse names that suggest different purposes.  
   - E.g. if you support proxies, don’t call that list `PROXIES_LIST` in one place and `proxy_pool` elsewhere.

3. **Pronounceable & Searchable**  
   - Choose words everyone can read aloud.  
   - Long names are OK if they’re crystal clear.  
   - Avoid abbreviations like `cfg`—write `config`.

4. **Consistent**  
   - Stick to one scheme: either `snake_case` for everything.  
   - Use the same word for the same concept (never mix `ua` and `user_agent`).

5. **Avoid Encoding Too Much**  
   - Function names shouldn’t repeat obvious info.  
   - If it’s in the module name (`http_utils.py`), you don’t need `http_` prefix on every function.

## Actions for `http_utils.py`

- Rename `fetch` → `fetch_with_retries` (makes retry intent explicit)  
- Rename `fetch_many` → `fetch_concurrent` (describes concurrency)  
- Rename `CONFIG` → `config` (match snake_case)  
- Rename `USER_AGENTS` → `user_agents` and `PROXIES` → `proxy_endpoints`  
- Parameter names: `headers` → `extra_headers`, `resp` → `response`

