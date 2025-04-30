import json
import os

def append_to_json_file(file_path, new_data):
    # Load existing data
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            try:
                existing_data = json.load(file)
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []

    # Ensure it's a list to append to
    if not isinstance(existing_data, list):
        raise ValueError("Existing data is not a list. Cannot append.")

    # Append new data
    if isinstance(new_data, list):
        existing_data.extend(new_data)
    else:
        existing_data.append(new_data)

    # Write updated data back
    with open(file_path, "w") as file:
        json.dump(existing_data, file, indent=4)


def load_filtered_metrics(json_path):
    with open(json_path, 'r') as f:
        raw_data = json.load(f)

    return [
        {
            "iteration": entry["iteration"],
            "avg_score": entry["avg_score"],
            "avg_num_lines_cleared": entry["num_lines_cleared"],
            "avg_points_per_line_cleared": entry["avg_points_per_line_cleared"]
        }
        for entry in raw_data
    ]
