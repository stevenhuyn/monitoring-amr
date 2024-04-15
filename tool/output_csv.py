import csv
import os

NEW_DATA = 'new_monitoring_amr.csv'
OLD_DATA = 'monitoring_amr.csv'

def write_to_csv(data):
    # Check if the CSV file already exists
    file_exists = os.path.exists(OLD_DATA)

    with open(OLD_DATA, 'a', newline='') as csvfile:
        fieldnames = data[0].keys() if data else []
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write data to CSV
        for row in data:
            writer.writerow(row)

    # If the old data file doesn't exist, create it and write the header
    if not file_exists:
        with open(OLD_DATA, 'w', newline='') as csvfile:
            fieldnames = data[0].keys() if data else []
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()

            # Write data to CSV
            for row in data:
                writer.writerow(row)

    # Always overwrite the new data file
    with open(NEW_DATA, 'w', newline='') as csvfile:
        fieldnames = data[0].keys() if data else []
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        # Write data to CSV
        for row in data:
            writer.writerow(row)

def main():
    # Sample data (replace this with your dictionary)
    data = [
        {"Name": "Francis", "Age": 40, "City": "Chicago"}
    ]

    # Write data to CSV
    write_to_csv(data)

if __name__ == "__main__":
    main()
