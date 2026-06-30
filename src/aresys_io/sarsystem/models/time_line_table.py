# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Generated module."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class EchoTypeType(Enum):
    ECHO = "Echo"
    WARM_UP = "WarmUp"
    NOISE = "Noise"
    INIT_CAL = "InitCal"
    INIT_CAL_TX_CAL = "InitCal_TxCal"
    INIT_CAL_RX_CAL = "InitCal_RxCal"
    INIT_CAL_EPDNCAL = "InitCal_EPDNCal"
    INIT_CAL_TACAL = "InitCal_TACal"
    INIT_CAL_APDNCAL = "InitCal_APDNCal"
    INIT_CAL_TX_CAL100 = "InitCal_TxCal100"
    INIT_CAL_RX_CAL100 = "InitCal_RxCal100"
    INIT_CAL_EPDNCAL100 = "InitCal_EPDNCal100"
    INIT_CAL_TACAL100 = "InitCal_TACal100"
    INIT_CAL_APDNCAL100 = "InitCal_APDNCal100"
    INIT_CAL_RFC_TX_CAL = "InitCal_RFC_TxCal"
    INIT_CAL_RFC_RX_CAL = "InitCal_RFC_RxCal"
    INIT_CAL_RFC_EPDNCAL = "InitCal_RFC_EPDNCal"
    INIT_CAL_RFC_TACAL = "InitCal_RFC_TACal"
    INIT_CAL_RFC_APDNCAL = "InitCal_RFC_APDNCal"
    INIT_CAL_TX_CAL_ISO = "InitCal_TxCalIso"
    INIT_CAL_RX_CAL_ISO = "InitCal_RxCalIso"
    INIT_CAL_EPDNCAL_ISO = "InitCal_EPDNCalIso"
    INIT_CAL_TACAL_ISO = "InitCal_TACalIso"
    INIT_CAL_APDNCAL_ISO = "InitCal_APDNCalIso"
    INIT_CAL_TX_CAL100_ISO = "InitCal_TxCal100Iso"
    INIT_CAL_RX_CAL100_ISO = "InitCal_RxCal100Iso"
    INIT_CAL_EPDNCAL100_ISO = "InitCal_EPDNCal100Iso"
    INIT_CAL_TACAL100_ISO = "InitCal_TACal100Iso"
    INIT_CAL_APDNCAL100_ISO = "InitCal_APDNCal100Iso"
    INIT_CAL_RFC_TX_CAL_ISO = "InitCal_RFC_TxCalIso"
    INIT_CAL_RFC_RX_CAL_ISO = "InitCal_RFC_RxCalIso"
    INIT_CAL_RFC_EPDNCAL_ISO = "InitCal_RFC_EPDNCalIso"
    INIT_CAL_RFC_TACAL_ISO = "InitCal_RFC_TACalIso"
    INIT_CAL_RFC_APDNCAL_ISO = "InitCal_RFC_APDNCalIso"
    CAL = "Cal"
    CAL_TX_CAL = "Cal_TxCal"
    CAL_RX_CAL = "Cal_RxCal"
    CAL_EPDNCAL = "Cal_EPDNCal"
    CAL_TACAL = "Cal_TACal"
    CAL_APDNCAL = "Cal_APDNCal"
    CAL_TX_CAL100 = "Cal_TxCal100"
    CAL_RX_CAL100 = "Cal_RxCal100"
    CAL_EPDNCAL100 = "Cal_EPDNCal100"
    CAL_TACAL100 = "Cal_TACal100"
    CAL_APDNCAL100 = "Cal_APDNCal100"
    CAL_RFC_TX_CAL = "Cal_RFC_TxCal"
    CAL_RFC_RX_CAL = "Cal_RFC_RxCal"
    CAL_RFC_EPDNCAL = "Cal_RFC_EPDNCal"
    CAL_RFC_TACAL = "Cal_RFC_TACal"
    CAL_RFC_APDNCAL = "Cal_RFC_APDNCal"
    CAL_TX_CAL_ISO = "Cal_TxCalIso"
    CAL_RX_CAL_ISO = "Cal_RxCalIso"
    CAL_EPDNCAL_ISO = "Cal_EPDNCalIso"
    CAL_TACAL_ISO = "Cal_TACalIso"
    CAL_APDNCAL_ISO = "Cal_APDNCalIso"
    CAL_TX_CAL100_ISO = "Cal_TxCal100Iso"
    CAL_RX_CAL100_ISO = "Cal_RxCal100Iso"
    CAL_EPDNCAL100_ISO = "Cal_EPDNCal100Iso"
    CAL_TACAL100_ISO = "Cal_TACal100Iso"
    CAL_APDNCAL100_ISO = "Cal_APDNCal100Iso"
    CAL_RFC_TX_CAL_ISO = "Cal_RFC_TxCalIso"
    CAL_RFC_RX_CAL_ISO = "Cal_RFC_RxCalIso"
    CAL_RFC_EPDNCAL_ISO = "Cal_RFC_EPDNCalIso"
    CAL_RFC_TACAL_ISO = "Cal_RFC_TACalIso"
    CAL_RFC_APDNCAL_ISO = "Cal_RFC_APDNCalIso"
    TXCAL512 = "TXCal512"
    RXCAL512 = "RXCal512"
    TXCAL_RFC = "TXCalRFC"
    RXCAL_RFC = "RXCalRFC"
    EPCAL32 = "EPCal32"
    TACAL32 = "TACal32"
    APCAL1 = "APCal1"
    SILENT = "silent"
    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"
    P5 = "P5"


