import openai

messages = [
    {
        "role": "system",
        "content": "You are a helpful AI assistant who is incredible at programming. You know lots of different programming languages are can provide incredible help to the user.",
    }
]

# The users turn


def UserTurn():
    messages.append({"role": "user", "content": input("\n" + "User:\n")})


# The AI assistants turn


def AITurn():
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7,
        max_tokens=250,
        top_p=0.9,
    )

    message = response.choices[0].message

    messages.append(message)

    print("\nAssistant:\n" + message.content)


# Back and forth forever 🫱🏻‍🫲🏾

while True:
    UserTurn()
    AITurn()
