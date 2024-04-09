from ursina import *

def check_level():
    with open('imp/saves/saves.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if 'map' in line:
                return int(line.replace('map ', ''))

def save_level(level):
    # Read all lines from the file
    with open('imp/saves/saves.txt', 'r') as file:
        lines = file.readlines()

    # Find the line containing "map"
    for i, line in enumerate(lines):
        if 'map' in line:
            # Modify the line
            lines[i] = 'map '+str(level)+'\n'  # Replace this with your new map data

    # Write the modified lines back to the file
    with open('imp/saves/saves.txt', 'w') as file:
        file.writelines(lines)

