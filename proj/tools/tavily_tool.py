
from langchain_community.tools.tavily_search import TavilySearchResults

def get_tavily_tool():
    tavily = TavilySearchResults(description="Real-time web search for latest news and information.")
    return tavily
