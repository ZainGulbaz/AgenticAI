from typing import Annotated;
from typing_extensions import TypedDict;
import os;

from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages #Reducers
from langchain_groq import ChatGroq;

from dotenv import load_dotenv;

load_dotenv();

llm= ChatGroq(model="llama3-8b-8192");

class State(TypedDict):
    messages:Annotated[list,add_messages]
    
graph_builder=StateGraph(State)


def chat_bot(state:State):
    return {"messages":[llm.invoke(state["messages"])]}

#ADD Node
graph_builder.add_node("LLM_CHATBOT",chat_bot);

#ADD Edges
graph_builder.add_edge(START,"LLM_CHATBOT");
graph_builder.add_edge("LLM_CHATBOT",END);

#Compile Graph
graph = graph_builder.compile();

# response = graph.invoke({"messages":"Hi"});


for event in graph.stream({"messages":"Hi"}):
    # print(event);
    
    for value in event.values():
        print(value["messages"]);

    