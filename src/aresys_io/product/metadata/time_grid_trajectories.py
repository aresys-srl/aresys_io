# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Time-grid trajectory metadata utilities."""

from dataclasses import dataclass
from typing import Self

from perseo_core.geometry.navigation import Trajectory

from aresys_io.product.metadata.channel import MetaData
from aresys_io.product.metadata.create_orbit import create_trajectory_from_state_vectors
from aresys_io.product.metadata.elements import TimeGridInfo


@dataclass
class Monostatic:
    """Trajectory data for a monostatic system."""

    trajectory: Trajectory


def _fill_monostatic(metadata: MetaData, data: TimeGridInfo.Monostatic) -> Monostatic:
    if data.state_vectors:
        return Monostatic(
            trajectory=create_trajectory_from_state_vectors(state_vectors=data.state_vectors)
        )

    return Monostatic(trajectory=metadata.trajectory())


@dataclass
class Bistatic:
    """Trajectory data for a bistatic system."""

    trajectory_rx: Trajectory
    trajectory_tx: Trajectory


def _fill_bistatic(metadata: MetaData, data: TimeGridInfo.Bistatic) -> Bistatic:
    if data.state_vectors_tx_rx:
        sv_tx, sv_rx = data.state_vectors_tx_rx
        trajectory_tx = create_trajectory_from_state_vectors(state_vectors=sv_tx)
        trajectory_rx = create_trajectory_from_state_vectors(state_vectors=sv_rx)
        return Bistatic(trajectory_rx=trajectory_rx, trajectory_tx=trajectory_tx)

    rx_channel = metadata.channels[0]

    tx_channel = None
    if len(metadata.channels) == 1:
        msg = "Bistatic time grid info without state_vectors, but no TX channel available"
        raise RuntimeError(msg)

    tx_channel = metadata.channels[1]
    content_id = tx_channel.content_id
    if content_id and content_id.upper() != "TX":
        msg = f"Unexpected content ID for the second channel: {content_id}"
        raise RuntimeError(msg)

    trajectory_rx = rx_channel.trajectory()
    trajectory_tx = tx_channel.trajectory()
    return Bistatic(trajectory_rx=trajectory_rx, trajectory_tx=trajectory_tx)


@dataclass
class BistaticSingleSystem:
    """Trajectory data for a bistatic single-system configuration."""

    trajectory: Trajectory


def _fill_bistatic_single_system(
    metadata: MetaData, data: TimeGridInfo.BistaticSingleSystem
) -> BistaticSingleSystem:
    if data.state_vectors:
        return BistaticSingleSystem(
            trajectory=create_trajectory_from_state_vectors(state_vectors=data.state_vectors)
        )

    return BistaticSingleSystem(trajectory=metadata.trajectory())


@dataclass
class TimeGridTrajectories:
    """Container for trajectory data extracted from time-grid metadata."""

    data: Monostatic | Bistatic | BistaticSingleSystem

    @classmethod
    def from_metadata(cls, metadata: MetaData) -> Self:
        """Build trajectories from the provided metadata."""
        rx_channel = metadata.channels[0]

        if "TimeGridInfo" not in rx_channel:
            return cls(data=Monostatic(trajectory=rx_channel.trajectory()))

        data = rx_channel.time_grid_info.data

        match data:
            case TimeGridInfo.Monostatic():
                return cls(data=_fill_monostatic(metadata=metadata, data=data))
            case TimeGridInfo.Bistatic():
                return cls(data=_fill_bistatic(metadata=metadata, data=data))
            case TimeGridInfo.BistaticSingleSystem():
                return cls(data=_fill_bistatic_single_system(metadata=metadata, data=data))
            case _:
                msg = f"Unsupported time grid info type: {type(data)!r}"
                raise TypeError(msg)
