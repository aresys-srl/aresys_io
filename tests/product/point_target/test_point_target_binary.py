# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Unit tests for Point Target Binary main functionalities."""

from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np
import numpy.typing as npt
import pytest

from aresys_io.product.metadata.io import read_metadata
from aresys_io.product.point_target import point_target_binary
from aresys_io.product.point_target.nominal_point_targets import NominalPointTarget


@dataclass(frozen=True)
class PointTargetBinaryData:
    """Container for reusable point target binary test inputs."""

    coordinates: npt.NDArray[np.float64]
    rcs: npt.NDArray[np.complex128]
    n_targets: int
    selection_size: int


@pytest.fixture
def point_target_binary_data() -> PointTargetBinaryData:
    """Common test data for point target binary tests."""
    return PointTargetBinaryData(
        coordinates=np.array([2197913.48269014, 1102055.63813337, 5865641.60621928]),
        rcs=np.array([0 + 0j, 1 + 1j, 2 + 2j, 3 + 3j]),
        n_targets=10,
        selection_size=4,
    )


def _check_product_files(path: Path) -> None:
    """Checking files inside the product folder binary.


    Parameters
    ----------
    path : Path
        path to the product
    """
    assert path.exists()

    rasters = (
        point_target_binary.COORDINATES_RASTER_FILENAMES + point_target_binary.RCS_RASTER_FILENAMES
    )
    rasters = [path.joinpath(r) for r in rasters]
    metadata = [r.with_suffix(".xml") for r in rasters]

    for file in rasters:
        assert file.is_file()
    for file in metadata:
        assert file.is_file()

    lines = []
    for file in metadata:
        raster_info = read_metadata(file).raster_info
        lines.append(raster_info.lines)
        assert raster_info.samples == 1

    assert len(set(lines)) == 1


def _check_point_targets(
    points: dict[str, NominalPointTarget],
    num: int,
    coords: npt.NDArray[np.float64],
    rcs: npt.NDArray[np.complex128],
) -> None:
    """Checking point targets read from binary product."""
    assert isinstance(points, dict)
    assert len(points) == num

    for item in points.values():
        assert isinstance(item, NominalPointTarget)
        np.testing.assert_equal(item.xyz_coordinates, coords)
        np.testing.assert_equal(item.rcs_hh, rcs[0])
        np.testing.assert_equal(item.rcs_hv, rcs[1])
        np.testing.assert_equal(item.rcs_vh, rcs[2])
        np.testing.assert_equal(item.rcs_vv, rcs[3])


def test_writing_point_target_binary_1pt(point_target_binary_data: PointTargetBinaryData) -> None:
    """Testing creation of point target binary product."""
    with TemporaryDirectory() as tmpdir:
        prod_path = Path(tmpdir).joinpath("test")

        prod = point_target_binary.PointSetProduct(prod_path, open_mode="w")
        prod.write_data(
            coords=point_target_binary_data.coordinates,
            rcs=point_target_binary_data.rcs,
        )

        _check_product_files(path=prod_path)


def test_writing_point_target_binary_npt(point_target_binary_data: PointTargetBinaryData) -> None:
    """Testing creation of point target binary product."""
    with TemporaryDirectory() as tmpdir:
        prod_path = Path(tmpdir).joinpath("test")

        prod = point_target_binary.PointSetProduct(prod_path, open_mode="w")
        prod.write_data(
            coords=np.full(
                (point_target_binary_data.n_targets, 3),
                point_target_binary_data.coordinates,
            ),
            rcs=np.full((point_target_binary_data.n_targets, 4), point_target_binary_data.rcs),
        )

        _check_product_files(path=prod_path)


def test_read_point_target_binary_1pt(point_target_binary_data: PointTargetBinaryData) -> None:
    """Testing creation and read of point target binary product."""
    with TemporaryDirectory() as tmpdir:
        prod_path = Path(tmpdir).joinpath("test")

        prod_0 = point_target_binary.PointSetProduct(prod_path, open_mode="w")
        prod_0.write_data(
            coords=point_target_binary_data.coordinates,
            rcs=point_target_binary_data.rcs,
        )

        _check_product_files(path=prod_path)

        prod_1 = point_target_binary.PointSetProduct(prod_path)
        coords, rcs = prod_1.read_data()

        assert prod_1.number_of_targets == 1
        np.testing.assert_array_equal(coords, np.atleast_2d(point_target_binary_data.coordinates))
        np.testing.assert_array_equal(rcs, np.atleast_2d(point_target_binary_data.rcs))


def test_read_point_target_binary_npt(point_target_binary_data: PointTargetBinaryData) -> None:
    """Testing creation and read of point target binary product."""
    with TemporaryDirectory() as tmpdir:
        prod_path = Path(tmpdir).joinpath("test")

        prod_0 = point_target_binary.PointSetProduct(prod_path, open_mode="w")
        prod_0.write_data(
            coords=np.full(
                (point_target_binary_data.n_targets, 3),
                point_target_binary_data.coordinates,
            ),
            rcs=np.full((point_target_binary_data.n_targets, 4), point_target_binary_data.rcs),
        )

        _check_product_files(path=prod_path)

        prod_1 = point_target_binary.PointSetProduct(prod_path)
        coords, rcs = prod_1.read_data()

        assert prod_1.number_of_targets == point_target_binary_data.n_targets
        np.testing.assert_array_equal(
            coords,
            np.full((point_target_binary_data.n_targets, 3), point_target_binary_data.coordinates),
        )
        np.testing.assert_array_equal(
            rcs,
            np.full((point_target_binary_data.n_targets, 4), point_target_binary_data.rcs),
        )


