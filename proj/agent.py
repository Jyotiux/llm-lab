# agent.py

from langchain_community.tools import ArxivQueryRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper, ArxivAPIWrapper
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage
from typing_extensions import TypedDict
from typing import Annotated
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set API keys
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Import tools from tools folder
from tools.arxiv_tool import get_arxiv_tool
from tools.wiki_tool import get_wiki_tool
from tools.tavily_tool import get_tavily_tool

# Initialize the tools
arxiv = get_arxiv_tool()
wiki = get_wiki_tool()
tavily = get_tavily_tool()

# Combine tools
tools = [arxiv, wiki, tavily]

# Initialize LLM
llm = ChatGroq(model="qwen-qwq-32b")
llm_with_tools = llm.bind_tools(tools=tools)

# State Schema
class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]

# Tool-calling node
def tool_calling_llm(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# Build LangGraph
def create_graph():
    builder = StateGraph(State)
    builder.add_node("tool_calling_llm", tool_calling_llm)
    builder.add_node("tools", ToolNode(tools))

    ## Edgess
    builder.add_edge(START, "tool_calling_llm")
    builder.add_conditional_edges(
        "tool_calling_llm",
        # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
        # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
        tools_condition,
    )
    builder.add_edge("tools", "tool_calling_llm")

    graph = builder.compile()
    # builder = StateGraph(State)
    # builder.add_node("tool_calling_llm", tool_calling_llm)
    # builder.add_node("tools", ToolNode(tools))

    # builder.add_edge(START, "tool_calling_llm")
    # builder.add_conditional_edges("tool_calling_llm", tools_condition)
    # builder.add_edge("tools", END)

    # graph = builder.compile()
    return graph

# Create the graph
graph = create_graph()


# ### Node definition
# def tool_calling_llm(state:State):
#     return {"messages":[llm_with_tools.invoke(state["messages"])]}

# # Build graph
# builder = StateGraph(State)
# builder.add_node("tool_calling_llm", tool_calling_llm)
# builder.add_node("tools", ToolNode(tools))

# ## Edgess
# builder.add_edge(START, "tool_calling_llm")
# builder.add_conditional_edges(
#     "tool_calling_llm",
#     # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
#     # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
#     tools_condition,
# )
# builder.add_edge("tools", "tool_calling_llm")

# graph = builder.compile()

# # View
# display(Image(graph.get_graph().draw_mermaid_png()))