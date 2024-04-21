from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()

def get_variables():
    variables = []
    with open(os.path.join('tool','api_commands','variables_to_track.txt'),'r') as file:
        variables = file.readlines()
    for i in range(len(variables)):
        variables[i] = variables[i].strip()
    return variables

def get_synopsis_filter_command():
    synopsis_command = ''
    with open(os.path.join('tool','api_commands','synopsis.txt'),'r') as file:
        lines = file.readlines()
    for line in lines:
        synopsis_command += line.replace('\n',' ')
    return synopsis_command

def get_request_example():
    # synopsis_command = ''
    # with open(os.path.join('tool','api_commands','synopsis.txt'),'r') as file:
    #     lines = file.readlines()
    # for line in lines:
    #     synopsis_command += line.replace('\n',' ')
    # return synopsis_command
    return None

def get_request_command(variables): #TODO
    synopsis_command = ''
    with open(os.path.join('tool','api_commands','synopsis.txt'),'r') as file:
        lines = file.readlines()
    for line in lines:
        synopsis_command += line.replace('\n',' ')
    return synopsis_command


def generate_responses(data : list, command_text : str, behaviour_prompt : str, mode : str, gpt_model : str = 'gpt-3.5-turbo'):
    client = OpenAI()

    if mode == 'filter':
        for search_object in data:
            input_text = search_object.synopsis

            try:
                completion = client.chat.completions.create(
                model=gpt_model,
                messages=[
                    {"role": "system", "content": behaviour_prompt}, # One shot learning
                    {"role": "user", "content": command_text + '\n' + input_text}
                ]
                )
                search_object.get_synopsis_response(completion.choices[0].message.content) #TODO
            except Exception as e:
                search_object.get_synopsis_response('')
                print(f"Exception \n :{e}")
    else:
        for search_object in data:
            input_text = search_object.text

            try:
                completion = client.chat.completions.create(
                model=gpt_model,
                messages=[
                    {"role": "system", "content": behaviour_prompt}, # One shot learning
                    {"role": "user", "content": command_text + '\n' + input_text}
                ]
                )
                search_object.get_GPT_response(completion.choices[0].message.content) #TODO
            except Exception as e:
                search_object.get_GPT_response('')
                print(f"Exception \n :{e}")
