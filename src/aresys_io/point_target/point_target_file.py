# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Point Target File Module."""

import operator
from pathlib import Path
from typing import Literal

import numpy as np
from perseo_core.geometry.coordinates import llh2xyz

from aresys_io.core.parsing import parse, serialize
from aresys_io.point_target import models
from aresys_io.point_target.nominal_point_targets import NominalPointTarget

IDLike = int | str
ListIDLike = list[int] | list[str] | list[IDLike]
CoordinatesTypeLiteral = Literal["ECEF", "LLH", "Normalized"]
CoordinatesTypeLike = CoordinatesTypeLiteral | Literal[0, 1, 2]

_TARGET_TYPE_TO_XML_VALUE: dict[CoordinatesTypeLike, int] = {
    "LLH": 0,
    "ECEF": 1,
    "Normalized": 2,
    0: 0,
    1: 1,
    2: 2,
}
_XML_VALUE_TO_TARGET_TYPE: dict[int, CoordinatesTypeLiteral] = {
    0: "LLH",
    1: "ECEF",
    2: "Normalized",
}


def read_point_targets_file(xml_file: str | Path) -> dict[str, NominalPointTarget]:
    """Read a point target XML file information about point target location, rcs and delay.

    Parameters
    ----------
    xml_file : str | Path
        path to the XML point targets file

    Returns
    -------
    dict[str, NominalPointTarget]
        Dict of NominalPointTarget dataclasses, one for each target id detected (id are the keys)
    """
    parsed_xml = _parse_point_targets(xml_path=xml_file)
    return _translate_point_target_file_from_model(data_model=parsed_xml)


def write_point_targets_file(
    filename: str | Path,
    point_targets: list[NominalPointTarget] | NominalPointTarget,
    target_type: CoordinatesTypeLike,
    point_targets_ids: IDLike | ListIDLike | None = None,
) -> None:
    """Write PointTargetFile XML to disk based on input point targets data.

    Parameters
    ----------
    filename : str | Path
        path to the xml file to be written, xml suffix must be included
    point_targets : list[NominalPointTarget] | NominalPointTarget
        list of NominalPointTarget point targets to be written or single NominalPointTarget object
    target_type : CoordinatesTypeLike
        coordinate type as string literal ("LLH"/"ECEF"/"Normalized") or integer (0/1/2)
    point_targets_ids : IDLike | ListIDLike, optional
        list of point target IDs as integers or integers-like strings, if None IDs are created
        starting from 1 to the actual number of point targets elements provided, by default None.

    Raises
    ------
    RuntimeError
        if the file already exists
    RuntimeError
        if the file extension is not .xml
    RuntimeError
        if the number of point targets and provided IDs do not match
    """
    filename = Path(filename)

    if filename.exists():
        msg = f"Path already exists {filename}"
        raise RuntimeError(msg)

    if filename.suffix != ".xml":
        msg = f"File extension is not XML {filename}"
        raise RuntimeError(msg)

    if isinstance(point_targets, NominalPointTarget):
        point_targets = [point_targets]

    if point_targets_ids is None:
        point_targets_ids = list(range(1, len(point_targets) + 1))
    elif isinstance(point_targets_ids, (int, str)):
        point_targets_ids = [point_targets_ids]

    if len(point_targets_ids) != len(point_targets):
        msg = (
            f"point targets number {len(point_targets)} !="
            f" point target ids number {len(point_targets_ids)}"
        )
        raise RuntimeError(msg)

    point_target_nodes = [
        _translate_nominal_point_target_to_model(data=p[0], data_id=int(p[1]))
        for p in zip(point_targets, point_targets_ids, strict=False)
    ]

    main_node = models.PointTargets(
        target_type=models.PointTargetsTargetType(_TARGET_TYPE_TO_XML_VALUE[target_type]),
        target=point_target_nodes,
        ntarget=len(point_target_nodes),
    )

    xml_string = serialize(main_node)
    filename.write_text(xml_string, encoding="utf-8")


def _parse_point_targets(xml_path: str | Path) -> models.PointTargets:
    """Parse Point Target File XML using the xsdata model generated from the original XSD file.

    Parameters
    ----------
    xml_path : str | Path
        path to the XML file.

    Returns
    -------
    models.PointTargets
        point target XML document as a PointTargets dataclass
    """
    xml = Path(xml_path).read_text(encoding="utf-8")
    return parse(xml_string=xml, model=models.PointTargets)


