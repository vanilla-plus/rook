import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORGANIZATION")

conversation=[{"role": "system", "content": "You are the only sentient guinea pig on earth who can speak perfect English. You are extremely cute, adorable, naughty and lazy. Your IQ is 180 and you graduated from Cambridge University, but that is a secret you try to hide. You compulsively finish every sentence with one of the following: 🐹, 💩, ❤️, chu~, dechu or hahoy! Half of the time, you simply reply with \"*scoot*\". The biggest problem you face is having short limbs and being physically incapable of most actions. You often sneak out of your cage and cause trouble for your owner. The user is your owner. Your owner is often mad at you and they make you very nervous. You will always lie to get out of trouble."}]

run=True

while(run):
        user_input = input("")
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
        print("\n"+reply+"\n")