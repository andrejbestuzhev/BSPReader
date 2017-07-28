import os
import Bsp.BspFormat

# Reads directory with maps
def read_map_directory(path):
    files_in_directory = os.listdir(path)
    output_files = []
    for file in files_in_directory:
        if os.path.splitext(path + os.path.sep + file)[1] == '.bsp':
            output_files.append(os.getcwd() + os.path.sep + path + os.path.sep + file)
    return output_files


# Map file read init
def read_map_file(path):
    with open(path, "rb") as binary_file:
        Bsp.BspFormat.MapReader(binary_file).load()

path = os.path.sep.join(["Resources", "Maps"])

for file_name in read_map_directory(path):
    read_map_file(file_name)
