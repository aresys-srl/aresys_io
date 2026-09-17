# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""2D polynomial helpers built from current product metadata."""

from __future__ import annotations

import bisect
from dataclasses import dataclass, field
from typing import Generic, TypeAlias

import numpy as np
from perseo_core.timing import PreciseDateTime

from aresys_io.product_metadata.metadata_elements import (
    CoregPoly,
    CoregPolyVector,
    DopplerCentroidVector,
    DopplerRateVector,
    GroundToSlantVector,
    Poly2D,
    ReferenceAzimuthTimeT,
    SlantToElevationVector,
    SlantToGroundVector,
    SlantToIncidenceVector,
    TopsAzimuthModulationRateVector,
)

AzimuthReference: TypeAlias = PreciseDateTime | float
EvaluationPoint: TypeAlias = tuple[AzimuthReference, float]
PolynomialPairEvaluationPoint: TypeAlias = EvaluationPoint
PolynomialPairEvaluationResult: TypeAlias = tuple[float, float]
Poly2DVector: TypeAlias = (
    DopplerCentroidVector
    | DopplerRateVector
    | TopsAzimuthModulationRateVector
    | SlantToGroundVector
    | GroundToSlantVector
    | SlantToIncidenceVector
    | SlantToElevationVector
)
PolynomialPairVector: TypeAlias = CoregPolyVector


@dataclass(frozen=True, eq=False)
class Polynomial2D(Generic[ReferenceAzimuthTimeT]):
    """2D polynomial built from a metadata ``Poly2D`` instance."""

    reference_values: tuple[ReferenceAzimuthTimeT, float]
    coefficient_matrix: np.ndarray = field(
        default_factory=lambda: np.zeros((0, 0), dtype=float),
    )

    __hash__ = None

    def __eq__(self, other: object) -> bool:
        """Check equality of reference values and coefficient matrix."""
        if not isinstance(other, Polynomial2D):
            return False
        return self.reference_values == other.reference_values and np.array_equal(
            self.coefficient_matrix, other.coefficient_matrix
        )

    @property
    def ref_azimuth_time(self) -> ReferenceAzimuthTimeT:
        """Reference azimuth value or time."""
        return self.reference_values[0]

    @property
    def ref_range_time(self) -> float:
        """Reference range value or time."""
        return self.reference_values[1]

    @classmethod
    def from_metadata(
        cls: type[Polynomial2D[ReferenceAzimuthTimeT]],
        poly2d: Poly2D[ReferenceAzimuthTimeT],
    ) -> Polynomial2D[ReferenceAzimuthTimeT]:
        """Create a 2D polynomial from product metadata."""
        return cls(
            reference_values=(poly2d.t_ref_az, poly2d.t_ref_rg),
            coefficient_matrix=_coefficients_to_matrix(
                coefficients=poly2d.coefficients,
                powers_x=poly2d.POWERS_X,
                powers_y=poly2d.POWERS_Y,
            ),
        )

    def evaluate(
        self,
        values: tuple[ReferenceAzimuthTimeT, float],
    ) -> float:
        """Evaluate the polynomial at the provided azimuth and range values."""
        azimuth_value, range_value = values
        reference_azimuth = self.reference_values[0]
        azimuth_delta: float = azimuth_value - reference_azimuth  # pyright: ignore[reportAssignmentType]

        range_delta = range_value - self.reference_values[1]
        return float(
            np.polynomial.polynomial.polyval2d(
                azimuth_delta,
                range_delta,
                self.coefficient_matrix,
            ),
        )


