from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

def generate_responses(data : list, command_text : str = '', behaviour_prompt : str = 'default', model : str = 'gpt-3.5-turbo'):
    if behaviour_prompt == 'default': 
        behaviour = 'You are a program designed to be sent articles and extract information out of them. You are meant to be concise. If you are asked to output something specific and are uncertain, pick a value that seems reasonable given the text intputs you will receive.'
    else:
        behaviour = behaviour_prompt
    
    client = OpenAI()
    for search_object in data:
        input_text = search_object.text

        try:
            completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": behaviour},
                {"role": "user", "content": command_text + '\n' + input_text}
            ]
            )
            search_object.get_GPT_response(completion.choices[0].message.content) #TODO
        except Exception as e:
            search_object.get_GPT_response('')
            print(f"Exception \n :{e}")
