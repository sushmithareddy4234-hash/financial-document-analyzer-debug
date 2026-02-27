import os
from dotenv import load_dotenv
load_dotenv()

from crewai import Agent, LLM

# ✅ Correct Groq model
llm = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)

financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal="Carefully analyze the provided financial document and deliver accurate insights strictly based on the document and the user query: {query}",
    verbose=True,
    memory=False,
    backstory=(
        "You are a professional financial analyst. "
        "You carefully read financial statements and risk disclosures. "
        "You never fabricate information. "
        "You only use the provided document content. "
        "If information is missing, you clearly state limitations."
    ),
    llm=llm,
    max_iter=1,
    allow_delegation=False
)