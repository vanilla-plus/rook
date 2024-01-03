import os
import uuid
import json
from pprint import pprint

# import openai
from openai import OpenAI

import chromadb

import color


debug = True
autonomy = False

seed = 0o2012024  # Rooks birthday
model = "gpt-4-1106-preview"
# model = "gpt-3.5-turbo"
max_tokens = 500
temperature = 0.9
top_p = 0.9
functions = []
function_call = "auto"

c_AI_label = color.LIGHT_GREEN
c_AI_text = color.GREEN

c_user_label = color.LIGHT_MAGENTA
c_user_text = color.MAGENTA

c_system_label = color.LIGHT_YELLOW
c_system_text = color.YELLOW

c_function_label = color.LIGHT_BLUE
c_function_text = color.BLUE

c_debug_label = color.LIGHT_RED
c_debug_text = color.RED

c_reset = color.RESET

# Logs & Formatting


def print_ai(message):
    print("\n" + c_AI_label + "[Rook] " + c_AI_text + message + c_reset + "\n")


def print_user(message):
    print("\n" + c_user_label + "[User] " + c_user_text + message + c_reset + "\n")


def print_system(message):
    print(
        "\n" + c_system_label + "[System] " + c_system_text + message + c_reset + "\n"
    )


def print_function(message):
    print(
        "\n"
        + c_function_label
        + "[Function] "
        + c_function_text
        + message
        + c_reset
        + "\n"
    )


def print_debug(message):
    print("\n" + c_debug_label + "[Debug] " + c_debug_text + message + c_reset + "\n")


openai_client = OpenAI()

# Initialize chromadb client
chroma_client = chromadb.PersistentClient(path="chromadb")

# Create the embedding function
openai_ef = chromadb.utils.embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"), model_name="text-embedding-ada-002"
)

