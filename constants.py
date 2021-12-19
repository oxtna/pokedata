import json

with open("script_constants.json", "r") as file:
    constants = json.load(file)

# URL of Pokemon data in a csv format
POKEMON_DATA_URL = constants["Pokemon_data_URL"]
# Name of the csv file that the Pokemon data will be saved to
POKEMON_DATA_FILENAME = constants["Pokemon_data_filename"]
