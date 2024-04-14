import csv
import os

def write_to_csv(data, filename):
    # Check if the CSV file already exists
    file_exists = os.path.isfile(filename)

    with open(filename, 'a', newline='') as csvfile:
        fieldnames = data[0].keys() if data else []
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write header only if the file is newly created
        if not file_exists:
            writer.writeheader()

        # Write data to CSV
        for row in data:
            writer.writerow(row)

def main():
    # Sample data (replace this with your dictionary)
    data = [
        {"Name": "John", "Age": 30, "City": "New York"},
        {"Name": "Alice", "Age": 25, "City": "Los Angeles"},
    ]

    # CSV filename
    csv_filename = "output.csv"

    # Write data to CSV
    write_to_csv(data, csv_filename)

if __name__ == "__main__":
    main()
