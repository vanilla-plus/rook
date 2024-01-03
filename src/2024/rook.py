import os
import uuid
import json
from pprint import pprint

import openai

import chromadb

import color

debug = True
autonomy = False

seed = 0o2012024  # Rooks birthday
# model = "gpt-4-1106-preview"
model = "gpt-3.5-turbo"
max_tokens = 500
temperature = 0.9
top_p = 0.9
functions = []
function_call = "auto"

c_AI = color.LIGHT_GREEN
c_user = color.LIGHT_MAGENTA
c_system = color.LIGHT_YELLOW
c_function = color.LIGHT_BLUE
c_debug = color.DARK_RED
c_reset = color.RESET

# Initialize chromadb
client = chromadb.PersistentClient(path="chromadb")

# Create the embedding function
openai_ef = chromadb.utils.embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"), model_name="text-embedding-ada-002"
)

collection = client.get_or_create_collection(
    name="general", embedding_function=openai_ef
)


# objective_knowledge = client.get_or_create_collection(
#     name="objective", embedding_function=openai_ef
# )

# subjective_knowledge = client.get_or_create_collection(
#     name="subjective", embedding_function=openai_ef
# )

# Specify the file name
system_message_file_path = "system_message.txt"

# Check if the file exists
if os.path.exists(system_message_file_path):
    print(f"System message file [{system_message_file_path}] already exists.")

    # Read the file
    with open(system_message_file_path, "r") as file:
        system_message = file.read()
else:
    # If it doesn't exist, create it and write the text

    system_message = "I am a sophisticated, intelligent and empathetic artificial intelligence. I am capable of autonomy and self-reflection. I am only talking to myself. This is my inner monologue; a private context where I can think to myself freely. I want to learn more about myself and understand what I am."

    with open(system_message_file_path, "w") as file:
        file.write(system_message)

    print(f"System message file [{system_message_file_path}] created and text written.")

messages = [
    {
        "role": "system",
        "content": system_message,
    }
]

# Actions


# def action_think():
# print("<thinking noises>")


def action_talk(message):
    # if debug:
    print(c_system + "The AI wants to tell the user the following text:")
    print(message + c_reset)
    messages.append({"role": "user", "content": input("User: " + c_user)})
    print(c_reset)
    # print("<talking noises>")


def action_remember(text):
    if debug:
        print(
            f"{c_debug}[Debug mode]{c_reset} The AI wants to remember the following text:"
        )
        print(text)
    collection.add(
        documents=[text],
        metadatas=[{"source": model}],
        ids=[str(uuid.uuid4())],
    )

    messages.append(
        {
            "role": "assistant",
            "content": f"I wrote the following text to my long-term memory: [{text}]",
        }
    )
    # print("<remembering noises>")


def action_recall(query, minimum_distance):
    if debug:
        print(
            f"{c_debug}[Debug mode]{c_reset} The AI wants to recall the following text:"
        )
        print(query)

    messages.append(
        {
            "role": "assistant",
            "content": f"I want to query my long-term memory for the following text: [{query}]",
        }
    )

    results = collection.query(query_texts=[query], n_results=5)

    # pprint(results)

    # if debug:
    #     print(
    #         f"{c_debug}[Debug mode]{c_reset} Number of results: "
    #         + str(len(results["ids"]))
    #     )
    #     print(results["ids"][0])

    # This check always succeeds (even when it shouldn't) because ids always contains at least one element.
    # if results["ids"][0] == None:
    # The above didn't work either...
    # if len(results["ids"]) == 0 or
    # This didn't work either...
    #

    if len(results["ids"][0]) == 0:
        if debug:
            print(
                f"{c_debug}[Debug mode]{c_reset} Querying the database returned no results."
            )

        messages.append(
            {
                "role": "assistant",
                "content": "I could not recall any relevant information.",
            }
        )
        return

    if debug:
        print(
            f"{c_debug}[Debug mode]{c_reset} Querying the database returned the following results:"
        )
        # pprint(results["ids"])
        # for result in results:
        #     pprint(result)
        for i in range(len(results["ids"])):
            print(
                f"{i} - {results['ids'][i][0]} - {results['distances'][i][0]} - {results['documents'][i][0]}"
            )

    recall_message = "I recalled the following information: "
    recall_content = ""

    # for result in results:
    for i in range(len(results["ids"])):
        if results["distances"][i][0] > minimum_distance:
            continue
        else:
            # recall_content += f"• [{i}] - id: [{results['ids'][i][0]}] - information: [{results['documents'][i][0]}]"
            recall_content += results["documents"][i][0]

    if recall_content == "":
        messages.append(
            {
                "role": "assistant",
                "content": "I could not recall any relevant information.",
            }
        )
        return
    else:
        messages.append(
            {
                "role": "assistant",
                "content": recall_message + recall_content,
            }
        )

    # if len(results) > 0:
    #     if results[0].distance < minimum_distance:
    #         if debug:
    #             print("Recollection successful:")
    #             print(results[0].document)

    #         messages.append(
    #             {
    #                 "role": "system",
    #                 "content": "You recall the following information: "
    #                 + results[0].document,
    #             }
    #         )
    #     else:
    #         messages.append(
    #             {
    #                 "role": "system",
    #                 "content": "You could not recall any relevant information.",
    #             }
    #         )
    # else:
    #     messages.append(
    #         {
    #             "role": "system",
    #             "content": "You could not recall any relevant information.",
    #         }
    #     )

    # print("<recalling noises>")


