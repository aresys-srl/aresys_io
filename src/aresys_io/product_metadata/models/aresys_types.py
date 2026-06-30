# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Generated module."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

__NAMESPACE__ = "aresysTypes"


class AcquisitionModeType(Enum):
    NOT_SET = "NOT SET"
    STRIPMAP = "STRIPMAP"
    DOUBLE_POL = "DOUBLE POL"
    QUAD_POL = "QUAD POL"
    SCANSAR = "SCANSAR"
    TOPSAR = "TOPSAR"
    SPOT = "SPOT"
    WAVE = "WAVE"
    GMTI = "GMTI"


class AscendingDescendingType(Enum):
    ASCENDING = "ASCENDING"
    DESCENDING = "DESCENDING"
    NOT_AVAILABLE = "NOT_AVAILABLE"


class AttitudeType(Enum):
    NOMINAL = "NOMINAL"
    REFINED = "REFINED"


class CellTypeVerboseType(Enum):
    FLOAT_COMPLEX = "FLOAT_COMPLEX"
    FLOAT32 = "FLOAT32"
    DOUBLE_COMPLEX = "DOUBLE_COMPLEX"
    FLOAT64 = "FLOAT64"
    INT16 = "INT16"
    SHORT_COMPLEX = "SHORT_COMPLEX"
    INT32 = "INT32"
    INT_COMPLEX = "INT_COMPLEX"
    INT8 = "INT8"
    INT8_COMPLEX = "INT8_COMPLEX"
    CUSTOM = "CUSTOM"


@dataclass(kw_only=True)
class Dcomplex:
    class Meta:
        name = "DCOMPLEX"

    real_value: float = field(
        metadata={
            "name": "RealValue",
            "type": "Element",
            "namespace": "",
        }
    )
    imaginary_value: float = field(
        metadata={
            "name": "ImaginaryValue",
            "type": "Element",
            "namespace": "",
        }
    )


class Endianity(Enum):
    BIGENDIAN = "BIGENDIAN"
    LITTLEENDIAN = "LITTLEENDIAN"


class GlobalPolarizationType(Enum):
    SINGLE_POL = "SINGLE POL"
    DUAL_POL = "DUAL POL"


class ImageQuantityType(Enum):
    BETA = "BETA"
    GAMMA = "GAMMA"
    SIGMA = "SIGMA"


class LeftRightType(Enum):
    LEFT = "LEFT"
    RIGHT = "RIGHT"


class PolarizationType(Enum):
    H_H = "H/H"
    H_V = "H/V"
    V_H = "V/H"
    V_V = "V/V"
    X_X = "X/X"


class PulseTypeDirection(Enum):
    UP = "UP"
    DOWN = "DOWN"


class RasterFormatType(Enum):
    ARESYS_RASTER = "ARESYS_RASTER"
    ARESYS_GEOTIFF = "ARESYS_GEOTIFF"
    RASTER = "RASTER"


class ReferenceFrameType(Enum):
    GEOCENTRIC = "GEOCENTRIC"
    GEODETIC = "GEODETIC"
    ZERODOPPLER = "ZERODOPPLER"


class RotationOrderType(Enum):
    YPR = "YPR"
    YRP = "YRP"
    PRY = "PRY"
    PYR = "PYR"
    RPY = "RPY"
    RYP = "RYP"


class SensorNamesType(Enum):
    NOT_SET = "NOT SET"
    ASAR = "ASAR"
    PALSAR = "PALSAR"
    ERS1 = "ERS1"
    ERS2 = "ERS2"
    RADARSAT = "RADARSAT"
    TERRASARX = "TERRASARX"
    SENTINEL1 = "SENTINEL1"
    SENTINEL1_A = "SENTINEL1A"
    SENTINEL1_B = "SENTINEL1B"
    SENTINEL1_C = "SENTINEL1C"
    SENTINEL1_D = "SENTINEL1D"
    SAOCOM = "SAOCOM"
    SAOCOM_1_A = "SAOCOM-1A"
    SAOCOM_1_B = "SAOCOM-1B"
    UAVSAR = "UAVSAR"


@dataclass(kw_only=True)
class TreeElementBaseType:
    number: int | None = field(
        default=None,
        metadata={
            "name": "Number",
            "type": "Attribute",
        },
    )
    total: int | None = field(
        default=None,
        metadata={
            "name": "Total",
            "type": "Attribute",
        },
    )


class Units(Enum):
    VALUE = ""
    M = "m"
    S = "s"
    J = "j"
    D_B = "dB"
    RAD = "rad"
    DEG = "deg"
    M_S = "m/s"
    M_S2 = "m/s2"
    M_S3 = "m/s3"
    M_S4 = "m/s4"
    M_S5 = "m/s5"
    M_S6 = "m/s6"
    M_S7 = "m/s7"
    M_S8 = "m/s8"
    M_S9 = "m/s9"
    S_S = "s/s"
    S_S2 = "s/s2"
    S_S3 = "s/s3"
    S_S4 = "s/s4"
    S_S5 = "s/s5"
    HZ = "Hz"
    HZ_S = "Hz/s"
    HZ_S2 = "Hz/s2"
    HZ_S3 = "Hz/s3"
    HZ_S4 = "Hz/s4"
    HZ_S5 = "Hz/s5"
    HZ_S6 = "Hz/s6"
    HZ_S7 = "Hz/s7"
    HZ_S8 = "Hz/s8"
    HZ_S9 = "Hz/s9"
    RAD_S = "rad/s"
    RAD_S2 = "rad/s2"
    RAD_S3 = "rad/s3"
    RAD_S4 = "rad/s4"
    RAD_S5 = "rad/s5"
    RAD_S6 = "rad/s6"
    RAD_S7 = "rad/s7"
    RAD_S8 = "rad/s8"
    RAD_S9 = "rad/s9"
    S85 = "s85"
    UTC = "Utc"
    B = "b"
    K = "K"
    S_M = "s/m"
    S_M2 = "s/m2"
    S_M3 = "s/m3"
    S_M4 = "s/m4"
    S_M5 = "s/m5"
    S_M6 = "s/m6"
    S_M7 = "s/m7"
    S_M8 = "s/m8"
    S_M9 = "s/m9"
    DEG_S = "deg/s"
    DEG_S2 = "deg/s2"
    DEG_S3 = "deg/s3"
    DEG_S4 = "deg/s4"
    DEG_S5 = "deg/s5"
    DEG_S6 = "deg/s6"
    DEG_S7 = "deg/s7"
    DEG_S8 = "deg/s8"
    DEG_S9 = "deg/s9"


