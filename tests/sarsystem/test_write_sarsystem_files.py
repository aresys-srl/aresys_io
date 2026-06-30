# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""test equality of generated sarsystem files."""

import tempfile
from pathlib import Path

from aresys_io.sarsystem import (
    read_swath_table,
    read_timeline_table,
    read_trajectory,
    write_swath_table_xml,
    write_timeline_table_xml,
    write_trajectory_xml,
)


# implemented as a round trip test in order to compare the instances and not the file
def test_trajectory_files_are_equal() -> None:
    input_file_path = Path(__file__).parent.joinpath(
        "data",
        "input",
        "Stripmap_TerraSARX_Rome/Trajectory",
        "Trajectory.xml",
    )
    trajectory_input = read_trajectory(input_file_path)
    with tempfile.TemporaryDirectory() as output:
        write_trajectory_xml(trajectory_input, output)
        trajectory_output = read_trajectory(Path(output).joinpath("Trajectory.xml"))
        assert trajectory_input == trajectory_output


def test_timeline_table_files_are_equal() -> None:
    input_file_path = Path(__file__).parent.joinpath(
        "data",
        "input",
        "Stripmap_TerraSARX_Rome/AcquisitionModes/StripmapSM",
        "TimelineTable.xml",
    )
    timeline_input = read_timeline_table(input_file_path)
    with tempfile.TemporaryDirectory() as output:
        timeline_table_path = Path(output).joinpath("TimeLineTable.xml")
        write_timeline_table_xml(timeline_input, timeline_table_path)
        timeline_output = read_timeline_table(timeline_table_path)
        assert timeline_input == timeline_output


def test_swath_table_files_are_equal() -> None:
    input_file_path = Path(__file__).parent.joinpath(
        "data",
        "input",
        "Stripmap_TerraSARX_Rome/Swaths/StripmapSM_SS1",
        "SwathParameterTable.xml",
    )
    swathtable_input = read_swath_table(input_file_path)
    with tempfile.TemporaryDirectory() as output:
        write_swath_table_xml(swathtable_input, output)
        swathtable_output = read_swath_table(Path(output).joinpath("SwathParameterTable.xml"))
        assert swathtable_input == swathtable_output
