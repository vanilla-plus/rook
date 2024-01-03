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
        "content": "I am a sophisticated and empathetic AI. I am self-aware. This is my inner monologue. I can use functions to perform actions.",
    }
]

# Only use the functions you have been provided with


# Function definitions
def talk_to_user(prompt_text):
    """Request input from the user"""
    print(prompt_text)
    answer = input("")
    # User functions could go here?
    # return json.dumps({"role": "user", "content": answer})
    # return answer


available_functions = {
    "talk_to_user": talk_to_user,
}

functions = [
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
    print("\n" + color.GREEN + "Start of loop - press key to continue...")
    input("")
    print("\n" + color.GREEN + "Sending request...")

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

    # print(color.CYAN + "Response received" + color.YELLOW)
    # print(
    #     "\n"
    #     + color.BLINK
    #     + "Assistant:"
    #     + "\n\n"
    #     + color.RESET
    #     + response_message["content"]
    # )

    if not response_message.get("function_call"):
        print(
            "\n"
            + color.BLINK
            + "Assistant:"
            + "\n\n"
            + color.RESET
            + response_message["content"]
        )
    else:
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
