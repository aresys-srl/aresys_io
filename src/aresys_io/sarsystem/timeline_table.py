# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""timeline table dataclasses."""

from enum import Enum

import numpy as np
from pydantic import BaseModel

from aresys_io.sarsystem.models import time_line_table as model_timeline
from aresys_io.sarsystem.utils import (
    VectorInt,
    index_type_to_array,
)


class Pattern(BaseModel):
    """
    Represents a the pattern time interval with optional start and stop times.

    Attributes
    ----------
    start : float, optional
        Start time of the pattern, defaults to None.
    stop : float, optional
        Stop time of the pattern, defaults to None.
    """

    start: float | None = None
    stop: float | None = None

    @staticmethod
    def from_model(model: model_timeline.PatternListType.Pattern) -> "Pattern":
        """Construct a Pattern instance from a model object."""
        start = None
        stop = None
        if model.time_validity is not None:
            start = model.time_validity.start
            stop = model.time_validity.stop

        return Pattern(start=start, stop=stop)


class Echo(Enum):
    """Enumeration of echo types used in timeline periods."""

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


class TimeLinePeriod(BaseModel):
    """
    Represents a period within a timeline, with beam, echo, steering, and pattern information.

    Attributes
    ----------
    beam_id : str
        Identifier of the beam.
    echo : Echo
        Type of echo used in this period.
    n_echo : int
        Number of echoes in the period.
    azimuth_steering_index_tx : np.ndarray
        Transmit azimuth steering indices.
    azimuth_steering_index_rx : np.ndarray
        Receive azimuth steering indices.
    chirp_index : np.ndarray
        Chirp indices.
    pattern_list_rx : list of Pattern, optional
        Receive pattern list, if defined.
    pattern_list_tx : list of Pattern, optional
        Transmit pattern list, if defined.
    """

    beam_id: str
    echo: Echo
    n_echo: int
    azimuth_steering_index_tx: VectorInt
    azimuth_steering_index_rx: VectorInt
    chirp_index: VectorInt
    pattern_list_rx: list[Pattern] | None = None
    pattern_list_tx: list[Pattern] | None = None

    @staticmethod
    def from_model(model: model_timeline.TimeLinePeriodType) -> "TimeLinePeriod":
        """Construct a TimeLinePeriod instance from a model object."""
        pattern_list_tx = None
        pattern_list_rx = None
        if model.pattern_list_tx is not None:
            pattern_list_tx = [
                Pattern.from_model(pattern_model)
                for pattern_model in model.pattern_list_tx.pattern
            ]
        if model.pattern_list_rx is not None:
            pattern_list_rx = [
                Pattern.from_model(pattern_model)
                for pattern_model in model.pattern_list_rx.pattern
            ]
        azimuth_steering_index_rx = index_type_to_array(model.azimuth_steering_index_rx)
        azimuth_steering_index_tx = index_type_to_array(model.azimuth_steering_index_tx)
        chirp_index = index_type_to_array(model.chirp_index)

        return TimeLinePeriod(
            beam_id=model.beam_id,
            echo=Echo(model.echo_type.value),
            n_echo=model.number_of_echoes,
            azimuth_steering_index_rx=azimuth_steering_index_rx,
            azimuth_steering_index_tx=azimuth_steering_index_tx,
            chirp_index=chirp_index,
            pattern_list_rx=pattern_list_rx,
            pattern_list_tx=pattern_list_tx,
        )

    def __eq__(self, other: object) -> bool:
        """Equality comparison for TimeLinePeriod objects."""
        if not isinstance(other, TimeLinePeriod):
            return NotImplemented

        return (
            self.beam_id == other.beam_id
            and self.echo == other.echo
            and self.n_echo == other.n_echo
            and np.array_equal(self.azimuth_steering_index_tx, other.azimuth_steering_index_tx)
            and np.array_equal(self.azimuth_steering_index_rx, other.azimuth_steering_index_rx)
            and np.array_equal(self.chirp_index, other.chirp_index)
            and self.pattern_list_rx == other.pattern_list_rx
            and self.pattern_list_tx == other.pattern_list_tx
        )


class SteeringVelocity(BaseModel):
    """
    Represents the steering velocity for a specific beam.

    Attributes
    ----------
    val : float
        Steering velocity value.
    beam_id : str
        Identifier of the beam.
    """

    val: float
    beam_id: str

    @staticmethod
    def from_model(
        model: model_timeline.SteeringVelocityType,
        beam_index: int,
    ) -> "SteeringVelocity":
        """Create a SteeringVelocity object from a model SteeringVelocityType."""
        return SteeringVelocity(
            val=model.val[beam_index].value,
            beam_id=str(model.val[beam_index].beam_id),
        )


class TimeLine(BaseModel):
    """The full timeline of radar operations, including acquisition and calibration cycles."""

    steering_velocity_list: list[SteeringVelocity]
    mode_id: str
    acquisition_cycle: list[TimeLinePeriod]
    initial_cycle: list[TimeLinePeriod] | None = None
    end_cycle: list[TimeLinePeriod] | None = None
    model_config = {"arbitrary_types_allowed": True}

    @staticmethod
    def from_model(model: model_timeline.Sensor) -> "TimeLine":
        """Construct a TimeLine instance from a model."""
        initial_cycle = (
            [
                TimeLinePeriod.from_model(period)
                for period in model.mode.initial_cycle.timeline_period
            ]
            if model.mode.initial_cycle is not None
            else None
        )

        end_cycle = (
            [TimeLinePeriod.from_model(period) for period in model.mode.end_cycle.timeline_period]
            if model.mode.end_cycle is not None
            else None
        )

        acquisition_cycle = [
            TimeLinePeriod.from_model(period)
            for period in model.mode.acquisition_cycle.timeline_period
        ]

        steering_velocity_list = [
            SteeringVelocity.from_model(model.mode.steering_velocity, beam_index)
            for beam_index in range(len(model.mode.steering_velocity.val))
        ]
        return TimeLine(
            steering_velocity_list=steering_velocity_list,
            initial_cycle=initial_cycle,
            end_cycle=end_cycle,
            acquisition_cycle=acquisition_cycle,
            mode_id=str(model.mode.mode_id),
        )


__all__ = ["Echo", "Pattern", "SteeringVelocity", "TimeLine", "TimeLinePeriod"]
