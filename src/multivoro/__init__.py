import numpy as np
from collections.abc import Sequence

from ._multivoro import compute_voronoi_3d as _compute_voronoi_3d


INIT_MEMORY_ALLOCATION = 8


def compute_voronoi(
    points,
    *,
    limits,
    periodic_boundaries: tuple[bool] = (False, False, False),
    radii=None,
    blocks=None
):

    N = len(points)
    Lx, Ly, Lz = limits[1] - limits[0]

    # make bx, by, bz from blocks, or make it up
    if blocks is None:
        V = Lx * Ly * Lz
        Nthird = pow(N / V, 1.0 / 3.0)
        blocks = np.array(
            [
                max(1, round(Nthird * Lx)),
                max(1, round(Nthird * Ly)),
                max(1, round(Nthird * Lz)),
            ],
            dtype=np.uint32,
        )

    if len(points) != len(radii):
        raise RuntimeError("Number of points and radii are not consistent.")

    limits = np.asarray(limits, dtype=float)

    radii = np.array(radii, dtype=float)

    periodic_boundaries = np.asarray(periodic_boundaries, dtype=bool)

    cells = _compute_voronoi_3d(points, radii, limits, blocks, periodic_boundaries)

    breakpoint()
    print()
