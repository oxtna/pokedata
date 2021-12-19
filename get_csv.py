#!/usr/bin/env python3

import requests

from constants import POKEMON_DATA_URL, POKEMON_DATA_FILENAME

from typing import NoReturn


def download_data(url: str = POKEMON_DATA_URL) -> str:
    """
    Download data located at the url and return it as a decoded string.
    """
    req = requests.get(url)
    data = req.content.decode(req.encoding)
    return data


def save_data(data: str, filename: str = POKEMON_DATA_FILENAME) -> NoReturn:
    """
    Write data to a csv file. The constant POKEMON_DATA_FILENAME is the default
    filename for the csv file.
    """
    with open(filename, mode="w", encoding="utf-8") as file:
        file.write(data)


def main() -> NoReturn:
    """
    Download and save Pokemon data as a csv file.
    """
    data = download_data()
    save_data(data)


if __name__ == "__main__":
    main()
