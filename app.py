import streamlit as st
import pandas as pd
import requests
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt

# ---------------- LOAD ENV ---------------- #
load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))

# ---------------- SESSION ---------------- #
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------- AI FUNCTION ---------------- #
def ask_ai(question, df):
    api_key = os.getenv("OPENROUTER_API_KEY")

    if not api_key:
        return None, "API key not found"

    prompt = f"""
You are a data analyst.

Dataset columns: {list(df.columns)}

Sample data:
{df.head().to_string()}

User question: {question}

STRICT RULES:
- Return ONLY ONE LINE of Python code
- No explanations
- No print()
- No variable assignment
- Use only df

Correct example:
df['Sales'].mean()
"""

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost",
            "X-Title": "Data Analyst Copilot"
        },
        json={
            "model": "openai/gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}]
        }
    )

    result = response.json()

    if "choices" not in result:
        return None, f"API Error: {result}"

    code = result["choices"][0]["message"]["content"]
    return code, None

# ---------------- CLEAN CODE ---------------- #
def clean_code(code):
    code = code.strip()
    code = code.replace("```python", "").replace("```", "")

    lines = code.split("\n")

    # Keep only lines with df
    lines = [line.strip() for line in lines if "df" in line]

    if not lines:
        return code

    line = lines[-1]

    # Remove assignment
    if "=" in line:
        line = line.split("=")[-1].strip()

    # Remove print
    if "print" in line:
        line = line.replace("print(", "").replace(")", "")

    return line

# ---------------- EXECUTE ---------------- #
def execute_code(code, df):
    try:
        result = eval(code)

        if isinstance(result, pd.Series):
            return result.to_frame()

        return result

    except Exception as e:
        return f"Execution error: {e}"

# ---------------- AUTO CHART ---------------- #
def auto_chart(result):
    try:
        if isinstance(result, (pd.DataFrame, pd.Series)):
            fig, ax = plt.subplots()
            result.plot(kind="bar", ax=ax)
            return fig
    except:
        return None
    return None

# ---------------- UI ---------------- #
st.title("🤖 AI Data Analyst Copilot")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("📊 Data Preview")
    rows = st.slider("Rows to view", 5, len(df), 5)
    st.dataframe(df.head(rows))

    st.subheader("📈 Data Summary")
    st.write(df.describe())

    # ---------------- QUERY ---------------- #
    query = st.text_input("💬 Ask a question about your data")

    if query:
        code, error = ask_ai(query, df)

        if error:
            answer = error
            chart = None

        else:
            cleaned_code = clean_code(code)
            result = execute_code(cleaned_code, df)
            chart = auto_chart(result)

            answer = f"**Generated Code:**\n\n```python\n{cleaned_code}\n```\n\n**Result:**\n{result}"

        st.session_state.chat_history.append({
            "question": query,
            "answer": answer,
            "chart": chart
        })

# ---------------- CHAT ---------------- #
st.subheader("💬 Chat History")

for chat in st.session_state.chat_history:
    st.markdown(f"**🧑 You:** {chat['question']}")
    st.markdown(f"**🤖 AI:** {chat['answer']}")

    if chat["chart"]:
        st.pyplot(chat["chart"])

# ---------------- CLEAR ---------------- #
if st.button("🗑 Clear Chat"):
    st.session_state.chat_history = []
    st.rerun()