@dataclass(kw_only=True)
class AcquisitionTimelineType(TreeElementBaseType):
    """
    Acquisition timeline definition.

    Parameters
    ----------
    missing_lines_number
        Number of missing lines
    missing_lines_azimuthtimes
        Azimuth relative times for each missing line
    duplicated_lines_number
        Number of duplicated lines
    duplicated_lines_azimuthtimes
        Azimuth relative times for each duplicated line
    prf_changes_number
        Number of PRF changes
    prf_changes_azimuthtimes
        Azimuth relative times for each PRF change
    prf_changes_values
        PRF changes values
    swst_changes_number
        Number of SWST changes
    swst_changes_azimuthtimes
        Azimuth relative times for each SWST change
    swst_changes_values
        SWST changes values
    noise_packets_number
        Number of noise packets
    noise_packets_azimuthtimes
        Azimuth relative times for each noise packet
    internal_calibration_number
        Number of internal calibration packets
    internal_calibration_azimuthtimes
        Azimuth relative times for each internal calibration packet
    swl_changes_number
        Number of SWL changes
    swl_changes_azimuthtimes
        Relative azimuth times for each SWL change
    swl_changes_values
        SWL changes values
    chirp_period
        Periodic list of chirp indexes related to multi-chirp image acquisition
    """

    missing_lines_number: int = field(
        metadata={
            "name": "MissingLines_number",
            "type": "Element",
            "namespace": "",
        }
    )
    missing_lines_azimuthtimes: AcquisitionTimelineType.MissingLinesAzimuthtimes = field(
        metadata={
            "name": "MissingLines_azimuthtimes",
            "type": "Element",
            "namespace": "",
        }
    )
    duplicated_lines_number: int | None = field(
        default=None,
        metadata={
            "name": "DuplicatedLines_number",
            "type": "Element",
            "namespace": "",
        },
    )
    duplicated_lines_azimuthtimes: AcquisitionTimelineType.DuplicatedLinesAzimuthtimes | None = (
        field(
            default=None,
            metadata={
                "name": "DuplicatedLines_azimuthtimes",
                "type": "Element",
                "namespace": "",
            },
        )
    )
    prf_changes_number: int | None = field(
        default=None,
        metadata={
            "name": "PRF_changes_number",
            "type": "Element",
            "namespace": "",
        },
    )
    prf_changes_azimuthtimes: AcquisitionTimelineType.PrfChangesAzimuthtimes | None = field(
        default=None,
        metadata={
            "name": "PRF_changes_azimuthtimes",
            "type": "Element",
            "namespace": "",
        },
    )
    prf_changes_values: AcquisitionTimelineType.PrfChangesValues | None = field(
        default=None,
        metadata={
            "name": "PRF_changes_values",
            "type": "Element",
            "namespace": "",
        },
    )
    swst_changes_number: int = field(
        metadata={
            "name": "Swst_changes_number",
            "type": "Element",
            "namespace": "",
        }
    )
    swst_changes_azimuthtimes: AcquisitionTimelineType.SwstChangesAzimuthtimes = field(
        metadata={
            "name": "Swst_changes_azimuthtimes",
            "type": "Element",
            "namespace": "",
        }
    )
    swst_changes_values: AcquisitionTimelineType.SwstChangesValues = field(
        metadata={
            "name": "Swst_changes_values",
            "type": "Element",
            "namespace": "",
        }
    )
    noise_packets_number: int = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    noise_packets_azimuthtimes: AcquisitionTimelineType.NoisePacketsAzimuthtimes = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    internal_calibration_number: int = field(
        metadata={
            "name": "Internal_calibration_number",
            "type": "Element",
            "namespace": "",
        }
    )
    internal_calibration_azimuthtimes: AcquisitionTimelineType.InternalCalibrationAzimuthtimes = (
        field(
            metadata={
                "name": "Internal_calibration_azimuthtimes",
                "type": "Element",
                "namespace": "",
            }
        )
    )
    swl_changes_number: int | None = field(
        default=None,
        metadata={
            "name": "Swl_changes_number",
            "type": "Element",
            "namespace": "",
        },
    )
    swl_changes_azimuthtimes: AcquisitionTimelineType.SwlChangesAzimuthtimes | None = field(
        default=None,
        metadata={
            "name": "Swl_changes_azimuthtimes",
            "type": "Element",
            "namespace": "",
        },
    )
    swl_changes_values: AcquisitionTimelineType.SwlChangesValues | None = field(
        default=None,
        metadata={
            "name": "Swl_changes_values",
            "type": "Element",
            "namespace": "",
        },
    )
    chirp_period: str | None = field(
        default=None,
        metadata={
            "name": "ChirpPeriod",
            "type": "Element",
            "namespace": "",
        },
    )

    @dataclass(kw_only=True)
    class MissingLinesAzimuthtimes:
        val: list[AcquisitionTimelineType.MissingLinesAzimuthtimes.Val] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

        @dataclass(kw_only=True)
        class Val:
            value: float = field()
            unit: Units | None = field(
                default=None,
                metadata={
                    "type": "Attribute",
                },
            )
            n: int | None = field(
                default=None,
                metadata={
                    "name": "N",
                    "type": "Attribute",
                },
            )

    @dataclass(kw_only=True)
    class DuplicatedLinesAzimuthtimes:
        val: list[AcquisitionTimelineType.DuplicatedLinesAzimuthtimes.Val] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

        @dataclass(kw_only=True)
        class Val:
            value: float = field()
            unit: Units | None = field(
                default=None,
                metadata={
                    "type": "Attribute",
                },
            )
            n: int | None = field(
                default=None,
                metadata={
                    "name": "N",
                    "type": "Attribute",
                },
            )

    @dataclass(kw_only=True)
    class PrfChangesAzimuthtimes:
        val: list[AcquisitionTimelineType.PrfChangesAzimuthtimes.Val] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

        @dataclass(kw_only=True)
        class Val:
            value: float = field()
            unit: Units | None = field(
                default=None,
                metadata={
                    "type": "Attribute",
                },
            )
            n: int | None = field(
                default=None,
                metadata={
                    "name": "N",
                    "type": "Attribute",
                },
            )

    @dataclass(kw_only=True)
    class PrfChangesValues:
        val: list[AcquisitionTimelineType.PrfChangesValues.Val] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

        @dataclass(kw_only=True)
        class Val:
            value: float = field()
            unit: Units | None = field(
                default=None,
                metadata={
                    "type": "Attribute",
                },
            )
            n: int | None = field(
                default=None,
                metadata={
                    "name": "N",
                    "type": "Attribute",
                },
            )

    @dataclass(kw_only=True)
    class SwstChangesAzimuthtimes:
        val: list[AcquisitionTimelineType.SwstChangesAzimuthtimes.Val] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

        @dataclass(kw_only=True)
        class Val:
            value: float = field()
            unit: Units | None = field(
                default=None,
                metadata={
                    "type": "Attribute",
                },
            )
            n: int | None = field(
                default=None,
                metadata={
                    "name": "N",
                    "type": "Attribute",
                },
            )

    @dataclass(kw_only=True)
    class SwstChangesValues:
        val: list[AcquisitionTimelineType.SwstChangesValues.Val] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

        @dataclass(kw_only=True)
        class Val:
            value: float = field()
            unit: Units | None = field(
                default=None,
                metadata={
                    "type": "Attribute",
                },
            )
            n: int | None = field(
                default=None,
                metadata={
                    "name": "N",
                    "type": "Attribute",
                },
            )

    @dataclass(kw_only=True)
    class NoisePacketsAzimuthtimes:
        val: list[AcquisitionTimelineType.NoisePacketsAzimuthtimes.Val] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

        @dataclass(kw_only=True)
        class Val:
            value: float = field()
            n: int | None = field(
                default=None,
                metadata={
                    "name": "N",
                    "type": "Attribute",
                },
            )
            unit: Units | None = field(
                default=None,
                metadata={
                    "type": "Attribute",
                },
            )

    @dataclass(kw_only=True)
    class InternalCalibrationAzimuthtimes:
        val: list[AcquisitionTimelineType.InternalCalibrationAzimuthtimes.Val] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

        @dataclass(kw_only=True)
        class Val:
            value: float = field()
            n: int | None = field(
                default=None,
                metadata={
                    "name": "N",
                    "type": "Attribute",
                },
            )
            unit: Units | None = field(
                default=None,
                metadata={
                    "type": "Attribute",
                },
            )

    @dataclass(kw_only=True)
    class SwlChangesAzimuthtimes:
        val: list[AcquisitionTimelineType.SwlChangesAzimuthtimes.Val] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

        @dataclass(kw_only=True)
        class Val:
            value: float = field()
            unit: Units | None = field(
                default=None,
                metadata={
                    "type": "Attribute",
                },
            )
            n: int | None = field(
                default=None,
                metadata={
                    "name": "N",
                    "type": "Attribute",
                },
            )

    @dataclass(kw_only=True)
    class SwlChangesValues:
        val: list[AcquisitionTimelineType.SwlChangesValues.Val] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

        @dataclass(kw_only=True)
        class Val:
            value: float = field()
            unit: Units | None = field(
                default=None,
                metadata={
                    "type": "Attribute",
                },
            )
            n: int | None = field(
                default=None,
                metadata={
                    "name": "N",
                    "type": "Attribute",
                },
            )


