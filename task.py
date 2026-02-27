from crewai import Task
from agents import financial_analyst

analyze_financial_document = Task(
    description="""
Analyze the following financial document:

{document}

User Query:
{query}

Provide:
- Key financial highlights
- Revenue and profitability insights
- Risk factors
- Investment outlook strictly based on document
- Clear limitations if information is missing
""",
    expected_output="""
Provide structured analysis:

1. Executive Summary
2. Financial Highlights
3. Risk Analysis
4. Investment Perspective
5. Limitations
""",
    agent=financial_analyst,
    async_execution=False,
)