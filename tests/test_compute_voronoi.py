import pytest
import numpy as np
from multivoro import compute_voronoi

from numpy import testing as npt


@pytest.mark.parametrize(
    "cfg",
    [
        {
            "points": np.array([[-1.0, 0.0, 0.0], [1.0, 0.0, 0.0]]),
            "radii": np.array([1.0, 1.0]),
            "limits": np.array([[-2.0, -1.0, -1.0], [2.0, 1.0, 1.0]]),
            "expected": [
                {
                    "vertices": [
                        [-2.0, -1.0, -1.0],
                        [0.0, -1.0, -1.0],
                        [-2.0, 1.0, -1.0],
                        [0.0, 1.0, -1.0],
                        [-2.0, -1.0, 1.0],
                        [0.0, -1.0, 1.0],
                        [-2.0, 1.0, 1.0],
                        [0.0, 1.0, 1.0],
                    ],
                },
                {
                    "vertices": [
                        [0.0, -1.0, -1.0],
                        [2.0, -1.0, -1.0],
                        [0.0, 1.0, -1.0],
                        [2.0, 1.0, -1.0],
                        [0.0, -1.0, 1.0],
                        [2.0, -1.0, 1.0],
                        [0.0, 1.0, 1.0],
                        [2.0, 1.0, 1.0],
                    ],
                },
            ]
        },
    ],
)
def test_compute_voronoi(cfg):

    cells = compute_voronoi(
        points=cfg["points"],
        radii=cfg["radii"],
        limits=cfg["limits"],
    )
    assert len(cells) == len(cfg["expected"])
    for i, cell in enumerate(cells):
        npt.assert_allclose(cell.get_vertices(), cfg["expected"][i]["vertices"])



def test_compute_voronoi__raises():

    points = np.array([[-2.0, 0.0, 0.0], [1.0, 0.0, 0.0]])

    radii = np.array([1.0, 1.0])

    limits = np.array([[-1., -1., -1.], [1., 1., 1.]])

    with pytest.raises(ValueError):
        compute_voronoi(points, radii=radii, limits=limits)


def test_compute_voronoi__occlusion_raises():

    points = np.array([[-1.0, -1.0, -1.0], [1.0, 1.0, 1.0]])

    radii = np.array([1.0, 1.0])

    limits = np.array([[-1., -1., -1.], [1., 1., 1.]])

    with pytest.raises(ValueError):
        compute_voronoi(points, radii=radii, limits=limits)