@dataclass(kw_only=True)
class AntennaInfoType(TreeElementBaseType):
    """
    Antenna pattern information.

    Parameters
    ----------
    sensor_name
        Sensor name: ASAR, PALSAR, ...
    acquisition_mode
        Acquisition mode: STRIPMAP, TOPSAR, ...
    beam_name
        Acquisition beam name
    polarization
        Antenna polarization (H/H, H/V...)
    lines_per_pattern
        Contains number of lines for each pattern
    """

    sensor_name: SensorNamesType = field(
        metadata={
            "name": "SensorName",
            "type": "Element",
            "namespace": "",
        }
    )
    acquisition_mode: AcquisitionModeType = field(
        metadata={
            "name": "AcquisitionMode",
            "type": "Element",
            "namespace": "",
        }
    )
    beam_name: str = field(
        metadata={
            "name": "BeamName",
            "type": "Element",
            "namespace": "",
        }
    )
    polarization: PolarizationType = field(
        metadata={
            "name": "Polarization",
            "type": "Element",
            "namespace": "",
        }
    )
    lines_per_pattern: int | None = field(
        default=None,
        metadata={
            "name": "LinesPerPattern",
            "type": "Element",
            "namespace": "",
        },
    )


@dataclass(kw_only=True)
class AttitudeInfoType(TreeElementBaseType):
    """
    Sensor attitude information.

    Parameters
    ----------
    t_ref_utc
        Azimuth absolute start time for the first attitude value [Utc]
    dt_ypr_s
        Azimuth time interval between two consecutive attitude values [s]
    n_ypr_n
        Number of attitude values
    yaw_deg
        Yaw angle values [deg]
    pitch_deg
        Pitch angle values [deg]
    roll_deg
        Roll angle values [deg]
    reference_frame
        Reference frame: GEOCENTRIC, GEODETIC, ZERODOPPLER
    rotation_order
        Rotation order: YPR, YRP, PRY, PYR, RPY, RYP
    attitude_type
        Attitude type: NOMINAL, REFINED
    """

    t_ref_utc: str = field(
        metadata={
            "name": "t_ref_Utc",
            "type": "Element",
            "namespace": "",
        }
    )
    dt_ypr_s: AttitudeInfoType.DtYprS = field(
        metadata={
            "name": "dtYPR_s",
            "type": "Element",
            "namespace": "",
        }
    )
    n_ypr_n: AttitudeInfoType.NYprN = field(
        metadata={
            "name": "nYPR_n",
            "type": "Element",
            "namespace": "",
        }
    )
    yaw_deg: AttitudeInfoType.YawDeg = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    pitch_deg: AttitudeInfoType.PitchDeg = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    roll_deg: AttitudeInfoType.RollDeg = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    reference_frame: ReferenceFrameType = field(
        metadata={
            "name": "referenceFrame",
            "type": "Element",
            "namespace": "",
        }
    )
    rotation_order: RotationOrderType = field(
        metadata={
            "name": "rotationOrder",
            "type": "Element",
            "namespace": "",
        }
    )
    attitude_type: AttitudeType = field(
        metadata={
            "name": "AttitudeType",
            "type": "Element",
            "namespace": "",
        }
    )

    @dataclass(kw_only=True)
    class DtYprS:
        value: float = field()
        unit: Units | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass(kw_only=True)
    class NYprN:
        value: int = field()
        unit: Units | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass(kw_only=True)
    class YawDeg:
        val: list[AttitudeInfoType.YawDeg.Val] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

        @dataclass(kw_only=True)
        class Val:
            value: float = field()
            n: int | None = field(
                default=None,
                metadata={
                    "name": "N",
                    "type": "Attribute",
                },
            )
            unit: Units | None = field(
                default=None,
                metadata={
                    "type": "Attribute",
                },
            )

    @dataclass(kw_only=True)
    class PitchDeg:
        val: list[AttitudeInfoType.PitchDeg.Val] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

        @dataclass(kw_only=True)
        class Val:
            value: float = field()
            n: int | None = field(
                default=None,
                metadata={
                    "name": "N",
                    "type": "Attribute",
                },
            )
            unit: Units | None = field(
                default=None,
                metadata={
                    "type": "Attribute",
                },
            )

    @dataclass(kw_only=True)
    class RollDeg:
        val: list[AttitudeInfoType.RollDeg.Val] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

        @dataclass(kw_only=True)
        class Val:
            value: float = field()
            n: int | None = field(
                default=None,
                metadata={
                    "name": "N",
                    "type": "Attribute",
                },
            )
            unit: Units | None = field(
                default=None,
                metadata={
                    "type": "Attribute",
                },
            )


