# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Time-grid trajectory metadata utilities."""

from dataclasses import dataclass
from typing import Self

import numpy as np
import numpy.typing as npt
from perseo_core.geometry.geocoding import (
    direct_geocoding_bistatic,
    direct_geocoding_monostatic,
    inverse_geocoding_bistatic,
    inverse_geocoding_monostatic,
)
from perseo_core.geometry.navigation import Trajectory
from perseo_core.timing.precise_datetime import PreciseDateTime

from aresys_io.product.metadata.channel import MetaData
from aresys_io.product.metadata.create_orbit import create_trajectory_from_state_vectors
from aresys_io.product.metadata.elements import SideLooking, TimeGridInfo


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


def time_grid_times_to_ground_points(
    trajectories: TimeGridTrajectories,
    look_direction: SideLooking,
    azimuth_times: PreciseDateTime | npt.NDArray,
    range_times: float | npt.NDArray[np.float64],
    altitude: float,
) -> npt.NDArray[np.floating]:
    """Convert time coordinates into ground points."""
    match trajectories.data:
        case Monostatic(trajectory=trajectory):
            return direct_geocoding_monostatic(
                sensor_positions=trajectory.position(azimuth_times),
                sensor_velocities=trajectory.velocity(azimuth_times),
                range_times=range_times,
                doppler_frequencies=0,
                wavelength=1,
                altitude=altitude,
                look_direction=look_direction,
            )
        case BistaticSingleSystem(trajectory=trajectory):
            # pyrefly: ignore [unsupported-operation]
            azimuth_times_tx = azimuth_times - range_times
            return direct_geocoding_bistatic(
                sensor_positions_rx=trajectory.position(azimuth_times),
                sensor_velocities_rx=trajectory.velocity(azimuth_times),
                sensor_positions_tx=trajectory.position(azimuth_times_tx),
                sensor_velocities_tx=trajectory.velocity(azimuth_times_tx),
                range_times=range_times,
                doppler_frequencies=0,
                wavelength=1,
                altitude=altitude,
                look_direction=look_direction,
            )
        case Bistatic(trajectory_rx=trajectory_rx, trajectory_tx=trajectory_tx):
            # pyrefly: ignore [unsupported-operation]
            azimuth_times_tx = azimuth_times - range_times
            return direct_geocoding_bistatic(
                sensor_positions_rx=trajectory_rx.position(azimuth_times),
                sensor_velocities_rx=trajectory_rx.velocity(azimuth_times),
                sensor_positions_tx=trajectory_tx.position(azimuth_times_tx),
                sensor_velocities_tx=trajectory_tx.velocity(azimuth_times_tx),
                range_times=range_times,
                doppler_frequencies=0,
                wavelength=1,
                altitude=altitude,
                look_direction=look_direction,
            )


def ground_points_to_time_grid_times(
    trajectories: TimeGridTrajectories,
    ground_points: npt.NDArray[np.floating],
) -> tuple[PreciseDateTime | np.datetime64 | npt.NDArray, float | npt.NDArray[np.floating]]:
    """Convert ground points into time coordinates."""
    match trajectories.data:
        case Monostatic(trajectory=trajectory):
            return inverse_geocoding_monostatic(
                trajectory=trajectory,
                ground_points=ground_points,
                doppler_frequencies=0,
                wavelength=1,
            )
        case BistaticSingleSystem(trajectory=trajectory):
            return inverse_geocoding_bistatic(
                trajectory_rx=trajectory,
                trajectory_tx=trajectory,
                ground_points=ground_points,
                doppler_frequencies=0,
                wavelength=1,
            )
        case Bistatic(trajectory_rx=trajectory_rx, trajectory_tx=trajectory_tx):
            return inverse_geocoding_bistatic(
                trajectory_rx=trajectory_rx,
                trajectory_tx=trajectory_tx,
                ground_points=ground_points,
                doppler_frequencies=0,
                wavelength=1,
            )
