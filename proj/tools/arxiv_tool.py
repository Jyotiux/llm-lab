
from langchain_community.utilities import ArxivAPIWrapper
from langchain_community.tools import ArxivQueryRun

def get_arxiv_tool():
    api_wrapper_arxiv = ArxivAPIWrapper(top_k_results=2, doc_content_chars_max=500)
    arxiv = ArxivQueryRun(api_wrapper=api_wrapper_arxiv, description="Query Arxiv papers for latest research.")
    return arxiv