def test_read_point_target_binary_npt_selection(
    point_target_binary_data: PointTargetBinaryData,
) -> None:
    """Testing creation and read of point target binary product."""
    with TemporaryDirectory() as tmpdir:
        prod_path = Path(tmpdir).joinpath("test")

        prod_0 = point_target_binary.PointSetProduct(prod_path, open_mode="w")
        prod_0.write_data(
            coords=np.full(
                (point_target_binary_data.n_targets, 3),
                point_target_binary_data.coordinates,
            ),
            rcs=np.full((point_target_binary_data.n_targets, 4), point_target_binary_data.rcs),
        )

        _check_product_files(path=prod_path)

        prod_1 = point_target_binary.PointSetProduct(prod_path)
        coords, rcs = prod_1.read_data(
            start=point_target_binary_data.selection_size,
            num_points=point_target_binary_data.selection_size,
        )

        assert prod_1.number_of_targets == point_target_binary_data.n_targets
        np.testing.assert_array_equal(
            coords,
            np.full(
                (point_target_binary_data.selection_size, 3),
                point_target_binary_data.coordinates,
            ),
        )
        np.testing.assert_array_equal(
            rcs,
            np.full(
                (point_target_binary_data.selection_size, 4),
                point_target_binary_data.rcs,
            ),
        )


def test_memmap_read_point_target_binary(point_target_binary_data: PointTargetBinaryData) -> None:
    """Testing creation of read-only memmap to point target binary product."""
    with TemporaryDirectory() as tmpdir:
        prod_path = Path(tmpdir).joinpath("test")

        test_cases = [1, point_target_binary_data.n_targets]

        for num_points in test_cases:
            prod_0 = point_target_binary.PointSetProduct(prod_path, open_mode="w")
            prod_0.write_data(
                coords=np.full((num_points, 3), point_target_binary_data.coordinates),
                rcs=np.full((num_points, 4), point_target_binary_data.rcs),
            )

            _check_product_files(path=prod_path)

            prod_1 = point_target_binary.PointSetProduct(prod_path)
            with prod_1.read_data_as_memmap() as (coords_mm, rcs_mm):
                assert prod_1.number_of_targets == num_points
                for ic, arr_to_test in enumerate((coords_mm.x, coords_mm.y, coords_mm.z)):
                    np.testing.assert_array_equal(
                        arr_to_test.flatten(),
                        np.full((num_points), point_target_binary_data.coordinates[ic]),
                    )
                for ircs, arr_to_test in enumerate((rcs_mm.HH, rcs_mm.HV, rcs_mm.VH, rcs_mm.VV)):
                    np.testing.assert_array_equal(
                        arr_to_test.flatten(),
                        np.full((num_points), point_target_binary_data.rcs[ircs]),
                    )


def test_write_point_target_binary_error1(point_target_binary_data: PointTargetBinaryData) -> None:
    """Testing creation of point target binary product, raising errors."""
    # error: open in read mode, folder does not exist
    _ = point_target_binary_data
    with TemporaryDirectory() as tmpdir:
        prod_path = Path(tmpdir).joinpath("prova")
        with pytest.raises(RuntimeError):
            point_target_binary.PointSetProduct(prod_path)


def test_write_point_target_binary_error2(point_target_binary_data: PointTargetBinaryData) -> None:
    """Testing creation of point target binary product, raising errors."""
    # error: open in read mode, path not to folder
    _ = point_target_binary_data
    with TemporaryDirectory() as tmpdir:
        prod_path = Path(tmpdir).joinpath("prova.xml")
        prod_path.write_text("", encoding="utf-8")
        with pytest.raises(RuntimeError):
            point_target_binary.PointSetProduct(prod_path)


def test_write_point_target_binary_error3(point_target_binary_data: PointTargetBinaryData) -> None:
    """Testing creation of point target binary product, raising errors."""
    # error: write wrong shape data
    with TemporaryDirectory() as tmpdir:
        prod_path = Path(tmpdir)
        prod = point_target_binary.PointSetProduct(prod_path, open_mode="w")
        with pytest.raises(RuntimeError):
            prod.write_data(
                coords=point_target_binary_data.coordinates,
                rcs=point_target_binary_data.rcs.reshape(2, 2),
            )


def test_write_point_target_binary_error4(point_target_binary_data: PointTargetBinaryData) -> None:
    """Testing creation of point target binary product, raising errors."""
    # error: write wrong shape data
    with TemporaryDirectory() as tmpdir:
        prod_path = Path(tmpdir)
        prod = point_target_binary.PointSetProduct(prod_path, open_mode="w")
        with pytest.raises(RuntimeError):
            prod.write_data(
                coords=point_target_binary_data.coordinates.reshape(3, 1),
                rcs=point_target_binary_data.rcs,
            )


def test_write_point_target_binary_error5(point_target_binary_data: PointTargetBinaryData) -> None:
    """Testing creation of point target binary product, raising errors."""
    # error: input number mismatch
    with TemporaryDirectory() as tmpdir:
        prod_path = Path(tmpdir)
        prod = point_target_binary.PointSetProduct(prod_path, open_mode="w")
        with pytest.raises(RuntimeError):
            prod.write_data(
                coords=np.full(
                    (point_target_binary_data.n_targets, 3),
                    point_target_binary_data.coordinates,
                ),
                rcs=np.full(
                    (point_target_binary_data.selection_size, 4),
                    point_target_binary_data.rcs,
                ),
            )