@dataclass(frozen=True)
class PiecewisePolynomial2D(Generic[ReferenceAzimuthTimeT]):
    """Piecewise 2D polynomial selection over azimuth reference values."""

    _sorted_poly_list: list[Polynomial2D[ReferenceAzimuthTimeT]] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Ensure the input list is always sorted after initialization."""
        object.__setattr__(
            self,
            "_sorted_poly_list",
            sorted(self._sorted_poly_list, key=lambda poly: poly.reference_values[0]),
        )

    @classmethod
    def from_metadata(
        cls: type[PiecewisePolynomial2D[ReferenceAzimuthTimeT]],
        poly2d_vector: Poly2DVector,
    ) -> PiecewisePolynomial2D[ReferenceAzimuthTimeT]:
        """Create a piecewise 2D polynomial from product metadata."""
        return cls(
            _sorted_poly_list=[
                Polynomial2D.from_metadata(poly) for poly in poly2d_vector.poly_list
            ],
        )

    def evaluate(
        self,
        values: tuple[ReferenceAzimuthTimeT, float],
    ) -> float:
        """Evaluate the polynomial selected by the reference coordinate."""
        if not self._sorted_poly_list:
            msg = "Cannot evaluate an empty PiecewisePolynomial2D"
            raise ValueError(msg)

        reference_value = values[0]
        idx = bisect.bisect_right(
            self._sorted_poly_list,
            reference_value,
            key=lambda poly: poly.reference_values[0],
        )
        selected_poly = self._sorted_poly_list[max(0, idx - 1)]
        return selected_poly.evaluate(values)


@dataclass(frozen=True)
class PolynomialPair2D:
    """Pair of 2D polynomials built from current product metadata."""

    azimuth_poly: Polynomial2D[PreciseDateTime]
    range_poly: Polynomial2D[PreciseDateTime]

    __hash__ = None

    @classmethod
    def from_metadata(cls, poly: CoregPoly) -> PolynomialPair2D:
        """Create a polynomial pair from product metadata."""
        reference_values = (poly.t_ref_az, poly.t_ref_rg)
        return cls(
            azimuth_poly=Polynomial2D(
                reference_values=reference_values,
                coefficient_matrix=_coefficients_to_matrix(
                    coefficients=poly.coefficients_az,
                    powers_x=Poly2D.POWERS_X,
                    powers_y=Poly2D.POWERS_Y,
                ),
            ),
            range_poly=Polynomial2D(
                reference_values=reference_values,
                coefficient_matrix=_coefficients_to_matrix(
                    coefficients=poly.coefficients_rg,
                    powers_x=Poly2D.POWERS_X,
                    powers_y=Poly2D.POWERS_Y,
                ),
            ),
        )

    @property
    def ref_azimuth_time(self) -> PreciseDateTime:
        """Shared reference azimuth time for both polynomials."""
        return self.azimuth_poly.reference_values[0]

    @property
    def ref_range_time(self) -> float:
        """Shared reference range time for both polynomials."""
        return self.azimuth_poly.reference_values[1]

    def evaluate(
        self,
        values: tuple[PreciseDateTime, float],
    ) -> PolynomialPairEvaluationResult:
        """Evaluate both polynomials at the provided azimuth and range values."""
        return self.azimuth_poly.evaluate(values), self.range_poly.evaluate(values)


@dataclass(frozen=True)
class PiecewisePolynomialPair2D:
    """Piecewise selection of paired 2D polynomials over azimuth references."""

    _sorted_poly_list: list[PolynomialPair2D] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Ensure the input list is always sorted after initialization."""
        object.__setattr__(
            self,
            "_sorted_poly_list",
            sorted(
                self._sorted_poly_list,
                key=lambda poly: poly.azimuth_poly.reference_values[0],
            ),
        )

    @classmethod
    def from_metadata(
        cls: type[PiecewisePolynomialPair2D],
        poly_vector: PolynomialPairVector,
    ) -> PiecewisePolynomialPair2D:
        """Create a piecewise polynomial pair from product metadata."""
        return cls(
            _sorted_poly_list=[
                PolynomialPair2D.from_metadata(poly) for poly in poly_vector.poly_list
            ],
        )

    def evaluate(
        self,
        values: tuple[PreciseDateTime, float],
    ) -> PolynomialPairEvaluationResult:
        """Evaluate the selected polynomial pair."""
        if not self._sorted_poly_list:
            msg = "Cannot evaluate an empty PiecewisePolynomialPair2D"
            raise ValueError(msg)

        reference_value = values[0]
        idx = bisect.bisect_right(
            self._sorted_poly_list,
            reference_value,
            key=lambda poly: poly.azimuth_poly.reference_values[0],
        )
        selected_poly = self._sorted_poly_list[max(0, idx - 1)]
        return selected_poly.evaluate(values)


def _coefficients_to_matrix(
    coefficients: list[float],
    powers_x: tuple[int, ...],
    powers_y: tuple[int, ...],
) -> np.ndarray:
    if not coefficients:
        return np.zeros((0, 0), dtype=float)

    selected_powers_x = powers_x[: len(coefficients)]
    selected_powers_y = powers_y[: len(coefficients)]
    coefficient_matrix = np.zeros(
        (max(selected_powers_x) + 1, max(selected_powers_y) + 1),
        dtype=float,
    )

    for coefficient, power_x, power_y in zip(
        coefficients,
        selected_powers_x,
        selected_powers_y,
        strict=False,
    ):
        coefficient_matrix[power_x, power_y] = coefficient

    return coefficient_matrix
