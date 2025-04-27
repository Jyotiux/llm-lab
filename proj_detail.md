

### 📖 Project Title
> **Agentic Research Assistant using LangGraph, LLM, and External Tools**






### 🛠️ Environment Setup

```bash
python -m venv lenv
lenv\Scripts\activate  # (Windows) 
```
Install packages:

```bash
pip install streamlit langchain langgraph langchain_groq python-dotenv
```
(More depending on your LLM and tools, like `tavily-python`, etc.)

---

### 📋 Nodes in Your LangGraph

| Node             | Purpose                                                              |
|------------------|----------------------------------------------------------------------|
| **START**        | Start of graph (default LangGraph start node)                        |
| **AI Assistant** | (your `tool_calling_llm`) — decides whether to answer or use a tool   |
| **TOOLS**        | ToolNode (handles calling Wikipedia, Arxiv, Tavily)                  |
| **END**          | Terminates the conversation (when no tool call is needed)            |


### 🏗️ Full LangGraph Workflow
> **Start ➔ AI Assistant (Reasoning) ➔ (Tools if needed) ➔ End**

---

### 📜 State Schema and Message Handling
- Uses `TypedDict` and `Annotated` message types for clean flow
- Tracks user and assistant messages dynamically

---

### 🧠 AI Assistant Node (Main Brain)

This is the **reasoning step**:

```python
def tool_calling_llm(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}
```
- Takes input (`state`)
- Decides if a tool is needed
- Calls tool **OR** gives a direct reply

---

### 🧩 LangGraph Architecture Setup

```python
builder = StateGraph(State)

builder.add_node("tool_calling_llm", tool_calling_llm)  # AI Assistant node
builder.add_node("tools", ToolNode(tools))              # Tool node (Arxiv, Wiki, Tavily)

builder.add_edge(START, "tool_calling_llm")             # Start -> AI Assistant
builder.add_conditional_edges(
    "tool_calling_llm",
    tools_condition,                                    # If tool is called -> go to tools, else -> END
)
builder.add_edge("tools", END)                          # After tools, go to End

graph = builder.compile()
```

---

### 📚 Recap of Important Things:

- **START ➔ AI Assistant (tool_calling_llm) ➔ (Tools if needed) ➔ END**
- **Tools used**: Arxiv, Wikipedia, Tavily Internet Search
- **Reasoning + Acting**: AI first reasons whether tools are needed.

---
###  Directory Structure You Should Have

```plaintext
proj/
│
├── lenv/                     # your virtual env folder
├── tools/
│   ├── arxiv_tool.py
│   ├── wiki_tool.py
│   └── tavily_tool.py
├── agent.py                   # builds graph
├── app.py                     # streamlit UI
├── .env                       # API keys
└── requirements.txt           # (optional) dependencies
```

