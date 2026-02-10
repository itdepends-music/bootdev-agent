import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from config import SYSTEM_PROMPT
from function_schemas import (
    schema_get_file_content,
    schema_get_files_info,
    schema_run_python_file,
    schema_write_file,
)
from functions import call_function

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("API key not found")

client = genai.Client(api_key=api_key)

available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
for _ in range(20):
    content = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=SYSTEM_PROMPT
        ),
    )

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {content.usage_metadata.prompt_token_count}")  # type: ignore
        print(f"Response tokens: {content.usage_metadata.candidates_token_count}")  # type: ignore

    if content.candidates is not None:
        for candidate in content.candidates:
            messages.append(candidate.content)

    if content.function_calls is None:
        print(content.text)
        exit(0)
    else:
        function_results = []
        for function_call in content.function_calls:
            function_call_result = call_function(function_call)

            if len(function_call_result.parts) == 0:
                raise Exception("empty .parts list")
            function_response = function_call_result.parts[0].function_response
            if function_call_result.parts[0].function_response is None:
                raise Exception("function_response is None")
            if function_call_result.parts[0].function_response.response is None:
                raise Exception("function_response.response is None")
            function_results.append(function_call_result.parts[0])

            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")

        messages.append(types.Content(role="user", parts=function_results))

exit(1)  # reached maximum number of iterations
