import csv
import json

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
            cleaned_headers = [header.strip() for header in headers[2:] if header.strip()]  # Skip the first two columns and clean the headers

            locations_data = []
            for row in reader:
                # Extracting location name and hub name from the row
                location_name, hub_name = row[:2]
                distances = row[2:]

                # Prepare the routes with correct names and distances
                routes = [
                    {"name": cleaned_headers[i], "distance": distance.strip()}
                    for i, distance in enumerate(distances) if distance
                ]

                # Append this location's data to the overall list
                locations_data.append({
                    "name": location_name.strip(),
                    "hub_name": hub_name.strip(),
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
    data = []
    processed_data = []
    try:
        # Open the CSV file starting from line 8 to read column headers and data
        with open(input_csv_path, mode='r', encoding='utf-8') as csv_file:
            # Skip the first 7 lines
            for _ in range(7):
                next(csv_file)
            reader = csv.DictReader(csv_file)
            for row in reader:
                data.append(row)

        # Process the data to remove the last column from each row if it's an empty string
        for row in data:
            # Check if the last column value is an empty string and remove it if so
            if row and (list(row.values())[-1] == ''):
                row = dict(list(row.items())[:-1])
            processed_data.append(row)

        # Convert processed data to JSON
        with open(output_json_path, mode='w', encoding='utf-8') as json_file:
            json.dump(processed_data, json_file, indent=4)
            
        print(f"Successfully converted and saved to {output_json_path}")
        
    except Exception as e:
        print(f"Error during conversion: {e}")