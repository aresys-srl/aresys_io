# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""sarsystem utils."""

from typing import TypeAlias

import numpy as np
from numpydantic import NDArray, Shape
from perseo_core.geometry.pointing import (
    RotationOrder,
    euler_angles_to_rotation,
    rotation_to_euler_angles,
)
from scipy.spatial.transform import Rotation

from aresys_io.sarsystem.models import time_line_table as model_timeline
from aresys_io.sarsystem.models import trajectory_file as model_trajectory

# Shape typing
VectorShape: TypeAlias = Shape["*"]  # ruff: ignore[forward-annotation-syntax-error]  # pyright: ignore[reportInvalidTypeArguments]  # pyrefly: ignore[not-a-type]
Vector: TypeAlias = NDArray[VectorShape, np.float32 | np.float64]  # pyright: ignore[reportInvalidTypeArguments]
QuaternionShape: TypeAlias = Shape["*, 4"]  # ruff: ignore[forward-annotation-syntax-error]  # pyright: ignore[reportInvalidTypeArguments]  # pyrefly: ignore[not-a-type]
Quaternion: TypeAlias = NDArray[QuaternionShape, np.float32 | np.float64]  # pyright: ignore[reportInvalidTypeArguments]
StateVectorShape: TypeAlias = Shape["*, 3"]  # ruff: ignore[forward-annotation-syntax-error]  # pyright: ignore[reportInvalidTypeArguments]  # pyrefly: ignore[not-a-type]
StateVector: TypeAlias = NDArray[StateVectorShape, np.float32 | np.float64]  # pyright: ignore[reportInvalidTypeArguments]
SingleStateVectorShape: TypeAlias = Shape["3"]  # ruff: ignore[quoted-type-alias]  # pyright: ignore[reportInvalidTypeArguments]  # pyrefly: ignore[not-a-type]
SingleStateVector: TypeAlias = NDArray[SingleStateVectorShape, np.float32 | np.float64]  # pyright: ignore[reportInvalidTypeArguments]
VectorInt: TypeAlias = NDArray[VectorShape, np.int64]  # pyright: ignore[reportInvalidTypeArguments]


def index_type_to_array(
    index: model_timeline.IndexType,
) -> VectorInt:
    """Convert a IndexType object to a NumPy array."""
    values = np.zeros(len(index.val), dtype=np.int64)
    for position_index, item in enumerate(index.val):
        values[position_index] = item.value

    return values


def ypr_to_quaternion(
    yaw_deg_vec: Vector,
    pitch_deg_vec: Vector,
    roll_deg_vec: Vector,
    rotation_order: RotationOrder = "YPR",
) -> Quaternion:
    """
    Compute quaternion rotations from yaw, pitch, and roll angles (in degrees).

    Parameters
    ----------
    yaw_deg_vec : NDArray
        Array of yaw angles in degrees.
    pitch_deg_vec : NDArray
        Array of pitch angles in degrees.
    roll_deg_vec : NDArray
        Array of roll angles in degrees.
    rotation_order : RotationOrder, optional
        The order of rotations (default is YPR).

    Returns
    -------
    NDArray
        Array of quaternions (shape: [N, 4]), where the last component is the scalar.
    """
    rotation = euler_angles_to_rotation(
        order=rotation_order,
        ypr_rad=np.stack(
            [
                np.deg2rad(yaw_deg_vec),
                np.deg2rad(pitch_deg_vec),
                np.deg2rad(roll_deg_vec),
            ],
            axis=-1,
        ),
    )
    return rotation.as_quat()


def value_array_type_to_array(
    index: model_trajectory.ValueArrayType,
) -> Vector:
    """Convert a ValueArrayType object to a NumPy array."""
    values = np.zeros(len(index.val))
    for position_index, item in enumerate(index.val):
        values[position_index] = item.value

    return values


def quaternion_to_ypr(
    quaternions: Quaternion,
) -> tuple[
    Vector,
    Vector,
    Vector,
]:
    """
    Convert quaternion(s) to yaw, pitch, and roll angles (in degrees).

    Parameters
    ----------
    quaternions : np.ndarray
        An array of shape (N, 4), where each quaternion is in scalar-last (x, y, z, w) format.

    Returns
    -------
    yaw_deg_vec : np.ndarray (N,)
        Yaw angles in degrees.
    pitch_deg_vec : np.ndarray (N,)
        Pitch angles in degrees.
    roll_deg_vec : np.ndarray (N,)
        Roll angles in degrees.
    """
    rotation = Rotation.from_quat(quaternions)
    ypr_matrix = rotation_to_euler_angles(rotation=rotation, order="YPR")
    yaw_deg_vec = np.rad2deg(ypr_matrix[:, 0])
    pitch_deg_vec = np.rad2deg(ypr_matrix[:, 1])
    roll_deg_vec = np.rad2deg(ypr_matrix[:, 2])
    return yaw_deg_vec, pitch_deg_vec, roll_deg_vec
