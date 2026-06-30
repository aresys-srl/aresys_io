# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""write trajectory module."""

from pathlib import Path
from typing import Literal

import numpy as np

from aresys_io.core.parsing import serialize
from aresys_io.sarsystem.models import trajectory_file as trajectory_model
from aresys_io.sarsystem.trajectory import (
    AntennaPhaseCentrePositionTowardsBodyMassCenter,
    AntennaRotation,
    AttitudeInfo,
    StateVectorData,
    Trajectory,
)
from aresys_io.sarsystem.utils import SingleStateVector, Vector, quaternion_to_ypr

TrajectoryFormat = Literal["GSS", "RDB"]


def array_to_value_array_type(
    array: Vector,
) -> trajectory_model.ValueArrayType:
    """Convert a 1D NumPy array to a ValueArrayType object with sequential indices."""
    flat = array.flatten()
    return trajectory_model.ValueArrayType(
        val=[
            trajectory_model.ValueArrayType.Val(value=float(v), n=i + 1)
            for i, v in enumerate(flat)
        ],
    )


def array_to_value_array_type_apc(
    array: SingleStateVector,
) -> trajectory_model.ValueArrayType:
    """Convert a 3-element NumPy array to a ValueArrayType with APC coordinate labels."""
    flat = array.flatten()
    if len(flat) != 3:
        msg = "The input array doesn't have length 3"
        raise ValueError(msg)
    coord_order = ["Xcoord", "Ycoord", "Zcoord"]

    return trajectory_model.ValueArrayType(
        val=[
            trajectory_model.ValueArrayType.Val(value=float(v), n=coord)
            for v, coord in zip(
                flat,
                coord_order,
                strict=True,
            )  # strict = True to check for iterarator different lengths
        ],
    )


def array_to_value_array_type_ypr(
    array: SingleStateVector,
) -> trajectory_model.ValueArrayType:
    """Convert a 3-element NumPy array to a ValueArrayType with angular labels."""
    flat = array.flatten()
    if len(flat) != 3:
        msg = "The input array doesn't have length 3"
        raise ValueError(msg)
    angles_order = ["Yaw", "Pitch", "Roll"]

    return trajectory_model.ValueArrayType(
        val=[
            trajectory_model.ValueArrayType.Val(value=float(v), n=angle)
            for v, angle in zip(
                flat,
                angles_order,
                strict=True,
            )  # strict = True to check for iterarator different lengths
        ],
    )


def attitude_info_to_model(att: AttitudeInfo) -> trajectory_model.AttitudeInfoType:
    """
    Convert AttitudeInfo (Pydantic model) to AttitudeInfoType (dataclass format).

    Parameters
    ----------
    att : AttitudeInfo
        Input attitude information in Pydantic model format.

    Returns
    -------
    AttitudeInfoType
        Converted attitude information as a dataclass.
    """
    yaw, pitch, roll = quaternion_to_ypr(att.rotation)
    return trajectory_model.AttitudeInfoType(
        t_ref_utc=str(att.time_origin),
        dt_ypr_s=att.time_step,
        n_ypr_n=len(yaw),
        yaw_deg=array_to_value_array_type(yaw),
        pitch_deg=array_to_value_array_type(pitch),
        roll_deg=array_to_value_array_type(roll),
        reference_frame=trajectory_model.AttitudeInfoTypeReferenceFrame[att.reference_frame],
        rotation_order=trajectory_model.AttitudeInfoTypeRotationOrder.YPR,  # Can be parameterized
        attitude_type=trajectory_model.AttitudeInfoTypeAttitudeType[att.attitude_type.value],
    )


def state_vector_data_to_model(
    sv: StateVectorData,
) -> trajectory_model.StateVectorDataType:
    """Convert StateVectorData (Pydantic model) to StateVectorDataType (dataclass)."""
    return trajectory_model.StateVectorDataType(
        orbit_number=sv.orbit_number,
        track=sv.track,
        orbit_direction=trajectory_model.StateVectorDataTypeOrbitDirection[
            sv.orbit_direction.name
        ],
        p_sv_m=array_to_value_array_type(sv.position),
        v_sv_m_os=array_to_value_array_type(sv.velocity),
        t_ref_utc=str(sv.time_origin),
        dt_sv_s=sv.time_step,
        n_sv_n=len(sv.position),
        # pyrefly: ignore [bad-argument-type]
        ascending_node_time=str(sv.ascending_node.time) if sv.ascending_node else None,
        # pyrefly: ignore [bad-argument-type]
        ascending_node_coords=array_to_value_array_type(sv.ascending_node.position)
        if sv.ascending_node
        else None,
    )


