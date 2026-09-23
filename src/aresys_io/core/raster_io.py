# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Raster input output module."""

import mmap
from collections.abc import Generator, Sequence
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, Literal, SupportsInt, TypeAlias

import numpy as np
import numpy.typing as npt

__all__ = [
    "DataLayout",
    "read_binary_header",
    "read_raster",
    "read_raster_as_memmap",
    "read_row_prefix",
    "write_binary_header",
    "write_raster",
    "write_row_prefix",
]

SupportedSampleType: TypeAlias = Literal[
    "INT8",
    "UINT8",
    "INT16",
    "UINT16",
    "INT32",
    "UINT32",
    "FLOAT32",
    "FLOAT64",
    "INT8_COMPLEX",
    "INT16_COMPLEX",
    "INT_COMPLEX",
    "FLOAT_COMPLEX",
    "DOUBLE_COMPLEX",
]


Endianness: TypeAlias = Literal["BIGENDIAN", "LITTLEENDIAN"]


MemmappedNDArray: TypeAlias = np.ndarray


@dataclass(frozen=True)
class DataLayout:
    """Data layout and format information.

    Parameters
    ----------
    data_type : SupportedSampleType
        The data type of the raster file.
        Available types:
            - "INT8"
            - "UINT8"
            - "INT16"
            - "UINT16"
            - "INT32"
            - "UINT32"
            - "FLOAT32"
            - "FLOAT64"
            - "INT8_COMPLEX"
            - "INT16_COMPLEX"
            - "INT_COMPLEX"
            - "FLOAT_COMPLEX"
            - "DOUBLE_COMPLEX"
    endianness : ENDIANNESS
        The endianness of the raster file.
        Available types:
            - "BIGENDIAN"
            - "LITTLEENDIAN"
    num_of_samples : int
        Number of samples (columns) in the raster.
    num_of_lines : int
        Number of lines (rows) in the raster.
    header_offset : int, optional
        Size of the file header in bytes, by default 0.
    row_prefix : int, optional
        Size of the row prefix in bytes, by default 0.

    """

    data_type: SupportedSampleType
    endianness: Endianness
    num_of_samples: int
    num_of_lines: int
    header_offset: int = 0
    row_prefix: int = 0

    data_type_dict: ClassVar[dict[SupportedSampleType, str]] = {
        "FLOAT32": "f4",
        "FLOAT_COMPLEX": "c8",
        "INT16": "i2",
        "INT32": "i4",
        "UINT16": "u2",
        "UINT32": "u4",
        "INT8": "b",
        "UINT8": "B",
        "INT16_COMPLEX": "i2, i2",
        "INT_COMPLEX": "i4, i4",
        "DOUBLE_COMPLEX": "c16",
        "FLOAT64": "f8",
        "INT8_COMPLEX": "i1, i1",
    }
    endianness_mapping: ClassVar[dict[Endianness, str]] = {"BIGENDIAN": ">", "LITTLEENDIAN": "<"}

    def __post_init__(self) -> None:
        """Post init validation to ensure all values are valid and non-negative."""
        if self.data_type not in self.data_type_dict:
            msg = f"Unknown data type id: {self.data_type}"
            raise ValueError(msg)

        if self.endianness not in self.endianness_mapping:
            msg = f"Unknown data endianness: {self.endianness}"
            raise ValueError(msg)

        if self.num_of_samples <= 0:
            msg = "num_of_samples should be positive"
            raise ValueError(msg)
        if self.num_of_lines <= 0:
            msg = "num_of_lines should be positive"
            raise ValueError(msg)
        if self.header_offset < 0:
            msg = "header_offset should be non-negative"
            raise ValueError(msg)
        if self.row_prefix < 0:
            msg = "row_prefix should be non-negative"
            raise ValueError(msg)

    @property
    def dtype(self) -> np.dtype:
        """The numpy dtype corresponding to the data format."""
        return np.dtype(
            self.endianness_mapping[self.endianness] + self.data_type_dict[self.data_type],
        )

    def start_line_offset(self, line_index: int) -> int:
        """Compute the starting byte offset of a given line in the raster.

        Parameters
        ----------
        line_index : int
            Index of the line (0-based). Note: can be num_of_lines to compute
            the total file size.

        Returns
        -------
        int
            Starting byte offset of the specified line in the raster.
        """
        line_size = self.num_of_samples * self.dtype.itemsize + self.row_prefix
        return self.header_offset + line_index * line_size

    def raster_total_size(self) -> int:
        """Compute the total size in bytes of the raster file.

        Returns
        -------
        int
            Total size in bytes including header and all lines.
        """
        return self.start_line_offset(self.num_of_lines)

    def normalize_read_block(
        self,
        block_to_read: Sequence[SupportsInt] | None,
    ) -> tuple[int, int, int, int]:
        """Normalize and validate a read block definition.

        Parameters
        ----------
        block_to_read : Sequence[SupportsInt] | None
            Read block as [first_line, first_sample, lines_to_read, samples_to_read].
            If None, the whole raster dimensions are returned.

        Returns
        -------
        int
            First line of the block to read.
        int
            First sample of the block to read.
        int
            Number of lines to read.
        int
            Number of samples to read.

        Raises
        ------
        RuntimeError
            If the block is malformed or exceeds raster bounds.
        """
        if block_to_read is None:
            first_line = 0
            first_sample = 0

            lines_to_read = self.num_of_lines
            samples_to_read = self.num_of_samples
        else:
            if len(block_to_read) != 4:
                msg = "Block to read should have 4 elements"
                raise RuntimeError(msg)

            try:
                first_line = int(block_to_read[0])
                first_sample = int(block_to_read[1])
                lines_to_read = int(block_to_read[2])
                samples_to_read = int(block_to_read[3])
            except (TypeError, ValueError) as exc:
                msg = "Block to read elements should be integer-convertible"
                raise RuntimeError(msg) from exc

        if first_line < 0:
            msg = "First line to read should be non-negative"
            raise RuntimeError(msg)

        if first_sample < 0:
            msg = "First sample to read should be non-negative"
            raise RuntimeError(msg)

        if lines_to_read < 0:
            msg = "Number of lines to read should be non-negative"
            raise RuntimeError(msg)

        if samples_to_read < 0:
            msg = "Number of samples to read should be non-negative"
            raise RuntimeError(msg)

        if first_line + lines_to_read > self.num_of_lines:
            msg = "Block to read exceeds max num lines"
            raise RuntimeError(msg)

        if first_sample + samples_to_read > self.num_of_samples:
            msg = "Block to read exceeds max num samples"
            raise RuntimeError(msg)

        return first_line, first_sample, lines_to_read, samples_to_read


