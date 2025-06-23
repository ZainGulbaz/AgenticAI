from langchain_tavily import TavilySearch
from langgraph.graph.message import add_messages


from langchain_groq import ChatGroq;
from dotenv import load_dotenv;
import os

from typing import Annotated;
from typing_extensions import TypedDict;

from langgraph.graph import StateGraph,START,END;
from langgraph.prebuilt import ToolNode;
from langgraph.prebuilt import tools_condition;

load_dotenv();

llm=ChatGroq(model="llama3-8b-8192");

tavily_search_tool=TavilySearch(max_results=2);

tools=[tavily_search_tool];

llm_with_tools = llm.bind_tools(tools);

class State(TypedDict):
    messages:Annotated[list,add_messages]

builder=StateGraph(State);

#Tool Defination
def tool_calling_llm(state:State):
    return {"messages":[llm_with_tools.invoke(state["messages"])]};

builder.add_node("tool_calling_llm",tool_calling_llm);
builder.add_node("tools",ToolNode(tools));

builder.add_edge(START,"tool_calling_llm");
builder.add_conditional_edges("tool_calling_llm",tools_condition)

builder.add_edge("tools",END);

graph=builder.compile();

response=graph.invoke({"messages":"Give me latest news on NLP?"});

print(response["messages"][-1].content);