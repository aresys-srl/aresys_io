# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""sat tables (timeline table, swathtable) dataclasses."""

from pydantic import BaseModel

from aresys_io.sarsystem.swathtable import SwathTable
from aresys_io.sarsystem.timeline_table import SteeringVelocity, TimeLine, TimeLinePeriod


class BeamNumberEachPeriod(BaseModel):
    """Beam period."""

    acquisition_cycle: list[TimeLinePeriod] | None = None
    initial_cycle: list[TimeLinePeriod] | None = None
    end_cycle: list[TimeLinePeriod] | None = None


class SatTable(BaseModel):
    """Satellite table."""

    timeline_table: TimeLine
    swath_table: dict[str, SwathTable]
    beam_name2number: list[SteeringVelocity]
    beam_number_each_period: BeamNumberEachPeriod

    model_config = {"arbitrary_types_allowed": True}


__all__ = ["BeamNumberEachPeriod", "SatTable"]