def read_raster(
    raster_file_name: str | Path,
    data_layout: DataLayout,
    block_to_read: Sequence[SupportsInt] | None = None,
) -> npt.NDArray:
    """Read raster file data.

    Parameters
    ----------
    raster_file_name : str | Path
        path to the raster file to be read
    data_layout : DataLayout
        layout and format information for the raster
    block_to_read : Sequence[SupportsInt] | None, optional
        data block to be read, to be specified as a sequence of 4 integers, in the form:
            0. first line to be read
            1. first sample to be read
            2. total number of lines to be read
            3. total number of samples to be read.

        if None, the whole raster is read. If lines or samples to read is 0,
        returns an empty array of shape (0, samples) or (lines, 0), by default None

    Returns
    -------
    npt.NDArray
        numpy array containing the data read from raster file, with shape (lines, samples)

    """
    first_line, first_sample, lines_to_read, samples_to_read = data_layout.normalize_read_block(
        block_to_read,
    )

    dtype = data_layout.dtype
    with Path(raster_file_name).open("rb") as fdesc:
        if samples_to_read == data_layout.num_of_samples and data_layout.row_prefix == 0:
            offset_byte = data_layout.start_line_offset(first_line)
            data = np.fromfile(
                fdesc,
                dtype=dtype,
                count=lines_to_read * samples_to_read,
                offset=offset_byte,
            )

            return data.reshape((lines_to_read, samples_to_read))

        data = np.empty((lines_to_read, samples_to_read), dtype=dtype)

        first_line_offset = data_layout.start_line_offset(first_line)
        offset_byte = first_line_offset + data_layout.row_prefix + first_sample * dtype.itemsize
        fdesc.seek(offset_byte, 0)

        offset_line_byte = (
            data_layout.num_of_samples - samples_to_read
        ) * dtype.itemsize + data_layout.row_prefix

        for line in range(lines_to_read):
            offset_byte = offset_line_byte if line > 0 else 0
            data[line, :] = np.fromfile(
                fdesc,
                dtype=dtype,
                count=samples_to_read,
                offset=offset_byte,
            )

        return data