def antenna_rotation_to_model(
    rot: AntennaRotation,
) -> trajectory_model.ChannelType.AntennaRotationYpr:
    """Convert quaternion-based AntennaRotation to yaw-pitch-roll format."""
    yaw_tx, pitch_tx, roll_tx = quaternion_to_ypr(rot.tx)
    yaw_rx, pitch_rx, roll_rx = quaternion_to_ypr(rot.rx)
    return trajectory_model.ChannelType.AntennaRotationYpr(
        tx=array_to_value_array_type_ypr(np.vstack([yaw_tx, pitch_tx, roll_tx])),
        rx=array_to_value_array_type_ypr(np.vstack([yaw_rx, pitch_rx, roll_rx])),
    )


def apc_to_model(
    apc: AntennaPhaseCentrePositionTowardsBodyMassCenter,
) -> trajectory_model.ChannelType.AntennaPhaseCentrePositionTowardsBodyMassCenter:
    """Convert APC data to corresponding dataclass format."""
    return trajectory_model.ChannelType.AntennaPhaseCentrePositionTowardsBodyMassCenter(
        tx=array_to_value_array_type_apc(apc.tx),
        rx=array_to_value_array_type_apc(apc.rx),
    )


def trajectory_to_gss_model(
    gss_trajectory: Trajectory,
    version_number: str = "2.0",
    description: str = "GSS Trajectory file",
    number: int = 1,
    total: int = 1,
) -> trajectory_model.GsstrajectoryFile:
    """Create a GSS trajectory model from a `Trajectory` object."""
    channel = trajectory_model.ChannelType(
        description=description,
        number=number,
        total=total,
        full_orbit_cycle_length=trajectory_model.ChannelType.FullOrbitCycleLength(
            value=gss_trajectory.orbit_length,
        ),
        attitude_info=attitude_info_to_model(gss_trajectory.attitude_info),
        state_vector_data=state_vector_data_to_model(gss_trajectory.state_vector),
        antenna_rotation_ypr=antenna_rotation_to_model(gss_trajectory.antenna_rotation),  # pyrefly: ignore[bad-argument-type]
        antenna_phase_centre_position_towards_body_mass_center=apc_to_model(
            gss_trajectory.antenna_phase_centre_position_towards_body_mass_center,  # pyrefly: ignore[bad-argument-type]
        ),
    )
    return trajectory_model.GsstrajectoryFile(version_number=version_number, channel=channel)


def trajectory_to_rdb_model(
    rdb_trajectory: Trajectory,
    version_number: str = "2.1",
    channel_number: int = 1,
    total_channels_number: int = 1,
) -> trajectory_model.AresysXmlDoc:
    """Create a RDB trajectory model from a custom `Trajectory` object."""
    channel = trajectory_model.ChannelType(
        description=None,
        number=channel_number,
        total=total_channels_number,
        full_orbit_cycle_length=None,
        attitude_info=attitude_info_to_model(rdb_trajectory.attitude_info),
        state_vector_data=state_vector_data_to_model(rdb_trajectory.state_vector),
        antenna_rotation_ypr=antenna_rotation_to_model(rdb_trajectory.antenna_rotation),  # pyrefly: ignore[bad-argument-type]
        antenna_phase_centre_position_towards_body_mass_center=apc_to_model(
            rdb_trajectory.antenna_phase_centre_position_towards_body_mass_center,  # pyrefly: ignore[bad-argument-type]
        ),
    )

    return trajectory_model.AresysXmlDoc(
        version_number=version_number,
        number_of_channels=total_channels_number,
        description="Trajectory RDB format",
        channel=channel,
    )


def write_trajectory_xml(
    trajectory: Trajectory,
    filename: str | Path,
    traj_format: TrajectoryFormat = "GSS",
) -> None:
    """Serialize the trajectory model to XML and write to file.

    Parameters
    ----------
    trajectory : Trajectory
        Trajectory object to serialize.
    filename : str | Path
        Output XML file path or destination directory path.
    traj_format : TrajectoryFormat
        Format of the XML file: possible values "GSS" or "RDB".

    Raises
    ------
    TypeError
        If the provided trajectory is not a Trajectory object.
    ValueError
        If the provided trajectory format is not supported.
    """
    if not isinstance(trajectory, Trajectory):
        msg = "trajectory  is not a GssTrajectory object"
        raise TypeError(msg)

    if traj_format not in {"GSS", "RDB"}:
        msg = "Unsupported trajectory file format. Use 'GSS' or 'RDB'."
        raise ValueError(msg)

    trajectory_model = (
        trajectory_to_gss_model(trajectory)
        if traj_format == "GSS"
        else trajectory_to_rdb_model(trajectory)
    )

    output_path = Path(filename)
    if output_path.suffix.lower() != ".xml":
        output_path = output_path.joinpath("Trajectory.xml")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(serialize(trajectory_model), encoding="utf-8")


__all__ = ["write_trajectory_xml"]
