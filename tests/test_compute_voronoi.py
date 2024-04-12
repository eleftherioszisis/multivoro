import numpy as np
from multivoro import compute_voronoi



def test_compute_voronoi():

    points = np.array([
        [0., 0., 0.],
        [0., 1., 0.],
        [0., 0., 1.],
        [1., 0., 0.],
        [1., 1., 0.],
        [1., 0., 1.],
        [1., 1., 1.],
    ]
                      )
    radii = np.array([
        0.1,
        0.1,
        0.1,
        0.1,
        0.1,
        0.1,
        0.1,
    ])
    limits = np.array([
        [-1., -1., -1.],
        [2., 2., 2.],
    ])
    compute_voronoi(points=points, radii=radii, limits=limits)


if __name__ == "__main__":

    test_compute_voronoi()
