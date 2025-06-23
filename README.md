# 💡 SmartSDLC - AI-Enhanced Software Development Lifecycle

SmartSDLC is a powerful AI assistant that streamlines software development tasks by leveraging IBM Watsonx's Granite LLM models. This Streamlit web application offers a suite of intelligent SDLC modules to assist developers and product teams at every phase.

---

## 🚀 Features

This AI-powered assistant includes the following modules:

1. **📥 Requirement Upload & Classification**
   - Upload PDF requirement documents.
   - Automatically extract and classify content into SDLC phases.
   - Generates structured user stories from raw requirements.

2. **💻 AI Code Generator**
   - Converts natural language prompts into working Python code.

3. **🪲 Bug Fixer**
   - Automatically detects and corrects issues in your code snippets.

4. **🧪 Test Case Generator**
   - Generates unit test cases using `unittest` or `pytest` based on your code or requirements.

5. **📄 Code Summarizer**
   - Produces concise summaries and explanations for given code snippets.

6. **💬 Chat Assistant**
   - Interactive chatbot for any SDLC-related queries or coding help.

---

## 🧰 Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **AI Backend**: [IBM Watsonx.ai](https://www.ibm.com/products/watsonx-ai) with Granite LLMs
- **PDF Parsing**: [PyMuPDF (fitz)](https://pymupdf.readthedocs.io/)
- **Language**: Python 3.12+

---

## 🔐 IBM Watsonx Setup

To run this app, you need to configure IBM Watsonx credentials:

```python
api_key = "<YOUR_API_KEY>"
project_id = "<YOUR_PROJECT_ID>"
base_url = "https://<your-region>.ml.cloud.ibm.com"
model_id = "ibm/granite-3-3-8b-instruct"
