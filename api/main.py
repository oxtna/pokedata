from fastapi import FastAPI
from pymongo import MongoClient
from typing import Any, Iterable

MIN_POKEMON_STAT_VALUE = 0
MAX_POKEMON_STAT_VALUE = 1000

app = FastAPI()

uri = "mongodb://localhost"
port = 27017
db_client = MongoClient(uri, port)
db = db_client.get_database("pokemon_database")
pokemon = db.get_collection("pokemon_collection")


def _strip_db_indexing_key(obj: dict[str, Any]):
    """
    Strip MongoDB's ObjectId key `_id`.
    """
    return {key: obj[key] for key in obj if key != "_id"}


@app.get("/")
async def root():
    return {}


@app.get("/pokemon")
async def get_pokemon():
    all_pokemon: Iterable[dict[str, Any]] = pokemon.find({})
    res = []
    for pkmn in all_pokemon:
        res.append(_strip_db_indexing_key(pkmn))
    return res


@app.get("/pokemon/")
async def query_pokemon(
    name: str = "",
    types: str = "",
    legendary: bool = None,
    gen: int = None,
    min_total: int = MIN_POKEMON_STAT_VALUE,
    max_total: int = MAX_POKEMON_STAT_VALUE,
    min_hp: int = MIN_POKEMON_STAT_VALUE,
    max_hp: int = MAX_POKEMON_STAT_VALUE,
    min_attack: int = MIN_POKEMON_STAT_VALUE,
    max_attack: int = MAX_POKEMON_STAT_VALUE,
    min_defense: int = MIN_POKEMON_STAT_VALUE,
    max_defense: int = MAX_POKEMON_STAT_VALUE,
    min_sp_attack: int = MIN_POKEMON_STAT_VALUE,
    max_sp_attack: int = MAX_POKEMON_STAT_VALUE,
    min_sp_defense: int = MIN_POKEMON_STAT_VALUE,
    max_sp_defense: int = MAX_POKEMON_STAT_VALUE,
    min_speed: int = MIN_POKEMON_STAT_VALUE,
    max_speed: int = MAX_POKEMON_STAT_VALUE,
):
    types = types.split()
    if len(types) > 2:
        return []

    matching_pokemon: Iterable[dict[str, Any]] = pokemon.find(
        {
            "$and": [
                {"name": {"$regex": name, "$options": "i"}},
                {
                    "$or": [
                        {"type1": types[0].lower(), "type2": types[1].lower()},
                        {"type1": types[1].lower(), "type2": types[0].lower()},
                    ]
                    if len(types) == 2
                    else [{"type1": types[0].lower()}, {"type2": types[0].lower()}]
                    if len(types) == 1
                    else [{"type1": {"$exists": True}}]
                },
                {"total": {"$gte": min_total, "$lte": max_total}},
                {"hp": {"$gte": min_hp, "$lte": max_hp}},
                {"attack": {"$gte": min_attack, "$lte": max_attack}},
                {"defense": {"$gte": min_defense, "$lte": max_defense}},
                {"sp_attack": {"$gte": min_sp_attack, "$lte": max_sp_attack}},
                {"sp_defense": {"$gte": min_sp_defense, "$lte": max_sp_defense}},
                {"speed": {"$gte": min_speed, "$lte": max_speed}},
                {"generation": gen if gen is not None else {"$exists": True}},
                {
                    "legendary": legendary
                    if legendary is not None
                    else {"$exists": True}
                },
            ]
        }
    )
    res = []
    # Skip MongoDB's ObjectId's key `_id`
    for pkmn in matching_pokemon:
        res.append(_strip_db_indexing_key(pkmn))
    return res


@app.get("/pokemon/{id_}")
async def get_pokemon_with_id(id_: int):
    found_pokemon: dict[str, Any] = pokemon.find_one({"id_": id_})
    # Skip MongoDB's ObjectId key `_id`
    res = _strip_db_indexing_key(found_pokemon)
    return res


@app.get("/type/{type_}")
async def get_pokemon_with_type(type_: str):
    matching_type: Iterable[dict[str, Any]] = pokemon.find(
        {"$or": [{"type1": type_.lower()}, {"type2": type_.lower()}]}
    )
    res = []
    # Skip MongoDB's ObjectId key `_id`
    for pkmn in matching_type:
        res.append(_strip_db_indexing_key(pkmn))
    return res


@app.get("/gen/{gen}")
async def get_pokemon_of_generation(gen: int):
    matching_gen: Iterable[dict[str, Any]] = pokemon.find({"generation": gen})
    res = []
    # Skip MongoDB's ObjectId key `_id`
    for pkmn in matching_gen:
        res.append(_strip_db_indexing_key(pkmn))
    return res


@app.get("/legendary")
async def get_legendary_pokemon():
    legendary_pokemon: Iterable[dict[str, Any]] = pokemon.find({"legendary": True})
    res = []
    # Skip MongoDB's ObjectId key `_id`
    for pkmn in legendary_pokemon:
        res.append(_strip_db_indexing_key(pkmn))
    return res
