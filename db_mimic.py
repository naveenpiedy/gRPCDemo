# Created by NaveenPiedy at 6/18/2024 8:43 AM
from dataclasses import dataclass
from typing import Dict, List

"""
The dataclass and dicts are to mimic a database. 
"""
@dataclass
class Movie:
    id: str
    name: str
    actors: List[str]
    director: str
    rating: float


@dataclass
class Actor:
    id: str
    actor_name: str
    movie_names: List[str]


movies_db: Dict[str, Movie] = {}
actors_db: Dict[str, Actor] = {}

avengers = Movie('1', 'Avengers', ["Robert", "Chris"], 'Joss Wheadon', 4.2)

movies_db['avengers'] = avengers
actors_db['robert'] = Actor('1', 'Robert', ['Avengers'])
actors_db['chris'] = Actor('2', 'Chris', ['Avengers'])