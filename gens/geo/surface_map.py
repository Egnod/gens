from typing import List, Tuple, Union
from uuid import uuid4

import numpy as np
from scipy import ndimage
from scipy.ndimage import generate_binary_structure

from gens.geo.biom import Biom
from gens.geo.enums import BiomLevel, BiomType, GeoClass


class SurfaceMap:
    def __init__(self, noise_map: np.ndarray) -> None:
        self._noise_map = noise_map
        self._surface_map = None

        self._bioms: List[Biom] = []

    def _extract_surface_map(self) -> None:
        self._surface_map = np.where(self._noise_map >= 0, 1, 0)

    def _inverse_surface_map(self) -> np.ndarray:
        return self._surface_map - 1

    def _distinct_surface_map(self, surface_map: np.ndarray) -> Tuple[Union[np.ndarray, int], int]:
        return ndimage.label(surface_map, structure=generate_binary_structure(2, 2))

    def _get_geo_class(self, biom_area, biom_class):
        biom_area_percent = round(biom_area / (len(self._noise_map) ** 2), 2)

        if biom_class == BiomType.water:
            if 0.1 > biom_area_percent:
                return GeoClass.lake

            elif 0.25 > biom_area_percent > 0.1:
                return GeoClass.sea

            else:
                return GeoClass.ocean

        elif biom_class == BiomType.ground:
            if 0.1 > biom_area_percent:
                return GeoClass.island
            else:
                return GeoClass.continent

    def _extract_ground_bioms(self):
        ground_map, count_bioms = self._distinct_surface_map(self._surface_map)

        for biom_index in range(1, count_bioms + 1):
            coordinates = np.column_stack(np.where(ground_map == biom_index))

            biom = Biom(
                biom_id=uuid4(),
                biom_level=BiomLevel.surface,
                biom_type=BiomType.ground,
                geo_class=self._get_geo_class(len(coordinates), BiomType.ground),
                coordinates=coordinates,
            )

            self._bioms.append(biom)

    def _extract_water_bioms(self):
        inversed_map = self._inverse_surface_map()
        water_map, count_bioms = self._distinct_surface_map(inversed_map)

        for biom_index in range(1, count_bioms + 1):
            coordinates = np.column_stack(np.where(water_map == biom_index))

            biom = Biom(
                biom_id=uuid4(),
                biom_level=BiomLevel.surface,
                biom_type=BiomType.water,
                geo_class=self._get_geo_class(len(coordinates), BiomType.water),
                coordinates=coordinates,
            )

            self._bioms.append(biom)

    def extract(self) -> "SurfaceMap":
        self._extract_surface_map()

        self._extract_ground_bioms()
        # self._extract_water_bioms()

        return self
