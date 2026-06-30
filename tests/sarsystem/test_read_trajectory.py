# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""test read trajectory."""

from pathlib import Path

from aresys_io.sarsystem import read_trajectory
from aresys_io.sarsystem.trajectory_read import Trajectory


def test_open_file() -> None:
    filename = Path(__file__).parent.joinpath(
        "data",
        "input",
        "Stripmap_TerraSARX_Rome/Trajectory",
        "Trajectory.xml",
    )
    trajectory = read_trajectory(filename)
    assert isinstance(trajectory, Trajectory)


def test_shape_position() -> None:
    filename = Path(__file__).parent.joinpath(
        "data",
        "input",
        "Stripmap_TerraSARX_Rome/Trajectory",
        "Trajectory.xml",
    )
    trajectory = read_trajectory(filename)
    n_col = trajectory.state_vector.position.shape[1]
    assert n_col == 3


def test_shape_velocity() -> None:
    filename = Path(__file__).parent.joinpath(
        "data",
        "input",
        "Stripmap_TerraSARX_Rome/Trajectory",
        "Trajectory.xml",
    )
    trajectory = read_trajectory(filename)
    n_col = trajectory.state_vector.velocity.shape[1]
    assert n_col == 3


def test_count_ypr_equal_sv() -> None:
    filename = Path(__file__).parent.joinpath(
        "data",
        "input",
        "Stripmap_TerraSARX_Rome/Trajectory",
        "Trajectory.xml",
    )
    trajectory = read_trajectory(filename)
    n_attitude = trajectory.attitude_info.rotation.shape[0]  # number of attitude vector
    n_sv = trajectory.state_vector.position.shape[0]  # number of state vector
    assert n_attitude == n_sv
