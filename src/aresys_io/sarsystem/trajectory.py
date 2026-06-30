# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""trajectory dataclasses."""

from enum import Enum

import numpy as np
from perseo_core.geometry.pointing import ReferenceFrame, RotationOrder
from perseo_core.timing import PreciseDateTime
from pydantic import BaseModel

from aresys_io.sarsystem.models import trajectory_file as model_trajectory
from aresys_io.sarsystem.utils import (
    Quaternion,
    SingleStateVector,
    StateVector,
    value_array_type_to_array,
    ypr_to_quaternion,
)

_ROTATION_ORDER_FROM_MODEL: dict[model_trajectory.AttitudeInfoTypeRotationOrder, RotationOrder] = {
    model_trajectory.AttitudeInfoTypeRotationOrder.YPR: "YPR",
    model_trajectory.AttitudeInfoTypeRotationOrder.YRP: "YRP",
    model_trajectory.AttitudeInfoTypeRotationOrder.PYR: "PYR",
    model_trajectory.AttitudeInfoTypeRotationOrder.PRY: "PRY",
    model_trajectory.AttitudeInfoTypeRotationOrder.RYP: "RYP",
    model_trajectory.AttitudeInfoTypeRotationOrder.RPY: "RPY",
}

_REFERENCE_FRAME_FROM_MODEL: dict[
    model_trajectory.AttitudeInfoTypeReferenceFrame, ReferenceFrame
] = {
    model_trajectory.AttitudeInfoTypeReferenceFrame.ZERODOPPLER: "ZERODOPPLER",
    model_trajectory.AttitudeInfoTypeReferenceFrame.GEODETIC: "GEODETIC",
    model_trajectory.AttitudeInfoTypeReferenceFrame.GEOCENTRIC: "GEOCENTRIC",
}


class AttitudeType(Enum):
    """
    Enumeration for attitude type.

    Attributes
    ----------
    NOMINAL : str
        Nominal attitude.
    REFINED : str
        Refined attitude.
    """

    NOMINAL = "NOMINAL"
    REFINED = "REFINED"


class OrbitDirection(Enum):
    """
    Enumeration for orbit direction.

    Attributes
    ----------
    ASCENDING : str
        Ascending orbit direction.
    DESCENDING : str
        Descending orbit direction.
    """

    ASCENDING = "ASCENDING"
    DESCENDING = "DESCENDING"


class AttitudeInfo(BaseModel):
    """
    Attitude information for the trajectory.

    Attributes
    ----------
    time_origin : PreciseDateTime
        Reference time for the attitude data.
    time_step : float
        Time step between attitude samples.
    rotation : NDArray
        Rotation represented as quaternion, the last component is the scalar.
    reference_frame : ReferenceFrame
        Reference frame for the attitude.
    attitude_type : AttitudeType
        Type of attitude (nominal or refined).
    """

    time_origin: PreciseDateTime
    time_step: float
    """Rotation represented as quaternion, the last component of quaternion is the scalar one."""
    rotation: Quaternion
    reference_frame: ReferenceFrame
    attitude_type: AttitudeType
    model_config = {"arbitrary_types_allowed": True}

    @staticmethod
    def from_model(model: model_trajectory.AttitudeInfoType) -> "AttitudeInfo":
        """Create an AttitudeInfo object from a model AttitudeInfoType."""
        yaw_deg_vec = value_array_type_to_array(model.yaw_deg)
        pitch_deg_vec = value_array_type_to_array(model.pitch_deg)
        roll_deg_vec = value_array_type_to_array(model.roll_deg)
        rotation_order = _ROTATION_ORDER_FROM_MODEL[model.rotation_order]
        rotation = ypr_to_quaternion(yaw_deg_vec, pitch_deg_vec, roll_deg_vec, rotation_order)
        return AttitudeInfo(
            time_origin=PreciseDateTime.from_utc_string(model.t_ref_utc),
            time_step=model.dt_ypr_s,
            rotation=rotation,
            reference_frame=_REFERENCE_FRAME_FROM_MODEL[model.reference_frame],
            attitude_type=AttitudeType(model.attitude_type.value),
        )

    def __eq__(self, other: object) -> bool:
        """Equality comparison for AttitudeInfo objects."""
        if not isinstance(other, AttitudeInfo):
            return NotImplemented
        return (
            self.time_origin == other.time_origin
            and self.time_step == other.time_step
            and np.array_equal(self.rotation, other.rotation)
            and self.reference_frame == other.reference_frame
            and self.attitude_type == other.attitude_type
        )


