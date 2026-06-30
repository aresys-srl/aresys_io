# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Unit tests for aresys_io.core.raster_io."""

from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np
import pytest

from aresys_io.core.raster_io import (
    DataLayout,
    Endianness,
    SupportedSampleType,
    read_binary_header,
    read_raster,
    read_raster_as_memmap,
    read_row_prefix,
    write_binary_header,
    write_raster,
    write_row_prefix,
)


def test_write_raster() -> None:
    layout = DataLayout(
        data_type="FLOAT32",
        endianness="LITTLEENDIAN",
        num_of_lines=12,
        num_of_samples=9,
        header_offset=16,
        row_prefix=4,
    )
    data = (
        np.arange(layout.num_of_lines * layout.num_of_samples, dtype=np.float32).reshape(
            (layout.num_of_lines, layout.num_of_samples),
        )
        + 1.0
    )

    with TemporaryDirectory() as tmpdir:
        raster_file = Path(tmpdir) / "GRD_0001"
        assert not raster_file.exists()

        write_raster(
            raster_file_name=raster_file,
            data=data,
            data_layout=layout,
        )

        assert raster_file.exists()
        assert raster_file.is_file()


def test_write_raster_on_existing_full_file_keeps_size() -> None:
    layout = DataLayout(
        data_type="FLOAT32",
        endianness="LITTLEENDIAN",
        num_of_lines=4,
        num_of_samples=5,
        header_offset=16,
        row_prefix=4,
    )
    full_data = np.arange(20, dtype=np.float32).reshape((4, 5)) + 1.0
    patch_data = np.array([[101.0, 102.0]], dtype=np.float32)

    with TemporaryDirectory() as tmpdir:
        raster_file = Path(tmpdir) / "existing_full.bin"

        write_raster(raster_file_name=raster_file, data=full_data, data_layout=layout)
        size_before = raster_file.stat().st_size

        write_raster(
            raster_file_name=raster_file,
            data=patch_data,
            data_layout=layout,
            writing_offset=(2, 1),
        )

        size_after = raster_file.stat().st_size
        read_back = read_raster(raster_file_name=raster_file, data_layout=layout)

        expected = full_data.copy()
        expected[2, 1:3] = patch_data[0]

        assert size_after == size_before
        np.testing.assert_array_equal(read_back, expected)


@pytest.mark.parametrize(
    ("header_offset", "row_prefix"),
    [
        (0, 0),
        (16, 0),
        (0, 4),
        (16, 4),
    ],
    ids=[
        "no_header_no_prefix",
        "header_only",
        "row_prefix_only",
        "header_and_row_prefix",
    ],
)
@pytest.mark.parametrize(
    ("writing_offset", "block_shape"),
    [
        ((0, 0), (2, 3)),
        ((3, 4), (2, 3)),
        ((6, 7), (2, 3)),
    ],
    ids=["block_at_start", "block_in_middle", "block_at_end"],
)
def test_write_raster_block_positions(
    header_offset: int,
    row_prefix: int,
    writing_offset: tuple[int, int],
    block_shape: tuple[int, int],
) -> None:
    layout = DataLayout(
        data_type="FLOAT32",
        endianness="LITTLEENDIAN",
        num_of_lines=8,
        num_of_samples=10,
        header_offset=header_offset,
        row_prefix=row_prefix,
    )

    block_lines, block_samples = block_shape
    block_data = (
        np.arange(block_lines * block_samples, dtype=np.float32).reshape(block_shape) + 1.0
    )

    with TemporaryDirectory() as tmpdir:
        raster_file = Path(tmpdir) / "GRD_0001"

        write_raster(
            raster_file_name=raster_file,
            data=block_data,
            data_layout=layout,
            writing_offset=writing_offset,
        )

        read = read_raster(
            raster_file_name=raster_file,
            data_layout=layout,
        )

        expected = np.zeros((layout.num_of_lines, layout.num_of_samples), dtype=np.float32)
        start_line, start_sample = writing_offset
        expected[
            start_line : start_line + block_lines,
            start_sample : start_sample + block_samples,
        ] = block_data

        np.testing.assert_array_equal(read, expected)


