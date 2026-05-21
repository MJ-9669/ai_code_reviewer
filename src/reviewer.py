import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class CodeReviewer:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")
            
        genai.configure(api_key=api_key)
        
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def review_code_chunk(self, file_name: str, chunk_type: str, chunk_name: str, code_content: str) -> list:
        """
        Sends a single code chunk to Gemini and demands a schema-valid JSON array of review comments.
        """
        system_prompt = (
            "You are an expert production-grade automated code review agent.\n"
            "Your task is to analyze the provided code snippet and return actionable, constructive feedback.\n\n"
            "CRITICAL REQUIREMENT: You must respond ONLY with a valid JSON object matching this exact structure:\n"
            "{\n"
            "  \"reviews\": [\n"
            "    {\n"
            "      \"line_number\": <int_or_null_relative_to_snippet>,\n"
            "      \"severity\": \"INFO\" | \"WARNING\" | \"CRITICAL\",\n"
            "      \"comment\": \"Clear explanation of the issue and how to fix it.\",\n"
            "      \"confidence_score\": <int_between_0_and_100>\n"
            "    }\n"
            "  ]\n"
            "}\n\n"
            "Rules for analysis:\n"
            "1. Focus on code quality, performance bugs, security vulnerabilities, and adherence to Python best practices (PEP 8).\n"
            "2. If the code looks pristine and has zero issues, return an empty array for \"reviews\".\n"
            "3. Be brutally honest with the confidence_score. If you are uncertain or making an assumption, lower the score below 50."
        )

        user_content = f"File: {file_name}\nType: {chunk_type}\nName: {chunk_name}\n\nCode Content:\n```python\n{code_content}\n```"
        
        full_prompt = f"{system_prompt}\n\n{user_content}"

        try:
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json",
                    temperature=0.2
                )
            )
            
            raw_json = response.text
            parsed_data = json.loads(raw_json)
            return parsed_data.get("reviews", [])

        except Exception as e:
            print(f"  [-] LLM analysis failed for {chunk_name}: {e}")
            return []



