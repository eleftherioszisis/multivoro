import numpy as np
import pytest
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
            ],
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

    limits = np.array([[-1.0, -1.0, -1.0], [1.0, 1.0, 1.0]])

    with pytest.raises(ValueError):
        compute_voronoi(points, radii=radii, limits=limits)


def test_compute_voronoi__three_cells():
    points = np.array(
        [
            [-0.33714694, -0.89021149, -1.7435466],
            [-1.2302039, 0.49462818, 1.54245981],
            [-0.61253835, 1.25474613, 1.70555295],
        ]
    )

    limits = np.array([[-2.0, -2.0, -2.0], [2.0, 2.0, 2.0]])

    radii = np.array([0.1, 0.1, 0.1])

    cell1, cell2, cell3 = compute_voronoi(points=points, radii=radii, limits=limits)

    expected_vertices_1 = np.array(
        [
            (-2.0, -2.0, -2.0),
            (2.0, -2.0, -2.0),
            (-2.0, 2.0, -2.0),
            (2.0, 2.0, -2.0),
            (-2.0, -2.0, 0.32840356693596906),
            (2.0, -2.0, 1.4155066887920684),
            (-2.0, 2.0, -1.3573383264924677),
            (2.0, 1.9999999999999996, -0.951822652748408),
            (-1.551204502023337, 2.0, -1.2353665797611193),
            (2.0, -1.400224074487332, 1.162739837715439),
        ]
    )
    npt.assert_allclose(cell1.get_vertices(), expected_vertices_1, rtol=1e-6)

    expected_neighbors_1 = np.array([-5, -2, -3, -1, -4, 1, 2])
    npt.assert_array_equal(cell1.get_neighbors(), expected_neighbors_1)

    expected_faces_1 = np.array(
        [
            4,
            1,
            3,
            2,
            0,
            5,
            1,
            5,
            9,
            7,
            3,
            4,
            1,
            0,
            4,
            5,
            4,
            2,
            6,
            4,
            0,
            5,
            2,
            3,
            7,
            8,
            6,
            5,
            4,
            6,
            8,
            9,
            5,
            3,
            7,
            9,
            8,
        ]
    )
    npt.assert_array_equal(cell1.get_face_vertices(), expected_faces_1)

    expected_vertices_2 = np.array(
        [
            (-2.0, -2.0, 0.32840356693596906),
            (2.0, -2.0, 1.4155066887920689),
            (-2.0, 1.9999999999999998, -1.3573383264924672),
            (-2.0, 2.0, 0.46430950964627904),
            (-2.0, -2.0, 2.0),
            (2.0, -2.0, 2.0),
            (2.0, -1.5798690759690044, 2.0),
            (-2.0, 1.6704977343455365, 2.0),
            (2.0, -1.40022407448733, 1.1627398377154385),
            (-1.5512045020233343, 1.9999999999999998, -1.2353665797611182),
        ]
    )
    npt.assert_allclose(cell2.get_vertices(), expected_vertices_2, rtol=1e-6)

    expected_neighbors_2 = np.array([0, -2, -3, -1, -4, 2, -6])
    npt.assert_array_equal(cell2.get_neighbors(), expected_neighbors_2)

    expected_faces_2 = np.array(
        [
            5,
            1,
            8,
            9,
            2,
            0,
            4,
            1,
            5,
            6,
            8,
            4,
            1,
            0,
            4,
            5,
            5,
            2,
            3,
            7,
            4,
            0,
            3,
            2,
            9,
            3,
            5,
            3,
            9,
            8,
            6,
            7,
            4,
            4,
            7,
            6,
            5,
        ]
    )
    npt.assert_array_equal(cell2.get_face_vertices(), expected_faces_2)

    expected_vertices_3 = np.array(
        [
            (-2.0, 2.0, 0.46430950964627815),
            (2.0000000000000004, -1.4002240744873307, 1.1627398377154388),
            (-1.5512045020233347, 2.0, -1.2353665797611182),
            (2.0, 2.0, -0.9518226527484073),
            (-2.0, 1.6704977343455365, 2.0),
            (1.9999999999999996, -1.579869075969004, 2.0),
            (-2.0, 2.0, 2.0),
            (2.0, 2.0, 2.0),
        ]
    )
    npt.assert_allclose(cell3.get_vertices(), expected_vertices_3, rtol=1e-6)

    expected_neighbors_3 = np.array([1, 0, -2, -4, -6, -1])
    npt.assert_array_equal(cell3.get_neighbors(), expected_neighbors_3)

    expected_faces_3 = np.array(
        [5, 1, 2, 0, 4, 5, 3, 1, 3, 2, 4, 1, 5, 7, 3, 5, 2, 3, 7, 6, 0, 4, 4, 6, 7, 5, 3, 4, 0, 6]
    )
    npt.assert_array_equal(cell3.get_face_vertices(), expected_faces_3)