@pytest.mark.parametrize(
    ("header_offset", "row_prefix"),
    [
        (0, 0),
        (16, 0),
        (0, 4),
        (16, 4),
    ],
    ids=[
        "no_header_no_prefix",
        "header_only",
        "row_prefix_only",
        "header_and_row_prefix",
    ],
)
@pytest.mark.parametrize(
    ("block_to_read", "slice_rows", "slice_cols"),
    [
        ([0, 0, 2, 3], slice(0, 2), slice(0, 3)),
        ([3, 4, 2, 3], slice(3, 5), slice(4, 7)),
        ([6, 7, 2, 3], slice(6, 8), slice(7, 10)),
    ],
    ids=["block_at_start", "block_in_middle", "block_at_end"],
)
def test_read_raster_block_positions(
    header_offset: int,
    row_prefix: int,
    block_to_read: list[int],
    slice_rows: slice,
    slice_cols: slice,
) -> None:
    layout = DataLayout(
        data_type="FLOAT32",
        endianness="LITTLEENDIAN",
        num_of_lines=8,
        num_of_samples=10,
        header_offset=header_offset,
        row_prefix=row_prefix,
    )
    data = (
        np.arange(layout.num_of_lines * layout.num_of_samples, dtype=np.float32).reshape(
            (layout.num_of_lines, layout.num_of_samples),
        )
        + 1.0
    )

    with TemporaryDirectory() as tmpdir:
        raster_file = Path(tmpdir) / "GRD_0001"

        write_raster(
            raster_file_name=raster_file,
            data=data,
            data_layout=layout,
        )
        read = read_raster(
            raster_file_name=raster_file,
            data_layout=layout,
            block_to_read=block_to_read,
        )

        expected = data[slice_rows, slice_cols]
        np.testing.assert_array_equal(read, expected)


@pytest.mark.parametrize(
    ("header_offset", "row_prefix"),
    [
        (0, 0),
        (16, 0),
        (0, 4),
        (16, 4),
    ],
    ids=[
        "no_header_no_prefix",
        "header_only",
        "row_prefix_only",
        "header_and_row_prefix",
    ],
)
def test_read_binary_header(header_offset: int, row_prefix: int) -> None:
    layout = DataLayout(
        data_type="FLOAT32",
        endianness="LITTLEENDIAN",
        num_of_lines=12,
        num_of_samples=9,
        header_offset=header_offset,
        row_prefix=row_prefix,
    )
    data = np.zeros((layout.num_of_lines, layout.num_of_samples), dtype=np.float32)

    with TemporaryDirectory() as tmpdir:
        raster_file = Path(tmpdir) / "GRD_0001"

        write_raster(
            raster_file_name=raster_file,
            data=data,
            data_layout=layout,
        )
        header = bytes((i + 1) % 256 for i in range(layout.header_offset))
        write_binary_header(
            raster_file=raster_file,
            header=header,
            header_size=layout.header_offset,
        )
        read = read_binary_header(
            raster_file=raster_file,
            header_size=layout.header_offset,
        )

        assert read == header


def test_write_binary_header() -> None:
    layout = DataLayout(
        data_type="FLOAT32",
        endianness="LITTLEENDIAN",
        num_of_lines=12,
        num_of_samples=9,
        header_offset=16,
        row_prefix=4,
    )
    data = (
        np.arange(layout.num_of_lines * layout.num_of_samples, dtype=np.float32).reshape(
            (layout.num_of_lines, layout.num_of_samples),
        )
        + 1.0
    )

    with TemporaryDirectory() as tmpdir:
        raster_file = Path(tmpdir) / "GRD_0001"

        write_raster(
            raster_file_name=raster_file,
            data=data,
            data_layout=layout,
        )

        file_size_before = raster_file.stat().st_size
        header = bytes((255 - i) % 256 for i in range(layout.header_offset))

        write_binary_header(
            raster_file=raster_file,
            header=header,
            header_size=layout.header_offset,
        )

        read_header = read_binary_header(
            raster_file=raster_file,
            header_size=layout.header_offset,
        )
        read_payload = read_raster(
            raster_file_name=raster_file,
            data_layout=layout,
        )
        file_size_after = raster_file.stat().st_size

        assert read_header == header
        np.testing.assert_array_equal(read_payload, data)
        assert file_size_after == file_size_before


