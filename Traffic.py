import json


def load_config(config_file):
    with open(config_file, 'r') as file:
        return json.load(file)


def is_valid_traffic_light_sequence(sequence, config):
    sequences = config.get("sequences")
    if sequences:
        for name, valid_seq in sequences.items():
            if sequence == valid_seq:
                return True, name  # Return True and the name of the valid sequence

    return False, None  # If the sequence is not valid


def check_traffic_light_behavior(data, config):
    transitions = {
        "Red": ["Yellow", "Red"],
        "Yellow": ["Green", "Red", "Yellow", "GreenLeft"],
        "Green": ["Green", "Blinking", "Yellow"],
        "Blinking": ["Green", "Blinking", "Yellow", "GreenLeft"],
        "GreenLeft": ["Green", "Blinking", "GreenLeft"],
    }

    for line_number in range(len(data) - 1):
        current_line = data[line_number]
        next_line = data[line_number + 1]

        is_valid, current_color = is_valid_traffic_light_sequence(current_line, config)
        if not is_valid:
            raise Exception(f"Invalid sequence found at line {line_number + 1}: {current_line}")

        is_valid, next_color = is_valid_traffic_light_sequence(next_line, config)
        if not is_valid:
            raise Exception(f"Invalid sequence found at line {line_number + 2}: {next_line}")

        if next_color not in transitions.get(current_color, []):
            raise Exception(f"Invalid transition from {current_color} to {next_color} at line {line_number + 1}")


def analyze_traffic_light(file_path, config_file):
    try:
        config = load_config(config_file)

        with open(file_path, 'r') as file:
            data = []
            for line in file:
                states = [int(bit) for bit in line.strip().split(',')]
                data.append(states)

            check_traffic_light_behavior(data, config)

            print("Traffic light is working correctly.")
            return True

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return False


def main():
    file_path = "C:/develop/training/data.txt"  # Replace with your file path
    config_file = "C:/develop/training/config.json"  # Replace with the path to your configuration file
    analyze_traffic_light(file_path, config_file)


if __name__ == "__main__":
    main()
