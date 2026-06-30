# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Point Target Binary Module."""

from collections.abc import Generator
from contextlib import ExitStack, contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, get_args

import numpy as np

import aresys_io.product_metadata.metadata as mtd
from aresys_io.core.raster_io import DataLayout, write_raster
from aresys_io.product_metadata.metadata_elements import RasterInfo
from aresys_io.product_metadata.metadata_io import (
    read_metadata,
    write_metadata,
)
from aresys_io.product_metadata.raster_io_from_metadata import (
    MemmappedNDArray,
    read_raster_as_memmap_with_raster_info,
    read_raster_with_raster_info,
)

COORDINATES_RASTER_FILENAMES = [
    "PointTargetPosX",
    "PointTargetPosY",
    "PointTargetPosZ",
]

RCS_RASTER_FILENAMES = [
    "PointTargetRCSHH",
    "PointTargetRCSHV",
    "PointTargetRCSVH",
    "PointTargetRCSVV",
]

METADATA_EXTENSION = ".xml"
OpenMode = Literal["r", "w"]


@dataclass()
class CoordinatesMemmap:
    """Coordinates memmap."""

    x: MemmappedNDArray
    y: MemmappedNDArray
    z: MemmappedNDArray


@dataclass()
class RCSMemmap:
    """RCS memmap."""

    HH: MemmappedNDArray
    HV: MemmappedNDArray
    VH: MemmappedNDArray
    VV: MemmappedNDArray


