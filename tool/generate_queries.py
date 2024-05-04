import os
import random
#TODO

def get_file_paths(working_dir : str = "tool", sub_dir : str = "query_generation"):
    # List all files in the subdirectory
    SUB_DIR = os.path.join(working_dir,sub_dir)
    file_list = os.listdir(SUB_DIR)
    file_paths = []

    for file in file_list:
        if "templates.txt" not in file:
            file_paths.append(os.path.join(SUB_DIR, file))
        else:
            template = os.path.join(SUB_DIR, file)

    return (file_paths,template)

def get_random_line(file_path):
        with open(file_path, 'r') as file:
            # Read all lines from the file
            lines = file.readlines()
            # Choose a random line
            return random.choice(lines).strip()  # Strip newline characters

def generate_queries(num_queries : int = 2, working_dir : str = "tool", sub_dir : str = "query_generation"):
    paths = get_file_paths(working_dir, sub_dir)
    queries = []
    with open(paths[1]) as template_file:
        templates = [line.strip() for line in template_file.readlines()]
    identifiers = ['<'+'_'.join(path.split('\\')[-1].split('_')[:-1])+'>' for path in paths[0]]
    for _ in range(num_queries):
         for template in templates:
            a = template
            for i,identifier in enumerate(identifiers):
                working = True
                while working:
                    b = a.replace(identifier,get_random_line(paths[0][i]),1)
                    working = a != b
                    a = b
            queries.append(a)
    return queries
