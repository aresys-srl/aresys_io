# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""swathtable dataclasses."""

from pydantic import BaseModel

from aresys_io.sarsystem.models import swath_parameter_table as swathtable_model


class ParameterPeriod(BaseModel):
    """
    Represents a period of radar system parameters within a swath table.

    Attributes
    ----------
    start_time : float
        Relative start time of the parameter period.
    stop_time : float
        Relative stop time of the parameter period.
    prf : float
        Pulse Repetition Frequency (PRF) during the period.
    swst : float
        swst
    swl : float
        swl
    rank : int
        Rank  of the period.
    noise_figure : float
        Noise figure of the system in dB.
    temperature_ref : float
        System Reference temperature.
    f_c : float
        Carrier frequency in Hz.
    p_tx : float
        Transmitted power.

    Methods
    -------
    from_model(model: model_swathtable.ParameterPeriodType) -> ParameterPeriod
        Creates an instance of ParameterPeriod from an xsdata model-defined data structure.
    """

    start_time: float
    stop_time: float
    prf: float
    swst: float
    swl: float
    rank: int
    noise_figure: float
    temperature_ref: float
    f_c: float
    p_tx: float

    @staticmethod
    def from_model(model: swathtable_model.ParameterPeriodType) -> "ParameterPeriod":
        """Create a ParameterPeriod object from a model ParameterPeriodType."""
        return ParameterPeriod(
            start_time=model.relative_time_start,
            stop_time=model.relative_time_stop,
            prf=model.prf,
            swst=model.swst,
            swl=model.swl,
            rank=model.rank,
            noise_figure=model.noise_figure,
            temperature_ref=model.reference_temperature,
            f_c=model.radar_carrier_frequency,
            p_tx=model.transmitted_power,
        )


class SwathTable(BaseModel):
    """
    Represents the complete swath parameter table for a radar beam configuration.

    Attributes
    ----------
    beam_id : str
        Identifier for the radar beam.
    freq_sampling : float
        Frequency sampling rate used.
    parameter_period : list of ParameterPeriod
        list of parameter periods that define the radar configuration over time.
    """

    beam_id: str
    freq_sampling: float
    parameter_period: list[ParameterPeriod]

    model_config = {"arbitrary_types_allowed": True}


__all__ = ["ParameterPeriod", "SwathTable"]
