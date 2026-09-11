# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Binary debug data file management module."""

import struct
from pathlib import Path

import numpy as np

__all__ = ["read_debug"]

# The debug data file binary header is expected to be a sequence of three 32-bit integers,
# representing:
# * the cell type identifier
# * the number of samples of the data matrix
# * the number of lines of the data matrix
_HEADER_FORMAT = "iii"
_HEADER_SIZE = struct.calcsize(_HEADER_FORMAT)

_CELLTYPE_TO_DTYPE_MAP = {
    0: "float32",
    1: "complex64",
    2: "float64",
    3: "complex128",
    4: "int16",
    5: "int8",
    6: "int32",
    7: "int64",
}


def read_debug(filename: str | Path) -> np.ndarray:
    """Read binary debug data file content.

    Parameters
    ----------
    filename : str | Path
        binary debug data file name

    Returns
    -------
    np.ndarray
        array containing the data read from the input binary debug data file

    Raises
    ------
    RuntimeError
        in case of invalid content cell type
    """
    with Path(filename).open(mode="rb") as fdesc:
        header = fdesc.read(_HEADER_SIZE)

        celltype, samples, lines = struct.unpack(_HEADER_FORMAT, header)

        if celltype not in _CELLTYPE_TO_DTYPE_MAP:
            msg = f"Unknown cell type (cell type id = {celltype})"
            raise RuntimeError(msg)

        dtype = _CELLTYPE_TO_DTYPE_MAP[celltype]

        if samples == 0 or lines == 0:
            return np.empty((lines, samples), dtype)

        return np.fromfile(fdesc, dtype).reshape((lines, samples))
