import os

from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse

from prompts import system_prompt
from call_function import available_functions,call_function

load_dotenv()
def get_api_key(api_var):
    api_key = os.environ.get(api_var)
    if api_key is None:
        raise RuntimeError("No API key, enter a valid key.")
    return api_key

def get_token_used(response):
    if response.usage_metadata is None:
        raise RuntimeError("Couldnt fetch response metadata. Might be a failed request.")
    else:
        print(f'''
        Prompt tokens: {response.usage_metadata.prompt_token_count}
        Response tokens: {response.usage_metadata.candidates_token_count}
        ''')

def parse_prompt():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    return args


def send_prompt(api_key,prompt):
    client = genai.Client(api_key=api_key)
    response_test = client.models.generate_content(
        model='gemini-2.5-flash', contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions])

    )
    return response_test



def main():
    api_key = get_api_key('GEMINI_API_KEY')
    parsed_prompt = parse_prompt()
    user_prompt = parsed_prompt.user_prompt
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]
    llm_response = send_prompt(api_key,messages)
    functions_results_list = []
    if parsed_prompt.verbose:
        print(f"User prompt: {user_prompt}")
        get_token_used(llm_response)
    if llm_response.function_calls:
        for function_call in llm_response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
            function_call_result = call_function(function_call,parsed_prompt.verbose)
            if len(function_call_result.parts) < 1:
                raise Exception(f"doesnt have parts in function call results. function: {function_call.name}")
            if not function_call_result.parts[0].function_response:
                raise Exception(f"first part in response doesnt work. function: {function_call.name}")
            if not function_call_result.parts[0].function_response.response:
                raise Exception(f"no response in first part. function: {function_call.name} ")
            functions_results_list.append(function_call_result.parts[0])
            if parsed_prompt.verbose is True:
                print(f"-> {function_call_result.parts[0].function_response.response}")

    else:
        print(llm_response.text)

main()