@dataclass(kw_only=True)
class DataBlockStatisticsType(TreeElementBaseType):
    """
    Statistics computed from data.

    Parameters
    ----------
    num_samples
        Number of samples analyzed
    max_i
        Max of I (real) samples
    min_i
        Min of I (real) samples
    max_q
        Max of Q (imaginary) samples
    min_q
        Min of Q (imaginary) samples
    sum_i
        Sum of I (real) samples
    sum_q
        Sum of Q (imaginary) samples
    sum2_i
        Square Sum of I (real) samples
    sum2_q
        Square Sum of Q (imaginary) samples
    line_start
    line_stop
    """

    num_samples: DataBlockStatisticsType.NumSamples = field(
        metadata={
            "name": "NumSamples",
            "type": "Element",
            "namespace": "",
        }
    )
    max_i: DataBlockStatisticsType.MaxI = field(
        metadata={
            "name": "MaxI",
            "type": "Element",
            "namespace": "",
        }
    )
    min_i: DataBlockStatisticsType.MinI = field(
        metadata={
            "name": "MinI",
            "type": "Element",
            "namespace": "",
        }
    )
    max_q: DataBlockStatisticsType.MaxQ = field(
        metadata={
            "name": "MaxQ",
            "type": "Element",
            "namespace": "",
        }
    )
    min_q: DataBlockStatisticsType.MinQ = field(
        metadata={
            "name": "MinQ",
            "type": "Element",
            "namespace": "",
        }
    )
    sum_i: DataBlockStatisticsType.SumI = field(
        metadata={
            "name": "SumI",
            "type": "Element",
            "namespace": "",
        }
    )
    sum_q: DataBlockStatisticsType.SumQ = field(
        metadata={
            "name": "SumQ",
            "type": "Element",
            "namespace": "",
        }
    )
    sum2_i: DataBlockStatisticsType.Sum2I = field(
        metadata={
            "name": "Sum2I",
            "type": "Element",
            "namespace": "",
        }
    )
    sum2_q: DataBlockStatisticsType.Sum2Q = field(
        metadata={
            "name": "Sum2Q",
            "type": "Element",
            "namespace": "",
        }
    )
    line_start: int = field(
        metadata={
            "name": "lineStart",
            "type": "Attribute",
        }
    )
    line_stop: int = field(
        metadata={
            "name": "lineStop",
            "type": "Attribute",
        }
    )

    @dataclass(kw_only=True)
    class NumSamples:
        value: int = field()
        unit: Units | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass(kw_only=True)
    class MaxI:
        value: float = field()
        unit: Units | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass(kw_only=True)
    class MinI:
        value: float = field()
        unit: Units | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass(kw_only=True)
    class MaxQ:
        value: float = field()
        unit: Units | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass(kw_only=True)
    class MinQ:
        value: float = field()
        unit: Units | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass(kw_only=True)
    class SumI:
        value: float = field()
        unit: Units | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass(kw_only=True)
    class SumQ:
        value: float = field()
        unit: Units | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass(kw_only=True)
    class Sum2I:
        value: float = field()
        unit: Units | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass(kw_only=True)
    class Sum2Q:
        value: float = field()
        unit: Units | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )


@dataclass(kw_only=True)
class DataSetInfoType(TreeElementBaseType):
    """
    Information regarding the dataset.

    Parameters
    ----------
    sensor_name
        Name of the sensor used to acquire the image: ASAR, PALSAR, ...
    description
        Description of the image
    sense_date
        Image acquisition date
    acquisition_mode
        Image acquisition mode: STRIPMAP, TOPSAR, ...
    image_type
        Image type: RAW DATA, RANGE FOCUSED, AZIMUTH FOCUSED
    projection
        Image projection: SLANT RANGE, GROUND RANGE
    projection_parameters
    image_quantity
    acquisition_station
        Image acquisition station
    processing_center
        Image processing center
    processing_date
        Image processing date
    processing_software
        Image processing software
    fc_hz
        Radar carrier frequency [Hz]
    side_looking
        Radar side looking: LEFT, RIGHT
    external_calibration_factor
        External calibration factor
    data_take_id
    instrument_conf_id
    """

    sensor_name: str = field(
        metadata={
            "name": "SensorName",
            "type": "Element",
            "namespace": "",
        }
    )
    description: DataSetInfoType.Description = field(
        metadata={
            "name": "Description",
            "type": "Element",
            "namespace": "",
        }
    )
    sense_date: DataSetInfoType.SenseDate = field(
        metadata={
            "name": "SenseDate",
            "type": "Element",
            "namespace": "",
        }
    )
    acquisition_mode: DataSetInfoType.AcquisitionMode = field(
        metadata={
            "name": "AcquisitionMode",
            "type": "Element",
            "namespace": "",
        }
    )
    image_type: DataSetInfoType.ImageType = field(
        metadata={
            "name": "ImageType",
            "type": "Element",
            "namespace": "",
        }
    )
    projection: DataSetInfoType.Projection = field(
        metadata={
            "name": "Projection",
            "type": "Element",
            "namespace": "",
        }
    )
    projection_parameters: DataSetInfoType.ProjectionParameters | None = field(
        default=None,
        metadata={
            "name": "ProjectionParameters",
            "type": "Element",
            "namespace": "",
        },
    )
    image_quantity: ImageQuantityType | None = field(
        default=None,
        metadata={
            "name": "ImageQuantity",
            "type": "Element",
            "namespace": "",
        },
    )
    acquisition_station: DataSetInfoType.AcquisitionStation = field(
        metadata={
            "name": "AcquisitionStation",
            "type": "Element",
            "namespace": "",
        }
    )
    processing_center: DataSetInfoType.ProcessingCenter = field(
        metadata={
            "name": "ProcessingCenter",
            "type": "Element",
            "namespace": "",
        }
    )
    processing_date: DataSetInfoType.ProcessingDate = field(
        metadata={
            "name": "ProcessingDate",
            "type": "Element",
            "namespace": "",
        }
    )
    processing_software: DataSetInfoType.ProcessingSoftware = field(
        metadata={
            "name": "ProcessingSoftware",
            "type": "Element",
            "namespace": "",
        }
    )
    fc_hz: DataSetInfoType.FcHz = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    side_looking: LeftRightType = field(
        metadata={
            "name": "SideLooking",
            "type": "Element",
            "namespace": "",
        }
    )
    external_calibration_factor: float | None = field(
        default=None,
        metadata={
            "name": "ExternalCalibrationFactor",
            "type": "Element",
            "namespace": "",
        },
    )
    data_take_id: int | None = field(
        default=None,
        metadata={
            "name": "DataTakeID",
            "type": "Element",
            "namespace": "",
        },
    )
    instrument_conf_id: int | None = field(
        default=None,
        metadata={
            "name": "InstrumentConfID",
            "type": "Element",
            "namespace": "",
            "min_inclusive": 0,
            "max_inclusive": 99999999,
        },
    )

    @dataclass(kw_only=True)
    class Description:
        value: str = field(default="")
        unit: Units | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass(kw_only=True)
    class SenseDate:
        value: str = field(default="")
        unit: Units | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass(kw_only=True)
    class AcquisitionMode:
        value: str = field(default="")
        polarization: GlobalPolarizationType | None = field(
            default=None,
            metadata={
                "name": "Polarization",
                "type": "Attribute",
            },
        )

    @dataclass(kw_only=True)
    class ImageType:
        value: str = field(default="")
        unit: Units | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass(kw_only=True)
    class Projection:
        value: str = field(default="")
        unit: Units | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass(kw_only=True)
    class ProjectionParameters:
        value: str = field(default="")
        format: str = field(
            metadata={
                "name": "Format",
                "type": "Attribute",
            }
        )

    @dataclass(kw_only=True)
    class AcquisitionStation:
        value: str = field(default="")
        unit: Units | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass(kw_only=True)
    class ProcessingCenter:
        value: str = field(default="")
        unit: Units | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass(kw_only=True)
    class ProcessingDate:
        value: str = field(default="")
        unit: Units | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass(kw_only=True)
    class ProcessingSoftware:
        value: str = field(default="")
        unit: Units | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass(kw_only=True)
    class FcHz:
        value: float = field()
        unit: Units | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )


