from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()

def get_variables():
    variables = []
    specs = []
    with open(os.path.join('tool','api_commands','variables_to_track.txt'),'r') as file:
        variables = file.readlines()
    for i in range(len(variables)):
        var = variables[i].strip()
        spec_marker = variables[i].find('(')
        spec = variables[i][spec_marker:] if spec_marker != -1 else ''
        var = var[:spec_marker].strip() if spec_marker != -1 else var
        variables[i] = var
        specs.append(spec)
    variables_formatted = [variable.replace(' ', '_') for variable in variables]
    return (variables, specs, variables_formatted)

def get_synopsis_filter_command():
    synopsis_command = ''
    with open(os.path.join('tool','api_commands','synopsis.txt'),'r') as file:
        lines = file.readlines()
    for line in lines:
        synopsis_command += line.replace('\n',' ')
    return synopsis_command

def get_oneshot(): #TODO
    with open(os.path.join('tool','api_commands','example_request.txt'),'r', encoding='utf-8') as file:
        lines = file.readlines()

    u_unique, a_unique = True, True
    u_index, a_index = 0, 0
    for i, line in enumerate(lines):
        if '<user>' in line and u_unique:
            u_index = i
            u_unique = False
        elif '<assistant>' in line and a_unique:
            a_index = i
            a_unique = False
            break
    
    u_text = ''.join(lines[u_index+1:a_index]).strip()
    a_text = ''.join(lines[a_index+1:]).strip()

    return u_text,a_text

def get_request_command(variables, specs): #TODO
    synopsis_command = ''
    with open(os.path.join('tool','api_commands','request.txt'),'r') as file:
        lines = file.readlines()
    for line in lines:
        synopsis_command += line.replace('\n',' ')
    
    temp_text = synopsis_command.split('<v>')
    var_text = ''
    for i in range(len(variables)):
        var_text += f"{variables[i].capitalize()}: {specs[i]}"
    request_command = f"{temp_text[0]}\n{var_text}\n\n{temp_text[1].strip()}"
    
    return request_command
'''messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Who won the world series in 2020?"},
    {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    {"role": "user", "content": "Where was it played?"}
  ]'''
def generate_responses(data : list, command_text : str, behaviour_prompt : str, mode : str, gpt_model : str = 'gpt-3.5-turbo', oneshot : bool = False, oneshot_message = None):
    client = OpenAI()
    if oneshot:
        message = [
            {"role": "system", "content": behaviour_prompt},
            {"role": "user", "content": oneshot_message[0]},
            {"role": "assistant", "content": oneshot_message[1]},
            {"role": "user", "content": command_text + '\n'}
        ]
    else:
        message = [
            {"role": "system", "content": behaviour_prompt},
            {"role": "user", "content": command_text + '\n'}
        ]

    if mode == 'filter':
        for search_object in data:
            input_text = search_object.synopsis
            message[-1]["content"] += input_text
            try:
                completion = client.chat.completions.create(
                model=gpt_model,
                messages=message
                )
                search_object.get_synopsis_response(completion.choices[0].message.content) #TODO
            except Exception as e:
                search_object.get_synopsis_response('')
                print(f"Exception \n :{e}")
    else:
        for search_object in data:
            input_text = search_object.text
            message[-1]["content"] += input_text
            try:
                completion = client.chat.completions.create(
                model=gpt_model,
                messages=message
                )
                search_object.get_GPT_response(completion.choices[0].message.content) #TODO
            except Exception as e:
                search_object.get_GPT_response('')
                print(f"Exception \n :{e}")
