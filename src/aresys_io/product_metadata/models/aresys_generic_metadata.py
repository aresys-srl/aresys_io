# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Generated module."""

from __future__ import annotations

from dataclasses import dataclass, field

from aresys_io.product_metadata.models.aresys_types import (
    AcquisitionTimelineType,
    AntennaInfoType,
    AttitudeInfoType,
    BurstInfoType,
    DataSetInfoType,
    DataStatisticsType,
    GroundCornersPointsType,
    PolyCoregType,
    PolyType,
    PulseType,
    RasterInfoType,
    SamplingConstantsType,
    StateVectorDataType,
    SwathInfoType,
    TreeElementBaseType,
)


@dataclass(kw_only=True)
class ChannelType(TreeElementBaseType):
    content_id: str | None = field(
        default=None,
        metadata={
            "name": "ContentID",
            "type": "Attribute",
        },
    )


@dataclass(kw_only=True)
class AresysXmlDocType:
    number_of_channels: int = field(
        metadata={
            "name": "NumberOfChannels",
            "type": "Element",
        }
    )
    version_number: float = field(
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
    channel: list[AresysXmlDocType.Channel] = field(
        default_factory=list,
        metadata={
            "name": "Channel",
            "type": "Element",
        },
    )

    @dataclass(kw_only=True)
    class Channel(ChannelType):
        raster_info: RasterInfoType | None = field(
            default=None,
            metadata={
                "name": "RasterInfo",
                "type": "Element",
            },
        )
        data_set_info: DataSetInfoType | None = field(
            default=None,
            metadata={
                "name": "DataSetInfo",
                "type": "Element",
            },
        )
        swath_info: SwathInfoType | None = field(
            default=None,
            metadata={
                "name": "SwathInfo",
                "type": "Element",
            },
        )
        sampling_constants: SamplingConstantsType | None = field(
            default=None,
            metadata={
                "name": "SamplingConstants",
                "type": "Element",
            },
        )
        acquisition_time_line: AcquisitionTimelineType | None = field(
            default=None,
            metadata={
                "name": "AcquisitionTimeLine",
                "type": "Element",
            },
        )
        data_statistics: DataStatisticsType | None = field(
            default=None,
            metadata={
                "name": "DataStatistics",
                "type": "Element",
            },
        )
        burst_info: BurstInfoType | None = field(
            default=None,
            metadata={
                "name": "BurstInfo",
                "type": "Element",
            },
        )
        state_vector_data: StateVectorDataType | None = field(
            default=None,
            metadata={
                "name": "StateVectorData",
                "type": "Element",
            },
        )
        doppler_centroid: list[PolyType] = field(
            default_factory=list,
            metadata={
                "name": "DopplerCentroid",
                "type": "Element",
            },
        )
        doppler_rate: list[PolyType] = field(
            default_factory=list,
            metadata={
                "name": "DopplerRate",
                "type": "Element",
            },
        )
        tops_azimuth_modulation_rate: list[PolyType] = field(
            default_factory=list,
            metadata={
                "name": "TopsAzimuthModulationRate",
                "type": "Element",
            },
        )
        slant_to_ground: list[PolyType] = field(
            default_factory=list,
            metadata={
                "name": "SlantToGround",
                "type": "Element",
            },
        )
        ground_to_slant: list[PolyType] = field(
            default_factory=list,
            metadata={
                "name": "GroundToSlant",
                "type": "Element",
            },
        )
        slant_to_incidence: list[PolyType] = field(
            default_factory=list,
            metadata={
                "name": "SlantToIncidence",
                "type": "Element",
            },
        )
        slant_to_elevation: list[PolyType] = field(
            default_factory=list,
            metadata={
                "name": "SlantToElevation",
                "type": "Element",
            },
        )
        attitude_info: AttitudeInfoType | None = field(
            default=None,
            metadata={
                "name": "AttitudeInfo",
                "type": "Element",
            },
        )
        ground_corner_points: GroundCornersPointsType | None = field(
            default=None,
            metadata={
                "name": "GroundCornerPoints",
                "type": "Element",
            },
        )
        pulse: PulseType | None = field(
            default=None,
            metadata={
                "name": "Pulse",
                "type": "Element",
            },
        )
        coreg_poly: list[PolyCoregType] = field(
            default_factory=list,
            metadata={
                "name": "CoregPoly",
                "type": "Element",
            },
        )
        antenna_info: AntennaInfoType | None = field(
            default=None,
            metadata={
                "name": "AntennaInfo",
                "type": "Element",
            },
        )


@dataclass(kw_only=True)
class AresysXmlDoc(AresysXmlDocType):
    pass
