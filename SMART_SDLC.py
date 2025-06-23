import streamlit as st
from ibm_watsonx_ai.foundation_models import Model
import fitz  # PyMuPDF for PDF reading
import pandas as pd
import json

# --- IBM Watsonx Credentials ---
api_key = "DUmrdgim1LtffxQS89Pzk4Q8FF02MKixH4qJ18Mcr629"
project_id = "c6c1fddb-370c-4685-b247-fc9086d61a6d"
base_url = "https://eu-de.ml.cloud.ibm.com"
model_id = "ibm/granite-3-3-8b-instruct"

# --- Streamlit App Config ---
st.set_page_config(page_title="SmartSDLC", layout="wide")
st.title("💡 SmartSDLC - AI-Enhanced Software Development Lifecycle")

# --- Chat history (for chatbot only) ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Watsonx Query Function ---
def ask_watsonx(prompt):
    try:
        model = Model(
            model_id=model_id,
            credentials={"apikey": api_key, "url": base_url},
            project_id=project_id
        )

        result = model.generate_text(
            prompt=prompt,
            params={
                "max_new_tokens": 500,
                "temperature": 0.7,
                "top_p": 1.0,
                "decoding_method": "sample"
            }
        )

        if isinstance(result, dict):
            return result.get("generated_text", "⚠️ No 'generated_text' in response.")
        elif isinstance(result, str):
            try:
                parsed = json.loads(result)
                return parsed.get("generated_text", result)
            except json.JSONDecodeError:
                return result
        else:
            return "⚠️ Unexpected response type."
    except Exception as e:
        return f"❌ Watsonx Error: {str(e)}"

# --- Sidebar Menu ---
st.sidebar.title("📂 SDLC Modules")
module = st.sidebar.radio("Choose a module", [
    "Requirement Upload & Classification",
    "AI Code Generator",
    "Bug Fixer",
    "Test Case Generator",
    "Code Summarizer",
    "Chat Assistant"
])
st.write("Module selected:", module)
# --- Deduplicate and clean Watsonx output ---
def clean_code_output(raw_output):
    # Remove markdown wrappers
    cleaned = raw_output.replace("```python", "").replace("```", "").strip()
    
    # Remove duplicated lines while preserving order
    seen = set()
    final_lines = []
    for line in cleaned.splitlines():
        if line not in seen:
            seen.add(line)
            final_lines.append(line)
    
    return "\n".join(final_lines)

# --- Module 1: Requirement Upload & Classification ---
if module == "Requirement Upload & Classification":
    st.subheader("📥 Upload Requirements Document")
    uploaded_file = st.file_uploader("Upload a PDF with raw requirements", type="pdf")
    if uploaded_file:
        raw_text = ""
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        for page in doc:
            raw_text += page.get_text()

        st.success("✅ Text extracted from PDF.")
        prompt = f"Classify the following software requirements into SDLC phases (Requirements, Design, Development, Testing, Deployment) and convert into structured user stories:\n{raw_text}"
        output = ask_watsonx(prompt)
        st.text_area("🧾 Structured User Stories by SDLC Phase", output, height=400)

# --- Module 2: AI Code Generator ---
elif module == "AI Code Generator":
    st.subheader("💻 Generate Code from Prompt")
    user_prompt = st.text_area("Describe what the code should do")
    if st.button("Generate Code") and user_prompt:
        prompt = f"Generate only the implementation code (do not include test cases, markdown, or explanations):\n{user_prompt}"
        code = ask_watsonx(prompt)
        
        # Optional: Strip markdown if model still returns it
        code = code.strip().replace("```python", "").replace("```", "")
        
        st.code(code, language="python")

# --- Module 3: Bug Fixer ---


elif module == "Bug Fixer":
    st.subheader("🪲 Fix Buggy Code")
    buggy_code = st.text_area("Paste your buggy code here")
    if st.button("Fix Code") and buggy_code:
        prompt = f"Fix the following Python code. Return only the corrected code (no explanations, no markdown, no duplicates):\n{buggy_code}"
        raw_fix = ask_watsonx(prompt)
        fixed_code = clean_code_output(raw_fix)
        st.code(fixed_code, language="python")

# --- Module 4: Test Case Generator ---
elif module == "Test Case Generator":
    st.subheader("🧪 Generate Test Cases")
    code_input = st.text_area("Paste the function or requirement for test generation")
    if st.button("Generate Test Cases") and code_input:
        prompt = f"Generate unit test cases using Python's unittest or pytest for:\n{code_input}"
        test_cases = ask_watsonx(prompt)
        st.code(test_cases, language="python")

# --- Module 5: Code Summarizer ---
elif module == "Code Summarizer":
    st.subheader("📄 Summarize Code")
    code_to_summarize = st.text_area("Paste the code to summarize")
    if st.button("Summarize") and code_to_summarize:
        prompt = f"Summarize the following code snippet with an explanation and use case:\n{code_to_summarize}"
        summary = ask_watsonx(prompt)
        st.text_area("🧠 Summary", summary, height=300)

# --- Module 6: Chat Assistant ---
elif module == "Chat Assistant":
    st.subheader("💬 Ask Your SDLC Assistant")
    user_query = st.chat_input("Ask anything about SDLC, testing, coding, etc.")
    if user_query:
        st.session_state.chat_history.append(("user", user_query))
        response = ask_watsonx(f"User: {user_query}\nAssistant:")
        st.session_state.chat_history.append(("assistant", response))

    for role, msg in st.session_state.chat_history:
        with st.chat_message(role):
            st.markdown(msg)
