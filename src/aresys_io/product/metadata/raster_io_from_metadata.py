# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Input/output utilities using metadata objects."""

import warnings
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path
from typing import TypeAlias

import numpy.typing as npt

from aresys_io.core.raster_io import (
    DataLayout,
    read_binary_header,
    read_raster,
    read_raster_as_memmap,
    read_row_prefix,
    write_binary_header,
    write_raster,
    write_row_prefix,
)
from aresys_io.product.metadata.elements import RasterInfo

__all__ = [
    "MemmappedNDArray",
    "read_binary_header_with_raster_info",
    "read_raster_as_memmap_with_raster_info",
    "read_raster_with_raster_info",
    "read_row_prefix_with_raster_info",
    "retrieve_data_layout",
    "write_binary_header_with_raster_info",
    "write_raster_with_raster_info",
    "write_row_prefix_with_raster_info",
]


def retrieve_data_layout(raster_info: RasterInfo) -> DataLayout:
    """Retrieve the data layout from a RasterInfo object.

    Parameters
    ----------
    raster_info : metadata.RasterInfo
        RasterInfo metadata corresponding to the raster to be read

    Returns
    -------
    DataLayout
        Unified layout and format information for the raster

    Raises
    ------
    ValueError
        If the raster info cell type is 'custom', which is not supported for reading raster files
    """
    if raster_info.cell_type == "CUSTOM":
        msg = "Custom data type is not supported for reading raster files."
        raise ValueError(msg)

    return DataLayout(
        data_type=raster_info.cell_type,
        endianness=raster_info.byte_order,
        num_of_samples=raster_info.samples,
        num_of_lines=raster_info.lines,
        header_offset=raster_info.header_offset_bytes,
        row_prefix=raster_info.row_prefix_bytes,
    )


def read_raster_with_raster_info(
    raster_file: str | Path,
    raster_info: RasterInfo,
    block_to_read: list[int] | None = None,
) -> npt.NDArray:
    """Read raster file using information from a RasterInfo metadata object.

    Parameters
    ----------
    raster_file : str | Path
        path to the raster file to be read
    raster_info : metadata.RasterInfo
        RasterInfo metadata corresponding to the raster to be read
    block_to_read : list[int], optional
        data block to be read, to be specified as a list of 4 integers, in the form:
            0. first line to be read
            1. first sample to be read
            2. total number of lines to be read
            3. total number of samples to be read.

        if None, the whole raster is read, by default None

    Returns
    -------
    npt.NDArray
        numpy array containing the data read from raster file, with shape (lines, samples)

    """
    raster_file = Path(raster_file)

    if raster_file.name != raster_info.file_name:
        msg = (
            f"Raster file name {raster_file.name} differs "
            f"from raster info file name {raster_info.file_name}"
        )
        warnings.warn(msg, stacklevel=2)

    data_layout = retrieve_data_layout(raster_info)

    return read_raster(
        raster_file_name=raster_file,
        data_layout=data_layout,
        block_to_read=block_to_read,
    )


MemmappedNDArray: TypeAlias = npt.NDArray


@contextmanager
def read_raster_as_memmap_with_raster_info(
    raster_file: str | Path,
    raster_info: RasterInfo,
) -> Generator[MemmappedNDArray, None, None]:
    """Create and manage the lifecycle of a read-only memmap to a raster file.

    Usage
    -----
    with read_raster_as_memmap_with_raster_info(...) as data_as_memmap:
        ...

    Parameters
    ----------
    raster_file : str | Path
        path to the raster file to be read
    raster_info : metadata.RasterInfo
        RasterInfo metadata corresponding to the raster to be read

    Yields
    ------
    MemmappedNDArray (alias to np.ndarray)
        Memory-mapped numpy array containing raster data of shape (lines, samples)

    """
    raster_file = Path(raster_file)

    if raster_file.name != raster_info.file_name:
        msg = (
            f"Raster file name {raster_file.name} differs "
            f"from raster info file name {raster_info.file_name}"
        )
        warnings.warn(
            msg,
            stacklevel=2,
        )

    data_layout = retrieve_data_layout(raster_info)

    with read_raster_as_memmap(
        raster_file_name=raster_file,
        data_layout=data_layout,
    ) as data_as_memmap:
        yield data_as_memmap


