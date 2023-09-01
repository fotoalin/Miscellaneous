import argparse
import logging
import os
import re
import sys

logger = logging.getLogger("mp4_file_renamer")

# Set the logging level
logger.setLevel(logging.DEBUG)

# Create a file handler
file_handler = logging.FileHandler("rename.log")
file_handler.setLevel(logging.DEBUG)

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a logging format
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

"""
This script will attempt to rename all files in the current folder that matches given regex pattern according to the names found in the specified text file.
It will try to match the filename number with the number in the text file and rename the file accordingly.

The syntax is as follows:

    python3 rename.py -p <pattern> -f <text_file>

    <pattern> is a string that will be converted to a regular expression pattern.
    <text_file> is the name of the text file containing the new names, each on a separate line.

The text file should contain the new names, each on a separate line, in the following format:
    001 - Introduction
    002 - Getting Started
    003 - The Basics
    004 - Advanced Concepts
    005 - Conclusion
"""
# check python version and exit if it's not 3.6 or higher
if not sys.version_info >= (3, 10):
    logger.error("This script requires Python 3.6 or higher. Exiting...")
    sys.exit()

# ---------------------------------------------------------------
# Set up argparse to handle command-line arguments
parser = argparse.ArgumentParser(
    description="Rename .mp4 files based on a pattern and names from a file."
)
parser.add_argument(
    "-p",
    "--pattern",
    required=True,
    help="Pattern to match .mp4 files (e.g., lesson*.mp4)",
)
parser.add_argument(
    "-f",
    "--file",
    required=True,
    help="File containing new names, each on a separate line",
)
parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
# parser.add_argument('-h', '--help', action='store_true', help='Show help message')

# Parse the command-line arguments
args = parser.parse_args()

# check if debug mode is enabled
logger.setLevel(logging.INFO)
if args.debug:
    logger.setLevel(logging.DEBUG)
    logger.debug("Debug mode enabled")

if not args.file:
    logger.error(f"File is required. Exiting...")
    sys.exit()
elif args.file and not os.path.isfile(args.file):
    logger.error(f"File '{args.file}' not found. Exiting...")
    sys.exit()

# pattern and file are required arguments, so no need to check if they are empty
if not args.pattern:
    logger.error(f"Pattern is required. Exiting...")
    sys.exit()
elif args.pattern and not args.pattern.__contains__("*"):
    logger.error(
        f"Pattern '{args.pattern}' does not contain a wildcard character. Exiting..."
    )
    sys.exit()

# Convert user input pattern to a regular expression pattern
pattern = str(args.pattern)
pattern = re.compile(pattern)

# Get the name of the text file containing the new names
new_names_source_file = args.file
#  ---------------------------------------------------------------


# Ask for confirmation
reply = input(
    'This script will rename all .mp4 files in the current folder according to the names found in "Table of contents numbering.txt".\nAre you sure you want to do that? '
)

if not any(keyword in reply.lower() for keyword in ["yes", "y"]):
    logger.info("Exiting... No files were renamed.")
    sys.exit()

# Read the numbering from "Table of contents numbering.txt"
logger.debug(f"Opening {new_names_source_file}")
with open(new_names_source_file, "r") as table_of_contents_file:
    file_content = [line.strip() for line in table_of_contents_file.readlines()]

# Create a dictionary to store the mapping of old numbers to new names
logger.debug(f"Store the mapping of old numbers to new names")
new_names_dict = {}


for line in file_content:
    parts = line.strip().split("-", maxsplit=1)
    if len(parts) == 2:
        number, name = parts
        new_names_dict[int(number)] = name.strip()


# List all MP4 files in the current directory
logger.debug("Getting all video file names")

mp4_files = [
    file
    for file in os.listdir()
    if file.lower().endswith(".mp4") and re.match(pattern, file)
]

if len(mp4_files) == 0:
    logger.info("No .mp4 files found in the current directory. Exiting...")
    sys.exit()


# Rename the files based on the mapping
logger.debug("Starting the renaming process...")

for mp4_file in mp4_files:
    # Extract the number from the filename using regular expressions
    # match = re.match(r"lesson(\d+)\..*", mp4_file)
    match = re.match(pattern, mp4_file)

    if match:
        file_number = int(match.group(1))

        # print(f"Match: {match} -- Found file '{mp4_file}' with number '{file_number}'")

        if file_number in new_names_dict:
            new_name = f"{str(file_number).zfill(3)}-{new_names_dict[file_number]}.mp4"
            os.rename(mp4_file, new_name)
            logger.info(f"Renamed '{mp4_file}' to '{new_name}'")
        else:
            logger.info(f"Skipping file '{mp4_file}' -- match {match} not found")

    else:
        logger.info(f"Skipping file '{mp4_file}' -- no match found")

logger.debug("Finished the renaming process")
