from langchain_ollama import ChatOllama
from tools import (
    check_order_status,
    calculate_return_warranty
)
from vector_store import search_policy
import re


llm = ChatOllama(
    model="qwen3:0.6b",
    temperature=0
)


def ask_agent(question, purchase_date=None, category=None):

    q = question.lower()

    # 1. Order status
    if "status" in q or "where is my order" in q:

        match = re.search(
            r"ORD-\d+",
            question.upper()
        )

        if match:
            return check_order_status.invoke(
                match.group()
            )

        return "Please provide your Order ID."


    # 2. Return/warranty calculation
    if (
        ("return" in q or "warranty" in q)
        and (
            "when" in q
            or "expire" in q
            or "expires" in q
            or "how long" in q
        )
    ):

        if purchase_date and category:

            return calculate_return_warranty.invoke({
                "purchase_date": purchase_date,
                "category": category
            })

        return "Please upload your receipt first."


    # 3. General store policy
    policy = search_policy(question)

    response = llm.invoke(
        f"""
You are a store customer-support assistant.

Answer the user's question using ONLY the store policy below.

STORE POLICY:
{policy}

USER QUESTION:
{question}
"""
    )

    return response.content