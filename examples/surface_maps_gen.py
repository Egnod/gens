import matplotlib.pylab as plt
import seaborn

from gens.geo.map import Map

for _ in range(10):
    m = Map()

    m.generate()

    seaborn.heatmap(m._surface_map._surface_map)
    plt.show()
