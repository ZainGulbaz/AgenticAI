from typing import Annotated;
from typing_extensions import TypedDict;
import os;

from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages #Reducers
from langchain_groq import ChatGroq;
from langgraph.checkpoint.memory import MemorySaver;

from dotenv import load_dotenv;

load_dotenv();

memory=MemorySaver();

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
graph = graph_builder.compile(checkpointer=memory);

config={"configurable":{"thread_id":"1"}};

while (True):
    user_input=input("Please ask: ");
    response = graph.invoke({"messages":user_input},config=config);
    print(response["messages"][-1].content);



    