from collections.abc import Sequence

from ._multivoro import ContainerPoly as _ContainerPoly


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
        blocks = (
            max(1, round(Nthird * Lx)),
            max(1, round(Nthird * Ly)),
            max(1, round(Nthird * Lz)),
        )

    if len(points) != len(radii):
        raise RuntimeError("Number of points and radii are not consistent.")

    container = _ContainerPoly(
        float(limits[0][0]),  # ax
        float(limits[1][0]),  # bx
        float(limits[0][1]),  # ay
        float(limits[1][1]),  # by
        float(limits[0][2]),  # az
        float(limits[1][2]),  # bz
        blocks[0],  # nx
        blocks[1],  # ny
        blocks[2],  # nz
        periodic_boundaries[0],
        periodic_boundaries[1],
        periodic_boundaries[2],
        INIT_MEMORY_ALLOCATION,
        1
    )

    for i, point in enumerate(points):
        container.put(i, float(point[0]), float(point[1]), float(point[2]), float(radii[i]))
