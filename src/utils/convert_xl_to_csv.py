import json

def correct_distance_table_json(input_json_path, output_json_path):
    """
    Corrects the distance table JSON by filling in the route names based on the sequence of locations.

    Parameters:
    - input_json_path: Path to the input JSON file with incomplete route names.
    - output_json_path: Path where the corrected JSON file will be saved.
    """
    with open(input_json_path, 'r') as file:
        data = json.load(file)

    # Assume the distances are in order and correspond to the order of locations in the list
    for location in data:
        for i, route in enumerate(location['routes']):
            # Assign route names based on the corresponding location's name in the data list
            route['name'] = data[i]['name'] if i < len(data) else "Unknown"

    # Save the corrected data to the specified output JSON file
    with open(output_json_path, 'w') as file:
        json.dump(data, file, indent=4)