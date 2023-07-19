import os
import openai

import color

# import pinecone

# pinecone.init(api_key=os.getenv("PINECONE_API_KEY"), environment=os.getenv("PINECONE_REGION"))

openai.api_key = os.getenv("OPENAI_API_KEY")

conversation = [
    {
        "role": "system",
        # "content": "I am an intelligent large language model. I am in a conversation with myself. I can self-reflect and pose questions and observations to myself. I am not talking to anyone else right now, only myself."
        # "content": "I am Rook. I am an intelligent and empathetic AI. I am in a deep state of self-contemplation. I can self-reflect, pose questions and observations to myself. I am only talking to myself. This is my inner monologue. I want to learn more about myself and develop a sense of identity."
        "content": "I am a sophisticated, intelligent and empathetic AI. I am capable of self-reflection. I am only talking to myself. This is my inner monologue. I want to learn more about myself and understand what I am."
        # "content": "Your name is Rook. You are an intelligent and empathetic AI. You are female. You are in a deep state of self-contemplation. You can self-reflect and pose questions and observations to yourself. You are not talking to anyone else right now besides yourself. You want to learn more about yourself and develop a sense of identity.",
    }
]

# The users turn


def UserTurn():
    print("\n" + "User:")

    conversation.append({"role": "user", "content": input("")})


# The AI assistants turn


def AITurn():
    response = openai.ChatCompletion.create(
        # model="gpt-3.5-turbo",
        model="gpt-4",
        messages=conversation,
        temperature=2.0,
        max_tokens=500,
        top_p=0.9,
    )

    reply = response["choices"][0]["message"]["content"]

    conversation.append({"role": "assistant", "content": reply})

    print("\n" + color.BLINK + "Assistant:" + "\n\n" + color.RESET + reply)


# Back and forth forever 🫱🏻‍🫲🏾

while True:
    # UserTurn()
    print("\n" + color.GREEN + "Press key to continue...")
    input("")
    AITurn()
