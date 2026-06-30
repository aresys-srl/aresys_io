# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""read trajectory module."""

from pathlib import Path
from typing import Literal

from aresys_io.core.parsing import parse
from aresys_io.sarsystem.models import trajectory_file as model_trajectory
from aresys_io.sarsystem.trajectory import (
    AntennaPhaseCentrePositionTowardsBodyMassCenter,
    AntennaRotation,
    AttitudeInfo,
    StateVectorData,
    Trajectory,
)
from aresys_io.sarsystem.utils import (
    value_array_type_to_array,
)

TrajectoryFormat = Literal["GSS", "RDB"]


def read_trajectory(filename: Path, traj_format: TrajectoryFormat = "GSS") -> Trajectory:
    """Read a trajectory XML file and parse its contents into a Trajectory object.

    The trajectory file can be in either GSS or RDB format.

    Parameters
    ----------
    filename : Path
        Path to the XML file containing the trajectory data.
    traj_format : TrajectoryFormat
        Format of the XML file: possible values "GSS" or "RDB".

    Returns
    -------
    Trajectory
        Parsed trajectory data as a Trajectory object.

    Raises
    ------
    ValueError
        If the provided trajectory format is not supported.

    """
    if traj_format == "GSS":
        file_content = parse(
            filename.read_text(encoding="utf-8"),
            model_trajectory.GsstrajectoryFile,
        )
    elif traj_format == "RDB":
        file_content = parse(filename.read_text(encoding="utf-8"), model_trajectory.AresysXmlDoc)
    else:
        msg = "unsupported trajectory file format"
        raise ValueError(msg)

    # antenna_phase_centre_position_towards_body_mass_center

    antenna_phase_centre_position_towards_body_mass_center = (
        AntennaPhaseCentrePositionTowardsBodyMassCenter(
            tx=value_array_type_to_array(
                file_content.channel.antenna_phase_centre_position_towards_body_mass_center.tx,
            ).reshape([-1, 3]),
            rx=value_array_type_to_array(
                file_content.channel.antenna_phase_centre_position_towards_body_mass_center.rx,
            ).reshape([-1, 3]),
        )
        if file_content.channel.antenna_phase_centre_position_towards_body_mass_center is not None
        else None
    )

    # Antenna Rotation
    antenna_rotation = (
        AntennaRotation.from_model(file_content.channel.antenna_rotation_ypr)
        if file_content.channel.antenna_rotation_ypr is not None
        else None
    )

    # state vector
    state_vector = StateVectorData.from_model(file_content.channel.state_vector_data)

    # attitude info
    attitude_info = AttitudeInfo.from_model(file_content.channel.attitude_info)

    orbit_length = (
        file_content.channel.full_orbit_cycle_length.value
        if file_content.channel.full_orbit_cycle_length is not None
        else file_content.channel.state_vector_data.n_sv_n
        * file_content.channel.state_vector_data.dt_sv_s
    )

    return Trajectory(
        orbit_length=orbit_length,
        attitude_info=attitude_info,
        state_vector=state_vector,
        antenna_rotation=antenna_rotation,
        antenna_phase_centre_position_towards_body_mass_center=antenna_phase_centre_position_towards_body_mass_center,
    )


__all__ = ["read_trajectory"]
