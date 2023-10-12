from __future__ import annotations  
from dataclasses import dataclass
from random_gen import RandomGen

# Islands can have names other than this. This is just used for random generation.
ISLAND_NAMES = [
    "Dawn Island",
    "Shimotsuki Village",
    "Gecko Islands",
    "Baratie",
    "Conomi Islands",
    "Drum Island",
    "Water 7"
    "Ohara",
    "Thriller Bark",
    "Fish-Man Island",
    "Zou",
    "Wano Country",
    "Arabasta Kingdom",
    # 13 🌞 🏃‍♀️
    "Loguetown",
    "Cactus Island",
    "Little Garden",
    "Jaya",
    "Skypeia",
    "Long Ring Long Land",
    "Enies Lobby",
    "Sabaody Archipelago",
    "Impel Down",
    "Marineford",
    "Punk Hazard",
    "Dressrosa",
    "Whole Cake Island",
]

@dataclass
class Island:

    name: str
    money: float
    marines: int

    def __eq__(a: Island, b:Island):
        return (a.name == b.name and a.money == b.money and a.marines == b.marines)

    @classmethod
    def random(cls):
        return Island(
            RandomGen.random_choice(ISLAND_NAMES),
            RandomGen.random() * 500,
            RandomGen.randint(0, 300),
        )
