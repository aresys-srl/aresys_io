# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Generated module."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class PointTargetsTargetType(Enum):
    VALUE_0 = 0
    VALUE_1 = 1
    VALUE_2 = 2


@dataclass(kw_only=True)
class ValType:
    class Meta:
        name = "valType"

    value: float = field()
    n: int = field(
        metadata={
            "name": "N",
            "type": "Attribute",
        }
    )


@dataclass(kw_only=True)
class ValTypeComplex:
    class Meta:
        name = "valTypeComplex"

    re: float = field(
        metadata={
            "type": "Element",
        }
    )
    im: float = field(
        metadata={
            "type": "Element",
        }
    )
    n: int = field(
        metadata={
            "name": "N",
            "type": "Attribute",
        }
    )


@dataclass(kw_only=True)
class Rcstype:
    class Meta:
        name = "RCSType"

    val: list[ValTypeComplex] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 2,
            "max_occurs": 2,
        },
    )


@dataclass(kw_only=True)
class TargetTagType:
    coord: TargetTagType.Coord = field(
        metadata={
            "name": "Coord",
            "type": "Element",
        }
    )
    rcs_h: Rcstype = field(
        metadata={
            "name": "RCS_H",
            "type": "Element",
        }
    )
    rcs_v: Rcstype = field(
        metadata={
            "name": "RCS_V",
            "type": "Element",
        }
    )
    delay: TargetTagType.Delay = field(
        metadata={
            "name": "Delay",
            "type": "Element",
        }
    )
    number: int = field(
        metadata={
            "name": "Number",
            "type": "Attribute",
        }
    )

    @dataclass(kw_only=True)
    class Coord:
        val: list[ValType] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "min_occurs": 3,
                "max_occurs": 3,
            },
        )

    @dataclass(kw_only=True)
    class Delay:
        val: ValType = field(
            metadata={
                "type": "Element",
            }
        )


@dataclass(kw_only=True)
class PointTargets:
    """
    Parameters
    ----------
    target_type
        0: LLH, 1: ECEF, 2: Normalized
    target
    ntarget
    """

    target_type: PointTargetsTargetType = field(
        metadata={
            "name": "TargetType",
            "type": "Element",
        }
    )
    target: list[TargetTagType] = field(
        default_factory=list,
        metadata={
            "name": "Target",
            "type": "Element",
            "min_occurs": 1,
        },
    )
    ntarget: int = field(
        metadata={
            "name": "Ntarget",
            "type": "Element",
        }
    )
