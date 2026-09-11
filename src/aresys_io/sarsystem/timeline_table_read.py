# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""read timeline table module."""

from pathlib import Path

from aresys_io.core.parsing import parse
from aresys_io.sarsystem.models import time_line_table as model_timeline
from aresys_io.sarsystem.timeline_table import TimeLine

__all__ = ["read_timeline_table"]


def read_timeline_table(filename: Path) -> TimeLine:
    """Read a timeline table XML file and parse its contents into a TimeLine object."""
    return TimeLine.from_model(parse(filename.read_text(encoding="utf-8"), model_timeline.Sensor))
