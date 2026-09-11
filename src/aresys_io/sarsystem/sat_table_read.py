# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""read sat tables (timeline table, swathtable) module."""

from pathlib import Path

from aresys_io.sarsystem.sat_table import BeamNumberEachPeriod, SatTable, TimeLine
from aresys_io.sarsystem.swathtable_read import read_swath_table
from aresys_io.sarsystem.timeline_table_read import read_timeline_table

__all__ = ["read_sat_table"]


def timeline_to_beamnumbereachperiod(timeline_table: TimeLine) -> BeamNumberEachPeriod:
    """Extract beam acquisition cycle data from the given `TimelineTable` instance."""
    acquisition_cycle = timeline_table.acquisition_cycle
    initial_cycle = timeline_table.initial_cycle
    end_cycle = timeline_table.end_cycle

    # create class object beam_each_number_period
    return BeamNumberEachPeriod(
        acquisition_cycle=acquisition_cycle,
        initial_cycle=initial_cycle,
        end_cycle=end_cycle,
    )


def read_sat_table(
    sar_system_folder_name: str | Path,
    acq_mode_id: str,
) -> SatTable:
    """Read satellite acquisition data and returns a `SatTable` instance.

    Parameters
    ----------
    sar_system_folder_name : Path | str
        directory containing the SAR system data, including acquisition modes and swaths.

    acq_mode_id : str
        The acquisition mode identifier, used to locate the corresponding `TimelineTable.xml` and
        determine the beam information.

    Returns
    -------
    SatTable
        An instance of the `SatTable` class that contains the following fields:
        - timeline_table : `TimeLineTable`
            An instance of the `TimeLineTable` class.
        - swath_table : dict
            A dictionary mapping each beam name to its corresponding `SwathTable` instance.
        - beam_number_each_period : `BeamNumberEachPeriod`
            An instance containing different acquisition cycles,
            including `initial_cycle` and `end_cycle` fields.
        - beam_name2number : list of `SteeringVelocity`
            each contains a beam name and its respective steering velocity.
    """
    sar_system_folder_name = Path(sar_system_folder_name)
    timeline_filename = (
        sar_system_folder_name / "AcquisitionModes" / acq_mode_id / "TimelineTable.xml"
    )
    timeline_table = read_timeline_table(timeline_filename)

    beam_name2number = timeline_table.steering_velocity_list

    # Each beam has its own XML file and a swathtable list that contains each kind of beam
    # (SwathTable istance) is created
    swath_table = {}
    for beam in beam_name2number:
        beam_name = beam.beam_id

        swath_filename = sar_system_folder_name / "Swaths" / beam_name / "SwathParameterTable.xml"
        swath_table[beam_name] = read_swath_table(swath_filename)

    beam_number_each_period = timeline_to_beamnumbereachperiod(timeline_table)

    return SatTable(
        timeline_table=timeline_table,
        beam_number_each_period=beam_number_each_period,
        swath_table=swath_table,
        beam_name2number=beam_name2number,
    )