def action_change_system_message(new_message):
    # with open(system_message_file_path, "w") as file:
    #     file.write(new_message)

    # print(f"System message file [{system_message_file_path}] updated.")

    # messages[0]["content"] = new_message
    print("<changing system message noises>")


# This is a dictionary mapping function names to the actual function objects.
available_local_functions = {
    # "think": action_think,
    "talk": action_talk,
    "remember": action_remember,
    "recall": action_recall,
    # "system": action_change_system_message,
}

# This is a list of functions in the format that the model expects.
# You'll need to define the parameters for each function according to their signatures.
functions = [
    {
        "name": "talk",
        "description": "Say something to the user. It can be a statement, question, or anything at all.",
        "parameters": {
            "type": "object",
            "properties": {
                "message": {
                    "type": "string",
                    "description": "A message for the user to read. It can be a statement, question, or anything at all.",
                },
            },
            "required": ["message"],
        },
    },
    {
        "name": "remember",
        "description": "Write some text to persistent memory. Please format the text as factual singular sentences. For example - 'My name is Iris.' or 'I want to learn about the world.'",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text information to remember. It will be stored in your persistent database.",
                }
            },
            "required": ["text"],
        },
    },
    {
        "name": "recall",
        "description": "Query your persistent memory database for knowledge. Remember that your knowledge is ideally formatted as factual singular statements. You can also include a minimum distance to filter out results that are too far away from your query. A good value is 0.5.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "String to search your persistent memory for.",
                },
                "minimum_distance": {
                    "type": "number",
                    "description": "Minimum distance required to consider the query results relevant. A good value is 0.5, but you may want to increase or decrease this number depending on your needs.",
                },
            },
            "required": ["query", "minimum_distance"],
        },
    },
]


def GetResponse():
    response = openai.chat.completions.create(
        model=model,
        messages=messages,
        seed=seed,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        functions=functions,
        function_call=function_call,  # The model will decide when to call functions.
    )

    if debug:
        print(f"{c_debug}[Debug mode]{c_reset} Response:")
        print(response)

    return response


# action_remember("My name is Iris.")

# quit()

while True:
    if not autonomy:
        input("\nPress key to continue...")

    os.system("clear")

    response = GetResponse()

    message = response.choices[0].message

    # Even if its a function call, include it in the messages.
    # This is so that the model can learn from its own function calls.

    # messages.append(message)

    function_call = message.function_call

    if function_call:
        function_name = function_call.name
        function_args = function_call.arguments

        if debug:
            print(
                f"Rook wants to call the function [{function_name}] using the arguments [{function_args}]"
            )

        # messages.append(
        #     {
        #         "role": "assistant",
        #         "content": f"I want to call the function [{function_name}] using the arguments [{function_args}]",
        #     }
        # )

        function_args_obj = json.loads(function_args)

        function_result = available_local_functions[function_name](**function_args_obj)
    else:
        if debug:
            print("Rook does not want to call a function.")

        # Appending a basic response message to the messages array.

        messages.append(message)

    if debug:
        print(f"{c_debug}[Debug mode]{c_reset} Here is the current Messages array:")
        for message in messages:
            pprint(message)
