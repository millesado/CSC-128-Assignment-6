"""
CSC-128 Assignment 6: Grounded Policy Bot
Michelle Salgado

Sunny Days Childcare Policy Bot
"""

import streamlit as st
from groq import Groq

from retriever import Retriever


# Create the retriever
retriever = Retriever()


# Set up the Groq client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

st.set_page_config(
    page_title="Sunny Days Childcare Policy Bot",
    page_icon="☀️"
)

st.title("☀️ Sunny Days Childcare Policy Bot")

st.write(
    "Ask a question about Sunny Days Childcare policies. "
    "I will only answer using information from the parent handbook."
)
# Get a question from the user
question = st.text_input(
    "Ask a question:",
    placeholder="Example: What time do I need to pick up my child?"
)

if question:
    # Search the knowledge base first
    hits = retriever.search(question)

    # Short circuit: do not call the model if retrieval found nothing
    if not hits:
        st.warning(
            "I don't have enough information in the Sunny Days Parent "
            "Handbook to answer that question."
        )
    else:
        # Build context only from the retrieved handbook information
        context = retriever.build_context(hits)

        # Grounding prompt: the model may only use the retrieved context
        prompt = f"""
You are the Sunny Days Childcare Policy Bot.

Answer the parent's question using ONLY the information in the
retrieved handbook context below.

Do not use outside knowledge.
Do not guess or invent policies, rules, or other details.
Never guess numbers, dates, times, fees, ages, ratios, or quantities.

If the context does not contain enough information to answer the
question, say exactly:
"I don't have enough information in the Sunny Days Parent Handbook to answer that question."

--- RETRIEVED HANDBOOK CONTEXT ---
{context}
--- END RETRIEVED HANDBOOK CONTEXT ---

--- PARENT QUESTION ---
{question}
--- END PARENT QUESTION ---
"""
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        answer = response.choices[0].message.content

        st.subheader("Answer")
        st.write(answer)

        # Display source attribution
        st.subheader("Source")
        for document, score in hits:
            st.write(document["source"])