# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Create Orbit object from State Vectors."""

import numpy as np
from perseo_core.geometry.navigation import CubicSplineTrajectory

from aresys_io.product_metadata.metadata_elements import StateVectors

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
    time_axis = (
        np.arange(state_vectors.position_vector.shape[0]) * state_vectors.time_step  # pyrefly: ignore[unsupported-operation]
        + state_vectors.reference_time
    )
    return CubicSplineTrajectory(
        times=time_axis,
        positions=state_vectors.position_vector.reshape(-1, 3),
        velocities=state_vectors.velocity_vector.reshape(-1, 3),
    )
