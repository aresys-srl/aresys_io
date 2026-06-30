# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""read swathtable module."""

from os import PathLike
from pathlib import Path

from aresys_io.core.parsing import parse
from aresys_io.sarsystem.models import swath_parameter_table as swathtable_model
from aresys_io.sarsystem.swathtable import ParameterPeriod, SwathTable


def read_swath_table(filename: PathLike) -> SwathTable:
    """Read a swath table XML file and returns a SwathTable object.

    Parameters
    ----------
    filename : str or Path
        Path to the XML file containing the swath parameter table.

    Returns
    -------
    SwathTable
        Parsed data representing the swath table, including beam ID,
        frequency sampling, and parameter periods.

    """
    file_content = parse(
        Path(filename).read_text(encoding="utf-8"), swathtable_model.ConfigurationFileDoc
    )
    parameter_period = [
        ParameterPeriod.from_model(period) for period in file_content.beam.parameter_period
    ]
    return SwathTable(
        beam_id=file_content.beam.beam_id,
        freq_sampling=file_content.beam.sampling_frequency,
        parameter_period=parameter_period,
    )


__all__ = ["read_swath_table"]
