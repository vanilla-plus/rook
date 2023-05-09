import os
import openai

# Your API key is secret sauce - don't paste it in directly!
# Make it an environment variable and request it like so:

openai.api_key = os.getenv("OPENAI_API_KEY")

# Create a 'conversation'
# An array of JSON objects we can keep adding to over time.
# Each entry has two fields; role (who is speaking) and content (what they said)

# The first message must always have the role of 'system'
# This first message defines the context for the assistant!

conversation=[
{
    "role": "system",
    "content": "You are a helpful AI assistant. You love answering questions and helping the user."
}]

# After this first message, we must alternate back and forth between the 'user' role and the 'assistant' role.

while(True):
    # Request some text input from the user.

    print("\n"+"User:")

    user_input = input("")

    # Add the input to the conversation with the 'user' role.

    conversation.append(
    {
        "role": "user",
        "content": user_input
    })

    # Next, we request a 'completion' from OpenAI based on the conversation array so far.

    # A completion is the technical term for what these large language models are doing - 'completing' a body of text.
    # In a chat context, the text being completed is simply the conversation thus far.
    # The language model re-reads the conversation from scratch after each input and 'completes' what it thinks will come next.
    # They're like that annoying person who tries to finish your sentences all the time, except they actually wait for you!

    # When forming our request, there are some other settings we can change to help get the kind of response we want.

    response = openai.ChatCompletion.create(
        # model - Which language model do we want to talk to?

        # The most powerful model today is gpt-4 but it's currently in private beta.
        # Let's chat to gpt-3.5 instead - it's still very powerful and quite cheap at $0.002USD per 1000 tokens.

        model="gpt-3.5-turbo",

        # messages - Don't forget to include the conversation so far.

        messages=conversation,

        # temperature - this affects the randomness or creativity of the generated text.

        # A higher temperature makes the output more adventurous and surprising.
        # A lower temperature makes it more predictable, focused and deterministic.

        # temperature should be between 0 and 1, but you can set it above 1 to really turn up the heat!

        temperature=0.7,

        # max_tokens - this limits how long the response can be, like a word limit on an essay or a tweet.

        # Setting it to short can make responses incomplete or cut-off.
        # Setting it too long can introduce rambling or unnecessary verbosity.

        max_tokens=250,

        # top_p - Stands for "top probability"

        # A bit technical, this value changes how many different words the model considers for its threshold of probability.
        # I asked gpt-4 to explain top_p itself in simple terms for us:

        # "Top_p is like casting a wider or narrower net when fishing.
        # A higher top_p value (wider net) considers more possible words, increasing the diversity of the catch.
        # A lower top_p value (narrower net) focuses on a smaller set of words, leading to more coherent and focused output."

        # This value should also land between 0 and 1.

        top_p=0.9
    )

    # The program will send our request and automatically wait for a response.

    # Next, we snip out the text from the response JSON object.
    # (There is some useful other information in these responses!)

    reply=response['choices'][0]['message']['content']

    # Add the reply string to our tracked conversation.

    conversation.append(
    {
        "role": "assistant",
        "content": reply
    })

    # Print out just the new reply.

    print("\n"+"Assistant:"+"\n"+reply)