class PointSetProduct:
    """PointSetProduct class representing the point target binary file."""

    _raster_infos: list[RasterInfo] | None

    def __init__(
        self,
        path: str | Path,
        open_mode: OpenMode = "r",
    ) -> None:
        """PointSetProduct init.

        Parameters
        ----------
        path : Union[str, Path]
            path to the product folder
        open_mode : OpenMode, optional
            open mode (can be write "w" or read "r"), write mode will overwrite existing data,
            by default "r".

        Raises
        ------
        RuntimeError
            if open_mode is "r" and path does not exist or is not a directory
        ValueError
            if open_mode is not "r" or "w"

        """
        self._path = Path(path)
        if open_mode not in get_args(OpenMode):
            msg = f"Unsupported open mode: {open_mode}"
            raise ValueError(msg)

        self._open_mode = open_mode

        # generating full paths for metadata and raster files
        self._coords_metadata_files = [
            self._path.joinpath(c + METADATA_EXTENSION) for c in COORDINATES_RASTER_FILENAMES
        ]
        self._coords_raster_files = [self._path.joinpath(c) for c in COORDINATES_RASTER_FILENAMES]
        self._rcs_metadata_files = [
            self._path.joinpath(r + METADATA_EXTENSION) for r in RCS_RASTER_FILENAMES
        ]
        self._rcs_raster_files = [self._path.joinpath(r) for r in RCS_RASTER_FILENAMES]

        if self._open_mode == "r":
            # reading mode, asserting existence and being a directory
            if not self._path.exists():
                msg = f"Path does not exist {self._path}"
                raise RuntimeError(msg)
            if not self._path.is_dir():
                msg = f"Path is not a directory {self._path}"
                raise RuntimeError(msg)
            # reading number of targets from files
            self._raster_infos, self._num_targets = self._read_num_lines()

            # 3 coordinates files + 4 rcs polarizations
            assert len(self._coords_raster_files) + len(self._rcs_raster_files) == 7
        else:
            # writing mode
            self._raster_infos = None
            self._num_targets = 0

    @property
    def product_path(self) -> Path:
        """PointSetProduct folder path."""
        return self._path

    @property
    def number_of_targets(self) -> int:
        """Number of targets inside the PointSetProduct folder."""
        return self._num_targets

    def _read_num_lines(self) -> tuple[list[RasterInfo], int]:
        """Read the number of lines, i.e. the number of targets and raster info for each metadata.

        Checking also that all metadata files are consistent regarding number of lines value.

        Returns
        -------
        Tuple[List[mtd.RasterInfo], int]
            list of raster info for each metadata,
            number of point targets in the product folder binary

        Raises
        ------
        RuntimeError
            number of samples is different from 1
        """
        metadata = self._coords_metadata_files + self._rcs_metadata_files
        lines = []
        raster_infos = []
        for file in metadata:
            raster_info = read_metadata(file).get_raster_info()
            lines.append(raster_info.lines)
            raster_infos.append(raster_info)
            if raster_info.samples != 1:
                msg = "Number of samples is not 1"
                raise RuntimeError(msg)

        assert len(set(lines)) == 1, (
            "Metadata files are not consistent: different numbers of lines"
        )
        return raster_infos, lines[0]

    def _read_rasters(self, start: int, stop: int) -> tuple[np.ndarray, np.ndarray]:
        """Read binary raster files both for coordinates and rcs.

        Parameters
        ----------
        start : int
            start reading block
        stop : int
            last reading block.

        Returns
        -------
        Tuple[np.ndarray, np.ndarray]
            coordinates array (N, 3),
            rcs array (N, 4)
        """
        # block to be read [first line, first sample, lines to be read, samples to be read]
        block = [start, 0, stop - start, 1]

        assert stop <= self._num_targets
        assert start >= 0
        assert self._raster_infos is not None

        data = []
        for index, file in enumerate(self._coords_raster_files + self._rcs_raster_files):
            data.append(
                read_raster_with_raster_info(
                    raster_file=file,
                    raster_info=self._raster_infos[index],
                    block_to_read=block,
                ),
            )

        return np.hstack(data[:3]), np.hstack(data[-4:])

    @staticmethod
    def _write_rasters(
        data: np.ndarray,
        filenames: list[Path],
        data_type: Literal["FLOAT32", "FLOAT64", "FLOAT_COMPLEX", "DOUBLE_COMPLEX"],
    ) -> None:
        """Write input data to raster files using the specified data type.

        Parameters
        ----------
        data : np.ndarray
            array to be written to raster file
        filenames : List[Path]
            names of raster files to be written
        data_type : Literal["FLOAT32", "FLOAT64", "FLOAT_COMPLEX", "DOUBLE_COMPLEX"]
            data type to be used when writing data.
        """
        for index, file in enumerate(filenames):
            data_slice = np.atleast_2d(data[index]).T
            write_raster(
                raster_file_name=file,
                data=data_slice,
                data_layout=DataLayout(
                    data_type=data_type,
                    endianness="LITTLEENDIAN",
                    num_of_samples=1,
                    num_of_lines=data_slice.size,
                ),
            )

    @staticmethod
    def _write_metadata(
        filenames: list[Path],
        num_points: int,
        data_type: Literal["FLOAT32", "FLOAT64", "FLOAT_COMPLEX", "DOUBLE_COMPLEX"],
    ) -> None:
        """Write metadata files corresponding to raster files.

        Parameters
        ----------
        filenames : List[Path]
            metadata filenames to be written
        num_points : int
            total number of data blocks written to the corresponding raster file
        data_type : Literal["FLOAT32", "FLOAT64", "FLOAT_COMPLEX", "DOUBLE_COMPLEX"]
            data type used in writing the corresponding raster file.
        """
        for file in filenames:
            raster_info = RasterInfo(
                lines=num_points,
                samples=1,
                cell_type=data_type,
                file_name=file.stem,
            )

            metadata = mtd.create_new_metadata(description="Aresys XML metadata file")
            metadata.insert_element(raster_info)

            write_metadata(metadata, str(file))

    def read_data(
        self,
        start: int = 0,
        num_points: int | None = None,
    ) -> tuple[np.ndarray, np.ndarray]:
        """Read Point Target Binary rasters to extract point target data.

        Parameters
        ----------
        start : int, optional
            number of point targets from which to start reading the raster, by default 0
        num_points : int, optional
            number of points to be read, if None all points are read from the start to the end,
            by default None.

        Returns
        -------
        Tuple[np.ndarray, np.ndarray]
            coordinates array in the form (N, 3),
            rcs array (HH, HV, VH, VV) in the form (N, 4)

        Raises
        ------
        ValueError
            if start is negative
        ValueError
            if num_points is 0 or negative
        ValueError
            if start + num_points exceeds total number of points
        ValueError
            if start exceeds total number of points
        ValueError
            if num_points exceeds total number of points
        """
        if num_points is None:
            num_points = self._num_targets - start

        stop = start + num_points

        if start < 0:
            msg = f"Starting block cannot be negative {start}"
            raise ValueError(msg)

        if num_points <= 0:
            msg = f"Number of blocks to be read cannot be 0 or negative {num_points}"
            raise ValueError(msg)

        if stop > self._num_targets:
            msg = (
                "Blocks to be read exceed total number of readable blocks: "
                f"start + points to be read {stop} > "
                f"total number of points {self._num_targets}"
            )
            raise ValueError(
                msg,
            )

        if start > self._num_targets:
            msg = f"Starting block exceeds total number of blocks: {start} > {self._num_targets}"
            raise ValueError(
                msg,
            )

        if num_points > self._num_targets:
            msg = (
                "Number of blocks to be read exceeds total number of blocks: "
                f"{num_points} > {self._num_targets}"
            )
            raise ValueError(
                msg,
            )

        return self._read_rasters(start=start, stop=stop)

    @contextmanager
    def read_data_as_memmap(self) -> Generator[tuple[CoordinatesMemmap, RCSMemmap]]:
        """Create and manages the lifecycle of a memmap to the Point Target Binary rasters.

        Usage
        -----
        with prod.read_data_as_memmap() as (coords_mm, rcs_mm):
            ...

        Yields
        ------
        CoordinatesMemmap
            Object containing 3 memmaps (x, y, z) pointing to arrays of shape (N,)
        RCSMemmap
            Object containing 4 memmaps (HH, HV, VH, VV) pointing to arrays of shape (N,)
        """
        raw_memmaps: list[MemmappedNDArray] = []

        assert self._raster_infos is not None
        with ExitStack() as stack:
            for index, file in enumerate(self._coords_raster_files + self._rcs_raster_files):
                raw_memmaps.append(
                    stack.enter_context(
                        read_raster_as_memmap_with_raster_info(
                            raster_file=file,
                            raster_info=self._raster_infos[index],
                        ),
                    ),
                )

            yield CoordinatesMemmap(*raw_memmaps[:3]), RCSMemmap(*raw_memmaps[3:])

    def write_data(
        self,
        coords: np.ndarray,
        rcs: np.ndarray,
        coords_data_type: Literal["FLOAT32", "FLOAT64"] = "FLOAT64",
        rcs_data_type: Literal["FLOAT_COMPLEX", "DOUBLE_COMPLEX"] = "FLOAT_COMPLEX",
    ) -> None:
        """Write data to the Point Set Target folder.

        Parameters
        ----------
        coords : np.ndarray
            point target coordinates, in the form (N, 3)
        rcs : np.ndarray
            point target radar cross section values, in the form (N, 4) (HH,HV,VH,VV)
        coords_data_type : Literal["FLOAT32", "FLOAT64"]
            data type to be used in writing coordinates rasters
        rcs_data_type : Literal["FLOAT_COMPLEX", "DOUBLE_COMPLEX"]
            data type to be used in writing rcs rasters

        Raises
        ------
        RuntimeError
            if coordinates shape is wrong
        RuntimeError
            if rcs shape is wrong
        RuntimeError
            if coordinates shape does not match rcs shape
        """
        coords = np.atleast_2d(coords)
        rcs = np.atleast_2d(rcs)

        if coords.shape[1] != 3:
            msg = f"Wrong shape: {coords.shape[1]} != 3"
            raise RuntimeError(msg)

        if rcs.shape[1] != 4:
            msg = f"Wrong shape: {rcs.shape[1]} != 4"
            raise RuntimeError(msg)

        num_points = coords.shape[0]

        if num_points != rcs.shape[0]:
            msg = f"number of coordinates {num_points} != number of rcs {rcs.shape[0]}"
            raise RuntimeError(
                msg,
            )

        self._path.mkdir(exist_ok=True)

        # writing coordinates and rcs raster data
        self._write_rasters(
            data=coords.T,
            filenames=self._coords_raster_files,
            data_type=coords_data_type,
        )
        self._write_rasters(data=rcs.T, filenames=self._rcs_raster_files, data_type=rcs_data_type)

        # writing coordinates and rcs raster metadata
        self._write_metadata(
            filenames=self._coords_metadata_files,
            num_points=num_points,
            data_type=coords_data_type,
        )
        self._write_metadata(
            filenames=self._rcs_metadata_files,
            num_points=num_points,
            data_type=rcs_data_type,
        )


__all__ = ["CoordinatesMemmap", "PointSetProduct", "RCSMemmap"]
