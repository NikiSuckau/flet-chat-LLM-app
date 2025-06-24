# pip install -U langgraph langmem langchain-openai \
#               langchain-huggingface sentence-transformers

import os

from langchain_huggingface import HuggingFaceEmbeddings
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langgraph.store.memory import InMemoryStore
from langmem import create_manage_memory_tool

# 1️⃣ Point any OpenAI SDK call to Koboldcpp
os.environ["OPENAI_API_BASE"] = "http://localhost:5001/v1"
os.environ["OPENAI_API_KEY"] = "sk-kobold-dummy"  # Koboldcpp ignores it

# 2️⃣ Local embedding model (384-dim)
emb = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"},  # or "cuda"
)

store = InMemoryStore(
    index={
        "dims": 384,  # all-MiniLM-L6-v2 outputs 384-d vectors
        "embed": emb,  # <-   FIXED: pass the object, not a string
    }
)


# 3️⃣ Simple prompt that prepends retrieved memories
def prompt(state):
    query = state["messages"][-1]["content"]
    memories = store.search(("memories",), query=query)
    sys = f"## Memories\n{memories}\n\n"
    return [{"role": "system", "content": sys}, *state["messages"]]


# 4️⃣ Build agent with hot-path memory tool
agent = create_react_agent(
    "openai:gpt-3.5-turbo",  # name ignored by Koboldcpp
    prompt=prompt,
    tools=[create_manage_memory_tool(namespace=("memories",))],
    store=store,
    checkpointer=MemorySaver(),
)

if __name__ == "__main__":
    cfg = {"configurable": {"thread_id": "demo"}}

    # Teach a fact
    agent.invoke(
        {"messages": [{"role": "user", "content": "My favorite color is blue."}]},
        config=cfg,
    )

    # Ask to recall
    reply = agent.invoke(
        {"messages": [{"role": "user", "content": "What color do I like?"}]}, config=cfg
    )
    print(reply["messages"][-1]["content"])
