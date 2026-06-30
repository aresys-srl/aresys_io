# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""test read timeline."""

from pathlib import Path

from aresys_io.sarsystem import read_timeline_table
from aresys_io.sarsystem.timeline_table import TimeLine


def test_open_file() -> None:
    filename = Path(__file__).parent.joinpath(
        "data",
        "input",
        "Stripmap_TerraSARX_Rome/AcquisitionModes/StripmapSM",
        "TimelineTable.xml",
    )
    timeline_table = read_timeline_table(filename)
    assert isinstance(timeline_table, TimeLine)


def test_beam_id_name() -> None:
    filename = Path(__file__).parent.joinpath(
        "data",
        "input",
        "Stripmap_TerraSARX_Rome/AcquisitionModes/StripmapSM",
        "TimelineTable.xml",
    )
    timeline_table = read_timeline_table(filename)
    beam_id = timeline_table.acquisition_cycle[0].beam_id
    assert beam_id == "StripmapSM_SS1"