class AscendingNode(BaseModel):
    """
    Ascending node information.

    Attributes
    ----------
    time : PreciseDateTime
        Time of the ascending node crossing.
    position : NDArray
        Position vector at the ascending node (shape: [3]).
    """

    time: PreciseDateTime
    position: SingleStateVector
    model_config = {"arbitrary_types_allowed": True}

    def __eq__(self, other: object) -> bool:
        """Equality comparison for AscendingNode objects."""
        if not isinstance(other, AscendingNode):
            return NotImplemented
        return self.time == other.time and np.array_equal(self.position, other.position)


class StateVectorData(BaseModel):
    """
    State vector data for the trajectory.

    Attributes
    ----------
    orbit_number : str
        Orbit number.
    track : str
        Track identifier.
    time_origin : PreciseDateTime
        Reference time for the state vector.
    time_step : float
        Time step between state vector samples.
    position : NDArray
        Position vectors (shape: [N, 3]).
    velocity : NDArray
        Velocity vectors (shape: [N, 3]).
    orbit_direction : OrbitDirection
        Orbit direction (ascending or descending).
    ascending_node : AscendingNode | None
        Ascending node information.
    """

    orbit_number: str
    track: str
    time_origin: PreciseDateTime
    time_step: float
    position: StateVector
    velocity: StateVector
    orbit_direction: OrbitDirection
    ascending_node: AscendingNode | None = None

    model_config = {"arbitrary_types_allowed": True}

    @staticmethod
    def from_model(model: model_trajectory.StateVectorDataType) -> "StateVectorData":
        """Create a StateVectorData object from a model StateVectorDataType."""
        time_origin = PreciseDateTime.from_utc_string(model.t_ref_utc)
        # Position vector length check
        position = value_array_type_to_array(model.p_sv_m)
        if len(position) % 3 != 0:
            msg = "The position vector length is not divisible by 3."
            raise ValueError(msg)

        # Velocity vector length check
        velocity = value_array_type_to_array(model.v_sv_m_os)
        if len(velocity) % 3 != 0:
            msg = "The position vector length is not divisible by 3."
            raise ValueError(msg)

        # ascending node
        # Check that both fields are either None or both set
        if (model.ascending_node_time is None) != (model.ascending_node_coords is None):
            msg = (
                "Ascending_node_time and ascending_node_coords "
                "must be either both None or both set."
            )
            raise ValueError(msg)

        ascending_node = (
            None
            if model.ascending_node_time is None
            else AscendingNode(
                time=PreciseDateTime.from_utc_string(model.ascending_node_time),
                position=value_array_type_to_array(model.ascending_node_coords),
            )
        )

        return StateVectorData(
            orbit_number=model.orbit_number,
            track=model.track,
            time_origin=time_origin,
            time_step=model.dt_sv_s,
            position=position.reshape(-1, 3),
            velocity=velocity.reshape(-1, 3),
            orbit_direction=OrbitDirection(model.orbit_direction.value),
            ascending_node=ascending_node,
        )

    def __eq__(self, other: object) -> bool:
        """Equality comparison for StateVectorData objects."""
        if not isinstance(other, StateVectorData):
            return NotImplemented

        return (
            self.orbit_number == other.orbit_number
            and self.track == other.track
            and self.time_origin == other.time_origin
            and self.time_step == other.time_step
            and np.array_equal(self.position, other.position)
            and np.array_equal(self.velocity, other.velocity)
            and self.orbit_direction == other.orbit_direction
            and self.ascending_node == other.ascending_node
        )