@dataclass(kw_only=True)
class PointType:
    val: list[PointType.Val] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "namespace": "",
            "min_occurs": 5,
            "max_occurs": 5,
        },
    )

    @dataclass(kw_only=True)
    class Val:
        value: float = field()
        unit: Units | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )


@dataclass(kw_only=True)
class SamplingConstantsType(TreeElementBaseType):
    """
    Bandwidths and sampling frequencies.

    Parameters
    ----------
    frg_hz
        Range sampling frequency [Hz]
    brg_hz
        Range bandwidth [Hz]
    faz_hz
        Azimuth sampling frequency [Hz]
    baz_hz
        Azimuth bandwidth [Hz]
    """

    frg_hz: SamplingConstantsType.FrgHz = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    brg_hz: SamplingConstantsType.BrgHz = field(
        metadata={
            "name": "Brg_hz",
            "type": "Element",
            "namespace": "",
        }
    )
    faz_hz: SamplingConstantsType.FazHz = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    baz_hz: SamplingConstantsType.BazHz = field(
        metadata={
            "name": "Baz_hz",
            "type": "Element",
            "namespace": "",
        }
    )

    @dataclass(kw_only=True)
    class FrgHz:
        value: float = field()
        unit: Units | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass(kw_only=True)
    class BrgHz:
        value: float = field()
        unit: Units | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass(kw_only=True)
    class FazHz:
        value: float = field()
        unit: Units | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass(kw_only=True)
    class BazHz:
        value: float = field()
        unit: Units | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )


@dataclass(kw_only=True)
class StateVectorDataType(TreeElementBaseType):
    """
    Information regarding position and velocity of the sensor along the orbit (State Vector Data).

    Parameters
    ----------
    orbit_number
        Number of the orbit
    track
        Number of the track
    orbit_direction
        Direction of the orbit: ASCENDING, DESCENDING
    p_sv_m
        Orbit state vectors position coordinates (xyz) [m]
    v_sv_m_os
        Orbit state vectors velocity coordinates [m/s]
    t_ref_utc
        Azimuth absolute start time for the first state vector [Utc]
    dt_sv_s
        Azimuth time interval between two consecutive state vectors [s]
    n_sv_n
        Number of state vectors
    ascending_node_time
        Azimuth absolute time of the ascending node
    ascending_node_coords
        Coordinates of the ascending node
    """

    orbit_number: str = field(
        metadata={
            "name": "OrbitNumber",
            "type": "Element",
            "namespace": "",
        }
    )
    track: str = field(
        metadata={
            "name": "Track",
            "type": "Element",
            "namespace": "",
        }
    )
    orbit_direction: AscendingDescendingType = field(
        metadata={
            "name": "OrbitDirection",
            "type": "Element",
            "namespace": "",
        }
    )
    p_sv_m: StateVectorDataType.PSvM = field(
        metadata={
            "name": "pSV_m",
            "type": "Element",
            "namespace": "",
        }
    )
    v_sv_m_os: StateVectorDataType.VSvMOs = field(
        metadata={
            "name": "vSV_mOs",
            "type": "Element",
            "namespace": "",
        }
    )
    t_ref_utc: str = field(
        metadata={
            "name": "t_ref_Utc",
            "type": "Element",
            "namespace": "",
        }
    )
    dt_sv_s: StateVectorDataType.DtSvS = field(
        metadata={
            "name": "dtSV_s",
            "type": "Element",
            "namespace": "",
        }
    )
    n_sv_n: StateVectorDataType.NSvN = field(
        metadata={
            "name": "nSV_n",
            "type": "Element",
            "namespace": "",
        }
    )
    ascending_node_time: str | None = field(
        default=None,
        metadata={
            "name": "AscendingNodeTime",
            "type": "Element",
            "namespace": "",
        },
    )
    ascending_node_coords: StateVectorDataType.AscendingNodeCoords | None = field(
        default=None,
        metadata={
            "name": "AscendingNodeCoords",
            "type": "Element",
            "namespace": "",
        },
    )

    @dataclass(kw_only=True)
    class PSvM:
        val: list[StateVectorDataType.PSvM.Val] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

        @dataclass(kw_only=True)
        class Val:
            value: float = field()
            n: int | None = field(
                default=None,
                metadata={
                    "name": "N",
                    "type": "Attribute",
                },
            )
            unit: Units | None = field(
                default=None,
                metadata={
                    "type": "Attribute",
                },
            )

    @dataclass(kw_only=True)
    class VSvMOs:
        val: list[StateVectorDataType.VSvMOs.Val] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
            },
        )

        @dataclass(kw_only=True)
        class Val:
            value: float = field()
            n: int | None = field(
                default=None,
                metadata={
                    "name": "N",
                    "type": "Attribute",
                },
            )
            unit: Units | None = field(
                default=None,
                metadata={
                    "type": "Attribute",
                },
            )

    @dataclass(kw_only=True)
    class DtSvS:
        value: float = field()
        unit: Units | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass(kw_only=True)
    class NSvN:
        value: int = field()
        unit: Units | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass(kw_only=True)
    class AscendingNodeCoords:
        val: list[StateVectorDataType.AscendingNodeCoords.Val] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
                "min_occurs": 3,
                "max_occurs": 3,
            },
        )

        @dataclass(kw_only=True)
        class Val:
            value: float = field()
            n: int | None = field(
                default=None,
                metadata={
                    "name": "N",
                    "type": "Attribute",
                },
            )
            unit: Units | None = field(
                default=None,
                metadata={
                    "type": "Attribute",
                },
            )


@dataclass(kw_only=True)
class DoubleWithUnit:
    class Meta:
        name = "doubleWithUnit"

    value: float = field()
    unit: Units = field(
        metadata={
            "type": "Attribute",
        }
    )


@dataclass(kw_only=True)
class PolyCoregType(TreeElementBaseType):
    """
    Polynomial parametrization of the coregistration parameters.

    Parameters
    ----------
    pol_rg
        Polynomial coefficients of Range
    pol_az
        Polynomial coefficients of Azimuth
    trg0_s
        Polynomial range reference time [s]
    taz0_utc
        Polynomial azimuth reference time [Utc]
    """

    class Meta:
        name = "polyCoregType"

    pol_rg: PolyCoregType.PolRg = field(
        metadata={
            "name": "polRg",
            "type": "Element",
            "namespace": "",
        }
    )
    pol_az: PolyCoregType.PolAz = field(
        metadata={
            "name": "polAz",
            "type": "Element",
            "namespace": "",
        }
    )
    trg0_s: PolyCoregType.Trg0S = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    taz0_utc: PolyCoregType.Taz0Utc = field(
        metadata={
            "name": "taz0_Utc",
            "type": "Element",
            "namespace": "",
        }
    )

    @dataclass(kw_only=True)
    class PolRg:
        val: list[PolyCoregType.PolRg.Val] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
                "min_occurs": 4,
                "max_occurs": 4,
            },
        )

        @dataclass(kw_only=True)
        class Val:
            value: float = field()
            n: int | None = field(
                default=None,
                metadata={
                    "name": "N",
                    "type": "Attribute",
                },
            )
            unit: Units | None = field(
                default=None,
                metadata={
                    "type": "Attribute",
                },
            )

    @dataclass(kw_only=True)
    class PolAz:
        val: list[PolyCoregType.PolAz.Val] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
                "min_occurs": 4,
                "max_occurs": 4,
            },
        )

        @dataclass(kw_only=True)
        class Val:
            value: float = field()
            n: int | None = field(
                default=None,
                metadata={
                    "name": "N",
                    "type": "Attribute",
                },
            )
            unit: Units | None = field(
                default=None,
                metadata={
                    "type": "Attribute",
                },
            )

    @dataclass(kw_only=True)
    class Trg0S:
        value: float = field()
        unit: Units | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass(kw_only=True)
    class Taz0Utc:
        value: str = field(default="")
        unit: Units | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )


