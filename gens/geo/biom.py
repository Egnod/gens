from dataclasses import dataclass
from typing import List
from uuid import UUID

from gens.geo.enums import BiomLevel, BiomType, GeoClass


@dataclass
class Biom:
    biom_id: UUID
    biom_level: BiomLevel
    biom_type: BiomType
    geo_class: GeoClass
    coordinates: List[List[int]]