def test_write_binary_header_error() -> None:
    layout = DataLayout(
        data_type="FLOAT32",
        endianness="LITTLEENDIAN",
        num_of_lines=12,
        num_of_samples=9,
        header_offset=16,
        row_prefix=4,
    )
    data = (
        np.arange(layout.num_of_lines * layout.num_of_samples, dtype=np.float32).reshape(
            (layout.num_of_lines, layout.num_of_samples),
        )
        + 1.0
    )

    with TemporaryDirectory() as tmpdir:
        raster_file = Path(tmpdir) / "GRD_0001"

        write_raster(
            raster_file_name=raster_file,
            data=data,
            data_layout=layout,
        )

        with pytest.raises(RuntimeError):
            write_binary_header(
                raster_file=raster_file,
                header=bytes(layout.header_offset + 1),
                header_size=layout.header_offset,
            )


@pytest.mark.parametrize(
    ("header_offset", "row_prefix"),
    [
        (16, 4),
        (0, 4),
        (16, 0),
        (0, 0),
    ],
    ids=[
        "header_and_prefix",
        "no_header_with_prefix",
        "header_no_prefix",
        "no_header_no_prefix",
    ],
)
def test_read_row_prefix_interval(header_offset: int, row_prefix: int) -> None:
    layout = DataLayout(
        data_type="FLOAT32",
        endianness="LITTLEENDIAN",
        num_of_lines=12,
        num_of_samples=9,
        header_offset=header_offset,
        row_prefix=row_prefix,
    )
    data = np.zeros((layout.num_of_lines, layout.num_of_samples), dtype=np.float32)

    with TemporaryDirectory() as tmpdir:
        raster_file = Path(tmpdir) / "GRD_0001"

        write_raster(
            raster_file_name=raster_file,
            data=data,
            data_layout=layout,
        )
        read = read_row_prefix(
            raster_file=raster_file,
            line_interval=(3, 5),
            data_layout=layout,
        )

        assert read == [bytes(layout.row_prefix), bytes(layout.row_prefix)]


@pytest.mark.parametrize(
    ("header_offset", "row_prefix", "row_prefix_to_write"),
    [
        (16, 4, [b"ABCD", b"WXYZ"]),
        (0, 4, [b"ABCD", b"WXYZ"]),
        (16, 0, [b"", b""]),
        (0, 0, [b"", b""]),
    ],
    ids=[
        "header_and_prefix",
        "no_header_with_prefix",
        "header_no_prefix",
        "no_header_no_prefix",
    ],
)
def test_write_row_prefix_interval(
    header_offset: int,
    row_prefix: int,
    row_prefix_to_write: list[bytes],
) -> None:
    layout = DataLayout(
        data_type="FLOAT32",
        endianness="LITTLEENDIAN",
        num_of_lines=12,
        num_of_samples=9,
        header_offset=header_offset,
        row_prefix=row_prefix,
    )
    data = np.zeros((layout.num_of_lines, layout.num_of_samples), dtype=np.float32)

    with TemporaryDirectory() as tmpdir:
        raster_file = Path(tmpdir) / "GRD_0001"

        write_raster(
            raster_file_name=raster_file,
            data=data,
            data_layout=layout,
        )
        write_row_prefix(
            raster_file=raster_file,
            line_interval=(3, 5),
            row_prefix=row_prefix_to_write,
            data_layout=layout,
        )
        read = read_row_prefix(
            raster_file=raster_file,
            line_interval=(3, 5),
            data_layout=layout,
        )

        assert read == row_prefix_to_write


def test_write_row_prefix_error() -> None:
    layout = DataLayout(
        data_type="FLOAT32",
        endianness="LITTLEENDIAN",
        num_of_lines=12,
        num_of_samples=9,
        header_offset=16,
        row_prefix=4,
    )
    data = np.zeros((layout.num_of_lines, layout.num_of_samples), dtype=np.float32)

    with TemporaryDirectory() as tmpdir:
        raster_file = Path(tmpdir) / "GRD_0001"

        write_raster(
            raster_file_name=raster_file,
            data=data,
            data_layout=layout,
        )

        with pytest.raises(RuntimeError):
            write_row_prefix(
                raster_file=raster_file,
                line_interval=(3, 4),
                row_prefix=[b"ABCDE"],
                data_layout=layout,
            )


