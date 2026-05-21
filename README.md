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
   └─ Filters outputs by Severity and Confidence levels.
