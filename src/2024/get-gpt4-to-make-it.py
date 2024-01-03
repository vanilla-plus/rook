import json

from pprint import pprint

from openai import OpenAI

client = OpenAI()

# Define your functions as a part of the payload
functions = [
    {
        "name": "get_current_time",
        "description": "Get the current time",
    },
    {
        "name": "tell_a_joke",
        "description": "Tell a random joke",
    },
    {
        "name": "read_file",
        "description": "Read a file from a given filepath",
        "parameters": {
            "type": "object",
            "properties": {
                "filepath": {"type": "string", "description": "The file path to read"}
            },
            "required": ["filepath"],
        },
    },
]


def get_current_time():
    return "The current time is 12:00 PM."


def tell_a_joke():
    return "What do you call a fish with no eyes? A fsh."


def read_file(filepath):
    with open(filepath, "r") as f:
        return f.read()


function_map = {
    "get_current_time": get_current_time,
    "tell_a_joke": tell_a_joke,
    "read_file": read_file,
}


# Initialize messages list with system message
messages = [{"role": "system", "content": "You are a helpful AI assistant."}]

# Main chat loop
while True:
    user_input = input("User: ")
    user_message = {"role": "user", "content": user_input}
    messages.append(user_message)

    # Send the input to the OpenAI API along with the functions and the entire conversation history
    response = client.chat.completions.create(
        model="gpt-3.5-turbo", messages=messages, functions=functions
    )

    # Extract the response
    message = response.choices[0].message

    pprint(message)

    # Check if the response includes a function call
    function_call = message.function_call

    if function_call:
        function_name = function_call.name
        function_args = function_call.arguments
        function_args_obj = json.loads(function_args)
        function_result = function_map[function_name](**function_args_obj)
        function_response = {
            "role": "function",
            "name": function_name,
            "content": function_result,
        }
        messages.append(function_response)
        print("Bot:", function_result)
    else:
        # Append the assistant's message to the conversation history
        messages.append({"role": "assistant", "content": message.content})
        print("Bot:", message.content)
