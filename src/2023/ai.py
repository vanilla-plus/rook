import sys
import requests
import json
import os
import argparse
from requests import Response
from pathlib import Path

def main():

    # Argument definitions
    
    parser = argparse.ArgumentParser()

    parser.add_argument('prompt', help='Prompt to send to the model')
    parser.add_argument('-m', '--model', choices=['ada', 'babbage', 'chat'], default='ada', help='Model to use')
    # parser.add_argument('-c', '--command', choices=['fix', 'comment', 'complete'], default='complete', help='Command to execute')    
    parser.add_argument('-i', '--inputPath', help='Text file path to read content from. Text will be automatically added to the end of the prompt.')
    parser.add_argument('-o', '--outputPath', help='Text file path to write response into.')
    parser.add_argument('-t', '--temperature', type=float, default=0.7, help='Temperature of the model')
    parser.add_argument('-max', '--maxTokens', type=int, default=100, help='Maximum number of tokens to generate')
    parser.add_argument('-d', '--debug', action='store_true', default=False, help='Turn on debug mode')
    
    args = parser.parse_args()

    # Check if the specified model is valid
    
    model_map = {
        "ada": "text-ada-001",
        "babbage": "text-babbage-001",
        "chat": "gpt-3.5-turbo",
    }

    model = model_map[args.model]
    
    # Local prompt
    
    prompt = args.prompt

    # Initialize file_content with a default value (empty string)
    file_content = ""

    # Check if inputPath is present
    if args.inputPath is not None:
        # Read the file content
        with open(args.inputPath, 'r') as file:
            file_content = file.read()
            prompt = prompt + '\n\n' + file_content
            
    # def complete():
    #     # Implement the 'complete' command functionality here
    #     pass
    # 
    # def fix():
    #     # Implement the 'fix' command functionality here
    #     pass
    # 
    # def comment():
    #     # Implement the 'comment' command functionality here
    #     pass
    # 
    # # Map the commands to their corresponding functions
    # command_map = {
    #     "complete": complete,
    #     "fix": fix,
    #     "comment": comment
    # }
    # 
    # # Execute the appropriate function based on the command
    # command_function = command_map[args.command]
    # command_function()

    if args.debug:
        print(" 🧑🏽‍🌾 Full prompt:\n\n", prompt)

    # Make an API call to OpenAI using requests
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}",
    }
    data = {
        "prompt": prompt,
        "max_tokens": args.maxTokens,
        "n": 1,
        "stop": None,
        "temperature": args.temperature,
    }
    
    response = ''
    
    #if args.debug:
    #    response = Response()
    #    response.status_code = 200
    #    response._content = json.dumps({'id': 'cmpl-71Y5i5dKU9pmwncmZoV4BpqBcsK3L', 'object': 'text_completion', 'created': 1680603730, 'model': 'text-ada-001', 'choices': [{'text': '\n\nI like to sing-a,\nAbout the Sun-a\nAnd the Winter-a\n\nI like to sing-a,\nAbout the Earth-a\nAnd the Sun-a\nAnd the Moon-a', 'index': 0, 'logprobs': None, 'finish_reason': None}], 'usage': {'prompt_tokens': 52, 'completion_tokens': 48, 'total_tokens': 100}}).encode()
    #else:
    response = requests.post(f"https://api.openai.com/v1/engines/{model}/completions", headers=headers, json=data)

    # Check if the response is successful
    if response.status_code != 200:
        print(f"Error: {response.status_code}\n{response.text}")
        sys.exit(1)

    # Parse the response JSON
    response_json = response.json()
    
    # Extract the AI response
    ai_response = response_json['choices'][0]['text'].strip()

    # Print the AI response
    if args.debug:
        print("\n 🌾 Raw response:\n\n", response_json)
        print("\n 🍞 Extracted response:\n\n", ai_response)
    else:
        print("\n" + ai_response + '\n')

    # print("Current file location:", os.path.abspath(__file__)) <-- get the local file path like this
        
    if args.outputPath is None:
        pass
    else:
        # Ask the user for input
        user_input = input(f"Do you want to write this to {args.outputPath}? Y/N")

        # Check if the input is "Y", "return" (Enter key), or "N"
        if user_input.lower() == 'y' or user_input == '':
            # Write to the file
            print("Writing to the file...")
    
            with open(args.outputPath, 'w') as file:
                file.write(ai_response)


if __name__ == "__main__":
    main()
