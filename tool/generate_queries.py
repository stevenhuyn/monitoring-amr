import os
import random

def get_file_paths(working_dir : str = "tool", sub_dir : str = "keywords"):
    # List all files in the subdirectory
    SUB_DIR = os.path.join(working_dir,sub_dir)
    FILE_LIST = os.listdir(SUB_DIR)
    file_paths = []

    [file_paths.append(os.path.join(SUB_DIR, filename)) for filename in  FILE_LIST]
    return file_paths if len(file_paths) > 1 else file_paths[0]

def generate_queries(num_queries : int = 10, num_files_sampled : int = 3, 
    working_dir : str = "tool", sub_dir : str = "keywords"):
    # Function to get a random line from a file
    def get_random_line(file_path):
        with open(file_path, 'r') as file:
            # Read all lines from the file
            lines = file.readlines()
            # Choose a random line
            return random.choice(lines).strip()  # Strip newline characters

    paths = get_file_paths(working_dir, sub_dir)
    queries = []
    for i in range(num_queries):
        # Select 3 random filenames from the list
        random_files = random.sample(paths, min(num_files_sampled, len(paths)))

        query = []
        for file in random_files:
            # Get a random line from the file
            line = get_random_line(file)
            # Append the line to the queries list
            query.append(line)

        query.append(get_random_line(get_file_paths("tool", "locations")))
        query = ' '.join(query)
        queries.append(query)
    
    # Join the lines with spaces
    return queries
