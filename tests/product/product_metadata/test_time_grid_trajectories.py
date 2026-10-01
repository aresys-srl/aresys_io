# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Unit tests for time_grid_trajectories.py"""

from __future__ import annotations

import numpy as np
import pytest
from perseo_core.timing import PreciseDateTime

from aresys_io.product import create_new_metadata
from aresys_io.product.metadata import elements
from aresys_io.product.metadata.time_grid_trajectories import (
    Bistatic,
    BistaticSingleSystem,
    Monostatic,
    TimeGridTrajectories,
)


def _create_state_vectors(num: int) -> elements.StateVectors:
    reference_time = PreciseDateTime.from_numeric_datetime(year=2020)
    position_vector = np.arange(num * 3, dtype=np.float64).reshape(num, 3)
    velocity_vector = np.arange(num * 3, dtype=np.float64).reshape(num, 3) * 0.1
    time_step = 1.0
    return elements.StateVectors(
        position_vector=position_vector,
        velocity_vector=velocity_vector,
        reference_time=reference_time,
        time_step=time_step,
    )


def test_no_time_grid_info() -> None:
    metadata = create_new_metadata(num_metadata_channels=1)
    metadata.insert_element(_create_state_vectors(num=3))
    tg = TimeGridTrajectories.from_metadata(metadata)
    assert isinstance(tg.data, Monostatic)


def test_no_time_grid_info_no_sv() -> None:
    metadata = create_new_metadata(num_metadata_channels=1)
    with pytest.raises(
        RuntimeError,
        match="The element StateVectors is not available in the current metadata channel",
    ):
        TimeGridTrajectories.from_metadata(metadata)


def test_monostatic_time_grid_info_empty() -> None:
    metadata = create_new_metadata(num_metadata_channels=1)
    metadata.insert_element(elements.TimeGridInfo(data=elements.TimeGridInfo.Monostatic()))
    metadata.insert_element(_create_state_vectors(num=3))
    tg = TimeGridTrajectories.from_metadata(metadata)
    assert isinstance(tg.data, Monostatic)


def test_monostatic_time_grid_info_with_state_vectors() -> None:
    metadata = create_new_metadata(num_metadata_channels=1)
    metadata.insert_element(
        elements.TimeGridInfo(
            data=elements.TimeGridInfo.Monostatic(state_vectors=_create_state_vectors(num=3))
        )
    )
    tg = TimeGridTrajectories.from_metadata(metadata)
    assert isinstance(tg.data, Monostatic)


def test_bistatic_time_grid_info_empty_raises_when_no_tx_channel() -> None:
    metadata = create_new_metadata(num_metadata_channels=1)
    metadata.insert_element(elements.TimeGridInfo(data=elements.TimeGridInfo.Bistatic()))

    with pytest.raises(RuntimeError, match="no TX channel"):
        TimeGridTrajectories.from_metadata(metadata)


def test_bistatic_time_grid_info_empty_raises_on_unexpected_tx_content_id() -> None:
    metadata = create_new_metadata(num_metadata_channels=2)
    metadata.insert_element(elements.TimeGridInfo(data=elements.TimeGridInfo.Bistatic()))
    metadata[1].content_id = "WRONG"

    with pytest.raises(RuntimeError, match="Unexpected content ID"):
        TimeGridTrajectories.from_metadata(metadata)


def test_bistatic_time_grid_info_empty_with_tx_channel() -> None:
    metadata = create_new_metadata(num_metadata_channels=2)
    metadata.insert_element(elements.TimeGridInfo(data=elements.TimeGridInfo.Bistatic()))
    metadata.insert_element(_create_state_vectors(num=3))
    metadata[1].content_id = "TX"
    metadata[1].insert_element(_create_state_vectors(num=5))

    tg = TimeGridTrajectories.from_metadata(metadata)

    assert isinstance(tg.data, Bistatic)


def test_bistatic_time_grid_info_with_state_vectors() -> None:
    sv_tx = _create_state_vectors(num=5)
    sv_rx = _create_state_vectors(num=3)

    metadata = create_new_metadata(num_metadata_channels=1)
    metadata.insert_element(
        elements.TimeGridInfo(
            data=elements.TimeGridInfo.Bistatic(state_vectors_tx_rx=(sv_tx, sv_rx))
        )
    )

    tg = TimeGridTrajectories.from_metadata(metadata)
    assert isinstance(tg.data, Bistatic)

    np.testing.assert_allclose(tg.data.trajectory_tx.positions, sv_tx.position_vector)
    np.testing.assert_allclose(tg.data.trajectory_tx.velocities, sv_tx.velocity_vector)
    assert list(tg.data.trajectory_tx.times) == list(sv_tx.times)

    np.testing.assert_allclose(tg.data.trajectory_rx.positions, sv_rx.position_vector)
    np.testing.assert_allclose(tg.data.trajectory_rx.velocities, sv_rx.velocity_vector)
    assert list(tg.data.trajectory_rx.times) == list(sv_rx.times)


def test_bistatic_single_system_time_grid_info_empty() -> None:
    metadata = create_new_metadata(num_metadata_channels=1)
    metadata.insert_element(
        elements.TimeGridInfo(data=elements.TimeGridInfo.BistaticSingleSystem())
    )
    metadata.insert_element(_create_state_vectors(num=3))

    tg = TimeGridTrajectories.from_metadata(metadata)

    assert isinstance(tg.data, BistaticSingleSystem)


def test_bistatic_single_system_time_grid_info_with_state_vectors() -> None:
    sv = _create_state_vectors(num=4)
    metadata = create_new_metadata(num_metadata_channels=1)
    metadata.insert_element(
        elements.TimeGridInfo(data=elements.TimeGridInfo.BistaticSingleSystem(state_vectors=sv))
    )

    tg = TimeGridTrajectories.from_metadata(metadata)
    assert isinstance(tg.data, BistaticSingleSystem)

    np.testing.assert_allclose(tg.data.trajectory.positions, sv.position_vector)
    np.testing.assert_allclose(tg.data.trajectory.velocities, sv.velocity_vector)
    assert list(tg.data.trajectory.times) == list(sv.times)
