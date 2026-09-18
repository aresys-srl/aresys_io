# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Create Orbit object from State Vectors."""

from perseo_core.geometry.navigation import CubicSplineTrajectory

from aresys_io.product.metadata.elements import StateVectors

__all__ = ["create_trajectory_from_state_vectors"]


def create_trajectory_from_state_vectors(state_vectors: StateVectors) -> CubicSplineTrajectory:
    """Create a CubicSplineTrajectory from metadata StateVectors.

    Parameters
    ----------
    state_vectors : StateVectors
        product metadata StateVectors.

    Returns
    -------
    CubicSplineTrajectory
        interpolated trajectory object from given StateVectors
    """
    return CubicSplineTrajectory(
        times=state_vectors.times,
        positions=state_vectors.position_vector.reshape(-1, 3),
        velocities=state_vectors.velocity_vector.reshape(-1, 3),
    )
