# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Create Attitude object from AttitudeInfo."""

import numpy as np
from perseo_core.geometry.navigation import Trajectory
from perseo_core.geometry.pointing import (
    Attitude,
    compute_antenna_attitude_from_euler_angles,
    compute_sensor_local_axis,
)

from aresys_io.product_metadata.metadata_elements import AttitudeInfo

__all__ = ["create_attitude_from_attitude_info_and_trajectory"]


def create_attitude_from_attitude_info_and_trajectory(
    trajectory: Trajectory,
    attitude_info: AttitudeInfo,
) -> Attitude:
    """Create an Attitude object from Trajectory and AttitudeInfo."""
    times = attitude_info.times
    positions = trajectory.position(times)
    velocities = trajectory.velocity(times)
    sensor_local_axis = compute_sensor_local_axis(
        reference_frame=attitude_info.reference_frame,
        sensor_positions=positions,
        sensor_velocities=velocities,
    )
    return compute_antenna_attitude_from_euler_angles(
        ypr_rad=np.deg2rad(attitude_info.ypr_deg),
        times=times,
        sensor_local_axis=sensor_local_axis,
        rotation_order=attitude_info.rotation_order,
    )
