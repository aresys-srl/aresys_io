# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""test read trajectory."""

from pathlib import Path

from aresys_io.sarsystem import read_sat_table, read_timeline_table
from aresys_io.sarsystem.sat_table import (
    SatTable,
    SwathTable,
    TimeLine,
)


def test_open_file() -> None:
    sarsystem_folder = Path(__file__).parent.joinpath(
        "data",
        "input",
        "Stripmap_TerraSARX_Rome",
    )
    acq_mode = "StripmapSM"
    sat_table = read_sat_table(sarsystem_folder, acq_mode)
    assert isinstance(sat_table, SatTable)


def test_timeline_table_instance() -> None:
    sarsystem_folder = Path(__file__).parent.joinpath(
        "data",
        "input",
        "Stripmap_TerraSARX_Rome",
    )
    acq_mode = "StripmapSM"
    sat_table = read_sat_table(sarsystem_folder, acq_mode)
    timeline_table = sat_table.timeline_table
    assert isinstance(timeline_table, TimeLine)


def test_swath_table_instance() -> None:
    sarsystem_folder = Path(__file__).parent.joinpath(
        "data",
        "input",
        "Stripmap_TerraSARX_Rome",
    )
    acq_mode = "StripmapSM"
    sat_table = read_sat_table(sarsystem_folder, acq_mode)
    timeline_table = read_timeline_table(
        Path(__file__).parent.joinpath(
            "data",
            "input",
            "Stripmap_TerraSARX_Rome/AcquisitionModes/StripmapSM",
            "TimelineTable.xml",
        ),
    )
    beam_name2number = timeline_table.steering_velocity_list
    swath_table_dic = sat_table.swath_table
    swath_table = swath_table_dic[beam_name2number[0].beam_id]
    assert isinstance(swath_table, SwathTable)
