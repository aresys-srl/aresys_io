# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""write timeline table module."""

from pathlib import Path

import numpy as np

from aresys_io.core.parsing import serialize
from aresys_io.sarsystem.models import time_line_table as model_timeline
from aresys_io.sarsystem.timeline_table import Pattern, SteeringVelocity, TimeLine, TimeLinePeriod


def array_to_indextype(array: np.ndarray) -> model_timeline.IndexType:
    """Convert a numpy integer array to a model_timeline.IndexType dataclass."""
    vals = []
    for i, v in enumerate(array.tolist()):
        vals.append(model_timeline.IndexType.Val(value=int(v), n=i))
    return model_timeline.IndexType(val=vals)


def pattern_list_to_patternlisttype(
    patterns: list["Pattern"] | None = None,
) -> model_timeline.PatternListType | None:
    """Convert a list of Pattern objects to a model_timeline.PatternListType dataclass."""
    if patterns is None:
        return None
    pattern_list = []
    for i, pat in enumerate(patterns):
        # Start/stop/unit handling
        time_validity = None
        if pat.start is not None or pat.stop is not None:
            time_validity = model_timeline.PatternListType.Pattern.TimeValidity(
                start=pat.start if pat.start is not None else 0.0,
                stop=pat.stop if pat.stop is not None else 0.0,
                unit="percentage",
            )
        pattern_list.append(
            model_timeline.PatternListType.Pattern(
                pattern_index=i,
                time_validity=time_validity,
                n=i,
            ),
        )
    return model_timeline.PatternListType(pattern=pattern_list)


def steeringvelocitylist_to_steeringvelocitytype(
    steering_velocity_list: list[SteeringVelocity],
) -> model_timeline.SteeringVelocityType:
    """Convert a list of SteeringVelocity objects to a model_timeline.SteeringVelocityType."""
    vals = [
        model_timeline.SteeringVelocityType.Val(value=sv.val, beam_id=sv.beam_id)
        for sv in steering_velocity_list
    ]
    return model_timeline.SteeringVelocityType(val=vals)


def period_to_timelineperiodtype(
    period: TimeLinePeriod,
    period_number: int | None = None,
) -> model_timeline.TimeLinePeriodType:
    """Convert a TimeLinePeriod object to a model_timeline.TimeLinePeriodType dataclass."""
    return model_timeline.TimeLinePeriodType(
        beam_id=period.beam_id,
        echo_type=model_timeline.EchoTypeType(period.echo.value),
        number_of_echoes=period.n_echo,
        pattern_list_tx=pattern_list_to_patternlisttype(period.pattern_list_tx),
        pattern_list_rx=pattern_list_to_patternlisttype(period.pattern_list_rx),
        azimuth_steering_index_tx=array_to_indextype(period.azimuth_steering_index_tx),
        azimuth_steering_index_rx=array_to_indextype(period.azimuth_steering_index_rx),
        chirp_index=array_to_indextype(period.chirp_index),
        period_number=0 if period_number is None else period_number,
    )


def cycle_to_cycletype(
    periods: list[TimeLinePeriod] | None = None,
) -> model_timeline.CycleType | None:
    """Convert a list of TimeLinePeriod objects to a model_timeline.CycleType dataclass."""
    if periods is None:
        return None
    return model_timeline.CycleType(
        timeline_period=[
            period_to_timelineperiodtype(period, period_number=i)
            for i, period in enumerate(periods)
        ],
    )


def timeline_to_sensor(timeline: TimeLine, version: str = "1.0") -> model_timeline.Sensor:
    """Convert a TimeLine object into a model_timeline.Sensor dataclass for serialization."""
    mode = model_timeline.ModeType(
        steering_velocity=steeringvelocitylist_to_steeringvelocitytype(
            timeline.steering_velocity_list,
        ),
        initial_cycle=cycle_to_cycletype(timeline.initial_cycle),
        acquisition_cycle=cycle_to_cycletype(timeline.acquisition_cycle)
        or model_timeline.CycleType(timeline_period=[]),
        end_cycle=cycle_to_cycletype(timeline.end_cycle),
        mode_id=timeline.mode_id,
    )
    return model_timeline.Sensor(version=version, mode=mode)


def write_timeline_table_xml(timeline: TimeLine, file: str | Path) -> None:
    """Serialize the timeline model to XML and write it to file.

    Parameters
    ----------
    timeline : TimeLine
        Timeline object to be serialized.
    file : Path
        Destination folder path for the output XML.

    """
    Path(file).write_text(serialize(timeline_to_sensor(timeline=timeline)), encoding="utf-8")


__all__ = ["write_timeline_table_xml"]
