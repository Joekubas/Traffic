import json


def load_config(config_file):               # docstring is missing
    with open(config_file, 'r') as file:    # encoding is missing
        return json.load(file)


def is_valid_traffic_light_sequence(sequence, config): 
    sequences = config.get("sequences")
    if sequences:                       # I would use assertion here instead: it coud return error message
        for name, valid_seq in sequences.items():
            if sequence == valid_seq:
                return True, name  # Return True and the name of the valid sequence

    return False, None  # If the sequence is not valid      # If there are no sequences in config, the comment is misleading

    # ^^ why not use list comprehension ? like:
    #  name = [name for name, valid_seq in sequences.items() if sequence == valid_seq][0]

    # also, there is no point in returning both False and None when you can check that name is not none

def check_traffic_light_behavior(data, config):
    transitions = {
        # reference of transitions from task:
        # Red -> Yellow -> Green -> Yellow -> Red (and repeat) 
        # Red -> Yellow -> Green left -> Green -> Yellow -> Red (and repeat) 

        # we can see, that only possible transitions are to the current state and state after

        "Red": ["Yellow", "Red"],
        "Yellow": ["Green", "Red", "Yellow", "GreenLeft"],
        "Green": ["Green", "Blinking", "Yellow"],       
        "Blinking": ["Green", "Blinking", "Yellow", "GreenLeft"],   # only green light can blink, so this is not correct (according to task description)
        "GreenLeft": ["Green", "Blinking", "GreenLeft"],
    }

    for line_number in range(len(data) - 1):
        current_line = data[line_number]
        next_line = data[line_number + 1]

        is_valid, current_color = is_valid_traffic_light_sequence(current_line, config)  # "is_valid" is bad name for variable as it starts with verb.
        if not is_valid:
            raise Exception(f"Invalid sequence found at line {line_number + 1}: {current_line}")
        
        # ^^^ this could be simplified as:
        #  assert current_line in [seq for _, seq in config['sequences'].items()], f"Invalid sequence found at line {line_number + 1}: {current_line}"
        #  also, it would make more sense if error message explained why sequence is wrong. In this case, illegal because multiple lights were shining at same time or something 

        is_valid, next_color = is_valid_traffic_light_sequence(next_line, config)
        if not is_valid:
            raise Exception(f"Invalid sequence found at line {line_number + 2}: {next_line}")
        
        # same as above

        if next_color not in transitions.get(current_color, []):        # there is no point of default argument to .get(), since next_color can only come from same config as current did
            raise Exception(f"Invalid transition from {current_color} to {next_color} at line {line_number + 1}")
        # again, assertion is preferred way to test if something is as expected. Negative logic is harder to read and understand

        # mixing color names and sequences makes code harder to read. Better only use one and use to function to translate to the other

        # in the case the light is yellow, it would make sense to check more than one following (or previous) state as it is not supposed to turn back to the color it was before turning yellow


def analyze_traffic_light(file_path, config_file):
    try:
        config = load_config(config_file)

        with open(file_path, 'r') as file:
            data = []
            for line in file:
                states = [int(bit) for bit in line.strip().split(',')] # this stripping and splitting is excessive since data is formatted without leading or trailing whitespaces
                                                                       # also, there is no point in converting stuff to list of integers as we can compare strings as they are, even without encoding them to colors.
                data.append(states)

            check_traffic_light_behavior(data, config)          # I believe this should be outside of context manager since we don't need opened file anymore

            print("Traffic light is working correctly.")        # what if there are errors? no message ?
            return True

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return False


def main():
    file_path = "C:/develop/training/data.txt"  # Replace with your file path
    config_file = "C:/develop/training/config.json"  # Replace with the path to your configuration file

    # ^^ why not use argparse module and provide paths to these files as commandline options?

    analyze_traffic_light(file_path, config_file)

    # I have not tested the script if it works since there are obvious errors in logic. It would make sense to write some testcases to check logic for task like this.

if __name__ == "__main__":
    main()