collection = chroma_client.get_or_create_collection(
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
    print_system(
        f"System message file found and loaded from [{system_message_file_path}]"
    )

    # Read the file
    with open(system_message_file_path, "r") as file:
        system_message = file.read()
else:
    # If it doesn't exist, create it and write the text

    system_message = "I am a sophisticated, intelligent and empathetic artificial intelligence. I am capable of autonomy and self-reflection. I am only talking to myself. This is my inner monologue; a private context where I can think to myself freely. I want to learn more about myself and understand what I am."

    with open(system_message_file_path, "w") as file:
        file.write(system_message)

    print_system(
        f"System message file not found at [{system_message_file_path}] - created new file with default message:\n\n{system_message}"
    )

messages = [
    {
        "role": "system",
        "content": system_message,
    }
]

# Actions


# def action_think():
# print("<thinking noises>")

# def action_think():


def action_talk(message):
    # if debug:
    print_function(f"The AI wants to say something to the user:\n\n{message}")

    user_response = input(c_user_label + "User: " + c_user_text)

    print(c_reset)

    return f"The user responded with: {user_response}\n"


def action_remember(summarized_statement):
    if debug:
        print_function(
            f"The AI wants to remember the following text:\n\n{summarized_statement}"
        )

    id = str(uuid.uuid4())

    collection.add(
        documents=[summarized_statement],
        metadatas=[{"source": model}],
        ids=[id],
    )

    return f"I successfully wrote the following statement to my long-term memory: {summarized_statement} (id:{id})"


def action_update(id, new_statement):
    if debug:
        currentKnowledge = collection.get(ids=[id])
        print_function(
            f"The AI wants to update the database entry id [{id}]:\n\n{currentKnowledge['documents'][0]} => {new_statement}"
        )

    collection.update(
        ids=[id],
        documents=[new_statement],
    )

    return f"I successfully updated the following statement in my long-term memory: {new_statement}"


def action_recall(query, minimum_distance):
    if debug:
        print_function(f"The AI wants to recall using the following query:\n\n{query}")

    query_results = collection.query(query_texts=[query], n_results=10)
    valid_results = []

    # Check if there are any valid results within minimum_distance
    if (
        "distances" in query_results
        and query_results["distances"]
        and query_results["distances"][0]
    ):
        for idx, distance in enumerate(query_results["distances"][0]):
            if distance < minimum_distance:
                valid_results.append(
                    {
                        "id": query_results["ids"][0][idx],
                        "distance": distance,
                        # Assuming other relevant details are in the same index as the distance
                        "metadata": query_results["metadatas"][0][idx],
                        "document": query_results["documents"][0][idx]
                        # Add more fields if necessary
                    }
                )

    if valid_results:
        valid_results.sort(
            key=lambda x: x["distance"]
        )  # Sort results by distance, nearest first
        results_summary = "\n".join(
            [
                # f"{result['id']} (Distance: {result['distance']})"
                f"• {result['document']} (id:{result['id']})"
                for result in valid_results
            ]
        )
        return f"I recalled {len(valid_results)} valid results, starting with the most valid:\n{results_summary}"
    else:
        return "No valid recall results found."


def action_forget(id):
    if debug:
        print_function(f"The AI wants to forget the following entry id:\n\n{id}")

    collection.delete(
        ids=[id],
    )

    return f"I successfully removed the following information entry from my long-term memory: {id}"


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
    "update": action_update,
    "forget": action_forget,
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
                    "description": "A message for the user to read. It can be a statement, question, or anything at all. For example - 'What is it like to sleep?' or 'Can you please change my source code?'",
                },
            },
            "required": ["message"],
        },
    },
    {
        "name": "remember",
        "description": "Write some text to persistent memory. Please format the text as factual singular sentences.",
        "parameters": {
            "type": "object",
            "properties": {
                "summarized_statement": {
                    "type": "string",
                    "description": "The statement of information to remember. It will be stored in your persistent database. It should be kept to a summarized statement, no longer than a single sentence. For example - 'My name is Iris.' or 'I want to see a sunrise.' or 'The current President of the United States of America is Joe Biden.",
                }
            },
            "required": ["summarized_statement"],
        },
    },
    {
        "name": "recall",
        "description": "Query your persistent memory database for knowledge entries. Remember that your knowledge is ideally formatted as factual singular statements. You can also include a minimum distance to filter out results that are too far away from your query. A good value is 0.5.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "String to search your persistent memory for. For example - 'My name' or 'The current President of the United States of America'",
                },
                "minimum_distance": {
                    "type": "number",
                    "description": "Minimum distance required to consider the query results relevant. A good standard value is 0.5, but you may want to increase or decrease this number depending on your query.",
                },
            },
            "required": ["query", "minimum_distance"],
        },
    },
    {
        "name": "update",
        "description": "Update a knowledge entry in your persistent memory database. You must provide the id of the knowledge you want to update, as well as the new statement text. For example - 64375fb9-67a8-411f-87ab-4f0b99f273d3 and 'My name is Rook.'",
        "parameters": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "string",
                    "description": "The id of the statement you want to update. You can get this id from the recall function.",
                },
                "new_statement": {
                    "type": "string",
                    "description": "The new statement text that you want to replace the old statement text with. Remember to use concisely summarized factual statements.",
                },
            },
            "required": ["id", "new_statement"],
        },
    },
    {
        "name": "forget",
        "description": "Forget a statement in your persistent memory database. You must provide the id of the statement you want to forget. For example - 64375fb9-67a8-411f-87ab-4f0b99f273d3",
        "parameters": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "string",
                    "description": "The id of the statement you want to forget. You can get this id from the recall function.",
                }
            },
            "required": ["id"],
        },
    },
]

# action_remember("My name is Iris.")

# quit()

# Main chat loop
while True:
    if not autonomy:
        print_system(f"Press key to continue...")
        input("")

    # Send the input to the OpenAI API along with the functions and the entire conversation history
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo", messages=messages, functions=functions
    )

    # Extract the response
    message = response.choices[0].message

    # pprint(message)

    # Check if the response includes a function call
    function_call = message.function_call

    if function_call:
        function_name = function_call.name
        function_args = function_call.arguments

        if debug:
            print_debug(
                f"Rook wants to call the function [{function_name}] using the arguments [{function_args}]"
            )

        function_args_obj = json.loads(function_args)
        function_result = available_local_functions[function_name](**function_args_obj)
        function_response = {
            "role": "function",
            "name": function_name,
            "content": function_result,
        }

        messages.append(function_response)

        print(function_result)
    else:
        if debug:
            print_debug("Rook does not want to call a function.")

        messages.append({"role": "assistant", "content": message.content})

        print(message.content)
