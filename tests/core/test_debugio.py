# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Unit tests for aresys_io.core.debugio."""

import struct
from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np
import pytest

from aresys_io.core.debugio import read_debug


@pytest.mark.parametrize(
    ("celltype", "dtype"),
    [
        (0, np.float32),
        (1, np.complex64),
        (2, np.float64),
        (3, np.complex128),
        (4, np.int16),
        (5, np.int8),
        (6, np.int32),
        (7, np.int64),
    ],
)
def test_read_debug_supported_cell_types(celltype: int, dtype: type[np.generic]) -> None:
    samples = 3
    lines = 2
    data = np.arange(samples * lines, dtype=dtype).reshape((lines, samples))

    with TemporaryDirectory() as tmpdir:
        debug_file = Path(tmpdir) / "debug.bin"
        with debug_file.open("wb") as fdesc:
            fdesc.write(struct.pack("iii", celltype, samples, lines))
            fdesc.write(data.tobytes())

        read_data = read_debug(debug_file)

        assert read_data.dtype == np.dtype(dtype)
        np.testing.assert_array_equal(read_data, data)


def test_read_debug_zero_sized_matrix_returns_empty() -> None:
    celltype = 0
    samples = 0
    lines = 4

    with TemporaryDirectory() as tmpdir:
        debug_file = Path(tmpdir) / "debug.bin"
        with debug_file.open("wb") as fdesc:
            fdesc.write(struct.pack("iii", celltype, samples, lines))

        read_data = read_debug(debug_file)

        assert read_data.shape == (lines, samples)
        assert read_data.dtype == np.dtype(np.float32)
        assert read_data.size == 0


def test_read_debug_unknown_cell_type_raises() -> None:
    unknown_celltype = 99
    samples = 2
    lines = 2

    with TemporaryDirectory() as tmpdir:
        debug_file = Path(tmpdir) / "debug.bin"
        with debug_file.open("wb") as fdesc:
            fdesc.write(struct.pack("iii", unknown_celltype, samples, lines))
            fdesc.write(np.zeros((lines, samples), dtype=np.float32).tobytes())

        with pytest.raises(RuntimeError, match=r"Unknown cell type"):
            read_debug(debug_file)
