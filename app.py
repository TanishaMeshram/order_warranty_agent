import streamlit as st
from receipt_parser import parse_receipt
from tools import (
    calculate_return_warranty,
    check_order_status
)
from agent import ask_agent


st.set_page_config(
    page_title="Order & Warranty Assistant",
    page_icon="🛍️",
    layout="wide"
)


st.title("🛍️ Order & Warranty Assistant")

st.write(
    "Your AI-powered assistant for orders, returns and warranties."
)


with st.sidebar:

    st.header("📌 How it works")

    st.write("1. Upload your receipt")
    st.write("2. View your order details")
    st.write("3. Check order status")
    st.write("4. Check return & warranty")
    st.write("5. Ask the AI Assistant")

    st.divider()

    st.info(
        "🔒 Your receipt is processed locally "
        "by this application."
    )


uploaded_file = st.file_uploader(
    "📄 Upload your receipt",
    type=["txt"]
)


if uploaded_file:

    try:
        receipt = uploaded_file.read().decode("utf-8")
        result = parse_receipt(receipt)

    except Exception as e:
        st.error(
            "❌ Could not read this receipt. "
            "Please upload a valid receipt file."
        )
        st.stop()

    # Receipt Details

    st.header("📋 Receipt Details")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Order ID",
            result["order_id"]
        )

        st.metric(
            "Customer",
            result["customer"]
        )

    with col2:

        st.metric(
            "Purchase Date",
            result["purchase_date"]
        )

        st.metric(
            "Total Paid",
            f"₹{result['total_paid']}"
        )


    st.divider()


    # Items

    st.header("🛒 Items")

    for item in result["items"]:

        st.write(
            f"**{item['name']}**"
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.write(
                f"Category: {item['category']}"
            )

        with col2:
            st.write(
                f"Quantity: {item['quantity']}"
            )

        with col3:
            st.write(
                f"Price: ₹{item['unit_price']}"
            )


    st.divider()


    # Order Status

    st.header("📦 Order Status")

    order_status = check_order_status.invoke(
        result["order_id"]
    )

    st.success(order_status)


    # Return & Warranty

    st.header("🛡️ Return & Warranty")

    for item in result["items"]:

        warranty_result = calculate_return_warranty.invoke({
            "purchase_date": result["purchase_date"],
            "category": item["category"]
        })

        st.info(
        f"🛍️ **{item['name']}**\n\n"
        f"📂 **Category:** {item['category']}\n\n"
        f"🛡️ {warranty_result}"
    )


    st.divider()


    # AI Assistant

    st.header("🤖 AI Assistant")

    st.write(
        "Ask questions about your order, "
        "returns, warranties or store policies."
    )

    question = st.text_input(
        "💬 Your question"
    )

    if st.button("Ask AI 🤖"):

        if question:

            with st.spinner("AI is thinking..."):

                answer = ask_agent(
                    question,
                    result["purchase_date"],
                    result["items"][0]["category"]
                )

            st.write(answer)

        else:

            st.warning(
                "Please enter a question."
            )