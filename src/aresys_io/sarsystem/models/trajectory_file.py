# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Generated module."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class AttitudeInfoTypeAttitudeType(Enum):
    NOMINAL = "NOMINAL"
    REFINED = "REFINED"


class AttitudeInfoTypeReferenceFrame(Enum):
    ZERODOPPLER = "ZERODOPPLER"
    GEODETIC = "GEODETIC"
    GEOCENTRIC = "GEOCENTRIC"


class AttitudeInfoTypeRotationOrder(Enum):
    YPR = "YPR"
    YRP = "YRP"
    PYR = "PYR"
    PRY = "PRY"
    RYP = "RYP"
    RPY = "RPY"


class StateVectorDataTypeOrbitDirection(Enum):
    ASCENDING = "ASCENDING"
    DESCENDING = "DESCENDING"


@dataclass(kw_only=True)
class ValueArrayType:
    val: list[ValueArrayType.Val] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )

    @dataclass(kw_only=True)
    class Val:
        value: float = field()
        n: object = field(
            metadata={
                "name": "N",
                "type": "Attribute",
            }
        )


@dataclass(kw_only=True)
class AttitudeInfoType:
    t_ref_utc: str = field(
        metadata={
            "name": "t_ref_Utc",
            "type": "Element",
        }
    )
    dt_ypr_s: float = field(
        metadata={
            "name": "dtYPR_s",
            "type": "Element",
        }
    )
    n_ypr_n: int = field(
        metadata={
            "name": "nYPR_n",
            "type": "Element",
        }
    )
    yaw_deg: ValueArrayType = field(
        metadata={
            "type": "Element",
        }
    )
    pitch_deg: ValueArrayType = field(
        metadata={
            "type": "Element",
        }
    )
    roll_deg: ValueArrayType = field(
        metadata={
            "type": "Element",
        }
    )
    reference_frame: AttitudeInfoTypeReferenceFrame = field(
        metadata={
            "name": "referenceFrame",
            "type": "Element",
        }
    )
    rotation_order: AttitudeInfoTypeRotationOrder = field(
        metadata={
            "name": "rotationOrder",
            "type": "Element",
        }
    )
    attitude_type: AttitudeInfoTypeAttitudeType = field(
        metadata={
            "name": "AttitudeType",
            "type": "Element",
        }
    )


@dataclass(kw_only=True)
class StateVectorDataType:
    orbit_number: str = field(
        metadata={
            "name": "OrbitNumber",
            "type": "Element",
        }
    )
    track: str = field(
        metadata={
            "name": "Track",
            "type": "Element",
        }
    )
    orbit_direction: StateVectorDataTypeOrbitDirection = field(
        metadata={
            "name": "OrbitDirection",
            "type": "Element",
        }
    )
    p_sv_m: ValueArrayType = field(
        metadata={
            "name": "pSV_m",
            "type": "Element",
        }
    )
    v_sv_m_os: ValueArrayType = field(
        metadata={
            "name": "vSV_mOs",
            "type": "Element",
        }
    )
    t_ref_utc: str = field(
        metadata={
            "name": "t_ref_Utc",
            "type": "Element",
        }
    )
    dt_sv_s: float = field(
        metadata={
            "name": "dtSV_s",
            "type": "Element",
        }
    )
    n_sv_n: int = field(
        metadata={
            "name": "nSV_n",
            "type": "Element",
        }
    )
    ascending_node_time: str = field(
        metadata={
            "name": "AscendingNodeTime",
            "type": "Element",
        }
    )
    ascending_node_coords: ValueArrayType = field(
        metadata={
            "name": "AscendingNodeCoords",
            "type": "Element",
        }
    )


@dataclass(kw_only=True)
class ChannelType:
    description: str | None = field(
        default=None,
        metadata={
            "name": "Description",
            "type": "Element",
        },
    )
    full_orbit_cycle_length: ChannelType.FullOrbitCycleLength | None = field(
        default=None,
        metadata={
            "name": "fullOrbitCycleLength",
            "type": "Element",
        },
    )
    state_vector_data: StateVectorDataType = field(
        metadata={
            "name": "StateVectorData",
            "type": "Element",
        }
    )
    attitude_info: AttitudeInfoType = field(
        metadata={
            "name": "AttitudeInfo",
            "type": "Element",
        }
    )
    antenna_phase_centre_position_towards_body_mass_center: ChannelType.AntennaPhaseCentrePositionTowardsBodyMassCenter = field(
        metadata={
            "name": "AntennaPhaseCentrePositionTowardsBodyMassCenter",
            "type": "Element",
        }
    )
    antenna_rotation_ypr: ChannelType.AntennaRotationYpr = field(
        metadata={
            "name": "AntennaRotationYPR",
            "type": "Element",
        }
    )
    number: object = field(
        metadata={
            "name": "Number",
            "type": "Attribute",
        }
    )
    total: object = field(
        metadata={
            "name": "Total",
            "type": "Attribute",
        }
    )

    @dataclass(kw_only=True)
    class FullOrbitCycleLength:
        value: float = field()
        unit: str = field(
            init=False,
            default="s",
            metadata={
                "type": "Attribute",
                "required": True,
            },
        )

    @dataclass(kw_only=True)
    class AntennaPhaseCentrePositionTowardsBodyMassCenter:
        tx: ValueArrayType = field(
            metadata={
                "name": "TX",
                "type": "Element",
            }
        )
        rx: ValueArrayType = field(
            metadata={
                "name": "RX",
                "type": "Element",
            }
        )
        unit: str = field(
            init=False,
            default="m",
            metadata={
                "type": "Attribute",
                "required": True,
            },
        )

    @dataclass(kw_only=True)
    class AntennaRotationYpr:
        tx: ValueArrayType = field(
            metadata={
                "name": "TX",
                "type": "Element",
            }
        )
        rx: ValueArrayType = field(
            metadata={
                "name": "RX",
                "type": "Element",
            }
        )
        unit: str = field(
            init=False,
            default="deg",
            metadata={
                "type": "Attribute",
                "required": True,
            },
        )


@dataclass(kw_only=True)
class AresysXmlDoc:
    number_of_channels: int = field(
        metadata={
            "name": "NumberOfChannels",
            "type": "Element",
        }
    )
    version_number: str = field(
        metadata={
            "name": "VersionNumber",
            "type": "Element",
        }
    )
    description: str = field(
        metadata={
            "name": "Description",
            "type": "Element",
        }
    )
    channel: ChannelType = field(
        metadata={
            "name": "Channel",
            "type": "Element",
        }
    )


@dataclass(kw_only=True)
class GsstrajectoryFile:
    class Meta:
        name = "GSSTrajectoryFile"

    version_number: str = field(
        metadata={
            "name": "VersionNumber",
            "type": "Element",
        }
    )
    channel: ChannelType = field(
        metadata={
            "name": "Channel",
            "type": "Element",
        }
    )
