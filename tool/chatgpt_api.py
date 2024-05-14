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

def get_request_example(): #TODO
    # synopsis_command = ''
    # with open(os.path.join('tool','api_commands','synopsis.txt'),'r') as file:
    #     lines = file.readlines()
    # for line in lines:
    #     synopsis_command += line.replace('\n',' ')
    # return synopsis_command
    return None

'''
response = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Who won the world series in 2020?"},
    {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
    {"role": "user", "content": "Where was it played?"}
  ]
)



'''

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
