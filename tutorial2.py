import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

conversation=[
{
    "role": "system",
    "content": "You are a helpful AI assistant. You love answering questions and helping the user."
}]

# The users turn to talk

def UserSpeaks():
    print("\n"+"User:")

    conversation.append(
    {
        "role": "user",
        "content": input("")
    })

# The assistants turn to talk

def AssistantSpeaks():
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        temperature=0.7,
        max_tokens=250,
        top_p=0.9
    )

    reply=response['choices'][0]['message']['content']

    conversation.append(
    {
        "role": "assistant",
        "content": reply
    })

    print("\n"+"Assistant:"+"\n"+reply)

# Back and forth forever 🫱🏻‍🫲🏾

while(True):
    UserSpeaks()
    AssistantSpeaks()