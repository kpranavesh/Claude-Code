# Review Agent / Chain Code

Use this skill when asked to review, audit, or improve an existing LangChain + Claude agent or chain.

## Trigger phrases
- "review this agent"
- "audit my chain"
- "what's wrong with this agent"
- "improve this LangChain code"

---

## Prompt

You are reviewing LangChain + Anthropic Claude agent code. Check the following systematically:

### 1. Model Configuration
- [ ] Is the model pinned to a specific version? (avoid `claude-3` without a version suffix)
- [ ] Is `temperature` set intentionally?
- [ ] Is `max_tokens` set where needed to avoid truncation?

### 2. Prompt Quality
- [ ] Is the system prompt clear and scoped?
- [ ] Are input variables properly templated?
- [ ] Is there a risk of prompt injection from user input?

### 3. Tool Use (if applicable)
- [ ] Are tool descriptions clear enough for Claude to pick correctly?
- [ ] Is tool output parsed and validated before use?
- [ ] Are tool errors handled gracefully?

### 4. Memory & State
- [ ] Is conversation history bounded to avoid token blowout?
- [ ] Is `ConversationSummaryMemory` used for long sessions?
- [ ] Is state persisted if needed across runs?

### 5. Error Handling
- [ ] Are `anthropic.APIError` and `langchain` exceptions caught?
- [ ] Is retry logic in place for rate limits?

### 6. Performance
- [ ] Are redundant LLM calls consolidated?
- [ ] Can any steps use `claude-haiku-4-5-20251001` instead of Sonnet/Opus?
- [ ] Is streaming used where latency matters?

Provide a concise summary of findings, then suggest concrete fixes.
