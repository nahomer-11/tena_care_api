from dotenv import load_dotenv
import os
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
from .memory import memory
from .tools import get_tools


llm = ChatGoogleGenerativeAI(
    model = "gemini-1.5-flash",
    temprature =0.3,
    google_api_key=os.getenv("GEMINI_API_KEY"),
    verbose=True,
)

agent = initialize_agent(
    tools=get_tools(),
    llm=llm,
    memory=memory,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    verbose=True,
)

