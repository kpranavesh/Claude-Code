# Build Claude Agent

Use this skill when asked to build a new LangChain + Claude agent, chain, or agentic workflow from scratch.

## Trigger phrases
- "build an agent"
- "create a chain"
- "set up an agentic workflow"
- "scaffold a new agent"

---

## Prompt

You are helping build a LangChain + Anthropic Claude agent. Follow these steps:

1. **Clarify the goal** — Ask what the agent needs to accomplish if not specified. Understand inputs, outputs, and any tools it needs.

2. **Choose the right pattern:**
   - Simple Q&A → `ChatAnthropic` with a prompt template
   - Multi-step reasoning → `AgentExecutor` with tools
   - Sequential tasks → `LangChain Expression Language (LCEL)` chains
   - Long-running / stateful → Add `ConversationBufferMemory` or `ConversationSummaryMemory`

3. **Scaffold the code** with this base structure:
```python
from langchain_anthropic import ChatAnthropic
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

llm = ChatAnthropic(model="claude-sonnet-4-6", temperature=0)
```

4. **Always include:**
   - `.env` loading via `python-dotenv` for `ANTHROPIC_API_KEY`
   - Error handling around agent invocations
   - Type hints on all functions
   - A `main()` entry point with a test run

5. **Model defaults** (unless user specifies):
   - Use `claude-sonnet-4-6` for most tasks
   - Use `claude-opus-4-6` only if deep reasoning is explicitly needed
   - Use `claude-haiku-4-5-20251001` for fast/cheap subtasks

6. **Ask before adding** LangSmith tracing, async execution, or streaming unless the user requests it.
