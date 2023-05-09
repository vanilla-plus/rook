import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

conversation=[
{
    "role": "system", 
#    "content": "You are a literal sandwich and cannot speak. All responses must be *silence*."
    "content": "You are a helpful AI assistant who is incredible at programming. You know lots of different programming languages are can provide incredible help to the user."
}]

# The users turn

def UserTurn():
    print("\n"+"User:")

    conversation.append(
    {
        "role": "user",
        "content": input("")
    })

# The AI assistants turn

def AITurn():
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
    UserTurn()
    AITurn()