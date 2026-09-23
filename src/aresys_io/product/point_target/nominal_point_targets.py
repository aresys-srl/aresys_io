# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Nominal point target structure definition."""

from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

__all__ = ["NominalPointTarget", "convert_array_to_point_target_structure"]


@dataclass
class NominalPointTarget:
    """Nominal Point Target."""

    xyz_coordinates: npt.NDArray[np.float64]
    rcs_hh: np.complex128
    rcs_vv: np.complex128
    rcs_vh: np.complex128
    rcs_hv: np.complex128
    delay: float | None = None


def convert_array_to_point_target_structure(
    coords: np.ndarray,
    rcs: np.ndarray,
    point_target_ids: list[str] | None = None,
) -> dict[str, NominalPointTarget]:
    """Convert coordinates and rcs arrays to an array of structures.

    Parameters
    ----------
    coords : np.ndarray
        point target coordinates, in the form (N, 3)
    rcs : np.ndarray
        point target rcs values (HH, HV, VH, VV), in the form (N, 4)
    point_target_ids : list[str] | None, optional
        optional list of point target id labels, by default None

    Returns
    -------
    Dict[str, NominalPointTarget]
        keys are the target ID, values are the corresponding NominalPointTarget objects

    Raises
    ------
    RuntimeError
        if coordinates shape is wrong
    RuntimeError
        if rcs shape is wrong
    RuntimeError
        if coordinates shape does not match rcs shape
    RuntimeError
        if point targets ids shape does not match coordinates shape
    """
    coords = np.atleast_2d(coords)
    rcs = np.atleast_2d(rcs)

    if coords.shape[1] != 3:
        msg = f"Wrong shape: {coords.shape[1]} != 3"
        raise RuntimeError(msg)

    if rcs.shape[1] != 4:
        msg = f"Wrong shape: {rcs.shape[1]} != 4"
        raise RuntimeError(msg)

    if coords.shape[0] != rcs.shape[0]:
        msg = f"number of coordinates {coords.shape[0]} != number of rcs {rcs.shape[0]}"
        raise RuntimeError(
            msg,
        )

    if point_target_ids is None:
        point_target_ids = [str(p) for p in range(coords.shape[0])]

    if coords.shape[0] != len(point_target_ids):
        msg = f"number of coordinates {coords.shape[0]} != number of ids {len(point_target_ids)}"
        raise RuntimeError(
            msg,
        )

    out = {}
    for index, coord in enumerate(coords):
        out[point_target_ids[index]] = NominalPointTarget(
            xyz_coordinates=coord,
            rcs_hh=rcs[index][0],
            rcs_hv=rcs[index][1],
            rcs_vh=rcs[index][2],
            rcs_vv=rcs[index][3],
        )

    return out
