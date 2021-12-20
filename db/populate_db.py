#!/usr/bin/env python3

import pymongo
import csv
from dataclasses import dataclass


@dataclass
class Pokemon:
    """
    Represents a Pokemon that holds its id, name, typings, statistics, generation, and legendary-ness.
    """

    id_: int
    name: str
    type1: str
    type2: str
    total: int
    hp: int
    attack: int
    defense: int
    sp_attack: int
    sp_defense: int
    speed: int
    generation: int
    legendary: bool


def extract_data_from_csv(filename: str) -> list[Pokemon]:
    """
    Extract Pokemon data from the csv file and create a list of Pokemon holding it.
    """
    pokemon_list = []
    with open(filename, mode="r", encoding="utf-8") as csv_file:
        csv_reader = csv.reader(csv_file)

        # Rows coming from csv_reader consist of:
        # ID `id_`,
        # name `name`,
        # main type `type1`,
        # secondary type `type2`,
        # total statistic points `total`,
        # hit points `hp`,
        # attack points `attack`,
        # defense points `defense`,
        # special attack points `sp_attack`,
        # special defense points `sp_defense`,
        # speed points `speed`,
        # generation number `generation`,
        # and a legendary boolean value `legendary`.
        for row in csv_reader:
            pokemon = Pokemon(
                int(row[0]),
                row[1],
                row[2].lower(),
                row[3].lower(),
                int(row[4]),
                int(row[5]),
                int(row[6]),
                int(row[7]),
                int(row[8]),
                int(row[9]),
                int(row[10]),
                int(row[11]),
                row[12] == "True",
            )
            pokemon_list.append(pokemon)
    return pokemon_list


def insert_data_into_db(pokemon: list[Pokemon]) -> None:
    """
    Establish a connection to the database, reset appropriate database,
    and insert data into a new collection.
    """
    client = pymongo.MongoClient()
    client.drop_database("pokemon_database")
    db = client["pokemon_database"]
    collection = db["pokemon_collection"]
    collection.insert_many([vars(p) for p in pokemon])
    client.close()


def main() -> None:
    """
    Load the data from a csv file and insert it into a MongoDB database.
    """
    import json

    with open("script_constants.json", "r") as file:
        constants = json.load(file)
    pokemon_data_filename = constants["Pokemon_data_filename"]
    pokemon = extract_data_from_csv(pokemon_data_filename)
    insert_data_into_db(pokemon)


if __name__ == "__main__":
    main()