@contextmanager
def read_raster_as_memmap(
    raster_file_name: str | Path,
    data_layout: DataLayout,
) -> Generator[MemmappedNDArray]:
    """Read raster file data as memmap by yielding a lifecycle-managed np.memmap.

    Usage
    -----
    with read_raster_as_memmap(...) as data_as_memmap:
        ...

    Parameters
    ----------
    raster_file_name : str | Path
        path to the raster file to be read
    data_layout : DataLayout
        layout and format information for the raster

    Yields
    ------
    MemmappedNDArray (alias to np.ndarray)
        Memory-mapped numpy array containing raster data of shape (lines, samples)

    Raises
    ------
    NotImplementedError
        if row_prefix is larger than zero, as numpy memmaps do not support row prefixes

    """
    if data_layout.row_prefix > 0:
        msg = "Non-null row prefix is not supported in memmap read."
        raise NotImplementedError(msg)

    dtype = data_layout.dtype

    memmap_shape = (data_layout.num_of_lines, data_layout.num_of_samples)

    with (
        Path(raster_file_name).open("rb") as f,
        mmap.mmap(
            f.fileno(),
            length=0,
            access=mmap.ACCESS_READ,
        ) as memmap_obj,
    ):
        yield np.ndarray(
            memmap_shape,
            dtype=dtype,
            offset=data_layout.header_offset,
            buffer=memmap_obj,
        )


def write_raster(
    raster_file_name: str | Path,
    data: npt.NDArray,
    data_layout: DataLayout,
    writing_offset: tuple[int, int] = (0, 0),
) -> None:
    """Write raster file to disk.

    Parameters
    ----------
    raster_file_name : str | Path
        path to the raster file to be read
    data : npt.NDArray
        data to be written
    data_layout : DataLayout
        layout and format information for the raster
    writing_offset : tuple[int, int], optional
        line and sample from where to start writing data, by default (0, 0)

    Raises
    ------
    ValueError
        if writing_offset is not a tuple of two non-negative integers
    RuntimeError
        if the final raster size does not match the expected size after writing

    """
    if len(writing_offset) != 2 or writing_offset[0] < 0 or writing_offset[1] < 0:
        msg = "Writing point should have two non-negative elements"
        raise ValueError(msg)

    # Convert data to data type
    dtype = data_layout.dtype
    data_to_write = np.array(data, dtype=dtype)

    first_line, first_sample = writing_offset
    lines_to_write, samples_to_write = data_to_write.shape

    if first_sample + samples_to_write > data_layout.num_of_samples:
        msg = "Input data exceeds max num samples"
        raise ValueError(msg)

    if first_line + lines_to_write > data_layout.num_of_lines:
        msg = "Input data exceeds max num lines"
        raise ValueError(msg)

    open_mode = "r+b" if Path(raster_file_name).is_file() else "wb"

    with Path(raster_file_name).open(open_mode) as fdesc:
        raster_size = data_layout.raster_total_size()

        # Ensure file is large enough to hold the entire raster
        fdesc.seek(0, 2)
        current_size = fdesc.tell()
        if current_size < raster_size:
            last_element_position = raster_size - dtype.itemsize
            fdesc.seek(last_element_position)
            fdesc.write(np.array(0, dtype=dtype).tobytes())

        # Write data to the file
        for line in range(lines_to_write):
            write_sample_offset = (
                data_layout.start_line_offset(first_line + line)
                + data_layout.row_prefix
                + first_sample * dtype.itemsize
            )
            fdesc.seek(write_sample_offset)
            fdesc.write(data_to_write[line].tobytes())

        # Verify final file size matches expected raster size
        fdesc.seek(0, 2)
        final_size = fdesc.tell()
        # In normal single-process I/O flow this should not happen; a mismatch here
        # usually indicates external file interference or filesystem-level anomalies.
        if final_size != raster_size:
            msg = (
                f"Final raster size mismatch: expected {raster_size} bytes, got {final_size} bytes"
            )
            raise RuntimeError(msg)


def read_binary_header(raster_file: str | Path, header_size: int) -> bytes:
    """Read raster binary header using information from a RasterInfo metadata object.

    Parameters
    ----------
    raster_file : str | Path
        path to the raster file to be read
    header_size : int
        size of the header in bytes

    Returns
    -------
    bytes
        header binary of the raster file
    """
    raster_file = Path(raster_file)

    if header_size == 0:
        return b""

    with raster_file.open("rb") as file:
        return file.read(header_size)


