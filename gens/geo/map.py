from typing import List, Optional, Union

import numpy as np
from hkb_diamondsquare import DiamondSquare

from gens.geo.surface_map import SurfaceMap


class Map:
    def __init__(self, seed: Optional[int] = None, size: Optional[int] = None) -> None:
        self._seed = seed if seed else self._generate_seed()

        self._randomizer = np.random.RandomState(seed=self._seed)
        self._size: int = size if size else self._randomizer.randint(200, 400)
        self._area: int = self._size ** 2
        self._octaves: List[Union[int, float]] = [0.6]

        self._noise_map: np.ndarray = np.zeros((self._size, self._size))
        self._map: Optional[np.ndarray] = None
        self._surface_map: Optional[SurfaceMap] = None

    def _generate_seed(self) -> int:
        return np.random.randint(2 ** 8, 2 ** 16 - 1)

    def _get_noise_layer(self, octave) -> np.ndarray:
        return DiamondSquare.diamond_square(
            shape=(self._size, self._size),
            min_height=-0.8 - (octave - self._randomizer.uniform(0.4, 0.5)),
            max_height=0.5 + octave - self._randomizer.uniform(0.2, 0.25),
            roughness=octave,
            random_seed=self._seed,
        )

    def _generate_noise_map(self) -> None:
        for octave in self._octaves:
            self._noise_map += self._get_noise_layer(octave)

    def generate(self):
        self._generate_noise_map()

        self._surface_map = SurfaceMap(self._noise_map).extract()