def test_write_row_prefix_interval_length_error() -> None:
    layout = DataLayout(
        data_type="FLOAT32",
        endianness="LITTLEENDIAN",
        num_of_lines=12,
        num_of_samples=9,
        header_offset=16,
        row_prefix=4,
    )
    data = np.zeros((layout.num_of_lines, layout.num_of_samples), dtype=np.float32)

    with TemporaryDirectory() as tmpdir:
        raster_file = Path(tmpdir) / "GRD_0001"

        write_raster(
            raster_file_name=raster_file,
            data=data,
            data_layout=layout,
        )

        with pytest.raises(RuntimeError):
            write_row_prefix(
                raster_file=raster_file,
                line_interval=(3, 5),
                row_prefix=[b"ABCD"],
                data_layout=layout,
            )


@pytest.mark.parametrize(
    ("layout_args", "error_match"),
    [
        (
            ("NOT_A_TYPE", "LITTLEENDIAN", 2, 2, 0, 0),
            "Unknown data type id",
        ),
        (
            ("FLOAT32", "NOT_ENDIAN", 2, 2, 0, 0),
            "Unknown data endianness",
        ),
        (
            ("FLOAT32", "LITTLEENDIAN", 2, 0, 0, 0),
            "num_of_samples should be positive",
        ),
        (
            ("FLOAT32", "LITTLEENDIAN", 0, 2, 0, 0),
            "num_of_lines should be positive",
        ),
        (
            ("FLOAT32", "LITTLEENDIAN", 2, 2, -1, 0),
            "header_offset should be non-negative",
        ),
        (
            ("FLOAT32", "LITTLEENDIAN", 2, 2, 0, -1),
            "row_prefix should be non-negative",
        ),
    ],
)
def test_data_layout_validation_errors(
    layout_args: tuple[SupportedSampleType, Endianness, int, int, int, int],
    error_match: str,
) -> None:
    data_type, endianness, num_of_lines, num_of_samples, header_offset, row_prefix = layout_args

    with pytest.raises(ValueError, match=error_match):
        DataLayout(
            data_type=data_type,
            endianness=endianness,
            num_of_lines=num_of_lines,
            num_of_samples=num_of_samples,
            header_offset=header_offset,
            row_prefix=row_prefix,
        )


@pytest.mark.parametrize(
    "block_to_read",
    [
        [0, 0, 1],
        ["a", 0, 1, 1],
        [-1, 0, 1, 1],
        [0, -1, 1, 1],
        [0, 0, -1, 1],
        [0, 0, 1, -1],
        [10, 0, 1, 1],
        [0, 10, 1, 1],
    ],
)
def test_read_raster_block_validation_errors(block_to_read: list[int]) -> None:
    layout = DataLayout(
        data_type="FLOAT32",
        endianness="LITTLEENDIAN",
        num_of_lines=4,
        num_of_samples=4,
    )

    with pytest.raises(RuntimeError):
        read_raster(
            raster_file_name="dummy.bin",
            data_layout=layout,
            block_to_read=block_to_read,
        )


def test_read_raster_fast_path_no_row_prefix() -> None:
    layout = DataLayout(
        data_type="FLOAT32",
        endianness="LITTLEENDIAN",
        num_of_lines=4,
        num_of_samples=5,
        header_offset=0,
        row_prefix=0,
    )
    data = np.arange(20, dtype=np.float32).reshape((4, 5))

    with TemporaryDirectory() as tmpdir:
        raster_file = Path(tmpdir) / "fast_path.bin"
        write_raster(raster_file_name=raster_file, data=data, data_layout=layout)

        read = read_raster(raster_file_name=raster_file, data_layout=layout)
        np.testing.assert_array_equal(read, data)


