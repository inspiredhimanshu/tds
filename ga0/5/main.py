from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import sys
import traceback
from io import StringIO

from openai import OpenAI


app = FastAPI(title="Code Interpreter with AI Error Analysis")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CodeRequest(BaseModel):
    code: str


class CodeResponse(BaseModel):
    error: List[int]
    result: str


class ErrorAnalysis(BaseModel):
    error_lines: List[int]


def execute_python_code(code: str) -> dict:
    old_stdout = sys.stdout
    redirected_output = StringIO()
    sys.stdout = redirected_output

    try:
        exec(code, {})
        output = redirected_output.getvalue()
        return {
            "success": True,
            "output": output,
            "error_lines": []
        }

    except Exception:
        exc_type, exc_value, exc_tb = sys.exc_info()
        output = traceback.format_exc()

        extracted = traceback.extract_tb(exc_tb)
        error_lines = []

        if extracted:
            last_user_frame = extracted[-1]
            error_lines = [last_user_frame.lineno]

        return {
            "success": False,
            "output": output,
            "error_lines": error_lines
        }

    finally:
        sys.stdout = old_stdout


def analyze_error_with_ai(code: str, traceback_str: str) -> List[int]:
    aipipe_token = os.getenv("AIPIPE_TOKEN")
    if not aipipe_token:
        return []

    client = OpenAI(
        api_key=aipipe_token,
        base_url="https://aipipe.org/openrouter/v1"
    )

    prompt = f"""
Return ONLY valid JSON.

Format:
{{"error_lines":[3]}}

Task:
Find the exact line number(s) in the USER CODE that caused the Python error.

Rules:
- Return JSON only
- No explanation
- No markdown
- Use traceback carefully
- Return only line numbers from the user code

USER CODE:
{code}

TRACEBACK:
{traceback_str}
"""

    try:
        response = client.chat.completions.create(
            model="google/gemini-2.0-flash-lite-001",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You output strict JSON only."},
                {"role": "user", "content": prompt},
            ],
            temperature=0,
        )

        content = response.choices[0].message.content
        parsed = ErrorAnalysis.model_validate_json(content)
        return parsed.error_lines

    except Exception:
        return []


@app.get("/")
def home():
    return {"message": "Code Interpreter API is running"}


@app.post("/code-interpreter", response_model=CodeResponse)
def code_interpreter(request: CodeRequest):
    execution = execute_python_code(request.code)

    if execution["success"]:
        return {
            "error": [],
            "result": execution["output"]
        }

    error_lines = execution["error_lines"]

    if not error_lines:
        error_lines = analyze_error_with_ai(request.code, execution["output"])

    return {
        "error": error_lines,
        "result": execution["output"]
    }