@dataclass(kw_only=True)
class IndexType:
    val: list[IndexType.Val] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )

    @dataclass(kw_only=True)
    class Val:
        value: int = field()
        n: int = field(
            metadata={
                "name": "N",
                "type": "Attribute",
            }
        )


@dataclass(kw_only=True)
class PatternListType:
    pattern: list[PatternListType.Pattern] = field(
        default_factory=list,
        metadata={
            "name": "Pattern",
            "type": "Element",
            "min_occurs": 1,
        },
    )

    @dataclass(kw_only=True)
    class Pattern:
        pattern_index: int = field(
            metadata={
                "name": "PatternIndex",
                "type": "Element",
            }
        )
        time_validity: PatternListType.Pattern.TimeValidity | None = field(
            default=None,
            metadata={
                "name": "TimeValidity",
                "type": "Element",
            },
        )
        n: int = field(
            metadata={
                "name": "N",
                "type": "Attribute",
            }
        )

        @dataclass(kw_only=True)
        class TimeValidity:
            start: float = field(
                metadata={
                    "name": "Start",
                    "type": "Element",
                }
            )
            stop: float = field(
                metadata={
                    "name": "Stop",
                    "type": "Element",
                }
            )
            unit: str = field(
                metadata={
                    "name": "Unit",
                    "type": "Attribute",
                }
            )


@dataclass(kw_only=True)
class SteeringVelocityType:
    val: list[SteeringVelocityType.Val] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
        },
    )
    unit: str = field(
        init=False,
        default="rad/s",
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )

    @dataclass(kw_only=True)
    class Val:
        value: float = field()
        beam_id: object = field(
            metadata={
                "name": "BeamID",
                "type": "Attribute",
            }
        )


@dataclass(kw_only=True)
class TimeLinePeriodType:
    beam_id: str = field(
        metadata={
            "name": "BeamID",
            "type": "Element",
        }
    )
    echo_type: EchoTypeType = field(
        metadata={
            "name": "EchoType",
            "type": "Element",
        }
    )
    number_of_echoes: int = field(
        metadata={
            "name": "NumberOfEchoes",
            "type": "Element",
        }
    )
    pattern_list_tx: PatternListType | None = field(
        default=None,
        metadata={
            "name": "PatternListTX",
            "type": "Element",
        },
    )
    pattern_list_rx: PatternListType | None = field(
        default=None,
        metadata={
            "name": "PatternListRX",
            "type": "Element",
        },
    )
    azimuth_steering_index_tx: IndexType = field(
        metadata={
            "name": "AzimuthSteeringIndexTX",
            "type": "Element",
        }
    )
    azimuth_steering_index_rx: IndexType = field(
        metadata={
            "name": "AzimuthSteeringIndexRX",
            "type": "Element",
        }
    )
    chirp_index: IndexType = field(
        metadata={
            "name": "ChirpIndex",
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
class CycleType:
    timeline_period: list[TimeLinePeriodType] = field(
        default_factory=list,
        metadata={
            "name": "TimelinePeriod",
            "type": "Element",
            "min_occurs": 1,
        },
    )


@dataclass(kw_only=True)
class ModeType:
    steering_velocity: SteeringVelocityType = field(
        metadata={
            "name": "SteeringVelocity",
            "type": "Element",
        }
    )
    initial_cycle: CycleType | None = field(
        default=None,
        metadata={
            "name": "InitialCycle",
            "type": "Element",
        },
    )
    acquisition_cycle: CycleType = field(
        metadata={
            "name": "AcquisitionCycle",
            "type": "Element",
        }
    )
    end_cycle: CycleType | None = field(
        default=None,
        metadata={
            "name": "EndCycle",
            "type": "Element",
        },
    )
    mode_id: object = field(
        metadata={
            "name": "ModeID",
            "type": "Attribute",
        }
    )


@dataclass(kw_only=True)
class Sensor:
    version: str = field(
        metadata={
            "name": "Version",
            "type": "Element",
        }
    )
    mode: ModeType = field(
        metadata={
            "name": "Mode",
            "type": "Element",
        }
    )
