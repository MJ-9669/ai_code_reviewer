import os
import json
import time
import re
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

class CodeReviewer:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")
            
        self.client = genai.Client(api_key=api_key)
        self.model_id = 'gemini-flash-latest'

    def review_code_chunk(self, file_name: str, chunk_type: str, chunk_name: str, code_content: str, retries: int = 4) -> list:
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
            "1. Focus on code quality, performance bugs, security vulnerabilities, and adherence to Python best practices.\n"
            "2. If the code looks pristine and has zero issues, return an empty array for \"reviews\".\n"
            "3. Be brutally honest with the confidence_score."
        )

        user_content = f"File: {file_name}\nType: {chunk_type}\nName: {chunk_name}\n\nCode Content:\n```python\n{code_content}\n```"
        full_prompt = f"{system_prompt}\n\n{user_content}"

        for attempt in range(retries):
            raw_text = ""
            try:
                time.sleep(2)
                
                response = self.client.models.generate_content(
                    model=self.model_id,
                    contents=full_prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.2,
                    )
                )
                
                raw_text = response.text
                if not raw_text:
                    raise ValueError("Empty response received from Gemini.")
                
                match = re.search(r'\{.*\}', raw_text, re.DOTALL)
                
                if not match:
                    raise ValueError(f"No JSON structure found in output. Output was: {raw_text[:100]}...")
                    
                json_str = match.group(0)
                parsed_data = json.loads(json_str)
                return parsed_data.get("reviews", [])

            except Exception as e:
                error_message = str(e)
                
                if "429" in error_message or "Quota" in error_message:
                    wait_time = 20
                    print(f"  [~] API Rate Limit hit. Pausing for {wait_time} seconds before retrying...")
                    time.sleep(wait_time)
                
                elif attempt < retries - 1:
                    print(f"  [~] Attempt {attempt + 1} failed for {chunk_name}, retrying in 3s...")
                    time.sleep(3)
                
                else:
                    print(f"  [-] LLM failed for {chunk_name} after {retries} attempts.")
                    print(f"      Error: {error_message}")
                    return []
                    



