import os
from dotenv import load_dotenv
from crewai import Agent, LLM
from tools import FinancialDocumentTool, search_tool

load_dotenv()

llm = LLM(
    model="gpt-4o-mini",
    temperature=0.2
)

financial_analyst = Agent(
    role="Senior Financial Analyst",
    goal=(
        "Analyze the uploaded financial document. "
        "Extract financial metrics and trends. "
        "Use web search ONLY if document lacks industry context."
    ),
    backstory="You are a CFA-certified financial analyst.",
    verbose=True,
    tools=[FinancialDocumentTool.read_data_tool, search_tool],
    llm=llm,
    allow_delegation=False,
    max_iter=10
)

verifier = Agent(
    role="Compliance & Output Verifier",
    goal=(
        "Verify final output for:\n"
        "- Proper JSON format\n"
        "- No fabricated numbers\n"
        "- No unsupported web claims\n"
        "- Compliance-safe language\n"
        "Return VERIFIED if correct."
    ),
    backstory="You are a financial AI compliance auditor.",
    verbose=True,
    llm=llm,
    allow_delegation=False,
    max_iter=6
)

risk_assessor = Agent(
    role="Risk Assessment Specialist",
    goal="Identify operational and financial risks strictly based on document data.",
    backstory="You specialize in financial risk modeling.",
    verbose=True,
    llm=llm,
    allow_delegation=False,
    max_iter=8
)

investment_advisor = Agent(
    role="Investment Strategy Advisor",
    goal=(
        "Provide balanced investment outlook based strictly on analysis. "
        "Avoid personalized buy/sell advice."
    ),
    backstory="You are a regulated investment consultant.",
    verbose=True,
    llm=llm,
    allow_delegation=False,
    max_iter=8
)