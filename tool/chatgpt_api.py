from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

def generate_response(input_text : str, command_text : str = '', behaviour_prompt : str = 'default', model : str = 'gpt-3.5-turbo'):
    if behaviour_prompt == 'default': # TODO need to work on the original behaviour prompt
        behaviour = 'You are a program designed to be sent articles and extract information out of them. You are meant to be concise. If you are asked to output something specific and are uncertain, pick a value that seems reasonable given the text intputs you will receive.'
    else:
        behaviour = behaviour_prompt
    
    client = OpenAI()

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": behaviour},
        {"role": "user", "content": command_text + '\n' + input_text}
    ]
    )
    return completion.choices[0].message
