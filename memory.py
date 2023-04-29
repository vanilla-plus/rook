import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORGANIZATION")

ansiiGreen = '\033[32m'
ansiiMagenta = '\033[95m'
ansiiCoral = '\033[91m'
ansiiGold = '\033[33m'
ansiiTeal = '\033[36m'
ansiiReset = '\033[0m'

ansiiUser=ansiiGreen
ansiiRook=ansiiTeal

memoryFilePath = "memory.txt"

systemInit = "You are Rook."

# No matter what, Rook always seems to start with no personality. You can awaken it by specifically requesting it, but she never seems to remember
# to act that way by default...

with open(memoryFilePath, 'r') as file:
    contents = file.read()
    if contents:
        # systemInit=systemInit+" Here is a list of all the things you know (this list is called your \"memory\"):\n\n"+contents.replace('-', '•')
        systemInit=systemInit+" Here is a list of all the things you know (this list is called your \"memory bank\"):\n\n"+contents
        
print('\n💆🏻‍♀️'+ansiiGold+' Rook is waking up... what do I remember?')

conversation=[{"role": "system", "content": systemInit}]

print(ansiiRook+'\n'+systemInit+'\n'+ansiiUser)

# response = openai.ChatCompletion.create(
#     model="gpt-3.5-turbo",
#     messages=conversation,
#     temperature=0.7,
#     max_tokens=250,
#     top_p=0.9
# )
#         
# reply=response['choices'][0]['message']['content']
#                     
# conversation.append({"role": "assistant", "content": reply})
# 
# print(reply+"\n"+ansiiUser)

run=True

while(run):
    user_input = input("")
    
    save=user_input == 'save'
    
    if save:
        # user_input="Assistant, please create a dot-point list of any new facts you have learned during this conversation. Use clear and concise sentences that involve the subject (e.g., a person) followed by the new information. For example, '{{person}} likes {{place}}', '{{person}} wants to go to {{activity}}', or '{{person}} has never been on a {{transport}}'. If you already knew the fact, do not include it in the list."
        # user_input="Assistant, please create a dot-point list of any new facts you have learned during this conversation. Use clear and concise sentences that involve the subject (e.g., a person) followed by the new information. For example, '• {{person}} likes {{place}}', '• {{person}} wants to go to {{activity}}', or '• {{person}} has never been on a {{transport}}'. If you already knew the fact, do not include it in the list. Do not say anything else beside the list."
        
        user_input="Can you read me out your memory bank?"
    
    conversation.append({"role": "user", "content": user_input})
        
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        temperature=0.7,
        max_tokens=250,
        top_p=0.9
    )
        
    reply=response['choices'][0]['message']['content']
                    
    conversation.append({"role": "assistant", "content": reply})

    print("\n"+ansiiRook+reply+"\n"+ansiiUser)
    
    if save:
        with open(memoryFilePath, "w") as file:
            # file.write('\n'+reply)
            file.write('•'+reply.split('•', 1)[1]) # This will trim anything that appears before the first bullet character