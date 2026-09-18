# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Unit tests for Attitude generation from metadata functionalities."""

import numpy as np
from perseo_core.geometry.pointing import compute_sensor_local_axis
from perseo_core.timing import PreciseDateTime

from aresys_io.product.metadata import (
    create_attitude_from_attitude_info_and_trajectory,
    create_trajectory_from_state_vectors,
    elements,
)


def test_create_attitude_returns_attitude_with_expected_axes() -> None:
    reference_time = PreciseDateTime.from_numeric_datetime(year=2020)
    state_vectors = elements.StateVectors(
        position_vector=np.array(
            [
                [7_000_000.0, 0.0, 0.0],
                [7_000_000.0, 7_500.0, 0.0],
                [7_000_000.0, 15_000.0, 0.0],
                [7_000_000.0, 22_500.0, 0.0],
            ],
            dtype=np.float64,
        ),
        velocity_vector=np.array(
            [[0.0, 7_500.0, 0.0]] * 4,
            dtype=np.float64,
        ),
        reference_time=reference_time,
        time_step=1.0,
    )
    trajectory = create_trajectory_from_state_vectors(state_vectors)
    attitude_info = elements.AttitudeInfo(
        ypr_deg=np.zeros((3, 3), dtype=np.float64),
        reference_time=reference_time,
        time_step=1.5,
        reference_frame="ZERODOPPLER",
        rotation_order="YPR",
    )
    expected_times = np.array([reference_time, reference_time + 1.5, reference_time + 3.0])
    expected_axes = compute_sensor_local_axis(
        reference_frame=attitude_info.reference_frame,
        sensor_positions=trajectory.position(expected_times),
        sensor_velocities=trajectory.velocity(expected_times),
    )

    attitude = create_attitude_from_attitude_info_and_trajectory(trajectory, attitude_info)

    assert list(attitude.times) == list(expected_times)
    np.testing.assert_allclose(attitude.reference_frames, expected_axes)
