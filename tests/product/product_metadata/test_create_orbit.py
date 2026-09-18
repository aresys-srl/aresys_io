# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Unit tests for Trajectory generation from metadata functionalities."""

import numpy as np
import pytest
from perseo_core.timing import PreciseDateTime

from aresys_io.product.metadata import create_trajectory_from_state_vectors, elements


def test_create_orbit_returns_trajectory_with_expected_axes() -> None:
    reference_time = PreciseDateTime.from_numeric_datetime(year=2020)
    state_vectors = elements.StateVectors(
        position_vector=np.array(
            [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0], [7.0, 8.0, 9.0]],
            dtype=np.float64,
        ),
        velocity_vector=np.array(
            [[11.0, 12.0, 13.0], [14.0, 15.0, 16.0], [17.0, 18.0, 19.0]],
            dtype=np.float64,
        ),
        reference_time=reference_time,
        time_step=1.5,
    )

    orbit = create_trajectory_from_state_vectors(state_vectors)

    assert list(orbit.times) == [
        reference_time,
        reference_time + 1.5,
        reference_time + 3.0,
    ]
    np.testing.assert_allclose(orbit.positions, state_vectors.position_vector)
    np.testing.assert_allclose(orbit.velocities, state_vectors.velocity_vector)


def test_create_orbit_requires_at_least_two_state_vectors() -> None:
    reference_time = PreciseDateTime.from_numeric_datetime(year=2021)
    state_vectors = elements.StateVectors(
        position_vector=np.array([[1.0, 2.0, 3.0]], dtype=np.float64),
        velocity_vector=np.array([[4.0, 5.0, 6.0]], dtype=np.float64),
        reference_time=reference_time,
        time_step=2.0,
    )

    with pytest.raises(ValueError, match="at least 2 elements"):
        create_trajectory_from_state_vectors(state_vectors)
