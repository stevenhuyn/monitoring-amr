import openai

def get_chat_response(prompt, api_key):
    openai.api_key = api_key

    # Sending the prompt to the API
    response = openai.Completion.create(
        engine="text-davinci-002",  # Choose the model you want to use
        prompt=prompt,
        max_tokens=150  # Adjust this according to your desired response length
    )

    return response.choices[0].text.strip()

# Example usage
api_key = "your_openai_api_key_here"
prompt = "Q: What is the capital of France?\nA: The capital of France is"
response = get_chat_response(prompt, api_key)
print("ChatGPT's response:", response)

# import subprocess

# def install_openai():
#     subprocess.call(['pip', 'install', 'openai'])

# # Call the function to install openai
# install_openai()
