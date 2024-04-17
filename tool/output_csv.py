import csv
import os

NEW_DATA = 'outputs/new_monitoring_amr.csv'
OLD_DATA = 'outputs/monitoring_amr.csv'

def check_new(data):
    pass

def process_results(data):
    for i,result in enumerate(data):
        del result.text
        # if result.GPT_response == '':
        #     data.pop(i)
            
def process_prompt(data):
    pass

def write_to_csv(data):
    process_results(data)
    # Check if the CSV file already exists
    file_exists = os.path.exists(OLD_DATA)

    # Get fieldnames from the class attributes of the search_result object
    fieldnames = data[0].__dict__.keys()

    # Write to the old data file
    with open(OLD_DATA, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write data to CSV
        for result in data:
            writer.writerow(result.__dict__)

    # If the old data file doesn't exist, create it and write the header
    if not file_exists:
        with open(OLD_DATA, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            # Write data to CSV
            for row in data:
                writer.writerow(row.__dict__)

    # Always overwrite the new data file
    with open(NEW_DATA, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Write data to CSV
        for row in data:
            writer.writerow(row.__dict__)