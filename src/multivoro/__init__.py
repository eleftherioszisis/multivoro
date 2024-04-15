import numpy as np
from collections.abc import Sequence

from ._multivoro import compute_voronoi_3d as _compute_voronoi_3d
from multivoro.exceptions import MultiVoroError


def compute_voronoi(
    points: np.ndarray,
    *,
    limits: np.ndarray,
    periodic_boundaries: tuple[bool] = (False, False, False),
    radii: np.ndarray | None = None,
    blocks: np.ndarray | None =None
):
    """Generate a Voronoi or Laguerre tessellation.
    """
    points = _parse_points(points)

    if radii is None:
        raise NotImplementedError("Not yet supported.")

    radii = _parse_radii(radii, len(points))

    limits = _limits(limits)
    blocks = _blocks(blocks, limits, len(points))
    periodic_boundaries = _periodic_boundaries(periodic_boundaries)

    return _compute_voronoi_3d(points, radii, limits, blocks, periodic_boundaries)


def _parse_points(points: np.ndarray) -> np.ndarray:
    """Ensure `points` array has the correct dtype, contiguous order, and shape."""

    result = np.asarray(points, dtype=float, order="C")

    if result.ndim != 2 or result.shape[1] != 3:
        raise MultiVoroError(f"Points array shape expected to be (N, 3), got shape: {result.shape}")

    return result


def _parse_radii(radii: np.ndarray | None, n_elements: int) -> np.ndarray | None:

    radii = np.asarray(radii, dtype=float, order="C")

    if radii.ndim != 1 or len(radii) != n_elements:
        raise MultiVoroError(f"`points` and `radii` shape mismatch. Expected {n_elements}, got {len(radii)}.")

    return radii


def _limits(limits: np.ndarray) -> np.ndarray:

    limits = np.asarray(limits, dtype=float)

    if limits.shape != (2, 3):
        raise MultiVoroError(f"`limits` shape should be (2, 3). Got: {limits.shape}")

    return limits


def _blocks(blocks: np.ndarray | None, limits: np.ndarray, n_elements: int) -> np.ndarray:

    if blocks is not None:
        blocks = np.asarray(blocks, dtype=np.uint32, order="C")

        if blocks.shape != (3,):
            raise MultiVoroError(f"`blocks` shape mismatch. Expected (3,), got {blocks.shape}")

    Lx, Ly, Lz = limits[1] - limits[0]

    Nthird = pow(n_elements / (Lx * Ly * Lz), 1.0 / 3.0)

    return np.array(
        [
            max(1, round(Nthird * Lx)),
            max(1, round(Nthird * Ly)),
            max(1, round(Nthird * Lz)),
        ],
        dtype=np.uint32,
    )


def _periodic_boundaries(periodic_boundaries: np.ndarray) -> np.ndarray:
    periodic_boundaries = np.asarray(periodic_boundaries, dtype=bool)

    if periodic_boundaries.shape != (3,):
        raise MultiVoroError(f"`periodic_boundaries` shape mismatch. Expected (3,), got {periofic.shape}")

    return periodic_boundaries
