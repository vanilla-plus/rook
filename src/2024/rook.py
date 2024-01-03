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
    print(c_AI_label + "[Rook] " + c_AI_text + message + c_reset + "\n")


def print_user(message):
    print(c_user_label + "[User] " + c_user_text + message + c_reset + "\n")


def print_system(message):
    print(c_system_label + "[System] " + c_system_text + message + c_reset + "\n")


def print_function(message):
    print(c_function_label + "[Function] " + c_function_text + message + c_reset + "\n")


def print_debug(message):
    print(c_debug_label + "[Debug] " + c_debug_text + message + c_reset + "\n")


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
    print_system(f"The AI wants to say something to the user:\n\n{message}")

    user_response = input(c_user_label + "User: " + c_user_text)

    print(c_reset)

    return json.dumps(
        {
            "action_result": "success",
            "comments": f"The user responded with: {user_response}",
        }
    )


def action_remember(summarized_statement):
    if debug:
        print_debug(
            f"The AI wants to remember the following text:\n\n{summarized_statement}"
        )

    collection.add(
        documents=[summarized_statement],
        metadatas=[{"source": model}],
        ids=[str(uuid.uuid4())],
    )

    return json.dumps(
        {
            "action_result": "success",
            "comments": f"I successfully wrote the following statement to my long-term memory: {summarized_statement}",
        }
    )


# def action_recall(query, minimum_distance):
#     if debug:
#         print_debug(f"The AI wants to recall using the following query:\n\n{query}")

#     query_results = collection.query(query_texts=[query], n_results=5)

#     # if any_valid_results: # this bool condition can be inline
#         # return json.dumps(
#         # {
#             # "input_query": query,
#             # "query_results": [
#                 # Any results that are within minimum_distance go here, in order of nearest first,
#                 # Any results that are within minimum_distance go here, in order of nearest first,
#                 # Any results that are within minimum_distance go here, in order of nearest first
#             # ]
#         # }
#     # )
#     # else:
#     # return json.dumps(
#         # {
#             # "input_query: query,
#             # "query_results": [],
#         # }
#     # )


#     print_debug(str(type(query_results)))

#     print_debug(str(query_results))

#     if "ids" in query_results and query_results["ids"] and query_results["ids"][0]:
#         # results were found!
#         print("snerp")
#     else:
#         # no results were found
#         return json.dumps(
#             {
#                 "action_result": "success",
#                 "comments": f"I successfully queried my long-term memory for the following text: {query}, but no valid results were found at all.",
#                 "query_results": results,
#             }
#         )

#     if debug:
#         for i in range(len(query_results["ids"])):
#             print_debug(
#                 f"{i} - {query_results['ids'][i][0]} - {query_results['distances'][i][0]} - {query_results['documents'][i][0]}"
#             )

#     results = {
#         "ids": query_results["ids"],
#         "distances": query_results["distances"],
#         "documents": query_results["documents"],
#     }

#     return json.dumps(
#         {
#             "action_result": "success",
#             "comments": f"I successfully queried my long-term memory for the following text: {query}",
#             "query_results": results,
#         }
#     )

#     # pprint(results)

#     # if debug:
#     #     print(
#     #         f"{c_debug}[Debug mode]{c_reset} Number of results: "
#     #         + str(len(results["ids"]))
#     #     )
#     #     print(results["ids"][0])

#     # This check always succeeds (even when it shouldn't) because ids always contains at least one element.
#     # if results["ids"][0] == None:
#     # The above didn't work either...
#     # if len(results["ids"]) == 0 or
#     # This didn't work either...
#     #

#     if len(query_results["ids"][0]) == 0:
#         if debug:
#             print(
#                 f"{c_debug_label}[Debug mode]{c_reset} Querying the database returned no results."
#             )

#         messages.append(
#             {
#                 "role": "assistant",
#                 "content": "I could not recall any relevant information.",
#             }
#         )
#         return

#     if debug:
#         print(
#             f"{c_debug_label}[Debug mode]{c_reset} Querying the database returned the following results:"
#         )
#         # pprint(results["ids"])
#         # for result in results:
#         #     pprint(result)
#         for i in range(len(query_results["ids"])):
#             print(
#                 f"{i} - {query_results['ids'][i][0]} - {query_results['distances'][i][0]} - {query_results['documents'][i][0]}"
#             )