@dataclass(kw_only=True)
class PolyType(TreeElementBaseType):
    """
    Polynomial parametrization of the geometry parameter.

    Parameters
    ----------
    pol
        Polynomial coefficients: const, rg, az, az*rg, rg^2, rg^3, rg^4 [Optional: rg^5 rg^6 .... rg^N]
    trg0_s
        Polynomial range reference time [s]
    taz0_utc
        Polynomial azimuth reference time [Utc]
    """

    class Meta:
        name = "polyType"

    pol: PolyType.Pol = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    trg0_s: PolyType.Trg0S = field(
        metadata={
            "type": "Element",
            "namespace": "",
        }
    )
    taz0_utc: PolyType.Taz0Utc = field(
        metadata={
            "name": "taz0_Utc",
            "type": "Element",
            "namespace": "",
        }
    )

    @dataclass(kw_only=True)
    class Pol:
        val: list[PolyType.Pol.Val] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
                "min_occurs": 7,
            },
        )

        @dataclass(kw_only=True)
        class Val:
            value: float = field()
            n: int | None = field(
                default=None,
                metadata={
                    "name": "N",
                    "type": "Attribute",
                },
            )
            unit: Units | None = field(
                default=None,
                metadata={
                    "type": "Attribute",
                },
            )

    @dataclass(kw_only=True)
    class Trg0S:
        value: float = field()
        unit: Units | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass(kw_only=True)
    class Taz0Utc:
        value: str = field(default="")
        unit: Units | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )


@dataclass(kw_only=True)
class StringWithUnit:
    class Meta:
        name = "stringWithUnit"

    value: str = field(default="")
    unit: Units = field(
        metadata={
            "type": "Attribute",
        }
    )


@dataclass(kw_only=True)
class BurstType:
    """
    Parameters
    ----------
    range_start_time
        Range absolute start time [s]
    azimuth_start_time
        Azimuth start time absolute value [Utc]
    burst_center_azimuth_shift
    n
    """

    range_start_time: DoubleWithUnit = field(
        metadata={
            "name": "RangeStartTime",
            "type": "Element",
            "namespace": "",
        }
    )
    azimuth_start_time: StringWithUnit = field(
        metadata={
            "name": "AzimuthStartTime",
            "type": "Element",
            "namespace": "",
        }
    )
    burst_center_azimuth_shift: DoubleWithUnit | None = field(
        default=None,
        metadata={
            "name": "BurstCenterAzimuthShift",
            "type": "Element",
            "namespace": "",
        },
    )
    n: int = field(
        metadata={
            "name": "N",
            "type": "Attribute",
        }
    )


@dataclass(kw_only=True)
class DataStatisticsType(TreeElementBaseType):
    """
    Statistics computed from data.

    Parameters
    ----------
    num_samples
        Number of samples analyzed
    max_i
        Max of I (real) samples
    min_i
        Min of I (real) samples
    max_q
        Max of Q (imaginary) samples
    min_q
        Min of Q (imaginary) samples
    sum_i
        Sum of I (real) samples
    sum_q
        Sum of Q (imaginary) samples
    sum2_i
        Square Sum of I (real) samples
    sum2_q
        Square Sum of Q (imaginary) samples
    std_dev_i
        Standard Deviation of I (real) samples
    std_dev_q
        Standard Deviation of Q (imaginary) samples
    statistics_list
    """

    num_samples: DataStatisticsType.NumSamples = field(
        metadata={
            "name": "NumSamples",
            "type": "Element",
            "namespace": "",
        }
    )
    max_i: DataStatisticsType.MaxI = field(
        metadata={
            "name": "MaxI",
            "type": "Element",
            "namespace": "",
        }
    )
    min_i: DataStatisticsType.MinI = field(
        metadata={
            "name": "MinI",
            "type": "Element",
            "namespace": "",
        }
    )
    max_q: DataStatisticsType.MaxQ = field(
        metadata={
            "name": "MaxQ",
            "type": "Element",
            "namespace": "",
        }
    )
    min_q: DataStatisticsType.MinQ = field(
        metadata={
            "name": "MinQ",
            "type": "Element",
            "namespace": "",
        }
    )
    sum_i: DataStatisticsType.SumI = field(
        metadata={
            "name": "SumI",
            "type": "Element",
            "namespace": "",
        }
    )
    sum_q: DataStatisticsType.SumQ = field(
        metadata={
            "name": "SumQ",
            "type": "Element",
            "namespace": "",
        }
    )
    sum2_i: DataStatisticsType.Sum2I = field(
        metadata={
            "name": "Sum2I",
            "type": "Element",
            "namespace": "",
        }
    )
    sum2_q: DataStatisticsType.Sum2Q = field(
        metadata={
            "name": "Sum2Q",
            "type": "Element",
            "namespace": "",
        }
    )
    std_dev_i: DataStatisticsType.StdDevI = field(
        metadata={
            "name": "StdDevI",
            "type": "Element",
            "namespace": "",
        }
    )
    std_dev_q: DataStatisticsType.StdDevQ = field(
        metadata={
            "name": "StdDevQ",
            "type": "Element",
            "namespace": "",
        }
    )
    statistics_list: DataStatisticsType.StatisticsList | None = field(
        default=None,
        metadata={
            "name": "StatisticsList",
            "type": "Element",
            "namespace": "",
        },
    )

    @dataclass(kw_only=True)
    class NumSamples:
        value: int = field()
        unit: Units | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass(kw_only=True)
    class MaxI:
        value: float = field()
        unit: Units | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass(kw_only=True)
    class MinI:
        value: float = field()
        unit: Units | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass(kw_only=True)
    class MaxQ:
        value: float = field()
        unit: Units | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass(kw_only=True)
    class MinQ:
        value: float = field()
        unit: Units | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass(kw_only=True)
    class SumI:
        value: float = field()
        unit: Units | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass(kw_only=True)
    class SumQ:
        value: float = field()
        unit: Units | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass(kw_only=True)
    class Sum2I:
        value: float = field()
        unit: Units | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass(kw_only=True)
    class Sum2Q:
        value: float = field()
        unit: Units | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass(kw_only=True)
    class StdDevI:
        value: float = field()
        unit: Units | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass(kw_only=True)
    class StdDevQ:
        value: float = field()
        unit: Units | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass(kw_only=True)
    class StatisticsList:
        data_block_statistic: list[DataBlockStatisticsType] = field(
            default_factory=list,
            metadata={
                "name": "DataBlockStatistic",
                "type": "Element",
                "namespace": "",
                "min_occurs": 1,
            },
        )


