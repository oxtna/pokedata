#!/usr/bin/env python3

import get_csv
import populate_db


def main() -> None:
    """
    Download, extract and save Pokemon data as a csv file,
    and insert it into a MongoDB database.
    """
    get_csv.main()
    populate_db.main()
