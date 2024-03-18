# Stdlib
import csv
import json

def clean_string(s):
    """
    Removes newline characters from a string.

    Parameters:
    - s (str): The original string.

    Returns:
    - str: The cleaned string.
    """
    return s.replace('\n', '').strip()

#* We are unable to use third-party packages so we must use the csv format.
def convert_distance_table_to_json(input_csv_path, output_json_path):
    """
    Converts a CSV file containing distance information into a JSON format where each location's
    routes are correctly named according to the CSV column headers.

    Parameters:
    - input_csv_path: Path to the input CSV file containing the distance table.
    - output_json_path: Path where the output JSON file will be saved.
    """
    try:
        with open(input_csv_path, mode='r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            # Skip initial rows that don't contain relevant data
            for _ in range(2):
                next(reader)
            headers = next(reader)  # This should now correctly read the headers row
            
            # Process the headers to clean and prepare them
            cleaned_headers = [header.strip() for header in headers[2:] if clean_string(header)]  # Skip the first two columns and clean the headers

            locations_data = []
            for row in reader:
                # Extracting location name and hub name from the row
                location_name, hub_name = row[:2]
                distances = row[2:]

                # Prepare the routes with correct names and distances
                routes = [
                    {"name": cleaned_headers[i], "distance": clean_string(distance)}
                    for i, distance in enumerate(distances) if distance
                ]

                # Append this location's data to the overall list
                locations_data.append({
                    "name": clean_string(location_name),
                    "hub_name": clean_string(hub_name),
                    "routes": routes
                })

        # Write the JSON output to the specified file
        with open(output_json_path, 'w', encoding='utf-8') as json_file:
            json.dump(locations_data, json_file, indent=4)
        
        print(f"Successfully converted and saved to {output_json_path}")
        
    except Exception as e:
        print(f"Error during conversion: {e}")



def convert_package_file_to_json(input_csv_path, output_json_path):
    """
    Converts package data from a CSV file to JSON, starting from line 8,
    and processes the data to remove the last column from each row if it's an empty string.
    Saves the processed data into a JSON file specified by output_json_path.

    Parameters:
    - input_csv_path: The file path for the input CSV file.
    - output_json_path: The file path for the output JSON file.
    """
    key_mapping = {
        "Package\nID": "id",
        "Address": "address",
        "City ": "city",
        "State": "state",
        "Zip": "zip",
        "Delivery\nDeadline": "deadline",
        "Weight\nKILO": "weight",
        "Special Notes": "notes"
    }

    try:
        with open(input_csv_path, mode='r', encoding='utf-8') as csv_file:
            for _ in range(7):  # Skip header lines if necessary
                next(csv_file)
            reader = csv.DictReader(csv_file)

            processed_data = []
            for row in reader:
                processed_row = {}
                for csv_key, json_key in key_mapping.items():
                    # Attempt to find the corresponding CSV key for each JSON key
                    csv_key_found = next((k for k in row.keys() if clean_string(csv_key) in clean_string(k)), None)
                    if csv_key_found:
                        processed_row[json_key] = clean_string(row[csv_key_found])
                    else:
                        # Ensure all keys are present, even if they're empty
                        processed_row[json_key] = ""

                # Ensure a 'notes' key exists for each entry
                processed_row.setdefault("notes", "")

                processed_data.append(processed_row)

        with open(output_json_path, mode='w', encoding='utf-8') as json_file:
            json.dump(processed_data, json_file, indent=4)

        print(f"Successfully converted and saved to {output_json_path}")
    except Exception as e:
        print(f"Error during conversion: {e}")