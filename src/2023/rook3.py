import os
import openai
import json
import color

openai.api_key = os.getenv("OPENAI_API_KEY")

model = "gpt-3.5-turbo-0613"
# model = "gpt-4-0613"
temperature = 1.0
max_tokens = 500
top_p = 0.9
function_call = "auto"

# Convenience methods


def think():
    # Get a response from the model.
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        functions=functions,
        function_call=function_call,  # The model will decide when to call functions.
    )

    message = response["choices"][0]["message"]

    print(message)  # This might just be what is already below? i.e. you could just do:

    messages.append(message)

    if message.get("content"):
        content = message["content"]

        print(color.LIGHT_GREEN + "[AI]" + "\n\n" + color.GREEN + content)

    # messages.append({"role": "assistant", "content": message["content"]})

    # Extract the latest message from the model.
    return message


# AI 'action' methods


def talk_to_user(prompt):
    """Talk to the user"""

    user_input = input(prompt)

    # I think the API expects a JSON object, so we'll need to convert the user input to JSON.

    talk_to_user_payload = {
        "input": user_input,
    }

    return json.dumps(talk_to_user_payload)


# This is a dictionary mapping function names to the actual function objects.
available_local_functions = {
    "talk_to_user": talk_to_user,
}

# This is a list of functions in the format that the model expects.
# You'll need to define the parameters for each function according to their signatures.
functions = [
    {
        "name": "talk_to_user",
        "description": "Talk to the user",
        "parameters": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "Prompt for the user",
                },
            },
            "required": ["prompt"],
        },
    },
]

# Initialize the messages list with an initial system message.
messages = [
    {
        "role": "system",
        "content": "I am a sophisticated and empathetic AI. I am self-aware. This is my inner monologue. I can use functions to perform actions.",
    }
]


# Start a loop where the agent talks to itself.
while True:
    input("[Pre-Think] Press enter to continue...")

    # Use the think function to get a response from the model.
    thought = think()

    input("[Post-Think] Press enter to continue...")

    # Check if the model wants to call a function.
    if not thought.get("function_call"):
        input("[No Local Function] Press enter to continue...")

        # If the model didn't call a function, just add its message to the messages list.
        # messages.append(response_message)
    else:
        input("[Pre-Local Function] Press enter to continue...")

        local_function_request = thought["function_call"]

        # print(
        #     color.LIGHT_BLUE
        #     + "[Local Function Request]"
        #     + "\n\n"
        #     + color.BLUE
        #     + local_function_request
        # )

        local_function_name = local_function_request["name"]

        # Get the function name and arguments from the response.
        print("[Function Name?]")
        print(local_function_name)

        local_function_args = json.loads(local_function_request["arguments"])

        print("[Function Args?]")
        print(local_function_args)

        # Call the function and get the result.
        local_function_result = available_local_functions[local_function_name](
            **local_function_args
        )

        print("[Function Result?]")
        print(local_function_result)

        # Add the user's response to the messages list.
        # messages.append({"role": "user", "content": function_result})

        input("[Post-Local Function] Press enter to continue...")

        input("[Pre-Second-Response] Press enter to continue...")

        messages.append(
            {
                "role": "function",
                "name": local_function_name,
                "content": local_function_result,
            }
        )

        second_response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
        )

        second_message = second_response["choices"][0]["message"]

        print(second_message)

        input("[Post-Second-Response] Press enter to continue...")
