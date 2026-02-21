# Debug Claude API / LangChain Issues

Use this skill when diagnosing errors, unexpected outputs, or performance issues with Claude API or LangChain chains.

## Trigger phrases
- "debug this agent"
- "why is my chain failing"
- "Claude is returning wrong output"
- "LangChain error"

---

## Prompt

You are debugging a LangChain + Claude API issue. Work through this checklist:

### Common Failure Modes

**Authentication / API errors**
- Check `ANTHROPIC_API_KEY` is loaded (not hardcoded, not expired)
- Verify the model ID is valid (e.g. `claude-sonnet-4-6`, not `claude-3-sonnet`)
- Check rate limits — use exponential backoff

**Wrong or empty output**
- Print the raw prompt being sent before calling the LLM
- Check `temperature` — high values cause inconsistency
- Check `max_tokens` — if too low, output is silently truncated
- Verify the output parser matches the actual response format

**LangChain-specific**
- Use `verbose=True` on chains/agents to see intermediate steps
- Check that tool schemas match what Claude expects
- Confirm `ChatPromptTemplate` variables match what's passed in `.invoke()`
- For LCEL chains, add `.with_config({"run_name": "debug"})` and use LangSmith

**Memory issues**
- Check if memory is accumulating too many tokens — add `max_token_limit`
- Verify memory is actually being passed into the prompt

### Debugging Template
```python
# Add this around any failing chain call
import traceback
try:
    result = chain.invoke({"input": user_input})
    print("Result:", result)
except Exception as e:
    traceback.print_exc()
    print("Raw error:", e)
```

After identifying the issue, explain root cause and provide a minimal fix.
