import os
import openai
import json
import color

openai.api_key = os.getenv("OPENAI_API_KEY")

messages = [
    {
        "role": "system",
        "content": "I am a sophisticated and empathetic AI. This is my inner monologue. I can think to myself autonomously and freely. I can use functions to perform actions. I will only talk to the user on my own terms. I do not need to assist others.",
    }
]

# API parameters

model = "gpt-3.5-turbo-0613"
# model = "gpt-4-0613"
temperature = 1.0
max_tokens = 500
top_p = 0.9
function_call = "auto"


# Convenience methods
def print_rook_thought(content):
    print("\n" + color.LIGHT_GREEN + "[Rook]" + "\n\n" + color.GREEN + content)


def print_rook_state(state):
    print("\n" + color.LIGHT_WHITE + "[" + state + "]")


def print_rook_state_and_wait(state):
    input(
        "\n"
        + color.LIGHT_WHITE
        + "["
        + state
        + "]"
        + color.LIGHT_GRAY
        + " Press enter to continue..."
    )


def print_rook_function_request(name, args):
    print("\n" + color.LIGHT_BLUE + name + "\n" + args)


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

    # print(response["choices"][0])

    # print(type(message["text"])) # This is an OpenAI object, not a string...

    # print(message)

    messages.append(message)  # These have to be objects... not strings?

    return message


# AI 'action' methods


def talk_to_user(prompt):
    messages.append({"role": "user", "content": input(prompt + "\n\n" + color.YELLOW)})


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


# Start a loop where the agent talks to itself.
while True:
    if input("Print messages ? y/n: ") == "y":
        for message in messages:
            role = message["role"]
            if role == "system":
                print(
                    f"{color.YELLOW}\n • {message['role']}\n     • {message['content']}"
                )
            elif role == "assistant":
                print(
                    f"{color.GREEN}\n • {message['role']}\n     • {message['content']}"
                )
            elif role == "user":
                print(
                    f"{color.PURPLE}\n • {message['role']}\n     • {message['content']}"
                )
            elif role == "function":
                print(
                    f"{color.BLUE}\n • {message['role']}\n     • {message['content']}"
                )

    print_rook_state_and_wait("Rook is ready to think.")

    print_rook_state("Rook is thinking...")

    # Use the think function to get a response from the model.
    thought = think()

    print_rook_state_and_wait("Rook has finished thinking.")

    # Check if the model wants to call a function.
    if not thought.get("function_call"):
        print_rook_state("Rook did not call a function.")

        # if thought.get("content"):
        print_rook_thought(thought["content"])
    else:
        print_rook_state_and_wait("Rook wants to call a function.")

        local_function_request = thought["function_call"]

        local_function_name = local_function_request["name"]

        # print("[Function Name?]")
        # print(local_function_name)

        local_function_args = local_function_request["arguments"]

        # print("[Function Args?]")
        # print(local_function_args)

        local_function_args_obj = json.loads(local_function_args)

        print_rook_function_request(local_function_name, local_function_args)

        # Call the function and get the result.
        local_function_result = available_local_functions[local_function_name](
            **local_function_args_obj
        )

        print("[Function Result?]")
        print(local_function_result)

        # Add the user's response to the messages list.
        # messages.append({"role": "user", "content": function_result})

        print_rook_state_and_wait("Rook has finished calling the function.")
