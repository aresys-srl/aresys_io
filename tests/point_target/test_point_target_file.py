# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Pytest for io/point_target_file functionalities."""

from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np
import numpy.typing as npt
import pytest

from aresys_io.point_target.nominal_point_targets import NominalPointTarget
from aresys_io.point_target.point_target_file import (
    read_point_targets_file,
    write_point_targets_file,
)


@dataclass(frozen=True)
class PointTargetData:
    """Container for reusable test inputs."""

    coordinates: npt.NDArray[np.float64]
    rcs: npt.NDArray[np.complex128]
    delays: float
    pt_id: int
    default_point_target: NominalPointTarget
    n_targets: int
    m_ids: int


@pytest.fixture
def point_target_data() -> PointTargetData:
    """Common test data for point target file tests."""
    coordinates = np.array([2197913.48269014, 1102055.63813337, 5865641.60621928])
    rcs = np.array([0 + 0j, 1 + 1j, 2 + 2j, 3 + 3j])
    delays = 5.0
    pt_id = 45
    default_point_target = NominalPointTarget(
        xyz_coordinates=coordinates,
        rcs_hh=rcs[0],
        rcs_hv=rcs[1],
        rcs_vv=rcs[2],
        rcs_vh=rcs[3],
        delay=delays,
    )

    return PointTargetData(
        coordinates=coordinates,
        rcs=rcs,
        delays=delays,
        pt_id=pt_id,
        default_point_target=default_point_target,
        n_targets=10,
        m_ids=6,
    )


def _check_point_targets(
    points: dict[str, NominalPointTarget],
    num: int,
    coords: npt.NDArray[np.float64],
    rcs: npt.NDArray[np.complex128],
    delays: float,
) -> None:
    """Checking point targets read from file."""
    assert isinstance(points, dict)
    assert len(points) == num
    for item in points.values():
        assert isinstance(item, NominalPointTarget)
        np.testing.assert_equal(item.xyz_coordinates, coords)
        np.testing.assert_equal(item.rcs_hh, rcs[0])
        np.testing.assert_equal(item.rcs_hv, rcs[1])
        np.testing.assert_equal(item.rcs_vv, rcs[2])
        np.testing.assert_equal(item.rcs_vh, rcs[3])
        np.testing.assert_equal(item.delay, delays)


def test_write_point_target_file_1pt(point_target_data: PointTargetData) -> None:
    """Testing point target file creation and dump to disk."""
    with TemporaryDirectory() as tmpdir:
        xml_path = Path(tmpdir).joinpath("test.xml")
        assert not xml_path.is_file()

        write_point_targets_file(
            filename=xml_path,
            point_targets=point_target_data.default_point_target,
            target_type=1,
        )

        assert xml_path.is_file()


def test_write_point_target_file_npt(point_target_data: PointTargetData) -> None:
    """Testing point target file creation and dump to disk."""
    with TemporaryDirectory() as tmpdir:
        xml_path = Path(tmpdir).joinpath("test.xml")
        assert not xml_path.is_file()

        write_point_targets_file(
            filename=xml_path,
            point_targets=[point_target_data.default_point_target] * point_target_data.n_targets,
            target_type=1,
        )

        assert xml_path.is_file()


def test_write_read_point_target_file_case0a(point_target_data: PointTargetData) -> None:
    """Testing point target file creation and dump to disk, case 0a."""
    # Test case 0a: writing 1 target, no target id
    with TemporaryDirectory() as tmpdir:
        xml_path = Path(tmpdir).joinpath("test.xml")
        assert not xml_path.is_file()

        write_point_targets_file(
            filename=xml_path,
            point_targets=point_target_data.default_point_target,
            target_type=1,
        )

        assert xml_path.is_file()

        point_targets = read_point_targets_file(xml_file=xml_path)

        _check_point_targets(
            points=point_targets,
            num=1,
            coords=point_target_data.coordinates,
            rcs=point_target_data.rcs,
            delays=point_target_data.delays,
        )