def write_binary_header(raster_file: str | Path, header: bytes, header_size: int) -> None:
    """Write raster binary header using information from a RasterInfo metadata object.

    Parameters
    ----------
    raster_file : str | Path
        path to the raster file to be read
    header : bytes
        header to be written in bytes
    header_size : int
        size of the header in bytes

    Raises
    ------
    ValueError
        if header_size is negative
    RuntimeError
        if the header size is incompatible with the header offset in the raster info
    """
    raster_file = Path(raster_file)

    if header_size < 0:
        msg = "Header size should be non-negative"
        raise ValueError(msg)

    if header_size != len(header):
        msg = f"Header size incompatible with header offset: {len(header)} != {header_size}"
        raise RuntimeError(msg)

    open_mode = "r+b" if Path(raster_file).is_file() else "wb"
    with Path(raster_file).open(open_mode) as file:
        file.write(header)


def read_row_prefix(
    raster_file: str | Path,
    line_interval: tuple[int, int],
    data_layout: DataLayout,
) -> list[bytes]:
    """Read the row prefix of a given line.

    Parameters
    ----------
    raster_file : str | Path
        path to the raster file to be read
    line_interval : tuple[int, int]
        raster line interval as (start_line, end_line), with end excluded
    data_layout : DataLayout
        layout and format information for the raster

    Returns
    -------
    list[bytes]
        row prefixes as byte sequences for all lines in interval

    Raises
    ------
    RuntimeError
        if the line interval is malformed or exceeds raster bounds
    """
    start_line, end_line = line_interval
    if start_line < 0 or end_line < 0:
        msg = "Line interval should be non-negative"
        raise RuntimeError(msg)
    if start_line > end_line:
        msg = "Line interval start should be <= end"
        raise RuntimeError(msg)
    if end_line > data_layout.num_of_lines:
        msg = "Line interval exceeds max num lines"
        raise RuntimeError(msg)

    raster_file = Path(raster_file)

    if data_layout.row_prefix == 0:
        return [b""] * (end_line - start_line)

    with raster_file.open("rb") as file:
        prefixes: list[bytes] = []
        for line_index in range(start_line, end_line):
            offset_byte = data_layout.start_line_offset(line_index)
            file.seek(offset_byte)
            prefixes.append(file.read(data_layout.row_prefix))
        return prefixes


def write_row_prefix(
    raster_file: str | Path,
    line_interval: tuple[int, int],
    row_prefix: list[bytes],
    data_layout: DataLayout,
) -> None:
    """Write the row prefix at a given line.

    Parameters
    ----------
    raster_file : str | Path
        path to the raster file to be read
    line_interval : tuple[int, int]
        raster line interval as (start_line, end_line), with end excluded
    row_prefix : list[bytes]
        row prefixes as byte sequences, one for each line in interval
    data_layout : DataLayout
        layout and format information for the raster

    Raises
    ------
    RuntimeError
        if row_prefix length is incompatible with line interval length or
        if any row prefix size is incompatible with the specified row prefix size
    """
    raster_file = Path(raster_file)
    start_line, end_line = line_interval
    if start_line < 0 or end_line < 0:
        msg = "Line interval should be non-negative"
        raise RuntimeError(msg)
    if start_line > end_line:
        msg = "Line interval start should be <= end"
        raise RuntimeError(msg)
    if end_line > data_layout.num_of_lines:
        msg = "Line interval exceeds max num lines"
        raise RuntimeError(msg)

    expected_line_count = end_line - start_line
    if len(row_prefix) != expected_line_count:
        msg = (
            "Row prefix list length incompatible with line interval length:"
            f"{len(row_prefix)} != {expected_line_count}"
        )
        raise RuntimeError(msg)

    for current_row_prefix in row_prefix:
        if len(current_row_prefix) != data_layout.row_prefix:
            msg = (
                "Row prefix size incompatible with specified row prefix size:"
                f"{len(current_row_prefix)} != {data_layout.row_prefix}"
            )
            raise RuntimeError(msg)

    open_mode = "r+b" if raster_file.is_file() else "wb"
    with raster_file.open(open_mode) as file:
        for line_index, current_row_prefix in zip(
            range(start_line, end_line),
            row_prefix,
            strict=True,
        ):
            offset_byte = data_layout.start_line_offset(line_index)
            file.seek(offset_byte)
            file.write(current_row_prefix)
