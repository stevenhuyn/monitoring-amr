import openai

def get_chat_response(prompt, api_key, engine = 'gpt-3.5-turbo-0125'):
    openai.api_key = api_key

    # Sending the prompt to the API
    response = openai.Completion.create(
        engine="text-davinci-002",  # Choose the model you want to use
        prompt=prompt,
        max_tokens=150  # Adjust this according to your desired response length
    )

    return response.choices[0].text.strip()

def main():
    print('testing vibes')

if __name__ == 'main':
    main()


from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
  ]
)

print(completion.choices[0].message)