def write_raster_with_raster_info(
    raster_file: str | Path,
    data: npt.NDArray,
    raster_info: RasterInfo,
    write_offset: tuple[int, int] = (0, 0),
) -> None:
    """Write data to the specified raster file on disk.

    Parameters
    ----------
    raster_file : str | Path
        path to the raster file to be written
    data : npt.NDArray
        data to be written
    raster_info : metadata.RasterInfo
        RasterInfo object containing all the info related to the raster of choice
    write_offset : tuple[int, int], optional
        start point from where to write (lines, samples), by default (0, 0).

    """
    raster_file = Path(raster_file)

    if raster_file.name != raster_info.file_name:
        msg = (
            f"Raster file name {raster_file.name} differs "
            f"from raster info file name {raster_info.file_name}"
        )
        warnings.warn(msg, stacklevel=2)

    data_layout = retrieve_data_layout(raster_info)

    write_raster(
        raster_file_name=raster_file,
        data=data,
        data_layout=data_layout,
        writing_offset=write_offset,
    )


def read_binary_header_with_raster_info(raster_file: str | Path, raster_info: RasterInfo) -> bytes:
    """Read raster binary header using information from a RasterInfo metadata object.

    Parameters
    ----------
    raster_file : str | Path
        path to the raster file to be read
    raster_info : metadata.RasterInfo
        RasterInfo metadata corresponding to the raster to be read.

    Returns
    -------
    bytes
        header binary of the raster file
    """
    return read_binary_header(raster_file=raster_file, header_size=raster_info.header_offset_bytes)


def write_binary_header_with_raster_info(
    raster_file: str | Path,
    header: bytes,
    raster_info: RasterInfo,
) -> None:
    """Write raster binary header using information from a RasterInfo metadata object.

    Parameters
    ----------
    raster_file : str | Path
        path to the raster file to be read
    header : bytes
        header to be written in bytes
    raster_info : metadata.RasterInfo
        RasterInfo metadata corresponding to the raster to be read.

    """
    write_binary_header(
        raster_file=raster_file,
        header=header,
        header_size=raster_info.header_offset_bytes,
    )


def read_row_prefix_with_raster_info(
    raster_file: str | Path,
    line_interval: tuple[int, int],
    raster_info: RasterInfo,
) -> list[bytes]:
    """Read the row prefix of a given line using information from a RasterInfo metadata object.

    Parameters
    ----------
    raster_file : str | Path
        path to the raster file to be read
    line_interval : tuple[int, int]
        raster line interval as (start_line, end_line), with end excluded
    raster_info : metadata.RasterInfo
        RasterInfo metadata corresponding to the raster to be read.

    Returns
    -------
    list[bytes]
        row prefixes as byte sequences
    """
    data_layout = retrieve_data_layout(raster_info)

    return read_row_prefix(
        raster_file=raster_file,
        line_interval=line_interval,
        data_layout=data_layout,
    )


def write_row_prefix_with_raster_info(
    raster_file: str | Path,
    line_interval: tuple[int, int],
    row_prefix: list[bytes],
    raster_info: RasterInfo,
) -> None:
    """Write the row prefix at a given line using information from a RasterInfo metadata object.

    Parameters
    ----------
    raster_file : str | Path
        path to the raster file to be read
    line_interval : tuple[int, int]
        raster line interval as (start_line, end_line), with end excluded
    row_prefix : list[bytes]
        row prefixes as byte sequences, one for each line in interval
    raster_info : metadata.RasterInfo
        RasterInfo metadata corresponding to the raster to be read.

    """
    data_layout = retrieve_data_layout(raster_info)

    write_row_prefix(
        raster_file=raster_file,
        line_interval=line_interval,
        row_prefix=row_prefix,
        data_layout=data_layout,
    )