@dataclass(kw_only=True)
class GroundCornersPointsType(TreeElementBaseType):
    easting_grid_size: GroundCornersPointsType.EastingGridSize = field(
        metadata={
            "name": "EastingGridSize",
            "type": "Element",
            "namespace": "",
        }
    )
    northing_grid_size: GroundCornersPointsType.NorthingGridSize = field(
        metadata={
            "name": "NorthingGridSize",
            "type": "Element",
            "namespace": "",
        }
    )
    north_west: GroundCornersPointsType.NorthWest = field(
        metadata={
            "name": "NorthWest",
            "type": "Element",
            "namespace": "",
        }
    )
    north_east: GroundCornersPointsType.NorthEast = field(
        metadata={
            "name": "NorthEast",
            "type": "Element",
            "namespace": "",
        }
    )
    south_west: GroundCornersPointsType.SouthWest = field(
        metadata={
            "name": "SouthWest",
            "type": "Element",
            "namespace": "",
        }
    )
    south_east: GroundCornersPointsType.SouthEast = field(
        metadata={
            "name": "SouthEast",
            "type": "Element",
            "namespace": "",
        }
    )
    center: GroundCornersPointsType.Center = field(
        metadata={
            "name": "Center",
            "type": "Element",
            "namespace": "",
        }
    )

    @dataclass(kw_only=True)
    class EastingGridSize:
        value: float = field()
        unit: Units | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass(kw_only=True)
    class NorthingGridSize:
        value: float = field()
        unit: Units | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass(kw_only=True)
    class NorthWest:
        point: PointType = field(
            metadata={
                "name": "Point",
                "type": "Element",
                "namespace": "",
            }
        )

    @dataclass(kw_only=True)
    class NorthEast:
        point: PointType = field(
            metadata={
                "name": "Point",
                "type": "Element",
                "namespace": "",
            }
        )

    @dataclass(kw_only=True)
    class SouthWest:
        point: PointType = field(
            metadata={
                "name": "Point",
                "type": "Element",
                "namespace": "",
            }
        )

    @dataclass(kw_only=True)
    class SouthEast:
        point: PointType = field(
            metadata={
                "name": "Point",
                "type": "Element",
                "namespace": "",
            }
        )

    @dataclass(kw_only=True)
    class Center:
        point: PointType = field(
            metadata={
                "name": "Point",
                "type": "Element",
                "namespace": "",
            }
        )


@dataclass(kw_only=True)
class PulseType(TreeElementBaseType):
    """
    Transmitted pulse parameters.

    Parameters
    ----------
    direction
        Pulse direction (UP, DOWN)
    pulse_length
        Pulse length [s]
    bandwidth
        Pulse bandwidth [Hz]
    pulse_energy
        Pulse energy [J]
    pulse_sampling_rate
        Pulse sampling rate [Hz]
    pulse_start_frequency
        Pulse start frequency [Hz]
    pulse_start_phase
        Pulse start phase [rad]
    """

    direction: PulseTypeDirection | None = field(
        default=None,
        metadata={
            "name": "Direction",
            "type": "Element",
            "namespace": "",
        },
    )
    pulse_length: DoubleWithUnit = field(
        metadata={
            "name": "PulseLength",
            "type": "Element",
            "namespace": "",
        }
    )
    bandwidth: DoubleWithUnit = field(
        metadata={
            "name": "Bandwidth",
            "type": "Element",
            "namespace": "",
        }
    )
    pulse_energy: DoubleWithUnit = field(
        metadata={
            "name": "PulseEnergy",
            "type": "Element",
            "namespace": "",
        }
    )
    pulse_sampling_rate: DoubleWithUnit = field(
        metadata={
            "name": "PulseSamplingRate",
            "type": "Element",
            "namespace": "",
        }
    )
    pulse_start_frequency: DoubleWithUnit | None = field(
        default=None,
        metadata={
            "name": "PulseStartFrequency",
            "type": "Element",
            "namespace": "",
        },
    )
    pulse_start_phase: DoubleWithUnit | None = field(
        default=None,
        metadata={
            "name": "PulseStartPhase",
            "type": "Element",
            "namespace": "",
        },
    )


@dataclass(kw_only=True)
class RasterInfoType(TreeElementBaseType):
    """
    Information regarding binary file format and time coordinates of the image.

    Parameters
    ----------
    file_name
        Name of the associated binary file
    lines
        Total number of lines (azimuth) of the image
    samples
        Total number of samples (range) of the image
    header_offset_bytes
        Number of bytes at the beginning of the file containing the header information
    row_prefix_bytes
        Number of bytes at the beginning of each line containing header information
    byte_order
        Endianity: BIGENDIAN or LITTLEENDIAN
    cell_type
        Byte format type: FLOAT_COMPLEX, FLOAT32, DOUBLE_COMPLEX, FLOAT64, INT16, SHORT_COMPLEX, INT32, INT_COMPLEX,
        INT8, INT8_COMPLEX
    lines_step
        Azimuth sampling step [s]
    samples_step
        Range sampling step [s]
    lines_start
        Azimuth absolute start time [Utc]
    samples_start
        Range absolute start time [s]
    raster_format
        Raster Format of the Data ( Default value is ARESYS_RASTER )
    invalid_value
    """

    file_name: str = field(
        metadata={
            "name": "FileName",
            "type": "Element",
            "namespace": "",
        }
    )
    lines: int = field(
        metadata={
            "name": "Lines",
            "type": "Element",
            "namespace": "",
        }
    )
    samples: int = field(
        metadata={
            "name": "Samples",
            "type": "Element",
            "namespace": "",
        }
    )
    header_offset_bytes: int = field(
        metadata={
            "name": "HeaderOffsetBytes",
            "type": "Element",
            "namespace": "",
        }
    )
    row_prefix_bytes: int = field(
        metadata={
            "name": "RowPrefixBytes",
            "type": "Element",
            "namespace": "",
        }
    )
    byte_order: Endianity = field(
        metadata={
            "name": "ByteOrder",
            "type": "Element",
            "namespace": "",
        }
    )
    cell_type: CellTypeVerboseType = field(
        metadata={
            "name": "CellType",
            "type": "Element",
            "namespace": "",
        }
    )
    lines_step: DoubleWithUnit = field(
        metadata={
            "name": "LinesStep",
            "type": "Element",
            "namespace": "",
        }
    )
    samples_step: DoubleWithUnit = field(
        metadata={
            "name": "SamplesStep",
            "type": "Element",
            "namespace": "",
        }
    )
    lines_start: StringWithUnit = field(
        metadata={
            "name": "LinesStart",
            "type": "Element",
            "namespace": "",
        }
    )
    samples_start: StringWithUnit = field(
        metadata={
            "name": "SamplesStart",
            "type": "Element",
            "namespace": "",
        }
    )
    raster_format: RasterFormatType | None = field(
        default=None,
        metadata={
            "name": "RasterFormat",
            "type": "Element",
            "namespace": "",
        },
    )
    invalid_value: Dcomplex | None = field(
        default=None,
        metadata={
            "name": "InvalidValue",
            "type": "Element",
            "namespace": "",
        },
    )


