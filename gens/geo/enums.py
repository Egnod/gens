from enum import Enum


class BiomType(Enum):
    water = "water"
    ground = "ground"


class BiomLevel(Enum):
    surface = "surface"


class GeoClass(Enum):
    lake = "lake"
    sea = "sea"
    ocean = "ocean"
    island = "island"
    continent = "continent"
