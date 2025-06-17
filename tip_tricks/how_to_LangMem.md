**In a nutshell:** you can treat Koboldcpp as a local “OpenAI-compatible” server and plug it into the LangChain ecosystem with a tiny custom wrapper; once the LLM is available through LangChain, LangMem’s *hot-path* tools let your agent deliberately **write**, **search** and **update** long-term memories during its main reasoning loop. Below is a step-by-step recipe that ties the three pieces together—Koboldcpp, a LangChain custom-LLM class, and LangMem’s `manage_memory` tool—so the agent can run fully offline while still remembering what happened last week.

---

## 1  Run Koboldcpp in “OpenAI-compatible” mode

1. **Compile or grab a pre-built binary** for your OS and model.([koboldai.com][1])
2. Launch with an OpenAI endpoint enabled (default port = 5001):

   ```bash
   ./koboldcpp --model ./models/phi-2.Q4_K.gguf --port 5001 --openai
   ```

   Versions ≥ 1.45 expose `/v1/completions` and `/v1/chat/completions`, which ordinary OpenAI clients (and therefore LangChain) can hit.([github.com][2], [koboldai.com][1])
3. Test locally:

   ```bash
   curl http://localhost:5001/v1/chat/completions \
        -H "Content-Type: application/json" \
        -d '{"model":"koboldcpp","messages":[{"role":"user","content":"Ping?"}]}'
   ```

   You should get a JSON answer, proving the endpoint is alive.([github.com][3])

---

## 2  Wrap Koboldcpp as a LangChain LLM

LangChain lets you register **any** backend by subclassing `BaseLLM`; the only method you *must* implement is `_call`.([python.langchain.com][4])

```python
from typing import Any, List
import requests, os
from langchain.llms.base import LLM

class KoboldCppLLM(LLM):
    base_url: str = "http://localhost:5001"      # adjust if needed
    model: str = "koboldcpp"
    api_key: str = os.getenv("DUMMY_KEY", "sk-none")  # Koboldcpp ignores it

    @property
    def _llm_type(self) -> str:
        return "koboldcpp"

    def _call(self, prompt: str,  stop: List[str] | None = None,
              **kwargs: Any) -> str:
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "stop": stop or [],
            "temperature": kwargs.get("temperature", 0.7)
        }
        r = requests.post(f"{self.base_url}/v1/chat/completions",
                          json=payload, timeout=60)
        return r.json()["choices"][0]["message"]["content"]
```

Now you can drop `llm = KoboldCppLLM()` anywhere a normal LangChain `ChatOpenAI` would appear.([mljourney.com][5])

---

## 3  Install and initialize LangMem

```bash
pip install -U langmem langgraph
```

LangMem provides:

* `MemoryStore` abstractions (SQLite, PGVector, Weaviate, etc.)([github.com][6])
* `manage_memory` **tool** that agents explicitly invoke to store or retrieve facts in the *hot path*.([langchain-ai.lang.chat][7], [deepwiki.com][8])

Example setup with a local SQLite vector store:

```python
from langmem.stores import SQLiteMemoryStore
mem_store = SQLiteMemoryStore("memory.sqlite")
```

---

## 4  Build a LangGraph agent that uses both

```python
from langgraph import Graph
from langmem.agent_tools import manage_memory
from langchain.tools import Tool

llm = KoboldCppLLM()

# Wrap the memory tool so the agent can call it like any other function
memory_tool = Tool.from_function(
    func=manage_memory(mem_store),
    name="manage_memory",
    description="Save or search long-term memories"
)

g = Graph()
g.set_llm(llm)
g.add_tool(memory_tool)

agent = g.compile()
```

Inside your system prompt (or via tool calls) instruct the agent **when** to save:

```python
agent.invoke("Remember that Alice’s cat is named Whiskers.")
# Agent decides to call manage_memory("save", "Alice’s cat is Whiskers")
```

Later:

```python
agent.invoke("What is Alice’s cat’s name?")
# Agent may call manage_memory("search", …) before answering
```

Everything runs locally: the LLM comes from Koboldcpp; the long-term store is a file on disk.

---

## 5  Tips & common pitfalls

| Topic              | Recommendation                                                                                                                                           |
| ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Embeddings**     | LangMem defaults to OpenAI embeddings. Swap in a local embedder (e.g. `SentenceTransformerEmbeddings`) to stay fully offline.([python.langchain.com][9]) |
| **Context length** | Match Koboldcpp’s `--contextsize`/`n_ctx` with `MemoryStore(…, max_tokens=…)` so retrieval fits.                                                         |
| **Tool routing**   | Because hot-path writes are deliberate, add heuristics (e.g. “if user says *remember* or *note*”) in the agent’s planner node.([deepwiki.com][8])        |
| **Concurrency**    | SQLite is fine for single-user; move to Postgres or Chroma for multi-user bots.([github.com][6])                                                         |
| **Testing**        | Use memory-heavy dialogs to verify the agent actually calls `manage_memory`; LangMem logs tool usage by default.([github.com][10])                       |

---

## 6  Putting it all together

Combine the snippets above in one `main.py`, run Koboldcpp, then start your Python script. The agent will:

1. Send prompts to your local model through the wrapper.
2. Decide—in its conscious reasoning loop—whether to “write a note” or “look something up,” and call the LangMem tool accordingly.
3. Retrieve vectors from the local store, inject them as context, and produce answers—no cloud calls involved.

With this stack you get **offline inference**, **long-term adaptive memory**, and **full control over storage**, making it ideal for privacy-sensitive chatbots or game NPCs. Enjoy hacking! 🎉

[1]: https://koboldai.com/KoboldCpp/?utm_source=chatgpt.com "KoboldCpp - KoboldAI"
[2]: https://github.com/LostRuins/koboldcpp/wiki?utm_source=chatgpt.com "Home · LostRuins/koboldcpp Wiki - GitHub"
[3]: https://github.com/LostRuins/koboldcpp/issues/654?utm_source=chatgpt.com "Changing the template for OpenAI-compatible chat completion"
[4]: https://python.langchain.com/docs/how_to/custom_llm/?utm_source=chatgpt.com "How to create a custom LLM class | ️ LangChain"
[5]: https://mljourney.com/langchain-agent-with-local-llm-a-practical-guide-to-running-autonomous-ai-locally/?utm_source=chatgpt.com "Langchain Agent with Local LLM: A Practical Guide to Running Autonomous ..."
[6]: https://github.com/langchain-ai/langmem?utm_source=chatgpt.com "langchain-ai/langmem - GitHub"
[7]: https://langchain-ai.lang.chat/langmem/hot_path_quickstart/?utm_source=chatgpt.com "Hot Path Quickstart Guide - langchain-ai.lang.chat"
[8]: https://deepwiki.com/langchain-ai/langmem/3.1-hot-path-memory-%28agent-driven%29?utm_source=chatgpt.com "Hot Path Memory (Agent-Driven) | langchain-ai/langmem | DeepWiki"
[9]: https://python.langchain.com/docs/how_to/local_llms/?utm_source=chatgpt.com "Run models locally | ️ LangChain"
[10]: https://github.com/langchain-ai/langmem/blob/main/docs/docs/hot_path_quickstart.md?utm_source=chatgpt.com "langmem/docs/docs/hot_path_quickstart.md at main · langchain-ai/langmem ..."
