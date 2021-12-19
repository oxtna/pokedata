#!/usr/bin/env python3

import requests


def download_data(url: str) -> str:
    """
    Download data located at the url and return it as a decoded string.
    """
    req = requests.get(url)
    data = req.content.decode(req.encoding)
    return data


def strip_column_names(data: str) -> str:
    """
    Strip the column names that are located at the start of the string,
    up until the first newline character.
    """
    first_newline_index = data.find("\n")
    if first_newline_index == -1:
        return data
    return data[first_newline_index + 1 :]


def save_data(data: str, filename: str) -> None:
    """
    Write data to a csv file.
    """
    with open(filename, mode="w", encoding="utf-8") as file:
        file.write(data)


def main() -> None:
    """
    Download, extract and save Pokemon data as a csv file.
    """
    import json

    with open("script_constants.json", "r") as file:
        constants = json.load(file)
    pokemon_data_url = constants["Pokemon_data_URL"]
    pokemon_data_filename = constants["Pokemon_data_filename"]
    data = download_data(pokemon_data_url)
    data = strip_column_names(data)
    save_data(data, pokemon_data_filename)


if __name__ == "__main__":
    main()
