# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""write swathtable module."""

from pathlib import Path

from aresys_io.core.parsing import serialize
from aresys_io.sarsystem.models import swath_parameter_table as swathtable_model
from aresys_io.sarsystem.swathtable import SwathTable

__all__ = ["write_swath_table_xml"]


def swathtable_to_model(
    swathtable: SwathTable,
    version_number: str = "2.0",
) -> swathtable_model.ConfigurationFileDoc:
    """Convert a SwathTable object into a ConfigurationFileDoc model.

    This function transforms a `SwathTable` data structure into a
    `ConfigurationFileDoc` object compatible with the `swathtable_model` format,
    optionally setting a specific version number.

    Parameters
    ----------
    swathtable : SwathTable
        SwathTable object to be converted.
    version_number : str, optional
        Version number to be set in the ConfigurationFileDoc, by default "2.0"

    Returns
    -------
    swathtable_model.ConfigurationFileDoc
        A ConfigurationFileDoc object representing the swathtable data.

    Raises
    ------
    TypeError
        If the provided swathtable is not a SwathTable object.

    """
    if not isinstance(swathtable, SwathTable):
        msg = "swathtable  is not a SwathTable object"
        raise TypeError(msg)

    parameter_period = [
        swathtable_model.ParameterPeriodType(
            relative_time_start=param.start_time,
            relative_time_stop=param.stop_time,
            prf=param.prf,
            swst=param.swst,
            swl=param.swl,
            rank=param.rank,
            noise_figure=param.noise_figure,
            reference_temperature=param.temperature_ref,
            radar_carrier_frequency=param.f_c,
            transmitted_power=param.p_tx,
            period_number=i + 1,  # Assuming period number starts from 1
        )
        for i, param in enumerate(swathtable.parameter_period)
    ]

    beam = swathtable_model.BeamType(
        sampling_frequency=swathtable.freq_sampling,
        parameter_period=parameter_period,
        beam_id=swathtable.beam_id,
    )

    return swathtable_model.ConfigurationFileDoc(version=version_number, beam=beam)


def write_swath_table_xml(swathtable: SwathTable, xml_dir_path: str | Path) -> None:
    """Serialize the swathtable model to XML and write to file.

    Parameters
    ----------
    swathtable : SwathTable
        SwathTable object to serialize.
    xml_dir_path : Path
        Destination folder path for the output XML.
    """
    swathtable_model = swathtable_to_model(swathtable=swathtable)
    xml_dir_path = Path(xml_dir_path)
    xml_path = xml_dir_path.joinpath("SwathParameterTable.xml")
    xml_path.parent.mkdir(parents=True, exist_ok=True)
    Path(xml_path).write_text(serialize(swathtable_model), encoding="utf-8")
