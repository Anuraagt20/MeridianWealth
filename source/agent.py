import json

from langchain.agents import create_agent

from langchain_core.tools import tool

from langchain_openai import ChatOpenAI

from source.config import OPENAI_API_KEY

from source.database_queries import (
    query_db,
    get_client_portfolio,
    search_market_data
)

from source.rag_pipeline import (
    retrieve_context
)


def get_llm():

    return ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=OPENAI_API_KEY
    )


@tool
def portfolio_lookup(
    client_id: str
) -> str:
    """
    Retrieve portfolio information
    for a client.
    """

    portfolio = get_client_portfolio(
        client_id.upper()
    )

    if not portfolio:

        return (
            f"Client {client_id} "
            f"not found."
        )

    return json.dumps(
        portfolio,
        indent=2,
        default=str
    )


@tool
def market_data_search(
    query: str
) -> str:
    """
    Search market data.
    """

    results = search_market_data(
        query
    )

    if not results:

        return (
            "No market data found."
        )

    return json.dumps(
        results,
        indent=2,
        default=str
    )


@tool
def policy_retriever(
    query: str
) -> str:
    """
    Search policy documents.
    """

    docs = retrieve_context(
        query
    )

    if not docs:

        return (
            "No policy information found."
        )

    return "\n\n".join(
        d.page_content
        for d in docs
    )


TOOLS = [
    portfolio_lookup,
    market_data_search,
    policy_retriever
]


SYSTEM_PROMPT = """
You are a senior Financial Analyst.

Available tools:

1. portfolio_lookup
2. market_data_search
3. policy_retriever

Responsibilities:

- Portfolio analysis
- Market analysis
- Policy compliance checks
- Client briefing preparation

Always use policy_retriever
before giving policy advice.

Use exact values from tools.

Do not fabricate information.
"""


AGENT = create_agent(
    model=get_llm(),
    tools=TOOLS,
    system_prompt=SYSTEM_PROMPT
)


def run_agent(
    query: str
):

    result = AGENT.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": query
                }
            ]
        }
    )

    final_message = result[
        "messages"
    ][-1]

    return final_message.content


def get_agent_info():

    return {
        "agent_name":
            "Financial Analyst Agent",

        "model":
            "gpt-4o-mini",

        "database":
            "SQLite",

        "vector_store":
            "FAISS",

        "status":
            "active"
    }