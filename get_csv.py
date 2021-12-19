#!/usr/bin/env python3

import requests

from constants import POKEMON_DATA_URL, POKEMON_DATA_FILENAME


def download_data(url: str = POKEMON_DATA_URL) -> str:
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


def save_data(data: str, filename: str = POKEMON_DATA_FILENAME) -> None:
    """
    Write data to a csv file. The constant POKEMON_DATA_FILENAME is
    the default filename for the csv file.
    """
    with open(filename, mode="w", encoding="utf-8") as file:
        file.write(data)


def main() -> None:
    """
    Download, extract and save Pokemon data as a csv file.
    """
    data = download_data()
    data = strip_column_names(data)
    save_data(data)


if __name__ == "__main__":
    main()