def test_write_read_point_target_file_case0b(point_target_data: PointTargetData) -> None:
    """Testing point target file creation and dump to disk, case 0b."""
    # Test case 0b: writing 1 target, with target id
    with TemporaryDirectory() as tmpdir:
        xml_path = Path(tmpdir).joinpath("test.xml")
        assert not xml_path.is_file()

        write_point_targets_file(
            filename=xml_path,
            point_targets=point_target_data.default_point_target,
            target_type=1,
            point_targets_ids=point_target_data.pt_id,
        )

        assert xml_path.is_file()

        point_targets = read_point_targets_file(xml_file=xml_path)

        assert next(iter(point_targets.keys())) == str(point_target_data.pt_id)
        _check_point_targets(
            points=point_targets,
            num=1,
            coords=point_target_data.coordinates,
            rcs=point_target_data.rcs,
            delays=point_target_data.delays,
        )


def test_write_read_point_target_file_case1a(point_target_data: PointTargetData) -> None:
    """Testing point target file creation and dump to disk, case 1a."""
    # Test case 1a: writing N targets, no ids
    with TemporaryDirectory() as tmpdir:
        xml_path = Path(tmpdir).joinpath("test.xml")
        assert not xml_path.is_file()

        write_point_targets_file(
            filename=xml_path,
            point_targets=[point_target_data.default_point_target] * point_target_data.n_targets,
            target_type=1,
        )

        assert xml_path.is_file()

        point_targets = read_point_targets_file(xml_file=xml_path)

        assert list(point_targets.keys()) == [
            str(p) for p in range(1, point_target_data.n_targets + 1)
        ]
        _check_point_targets(
            points=point_targets,
            num=point_target_data.n_targets,
            coords=point_target_data.coordinates,
            rcs=point_target_data.rcs,
            delays=point_target_data.delays,
        )


def test_write_read_point_target_file_case1b(point_target_data: PointTargetData) -> None:
    """Testing point target file creation and dump to disk, case 1b."""
    # Test case 1b: writing N targets, with target ids
    with TemporaryDirectory() as tmpdir:
        xml_path = Path(tmpdir).joinpath("test.xml")
        assert not xml_path.is_file()

        indexes = np.arange(point_target_data.n_targets) + 5
        write_point_targets_file(
            filename=xml_path,
            point_targets=[point_target_data.default_point_target] * point_target_data.n_targets,
            target_type=1,
            point_targets_ids=indexes.tolist(),
        )

        assert xml_path.is_file()

        point_targets = read_point_targets_file(xml_file=xml_path)

        assert list(point_targets.keys()) == [str(p) for p in indexes]
        _check_point_targets(
            points=point_targets,
            num=point_target_data.n_targets,
            coords=point_target_data.coordinates,
            rcs=point_target_data.rcs,
            delays=point_target_data.delays,
        )


def test_write_read_point_target_file_error0(point_target_data: PointTargetData) -> None:
    """Testing point target file creation and dump to disk triggering errors."""
    # error: writing N target, with M ids
    with TemporaryDirectory() as tmpdir:
        xml_path = Path(tmpdir).joinpath("test.xml")
        assert not xml_path.is_file()

        with pytest.raises(RuntimeError):
            write_point_targets_file(
                filename=xml_path,
                point_targets=[point_target_data.default_point_target]
                * point_target_data.n_targets,
                target_type=1,
                point_targets_ids=np.arange(point_target_data.m_ids).tolist(),
            )


def test_write_read_point_target_file_error1(point_target_data: PointTargetData) -> None:
    """Testing point target file creation and dump to disk triggering errors."""
    # error: writing xml file but already exists
    with TemporaryDirectory() as tmpdir:
        xml_path = Path(tmpdir).joinpath("test.xml")
        xml_path.write_text("", encoding="utf-8")

        with pytest.raises(RuntimeError):
            write_point_targets_file(
                filename=xml_path,
                point_targets=point_target_data.default_point_target,
                target_type=1,
            )


def test_write_read_point_target_file_error2(point_target_data: PointTargetData) -> None:
    """Testing point target file creation and dump to disk triggering errors."""
    # error: writing xml file but filename has no .xml in it
    with TemporaryDirectory() as tmpdir:
        xml_path = Path(tmpdir).joinpath("test")

        with pytest.raises(RuntimeError):
            write_point_targets_file(
                filename=xml_path,
                point_targets=point_target_data.default_point_target,
                target_type=1,
            )
