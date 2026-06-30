# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""test read swath table."""

from pathlib import Path

import pytest

from aresys_io.sarsystem import read_swath_table
from aresys_io.sarsystem.swathtable import SwathTable


def test_open_file() -> None:
    filename = Path(__file__).parent.joinpath(
        "data",
        "input",
        "Stripmap_TerraSARX_Rome/Swaths/StripmapSM_SS1",
        "SwathParameterTable.xml",
    )
    swath_table = read_swath_table(filename)
    assert isinstance(swath_table, SwathTable)


def test_prf_value() -> None:
    filename = Path(__file__).parent.joinpath(
        "data",
        "input",
        "Stripmap_TerraSARX_Rome/Swaths/StripmapSM_SS1",
        "SwathParameterTable.xml",
    )
    swath_table = read_swath_table(filename)
    prf = swath_table.parameter_period[0].prf
    assert prf == 2875


def test_swst_value() -> None:
    filename = Path(__file__).parent.joinpath(
        "data",
        "input",
        "Stripmap_TerraSARX_Rome/Swaths/StripmapSM_SS1",
        "SwathParameterTable.xml",
    )
    swath_table = read_swath_table(filename)
    swst = swath_table.parameter_period[0].swst
    assert swst == pytest.approx(6.41912894641136e-05)


def test_swl_value() -> None:
    filename = Path(__file__).parent.joinpath(
        "data",
        "input",
        "Stripmap_TerraSARX_Rome/Swaths/StripmapSM_SS1",
        "SwathParameterTable.xml",
    )
    swath_table = read_swath_table(filename)
    swl = swath_table.parameter_period[0].swl
    assert swl == pytest.approx(0.000156005955574837)
