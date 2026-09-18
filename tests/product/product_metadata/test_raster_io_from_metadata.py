# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Unit tests for raster input/output with metadata objects."""

from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np
import pytest

import aresys_io.product.metadata.raster_io_from_metadata as support
from aresys_io.product.metadata.elements import RasterInfo


class TestSupportFunctions:
    """Testing raster_io_from_metadata main functions."""

    def setup_method(self) -> None:
        self.lines = 600
        self.samples = 350
        self.header_offset = 150
        self.row_prefix = 20
        self.raster_info = RasterInfo(
            lines=self.lines,
            samples=self.samples,
            cell_type="FLOAT32",
            file_name="GRD_0001",
            header_offset_bytes=self.header_offset,
            row_prefix_bytes=self.row_prefix,
            byte_order="LITTLEENDIAN",
            invalid_value=None,
            format_type=None,
        )
        self.data = np.ones([self.lines, self.samples])

    def test_write_raster_with_raster_info(self) -> None:
        """Testing write_raster_with_raster_info function."""
        with TemporaryDirectory() as tmpdir:
            path = Path(tmpdir)
            file = path.joinpath(self.raster_info.file_name)
            assert not file.exists()

            support.write_raster_with_raster_info(
                raster_file=file,
                data=self.data,
                raster_info=self.raster_info,
            )
            assert file.exists()
            assert file.is_file()

    def test_read_raster_with_raster_info(self) -> None:
        """Testing read_raster_with_raster_info function."""
        with TemporaryDirectory() as tmpdir:
            path = Path(tmpdir)
            file = path.joinpath(self.raster_info.file_name)
            assert not file.exists()

            support.write_raster_with_raster_info(
                raster_file=file,
                data=self.data,
                raster_info=self.raster_info,
            )
            assert file.exists()
            assert file.is_file()

            read = support.read_raster_with_raster_info(
                raster_file=file,
                raster_info=self.raster_info,
            )

            np.testing.assert_array_equal(read, self.data)

    def test_read_binary_header_with_raster_info(self) -> None:
        """Testing read_binary_header_with_raster_info function."""
        with TemporaryDirectory() as tmpdir:
            path = Path(tmpdir)
            file = path.joinpath(self.raster_info.file_name)
            assert not file.exists()

            support.write_raster_with_raster_info(
                raster_file=file,
                data=self.data,
                raster_info=self.raster_info,
            )
            assert file.exists()
            assert file.is_file()

            read = support.read_binary_header_with_raster_info(
                raster_file=file,
                raster_info=self.raster_info,
            )

            assert bytes(self.header_offset) == read

    def test_write_binary_header_with_raster_info(self) -> None:
        """Testing write_binary_header_with_raster_info function."""
        with TemporaryDirectory() as tmpdir:
            path = Path(tmpdir)
            file = path.joinpath(self.raster_info.file_name)
            assert not file.exists()

            support.write_raster_with_raster_info(
                raster_file=file,
                data=self.data,
                raster_info=self.raster_info,
            )
            assert file.exists()
            assert file.is_file()

            support.write_binary_header_with_raster_info(
                raster_file=file,
                header=bytes(self.header_offset),
                raster_info=self.raster_info,
            )

    def test_write_binary_header_with_raster_info_error(self) -> None:
        """Testing write_binary_header_with_raster_info function, raising error."""
        with TemporaryDirectory() as tmpdir:
            path = Path(tmpdir)
            file = path.joinpath(self.raster_info.file_name)
            assert not file.exists()

            support.write_raster_with_raster_info(
                raster_file=file,
                data=self.data,
                raster_info=self.raster_info,
            )
            assert file.exists()
            assert file.is_file()
            with pytest.raises(RuntimeError):
                support.write_binary_header_with_raster_info(
                    raster_file=file,
                    header=bytes(self.header_offset + 1),
                    raster_info=self.raster_info,
                )

    def test_read_row_prefix_with_raster_info(self) -> None:
        """Testing read_row_prefix_with_raster_info function."""
        with TemporaryDirectory() as tmpdir:
            path = Path(tmpdir)
            file = path.joinpath(self.raster_info.file_name)
            assert not file.exists()

            support.write_raster_with_raster_info(
                raster_file=file,
                data=self.data,
                raster_info=self.raster_info,
            )
            assert file.exists()
            assert file.is_file()

            read = support.read_row_prefix_with_raster_info(
                raster_file=file,
                line_interval=(3, 4),
                raster_info=self.raster_info,
            )

            assert [bytes(self.row_prefix)] == read

    def test_write_row_prefix_with_raster_info(self) -> None:
        """Testing write_row_prefix_with_raster_info function."""
        with TemporaryDirectory() as tmpdir:
            path = Path(tmpdir)
            file = path.joinpath(self.raster_info.file_name)
            assert not file.exists()

            support.write_raster_with_raster_info(
                raster_file=file,
                data=self.data,
                raster_info=self.raster_info,
            )
            assert file.exists()
            assert file.is_file()

            support.write_row_prefix_with_raster_info(
                raster_file=file,
                line_interval=(3, 4),
                row_prefix=[bytes(self.row_prefix)],
                raster_info=self.raster_info,
            )

    def test_write_row_prefix_with_raster_info_error(self) -> None:
        """Testing write_row_prefix_with_raster_info function, raising error."""
        with TemporaryDirectory() as tmpdir:
            path = Path(tmpdir)
            file = path.joinpath(self.raster_info.file_name)
            assert not file.exists()

            support.write_raster_with_raster_info(
                raster_file=file,
                data=self.data,
                raster_info=self.raster_info,
            )
            assert file.exists()
            assert file.is_file()

            with pytest.raises(RuntimeError):
                support.write_row_prefix_with_raster_info(
                    raster_file=file,
                    line_interval=(3, 4),
                    row_prefix=[bytes(self.row_prefix + 1)],
                    raster_info=self.raster_info,
                )
