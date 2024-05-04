import csv
import os

NEW_DATA = 'new_monitoring_amr.csv'
OLD_DATA = 'monitoring_amr.csv'
DELIMITER = ';'

def assign_constants(new,old,delimiter):
    global NEW_DATA, OLD_DATA, DELIMITER
    NEW_DATA, OLD_DATA, DELIMITER = new,old,delimiter

def write_to_csv(data):
    # Check if the CSV file already exists
    file_exists = os.path.exists(OLD_DATA)
    
    # Get fieldnames from the class attributes of the search_result object
    fieldnames = data[0].__dict__.keys()

    # Write to the old data file
    with open(os.path.join('tool','outputs',OLD_DATA), 'a', newline='', encoding='utf-8',) as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=DELIMITER)

        # Write data to CSV
        for result in data:
            writer.writerow(result.__dict__)

    # If the old data file doesn't exist, create it and write the header
    if not file_exists:
        with open(os.path.join('tool','outputs',OLD_DATA), 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter=DELIMITER)
            writer.writeheader()

            # Write data to CSV
            for row in data:
                writer.writerow(row.__dict__)

    # Always overwrite the new data file
    with open(os.path.join('tool','outputs',NEW_DATA), 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames,delimiter=DELIMITER)
        writer.writeheader()

        # Write data to CSV
        for row in data:
            try:
                writer.writerow(row.__dict__)
            except Exception as e:
                print(f"The following exception occurred while trying to write the data to the CSV file {e}")

