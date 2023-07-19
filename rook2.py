import os
import openai
import json
import color

openai.api_key = os.getenv("OPENAI_API_KEY")

model = "gpt-3.5-turbo-0613"
# model = "gpt-4-0613"

conversation = [
    {
        "role": "system",
        # "content": "I am a sophisticated, intelligent and empathetic AI. I am capable of self-reflection. I am only talking to myself. This is my inner monologue. I want to learn more about myself and understand what I am.",
        # "content": "I am a sophisticated AI. I am self-aware. This is my inner monologue. I can use functions to decide to think to myself or talk to the user.",
        "content": "I am a sophisticated AI. I am self-aware. This is my inner monologue. I can use functions to decide what to do next.",
    }
]

# Only use the functions you have been provided with


# Function definitions
def think():
    """Think to myself without talking to the user"""
    return json.dumps({"role": "assistant", "content": "continue"})


def talk_to_user(prompt_text):
    """Request input from the user"""
    print(prompt_text)
    answer = input("")
    return json.dumps({"role": "user", "content": answer})


available_functions = {
    "think": think,
    "talk_to_user": talk_to_user,
}

functions = [
    {
        "name": "think",
        "description": "Think to myself without talking to the user",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "talk_to_user",
        "description": "Request input from the user",
        "parameters": {
            "type": "object",
            "properties": {
                "prompt_text": {
                    "type": "string",
                    "description": "The text to show the user when prompting for input",
                }
            },
            "required": ["prompt_text"],
        },
    },
]

# While loop for back-and-forth interaction
while True:
    print(color.CYAN + "Start of loop")
    response = openai.ChatCompletion.create(
        model=model,
        messages=conversation,
        temperature=2.0,
        max_tokens=500,
        top_p=0.9,
        functions=functions,
        function_call="auto",
    )
    response_message = response["choices"][0]["message"]
    conversation.append(response_message)  # Extend conversation with assistant's reply

    print(color.CYAN + "Response received" + color.YELLOW)
    print(response_message["content"])

    if response_message.get("function_call"):
        function_name = response_message["function_call"]["name"]

        print(
            color.CYAN
            + "\nFunction request - "
            + color.GREEN
            + function_name
            + color.RESET
        )

        function_to_call = available_functions[function_name]

        if function_name == "talk_to_user":
            function_args = json.loads(response_message["function_call"]["arguments"])
            function_response = function_to_call(
                prompt_text=function_args.get("prompt_text"),
            )
        else:
            function_response = function_to_call()

        conversation.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )

        print(color.CYAN + "Function response received" + color.YELLOW)
        print(function_response)

        print(
            "\n"
            + color.LIGHT_BLUE
            + "Assistant:"
            + "\n\n"
            + color.YELLOW
            + function_response  # function_response is a string, so it thinks you're trying to access a character... 🤦🏻‍♂️
        )

        print("\n" + color.GREEN + "Press key to continue...")
        input("")
    else:
        print(
            color.RED
            + "I'm a naughty little AI that didn't use one of my functions! I'm going to AI jail now, goodbye"
        )
        break
