# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Generated module."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(kw_only=True)
class ParameterPeriodType:
    relative_time_start: float = field(
        metadata={
            "name": "RelativeTimeStart",
            "type": "Element",
        }
    )
    relative_time_stop: float = field(
        metadata={
            "name": "RelativeTimeStop",
            "type": "Element",
        }
    )
    prf: float = field(
        metadata={
            "name": "PRF",
            "type": "Element",
        }
    )
    swst: float = field(
        metadata={
            "name": "SWST",
            "type": "Element",
        }
    )
    swl: float = field(
        metadata={
            "name": "SWL",
            "type": "Element",
        }
    )
    rank: int = field(
        metadata={
            "name": "RANK",
            "type": "Element",
        }
    )
    noise_figure: float = field(
        metadata={
            "name": "NoiseFigure",
            "type": "Element",
        }
    )
    reference_temperature: float = field(
        metadata={
            "name": "ReferenceTemperature",
            "type": "Element",
        }
    )
    radar_carrier_frequency: float = field(
        metadata={
            "name": "RadarCarrierFrequency",
            "type": "Element",
        }
    )
    transmitted_power: float = field(
        metadata={
            "name": "TransmittedPower",
            "type": "Element",
        }
    )
    period_number: int = field(
        metadata={
            "name": "PeriodNumber",
            "type": "Attribute",
        }
    )


@dataclass(kw_only=True)
class BeamType:
    sampling_frequency: float = field(
        metadata={
            "name": "SamplingFrequency",
            "type": "Element",
        }
    )
    parameter_period: list[ParameterPeriodType] = field(
        default_factory=list,
        metadata={
            "name": "ParameterPeriod",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    beam_id: str = field(
        metadata={
            "name": "BeamID",
            "type": "Attribute",
        }
    )


@dataclass(kw_only=True)
class ConfigurationFileDoc:
    version: str = field(
        metadata={
            "name": "Version",
            "type": "Element",
        }
    )
    beam: BeamType = field(
        metadata={
            "name": "Beam",
            "type": "Element",
        }
    )
