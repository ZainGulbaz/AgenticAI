from langchain_tavily import TavilySearch

tool=TavilySearch(max_results=2);

response = tool.invoke("What is lang graph");

print(response);