@dataclass(kw_only=True)
class SwathInfoType(TreeElementBaseType):
    """
    Swath general information.

    Parameters
    ----------
    swath
        Swath name
    swath_acquisition_order
        Swath acquisition order
    polarization
        Polarization: H/H, H/V, V/H, V/V
    rank
        Rank
    range_delay_bias
        Range delay bias [s]
    acquisition_start_time
        Acquisition start time [Utc]
    azimuth_steering_angle_reference_time
        Azimuth antenna steering angle polynomial reference time [s]
    azimuth_steering_angle_pol
        Azimuth antenna steering angle polynomial coefficients: const [rad], az [rad/s], az^2 [rad/s^2], az^3
        [rad/s^3]
    azimuth_steering_rate_reference_time
        Azimuth antenna steering rate polynomial reference time [s]
    azimuth_steering_rate_pol
        Azimuth antenna steering rate polynomial coefficients: const [rad/s], az [rad/s^2], az^2 [rad/s^3]
    acquisition_prf
        Acquisition Pulse Repetition Frequency
    echoes_per_burst
        Number of echoes for each burst
    channel_delay
        Range channel delay time
    rx_gain
        Value of the commandable Rx attenuation in the receiver channel
    """

    swath: SwathInfoType.Swath = field(
        metadata={
            "name": "Swath",
            "type": "Element",
            "namespace": "",
        }
    )
    swath_acquisition_order: SwathInfoType.SwathAcquisitionOrder = field(
        metadata={
            "name": "SwathAcquisitionOrder",
            "type": "Element",
            "namespace": "",
        }
    )
    polarization: PolarizationType = field(
        metadata={
            "name": "Polarization",
            "type": "Element",
            "namespace": "",
        }
    )
    rank: SwathInfoType.Rank = field(
        metadata={
            "name": "Rank",
            "type": "Element",
            "namespace": "",
        }
    )
    range_delay_bias: SwathInfoType.RangeDelayBias = field(
        metadata={
            "name": "RangeDelayBias",
            "type": "Element",
            "namespace": "",
        }
    )
    acquisition_start_time: SwathInfoType.AcquisitionStartTime = field(
        metadata={
            "name": "AcquisitionStartTime",
            "type": "Element",
            "namespace": "",
        }
    )
    azimuth_steering_angle_reference_time: DoubleWithUnit | None = field(
        default=None,
        metadata={
            "name": "AzimuthSteeringAngleReferenceTime",
            "type": "Element",
            "namespace": "",
        },
    )
    azimuth_steering_angle_pol: SwathInfoType.AzimuthSteeringAnglePol | None = field(
        default=None,
        metadata={
            "name": "AzimuthSteeringAnglePol",
            "type": "Element",
            "namespace": "",
        },
    )
    azimuth_steering_rate_reference_time: DoubleWithUnit | None = field(
        default=None,
        metadata={
            "name": "AzimuthSteeringRateReferenceTime",
            "type": "Element",
            "namespace": "",
        },
    )
    azimuth_steering_rate_pol: SwathInfoType.AzimuthSteeringRatePol | None = field(
        default=None,
        metadata={
            "name": "AzimuthSteeringRatePol",
            "type": "Element",
            "namespace": "",
        },
    )
    acquisition_prf: float = field(
        metadata={
            "name": "AcquisitionPRF",
            "type": "Element",
            "namespace": "",
        }
    )
    echoes_per_burst: int = field(
        metadata={
            "name": "EchoesPerBurst",
            "type": "Element",
            "namespace": "",
        }
    )
    channel_delay: float | None = field(
        default=None,
        metadata={
            "name": "ChannelDelay",
            "type": "Element",
            "namespace": "",
        },
    )
    rx_gain: float | None = field(
        default=None,
        metadata={
            "name": "RxGain",
            "type": "Element",
            "namespace": "",
        },
    )

    @dataclass(kw_only=True)
    class Swath:
        value: str = field(default="")
        unit: Units | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass(kw_only=True)
    class SwathAcquisitionOrder:
        value: int = field()
        unit: Units | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass(kw_only=True)
    class Rank:
        value: int = field()
        unit: Units | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass(kw_only=True)
    class RangeDelayBias:
        value: float = field()
        unit: Units | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass(kw_only=True)
    class AcquisitionStartTime:
        value: str = field(default="")
        unit: Units | None = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass(kw_only=True)
    class AzimuthSteeringAnglePol:
        val: list[SwathInfoType.AzimuthSteeringAnglePol.Val] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
                "min_occurs": 4,
                "max_occurs": 4,
            },
        )

        @dataclass(kw_only=True)
        class Val:
            value: float = field()
            n: int | None = field(
                default=None,
                metadata={
                    "name": "N",
                    "type": "Attribute",
                },
            )
            unit: Units | None = field(
                default=None,
                metadata={
                    "type": "Attribute",
                },
            )

    @dataclass(kw_only=True)
    class AzimuthSteeringRatePol:
        val: list[SwathInfoType.AzimuthSteeringRatePol.Val] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "namespace": "",
                "min_occurs": 3,
                "max_occurs": 3,
            },
        )

        @dataclass(kw_only=True)
        class Val:
            value: float = field()
            n: int | None = field(
                default=None,
                metadata={
                    "name": "N",
                    "type": "Attribute",
                },
            )
            unit: Units | None = field(
                default=None,
                metadata={
                    "type": "Attribute",
                },
            )


@dataclass(kw_only=True)
class BurstInfoType(TreeElementBaseType):
    """
    Bursts information.

    Parameters
    ----------
    number_of_bursts
        Number of bursts in the swath
    lines_per_burst
        Number of lines in each burst
    lines_per_burst_change_list
    burst_repetition_frequency
        Burst repetition frequency [Hz]
    burst
        Time coordinates of each burst
    """

    number_of_bursts: int = field(
        metadata={
            "name": "NumberOfBursts",
            "type": "Element",
            "namespace": "",
        }
    )
    lines_per_burst: int | None = field(
        default=None,
        metadata={
            "name": "LinesPerBurst",
            "type": "Element",
            "namespace": "",
        },
    )
    lines_per_burst_change_list: BurstInfoType.LinesPerBurstChangeList | None = field(
        default=None,
        metadata={
            "name": "LinesPerBurstChangeList",
            "type": "Element",
            "namespace": "",
        },
    )
    burst_repetition_frequency: DoubleWithUnit = field(
        metadata={
            "name": "BurstRepetitionFrequency",
            "type": "Element",
            "namespace": "",
        }
    )
    burst: list[BurstType] = field(
        default_factory=list,
        metadata={
            "name": "Burst",
            "type": "Element",
            "namespace": "",
            "min_occurs": 1,
        },
    )

    @dataclass(kw_only=True)
    class LinesPerBurstChangeList:
        lines: list[BurstInfoType.LinesPerBurstChangeList.Lines] = field(
            default_factory=list,
            metadata={
                "name": "Lines",
                "type": "Element",
                "namespace": "",
                "min_occurs": 1,
            },
        )

        @dataclass(kw_only=True)
        class Lines:
            value: int = field()
            from_burst: int = field(
                metadata={
                    "name": "FromBurst",
                    "type": "Attribute",
                }
            )
