# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Pytest for io/point_target_binary functionalities."""

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt
import pytest

from aresys_io.point_target.nominal_point_targets import (
    NominalPointTarget,
    convert_array_to_point_target_structure,
)


@dataclass(frozen=True)
class NominalPointTargetData:
    """Container for reusable nominal point target test inputs."""

    coordinates: npt.NDArray[np.float64]
    rcs: npt.NDArray[np.complex128]
    n_targets: int
    m_targets: int


@pytest.fixture
def nominal_point_target_data() -> NominalPointTargetData:
    """Common test data for nominal point target tests."""
    return NominalPointTargetData(
        coordinates=np.array([2197913.48269014, 1102055.63813337, 5865641.60621928]),
        rcs=np.array([0 + 0j, 1 + 1j, 2 + 2j, 3 + 3j]),
        n_targets=10,
        m_targets=4,
    )


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


def test_conversion_1pt(nominal_point_target_data: NominalPointTargetData) -> None:
    """Testing conversion to NominalPointTarget dictionary."""
    out = convert_array_to_point_target_structure(
        coords=nominal_point_target_data.coordinates,
        rcs=nominal_point_target_data.rcs,
    )

    _check_point_targets(
        points=out,
        coords=nominal_point_target_data.coordinates,
        rcs=nominal_point_target_data.rcs,
        num=1,
    )


def test_conversion_1pt_with_id(nominal_point_target_data: NominalPointTargetData) -> None:
    """Testing conversion to NominalPointTarget dictionary."""
    out = convert_array_to_point_target_structure(
        coords=nominal_point_target_data.coordinates,
        rcs=nominal_point_target_data.rcs,
        point_target_ids=["5"],
    )

    assert list(out.keys()) == ["5"]
    _check_point_targets(
        points=out,
        coords=nominal_point_target_data.coordinates,
        rcs=nominal_point_target_data.rcs,
        num=1,
    )


def test_conversion_npt(nominal_point_target_data: NominalPointTargetData) -> None:
    """Testing conversion to NominalPointTarget dictionary."""
    out = convert_array_to_point_target_structure(
        coords=np.full(
            (nominal_point_target_data.n_targets, 3),
            nominal_point_target_data.coordinates,
        ),
        rcs=np.full((nominal_point_target_data.n_targets, 4), nominal_point_target_data.rcs),
    )

    _check_point_targets(
        points=out,
        coords=nominal_point_target_data.coordinates,
        rcs=nominal_point_target_data.rcs,
        num=nominal_point_target_data.n_targets,
    )


def test_conversion_npt_with_id(nominal_point_target_data: NominalPointTargetData) -> None:
    """Testing conversion to NominalPointTarget dictionary."""
    ids = list(map(chr, range(97, 97 + nominal_point_target_data.n_targets)))
    out = convert_array_to_point_target_structure(
        coords=np.full(
            (nominal_point_target_data.n_targets, 3),
            nominal_point_target_data.coordinates,
        ),
        rcs=np.full((nominal_point_target_data.n_targets, 4), nominal_point_target_data.rcs),
        point_target_ids=ids,
    )

    assert list(out.keys()) == ids
    _check_point_targets(
        points=out,
        coords=nominal_point_target_data.coordinates,
        rcs=nominal_point_target_data.rcs,
        num=nominal_point_target_data.n_targets,
    )


def test_conversion_error1(nominal_point_target_data: NominalPointTargetData) -> None:
    """Testing conversion to NominalPointTarget dictionary, raising errors."""
    # error: shape mismatch
    with pytest.raises(RuntimeError):
        convert_array_to_point_target_structure(
            coords=np.full(
                (nominal_point_target_data.n_targets, 3),
                nominal_point_target_data.coordinates,
            ),
            rcs=np.full((nominal_point_target_data.m_targets, 4), nominal_point_target_data.rcs),
        )


def test_conversion_error2(nominal_point_target_data: NominalPointTargetData) -> None:
    """Testing conversion to NominalPointTarget dictionary, raising errors."""
    # error: wrong coord shape
    with pytest.raises(RuntimeError):
        convert_array_to_point_target_structure(
            coords=nominal_point_target_data.coordinates.reshape(3, 1),
            rcs=nominal_point_target_data.rcs,
        )


def test_conversion_error3(nominal_point_target_data: NominalPointTargetData) -> None:
    """Testing conversion to NominalPointTarget dictionary, raising errors."""
    # error: rcs coord shape
    with pytest.raises(RuntimeError):
        convert_array_to_point_target_structure(
            coords=nominal_point_target_data.coordinates,
            rcs=nominal_point_target_data.rcs.reshape(2, 2),
        )


def test_conversion_error4(nominal_point_target_data: NominalPointTargetData) -> None:
    """Testing conversion to NominalPointTarget dictionary, raising errors."""
    # error: rcs coord shape
    with pytest.raises(RuntimeError):
        convert_array_to_point_target_structure(
            coords=nominal_point_target_data.coordinates,
            rcs=nominal_point_target_data.rcs,
            point_target_ids=["1", "2"],
        )
