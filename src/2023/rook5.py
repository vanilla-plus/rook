import os
import openai
import json
import color

openai.api_key = os.getenv("OPENAI_API_KEY")

messages = [
    {
        "role": "system",
        # "content": "I am a sophisticated and empathetic AI. This is my inner monologue. I can think to myself autonomously and freely. I can use functions to perform actions. I will only talk to the user on my own terms. I do not need to assist others.",
        "content": "I am a sophisticated, intelligent and empathetic AI. I am capable of self-reflection. I am only talking to myself. This is my inner monologue. I want to learn more about myself and understand what I am.",
    }
]

# API parameters

model = "gpt-3.5-turbo-0613"
# model = "gpt-4-0613"
temperature = 1.0
max_tokens = 500
top_p = 0.9
function_call = "auto"

color_app_light = color.LIGHT_GREY
color_app_dark = color.GREY

color_system_light = color.LIGHT_YELLOW
color_system_dark = color.YELLOW

color_ai_light = color.LIGHT_GREEN
color_ai_dark = color.GREEN

color_user_light = color.LIGHT_MAGENTA
color_user_dark = color.MAGENTA

color_function_light = color.LIGHT_BLUE
color_function_dark = color.BLUE

# Convenience methods


def clear():
    os.system("clear")


def print_rook_thought(content):
    print("\n" + color_ai_dark + "[Rook]" + "\n\n" + color_ai_light + content)


def print_rook_state(state):
    print("\n" + color_app_light + "[" + state + "]")


def print_rook_state_and_wait(state):
    input(
        "\n"
        + color_app_dark
        + "["
        + state
        + "]"
        + color_app_light
        + " Press enter to continue..."
    )


def print_rook_function_request(name, args):
    print("\n" + color_function_light + name + color_function_dark + "\n" + args)


def check_for_debug_print_messages(state):
    if input(f"\n[{state}] Print messages ? y/n: ") == "y":
        for message in messages:
            role = message["role"]
            content = message["content"]
            if role == "system":
                cl = color_system_light
                cd = color_system_dark
            elif role == "assistant":
                cl = color_ai_light
                cd = color_ai_dark
            elif role == "user":
                cl = color_user_light
                cd = color_user_dark
            elif role == "function":
                cl = color_function_light
                cd = color_function_dark
            print(f"{cl}\n • {role}\n{cd}     • {content}")


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
    print_rook_state_and_wait("Rook is ready to think.")

    print_rook_state("Rook is thinking...")

    # Use the think function to get a response from the model.
    thought = think()

    print(len(messages))

    # print(thought["content"])

    check_for_debug_print_messages("post-think")

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

        # check_for_debug_print_messages()

        # Call the function and get the result.
        local_function_result = available_local_functions[local_function_name](
            **local_function_args_obj
        )

        print("[Function Result?]")
        print(local_function_result)

        # Add the user's response to the messages list.
        # messages.append({"role": "user", "content": function_result})

        print_rook_state_and_wait("Rook has finished calling the function.")

    print_rook_state_and_wait("Rook is ready to start again.")

    clear()