#     recall_message = "I recalled the following information: "
#     recall_content = ""

#     # for result in results:
#     for i in range(len(query_results["ids"])):
#         if query_results["distances"][i][0] > args.minimum_distance:
#             continue
#         else:
#             # recall_content += f"• [{i}] - id: [{results['ids'][i][0]}] - information: [{results['documents'][i][0]}]"
#             recall_content += query_results["documents"][i][0]

#     if recall_content == "":
#         messages.append(
#             {
#                 "role": "assistant",
#                 "content": "I could not recall any relevant information.",
#             }
#         )
#         return
#     else:
#         messages.append(
#             {
#                 "role": "assistant",
#                 "content": recall_message + recall_content,
#             }
#         )

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


def action_recall(query, minimum_distance):
    if debug:
        print_debug(f"The AI wants to recall using the following query:\n\n{query}")

    query_results = collection.query(query_texts=[query], n_results=5)
    filtered_results = []

    # Check if there are any valid results within minimum_distance
    if (
        "distances" in query_results
        and query_results["distances"]
        and query_results["distances"][0]
    ):
        for idx, distance in enumerate(query_results["distances"][0]):
            if distance < minimum_distance:
                # Assuming other relevant details are in the same index as the distance
                result_data = {
                    "id": query_results["ids"][0][idx],
                    "distance": distance,
                    "metadata": query_results["metadatas"][0][idx],
                    "document": query_results["documents"][0][idx]
                    # Add more fields if necessary
                }
                filtered_results.append(result_data)

    if filtered_results:
        # Sort results by distance, nearest first
        filtered_results.sort(key=lambda x: x["distance"])
        return json.dumps({"input_query": query, "query_results": filtered_results})
    else:
        return json.dumps({"input_query": query, "query_results": []})


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
                    "description": "The statement of information to remember. It will be stored in your persistent database. It should be kept to a summarized statement, no longer than a single sentence. For example - 'My name is Iris.' or 'I want to see a sun rise.' or 'The current President of the United States of America is Joe Biden.",
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
        print_debug(f"Response received:\n{response}")

    return response


# action_remember("My name is Iris.")

# quit()

while True:
    if not autonomy:
        print_system(f"Press key to continue...")
        input("")

    os.system("clear")

    response = GetResponse()

    pprint(response)

    message = response.choices[0].message

    function_call = message.function_call

    if function_call:
        function_name = function_call.name
        function_args = function_call.arguments

        if debug:
            print_debug(
                f"Rook wants to call the function [{function_name}] using the arguments [{function_args}]"
            )

        # messages.append(
        #     {
        #         "role": "assistant",
        #         "content": f"I want to call the function [{function_name}] using the arguments [{function_args}]",
        #     }
        # )

        function_args_obj = json.loads(function_args)

        # Oooookay, totally get it now.
        # The mistake you were making is that you were trying to inform the model about the results of the function call
        # by writing common-language messages to it at the end of messages.

        function_result = available_local_functions[function_name](**function_args_obj)

        if debug:
            print_debug(str(function_result))
            print_debug(str(type(function_result)))

        # The correct way to do this is first append a message saying that a function was called
        # by using the 'function' role

        messages.append(
            message
        )  # THIS was missing too?? OpenAI themselves do this in their main tute (weather demo)

        messages.append(
            {"role": "function", "name": function_name, "content": function_result}
        )

        # The 'results' of the function should be packaged in a JSON object returned from the function
        # and then I guess you just let the model figure out what to do with it?
        # It sounds bizarre, but there seems to be no way to give the model any documentation about
        # what this JSON 'result' object will contain - I guess its just up to you to name things
        # clearly and hope for the best...

        second_response = GetResponse()

        second_message = second_response.choices[0].message

        pprint(second_response)

        # if second_message.function_call:
        # print_system(f"Rook wants to call another function??? Is that legal?")
        # print_system(
        # f"Here is the function call:\n\n{second_message.function_call}"
        # )
        # else:
        # messages.append(second_response.choices[0].message)
    else:
        if debug:
            print_debug("Rook does not want to call a function.")

        # Appending a basic response message to the messages array.

        messages.append(message)

    if debug:
        print_debug(f"Here is the current Messages array:")
        for message in messages:
            pprint(message)
