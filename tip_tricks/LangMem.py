# pip install -U langgraph langmem langchain-openai \
#               langchain-huggingface sentence-transformers

import os
from langgraph.prebuilt import create_react_agent
from langgraph.store.memory import InMemoryStore
from langgraph.checkpoint.memory import MemorySaver
from langmem import create_manage_memory_tool
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.messages import SystemMessage           # NEW

# 1️⃣  Route OpenAI-style calls to Koboldcpp
os.environ["OPENAI_API_BASE"] = "http://localhost:5001/v1"
os.environ["OPENAI_API_KEY"]  = "sk-kobold-dummy"           # any non-empty string

# 2️⃣  Local embeddings (384-d, CPU)
emb = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
)
store = InMemoryStore(
    index={"dims": 384, "embed": emb}
)

# 3️⃣  Prompt builder that prepends retrieved memories
def prompt(state):
    messages  = state["messages"]
    query     = messages[-1].content                      # <-- FIXED
    memories  = store.search(("memories",), query=query)
    sys_msg   = SystemMessage(content=f"## Memories\n{memories}\n")
    return [sys_msg, *messages]                           # ensure system goes first

# 4️⃣  Build the LangGraph agent with “hot-path” memory
agent = create_react_agent(
    "openai:gpt-3.5-turbo",       # name ignored by Koboldcpp
    prompt=prompt,
    tools=[create_manage_memory_tool(namespace=("memories",))],
    store=store,
    checkpointer=MemorySaver(),
)

if __name__ == "__main__":
    cfg = {"configurable": {"thread_id": "demo"}}

    agent.invoke(                                           # teach the fact
        {"messages": [{"role": "user", "content": "My favorite color is blue."}]},
        config=cfg,
    )

    reply = agent.invoke(                                   # ask for recall
        {"messages": [{"role": "user", "content": "What color do I like?"}]},
        config=cfg,
    )
    print(reply["messages"][-1].content)                    # <-- FIXED

