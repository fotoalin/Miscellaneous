import os
import re
import logging

logger = logging.get_loger(__name__)

reply = input('This script will rename all .mp4 files in the current folder according to the names found in "Table of contents numbering.txt".\nAre you sure you want to do that? ')

if not any(keyword in reply.lower() for keyword in ['yes', 'y']):
    logger.info("Exiting the program.")
    sys.exit()

new_names_source_file = "Table of contents numbering.txt"

# Read the numbering from "Table of contents numbering.txt"
logger.debug(f'Opening {new_names_source_file}')
with open(new_names_source_file, "r") as table_of_contents_file:
    file_content = [line.strip() for line in table_of_contents_file.readlines()]

# Create a dictionary to store the mapping of old numbers to new names
logger.debug(f'Store the mapping of old numbers to new names')
new_names_dict = {}

for line in file_content:
    parts = line.strip().split("-", maxsplit=1)
    if len(parts) == 2:
        number, name = parts
        new_names_dict[int(number)] = name.strip()


# List all MP4 files in the current directory
logger.debug('Getting all video file names')
mp4_files = [file for file in os.listdir() if file.lower().endswith(".mp4")]



# Rename the files based on the mapping
logger.debug('Starting the renaming process...')

for mp4_file in mp4_files:
    # Extract the number from the filename using regular expressions
    match = re.match(r"lesson(\d+)\..*", mp4_file)    
    
    if match:
        file_number = int(match.group(1))

        # print(f"Match: {match} -- Found file '{mp4_file}' with number '{file_number}'")

        if file_number in new_names_dict:
            new_name = f"{str(file_number).zfill(3)}-{new_names_dict[file_number]}.mp4"
            os.rename(mp4_file, new_name)
            logger.info(f"Renamed '{mp4_file}' to '{new_name}'")
        else:
            logger.info(f"Skipping file '{mp4_file}' -- match {match} not found")

