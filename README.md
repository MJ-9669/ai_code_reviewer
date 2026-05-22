# 🕵️‍♂️ AI Code Review Agent

An autonomous, agentic AI pipeline that ingests GitHub repositories, parses source code using Abstract Syntax Trees (AST), and generates structured, confidence-rated code reviews using Google's Gemini LLM. 

Built in 3 days as part of an advanced AI engineering assignment.

## 🚀 Project Overview
This project goes beyond a simple LLM wrapper by implementing a fully orchestrated pipeline. Instead of feeding an entire repository into a context window blindly, this agent strategically clones the repository, uses Python's `ast` module to extract targeted functions and classes, and queries the LLM for precise, actionable feedback. 

**The Creative Twist:** Every generated review includes a `confidence_score` (0-100). The UI automatically buckets low-confidence reviews (under 80%) into a separate "Needs Verification" tab with a warning label, practicing production-grade epistemic humility.

## 🏗️ Architecture Diagram
The application follows a strict 4-stage sequential pipeline:

```text
[User Input: GitHub URL] 
       │
       ▼
1. INGESTION (GitPython)
   └─ Securely clones repo to local temp directory.
       │
       ▼
2. PARSING (Python AST)
   └─ Traverses files, extracts isolated functions & classes.
       │
       ▼
3. LLM REVIEW (Google GenAI / Gemini 1.5 Flash)
   ├─ Enforces strict JSON schema via Custom Prompting.
   ├─ Mitigates hallucinations via Regex JSON extraction.
   └─ Handles 429 Quota errors via Exponential Backoff.
       │
       ▼
4. DASHBOARD (Streamlit)
   ├─ Renders parsed metrics & actionable feedback.
   └─ Filters outputs by Severity and Confidence levels.```

```
## Setup Instructions

1. Clone the repository:

   ```
       git clone [https://github.com/MJ-9669/ai_code_reviewer.git]
       cd ai-code-reviewer
   ```

2. Install dependencies:

   It is recommended to use a Python virtual environment.
    ```
       pip install -r requirements.txt
    ```

3. Configure Environment Variables:

   Create a .env file in the root directory and add your Google Gemini API Key:

    ```
        GEMINI_API_KEY=your_actual_api_key_here
    ```
    
4. Run the Application:

   Launch the Streamlit dashboard:

    ```
       python -m streamlit run app.py
    ```


## Known Limitations

1. API Rate Limiting: Because the AST parser sends individual functions to the LLM concurrently, large repositories may trigger 429 (Too Many Requests) errors on free-tier LLM accounts. Mitigation applied: The pipeline includes an exponential backoff script that pauses execution for 20 seconds when limits are hit.

2. Context Isolation: Because the AST parser isolates functions, the LLM currently lacks global repository context (e.g., it might flag an unused variable that is actually imported and used in another file).

3. Language Support: Currently, the AST parser only supports .py (Python) files.


## What I Would Build Next (Future Scope)

With more time, I would expand this agent in the following ways:

1. GitHub API Integration: Instead of just a Streamlit dashboard, I would integrate PyGitHub to have the agent post these reviews directly as inline comments on live Pull Requests.

2. Multi-Language Support: Replace Python's native ast library with tree-sitter to support parsing JavaScript, Go, and Rust.

3. RAG-based Context: Implement a lightweight vector database (like ChromaDB) to store the entire repository. This would allow the LLM to cross-reference functions and understand global architecture before writing a review.