class AntennaRotation(BaseModel):
    """
    Antenna rotation information for TX and RX channels.

    Attributes
    ----------
    tx : NDArray
        Transmit antenna rotation as quaternions (shape: [N, 4]).
    rx : NDArray
        Receive antenna rotation as quaternions (shape: [N, 4]).
    """

    tx: Quaternion
    rx: Quaternion
    model_config = {"arbitrary_types_allowed": True}

    @staticmethod
    def from_model(
        model: model_trajectory.ChannelType.AntennaRotationYpr,
    ) -> "AntennaRotation":
        """Create an AntennaRotation object from a model AntennaRotationYpr."""
        # tx
        tx = value_array_type_to_array(model.tx)
        if len(tx) % 3 != 0:
            msg = "The antenna_rotation_tx length is not divisible by 3."
            raise ValueError(msg)
        tx = tx.reshape([3, -1])  # (3,N)
        tx_quat = ypr_to_quaternion(tx[0, :], tx[1, :], tx[2, :])
        # rx
        rx = value_array_type_to_array(model.rx)
        if len(rx) % 3 != 0:
            msg = "The antenna_rotation_rx length is not divisible by 3."
            raise ValueError(msg)
        rx = tx.reshape([3, -1])  # (3,N)
        rx_quat = ypr_to_quaternion(rx[0, :], rx[1, :], rx[2, :])
        return AntennaRotation(
            tx=tx_quat,
            rx=rx_quat,
        )

    def __eq__(self, other: object) -> bool:
        """Equality comparison for AntennaRotation objects."""
        if not isinstance(other, AntennaRotation):
            return NotImplemented
        return np.array_equal(self.tx, other.tx) and np.array_equal(self.tx, other.rx)


class AntennaPhaseCentrePositionTowardsBodyMassCenter(BaseModel):
    """
    Antenna phase centre positions towards the body mass center.

    Attributes
    ----------
    tx : NDArray
        Transmit antenna phase centre positions (shape: [N, 3]).
    rx : NDArray
        Receive antenna phase centre positions (shape: [N, 3]).
    """

    tx: StateVector
    rx: StateVector

    model_config = {"arbitrary_types_allowed": True}

    def __eq__(self, other: object) -> bool:
        """Equality comparison for AntennaPhaseCentrePositionTowardsBodyMassCenter objects."""
        if not isinstance(other, AntennaPhaseCentrePositionTowardsBodyMassCenter):
            return NotImplemented
        return np.array_equal(self.tx, other.tx) and np.array_equal(self.rx, other.rx)


class Trajectory(BaseModel):
    """
    Complete GSS trajectory data structure.

    Attributes
    ----------
    attitude_info : AttitudeInfo
        Attitude information.
    state_vector : StateVectorData
        State vector data.
    orbit_length : float
        Full orbit cycle length.
    antenna_rotation : AntennaRotation
        Antenna rotation information.
    antenna_phase_centre_position_towards_body_mass_center : AntennaPhaseCentrePositionTowardsBodyMassCenter
        Antenna phase centre positions towards the body mass center.
    """  # noqa: E501

    attitude_info: AttitudeInfo
    state_vector: StateVectorData
    orbit_length: float
    antenna_rotation: AntennaRotation | None
    antenna_phase_centre_position_towards_body_mass_center: (
        AntennaPhaseCentrePositionTowardsBodyMassCenter | None
    )
    model_config = {"arbitrary_types_allowed": True}


__all__ = [
    "AntennaPhaseCentrePositionTowardsBodyMassCenter",
    "AntennaRotation",
    "AscendingNode",
    "AttitudeInfo",
    "AttitudeType",
    "OrbitDirection",
    "StateVectorData",
    "Trajectory",
]