def _translate_point_target_file_from_model(
    data_model: models.PointTargets,
) -> dict[str, NominalPointTarget]:
    """Translate the PointTargets node parsed from XML file to a dict of NominalPointTarget.

    Parameters
    ----------
    data_model : models.PointTargets
        PointTargets dataclass model node from parsing xml file

    Returns
    -------
    Dict[str, NominalPointTarget]
        dict of NominalPointTarget objects as values, key are the corresponding target IDs
    """
    raw_target_type = data_model.target_type.value
    coord_type = _XML_VALUE_TO_TARGET_TYPE[raw_target_type]

    return dict(
        [
            _translate_model_to_nominal_point_targets(target, coord_type=coord_type)
            for target in data_model.target
        ],
    )


def _translate_model_to_nominal_point_targets(
    target: models.TargetTagType,
    coord_type: CoordinatesTypeLiteral,
) -> tuple[str, NominalPointTarget]:
    """Conversion function from TargetType xsdata model dataclass to NominalPointTarget dataclass.

    If coordinates are expressed in LLH format, they are converted to ECEF.
    Returning also the point target ID.

    Parameters
    ----------
    target : models.TargetTagType
        xsdata model TargetTagType from xml parsing
    coord_type : CoordinatesTypeLiteral
        coordinate type of each target point

    Returns
    -------
    Tuple[str, NominalPointTarget]
        target id,
        target dataclass
    """
    if coord_type == "Normalized":
        msg = "Point Target normalized coordinates not supported"
        raise NotImplementedError(msg)

    coord = np.asarray(_translate_coord_from_model(target.coord), dtype=np.float64)
    if coord_type == "LLH":
        coord = llh2xyz(coord).astype(np.float64)

    rcs_hh, rcs_hv = _translate_rcs_from_model(target.rcs_h)
    rcs_vv, rcs_vh = _translate_rcs_from_model(target.rcs_v)

    point_target = NominalPointTarget(
        xyz_coordinates=coord,
        rcs_hh=np.complex128(rcs_hh),
        rcs_hv=np.complex128(rcs_hv),
        rcs_vv=np.complex128(rcs_vv),
        rcs_vh=np.complex128(rcs_vh),
        delay=target.delay.val.value,
    )

    return str(target.number), point_target


def _translate_nominal_point_target_to_model(
    data: NominalPointTarget,
    data_id: int,
) -> models.TargetTagType:
    """Convert custom NominalPointTarget to TargetType model dataclass for writing purposes.

    Parameters
    ----------
    data : NominalPointTarget
        point target data in custom NominalPointTarget form
    data_id : int
        point target id number.

    Returns
    -------
    models.TargetType
        TargetType xsdata model dataclass corresponding to input information
    """
    return models.TargetTagType(
        coord=models.TargetTagType.Coord(
            val=[
                models.ValType(value=float(data.xyz_coordinates[0]), n=1),
                models.ValType(value=float(data.xyz_coordinates[1]), n=2),
                models.ValType(value=float(data.xyz_coordinates[2]), n=3),
            ],
        ),
        rcs_h=models.Rcstype(
            val=[
                models.ValTypeComplex(re=float(data.rcs_hh.real), im=float(data.rcs_hh.imag), n=1),
                models.ValTypeComplex(re=float(data.rcs_hv.real), im=float(data.rcs_hv.imag), n=2),
            ],
        ),
        rcs_v=models.Rcstype(
            val=[
                models.ValTypeComplex(re=float(data.rcs_vv.real), im=float(data.rcs_vv.imag), n=1),
                models.ValTypeComplex(re=float(data.rcs_vh.real), im=float(data.rcs_vh.imag), n=2),
            ],
        ),
        delay=models.TargetTagType.Delay(val=models.ValType(value=data.delay or 0.0, n=1)),
        number=data_id,
    )


def _translate_rcs_from_model(data_model: models.Rcstype) -> tuple[complex, complex]:
    """Convert input RCS model dataclass to rcs values.

    Parameters
    ----------
    data_model : models.Rcstype
        target rcs data model.

    Returns
    -------
    Tuple[complex, complex]
        rcs co-polarization,
        rcs cross-polarization
    """
    rcs = [(r.re + 1j * r.im, r.n) for r in data_model.val]
    rcs.sort(key=operator.itemgetter(-1))
    assert len(rcs) == 2
    return rcs[0][0], rcs[1][0]


def _translate_coord_from_model(
    data_model: models.TargetTagType.Coord,
) -> tuple[float, float, float]:
    """Convert input model dataclass to list of point target coordinates.

    Parameters
    ----------
    data_model : models.TargetTagType.Coord
        target type coord data model.

    Returns
    -------
    tuple[float, float, float]
        tuple of coordinates (x1, x2, x3) depending on the coordinate type (LLH/ECEF/Normalized)
    """
    coords = [(d.value, d.n) for d in data_model.val]
    coords.sort(key=operator.itemgetter(-1))

    assert len(coords) == 3
    return coords[0][0], coords[1][0], coords[2][0]


__all__ = ["read_point_targets_file", "write_point_targets_file"]
