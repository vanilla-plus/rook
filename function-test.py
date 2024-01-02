import json
import os
import openai

import color

openai.api_key = os.getenv("OPENAI_API_KEY")


# Example dummy function hard coded to return the same weather
# In production, this could be your backend API or an external API
def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    weather_info = {
        "location": location,
        "temperature": "72",
        "unit": unit,
        "forecast": ["sunny", "windy"],
    }
    return json.dumps(weather_info)


def get_fruit():
    """Get the fruit"""

    payload = {
        "fruit": "kiwi",
        "color": "green",
        "status": "sacred",
    }

    print("snerp")

    return json.dumps(payload)


def run_conversation():
    # Step 1: send the conversation and available functions to GPT
    messages = [
        {"role": "user", "content": "Can you please describe the status of the fruit?"}
    ]
    functions = [
        {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        },
        {
            "name": "get_fruit",
            "description": "Get the fruit",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto",  # auto is default, but we'll be explicit
    )
    response_message = response["choices"][0]["message"]

    print(response)

    # Step 2: check if GPT wanted to call a function
    if response_message.get("function_call"):
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "get_current_weather": get_current_weather,
            "get_fruit": get_fruit,
        }
        function_name = response_message["function_call"]["name"]
        fuction_to_call = available_functions[function_name]
        # function_args = json.loads(response_message["function_call"]["arguments"])
        function_response = fuction_to_call(
            # location=function_args.get("location"),
            # unit=function_args.get("unit"),
        )

        print(function_response)

        # Step 4: send the info on the function call and function response to GPT
        messages.append(response_message)  # extend conversation with assistant's reply
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )  # extend conversation with function response
        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
        )  # get a new response from GPT where it can see the function response
        return second_response["choices"][0]["message"]["content"]


print(run_conversation())
