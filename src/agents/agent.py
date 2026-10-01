from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.tools.tools import web_search, scrape_url
from dotenv import load_dotenv
import os
load_dotenv()

# Model Initialization

def get_llm(model_name: str = None, api_key: str = None) -> ChatGoogleGenerativeAI:
    selected_model = model_name or os.getenv("GEMINI_MODEL") or "models/gemini-3.5-flash-lite"
    key = api_key or os.getenv("GEMINI_API_KEY")
    return ChatGoogleGenerativeAI(
        model=selected_model,
        api_key=key,
        max_retries=2,
    )

llm = get_llm()


# 1st Agent: Search Agent 
def build_search_agent(model=None):
    return create_agent(
        model=model or llm,
        tools=[web_search],
    )


# 2nd Agent: Reader Agent
def build_reader_agent(model=None):
    return create_agent(
        model=model or llm,
        tools=[scrape_url],
    )

# writer chain
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer. Write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on the topic below.

    Topic: {topic}

    Research Gathered: {research}

    Structure the report as:
    - Introduction
    - Key Findings (minimum 3 well-explained points)
    - Conclusion
    - Sources (List all URLs found in the research)

    Be detailed, factual and professional."""),
])

def build_writer_chain(model=None):
    return writer_prompt | (model or llm) | StrOutputParser()

writer_chain = build_writer_chain()


# Critic chain
critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

    Report:{report}

    Respond in this exact format:

    Score: X/10;

    Strengths:
    - ...
    - ...

    Areas to improve:
    - ...
    - ...

    One Line Verdict: ...
"""),
])

def build_critic_chain(model=None):
    return critic_prompt | (model or llm) | StrOutputParser()

critic_chain = build_critic_chain()