def test_read_raster_as_memmap_success() -> None:
    layout = DataLayout(
        data_type="FLOAT32",
        endianness="LITTLEENDIAN",
        num_of_lines=3,
        num_of_samples=4,
        header_offset=8,
        row_prefix=0,
    )
    data = np.arange(12, dtype=np.float32).reshape((3, 4))

    with TemporaryDirectory() as tmpdir:
        raster_file = Path(tmpdir) / "memmap.bin"
        write_raster(raster_file_name=raster_file, data=data, data_layout=layout)
        write_binary_header(
            raster_file=raster_file,
            header=b"12345678",
            header_size=layout.header_offset,
        )

        with read_raster_as_memmap(raster_file_name=raster_file, data_layout=layout) as mapped:
            np.testing.assert_array_equal(mapped, data)


def test_read_raster_as_memmap_row_prefix_error() -> None:
    layout = DataLayout(
        data_type="FLOAT32",
        endianness="LITTLEENDIAN",
        num_of_lines=2,
        num_of_samples=2,
        row_prefix=4,
    )

    with (
        pytest.raises(NotImplementedError, match="Non-null row prefix is not supported"),
        read_raster_as_memmap(raster_file_name="dummy.bin", data_layout=layout),
    ):
        pass


def test_write_raster_invalid_writing_offset() -> None:
    layout = DataLayout(
        data_type="FLOAT32",
        endianness="LITTLEENDIAN",
        num_of_lines=3,
        num_of_samples=3,
    )
    data = np.ones((1, 1), dtype=np.float32)

    with TemporaryDirectory() as tmpdir:
        raster_file = Path(tmpdir) / "write_err.bin"
        with pytest.raises(
            ValueError,
            match="Writing point should have two non-negative elements",
        ):
            write_raster(
                raster_file_name=raster_file,
                data=data,
                data_layout=layout,
                writing_offset=(-1, 0),
            )


@pytest.mark.parametrize(
    ("writing_offset", "data_shape"),
    [
        ((0, 3), (1, 1)),
        ((3, 0), (1, 1)),
    ],
)
def test_write_raster_bounds_errors(
    writing_offset: tuple[int, int],
    data_shape: tuple[int, int],
) -> None:
    layout = DataLayout(
        data_type="FLOAT32",
        endianness="LITTLEENDIAN",
        num_of_lines=3,
        num_of_samples=3,
    )
    data = np.ones(data_shape, dtype=np.float32)

    with TemporaryDirectory() as tmpdir:
        raster_file = Path(tmpdir) / "write_bounds.bin"
        with pytest.raises(ValueError, match="Input data exceeds max num"):
            write_raster(
                raster_file_name=raster_file,
                data=data,
                data_layout=layout,
                writing_offset=writing_offset,
            )


def test_write_binary_header_negative_size_error() -> None:
    with pytest.raises(ValueError, match="Header size should be non-negative"):
        write_binary_header(
            raster_file="dummy.bin",
            header=b"",
            header_size=-1,
        )


@pytest.mark.parametrize("line_interval", [(-1, 1), (2, 1), (0, 13)])
def test_read_row_prefix_interval_errors(line_interval: tuple[int, int]) -> None:
    layout = DataLayout(
        data_type="FLOAT32",
        endianness="LITTLEENDIAN",
        num_of_lines=12,
        num_of_samples=9,
        header_offset=0,
        row_prefix=0,
    )

    with pytest.raises(RuntimeError):
        read_row_prefix(
            raster_file="dummy.bin",
            line_interval=line_interval,
            data_layout=layout,
        )


@pytest.mark.parametrize("line_interval", [(-1, 1), (2, 1), (0, 13)])
def test_write_row_prefix_interval_errors(line_interval: tuple[int, int]) -> None:
    layout = DataLayout(
        data_type="FLOAT32",
        endianness="LITTLEENDIAN",
        num_of_lines=12,
        num_of_samples=9,
        header_offset=0,
        row_prefix=0,
    )

    with pytest.raises(RuntimeError):
        write_row_prefix(
            raster_file="dummy.bin",
            line_interval=line_interval,
            row_prefix=[],
            data_layout=layout,
        )
