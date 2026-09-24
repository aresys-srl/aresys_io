# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""2D polynomial helpers built from current product metadata."""

from __future__ import annotations

import bisect
from dataclasses import dataclass, field
from typing import Generic, TypeAlias, overload

import numpy as np
import numpy.typing as npt
from perseo_core.timing import PreciseDateTime

from aresys_io.product.metadata.elements import (
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

__all__ = [
    "CoregistrationPoly",
    "DopplerCentroidPoly",
    "DopplerRatePoly",
    "GroundToSlantPoly",
    "PiecewisePolynomial2D",
    "Polynomial2D",
    "PolynomialPair2D",
    "PolynomialPairEvaluationResult",
    "SlantToElevationPoly",
    "SlantToGroundPoly",
    "SlantToIncidencePoly",
    "TopsAzimuthModulationRatePoly",
]

PolynomialPairEvaluationResult: TypeAlias = (
    tuple[float, float] | tuple[npt.NDArray[np.floating], npt.NDArray[np.floating]]
)


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

    @overload
    def evaluate(
        self,
        azimuth_value: float,
        range_values: float,
    ) -> float: ...

    @overload
    def evaluate(
        self,
        azimuth_value: PreciseDateTime,
        range_values: float,
    ) -> float: ...

    @overload
    def evaluate(
        self,
        azimuth_value: float,
        range_values: npt.NDArray[np.floating],
    ) -> npt.NDArray[np.floating]: ...

    @overload
    def evaluate(
        self,
        azimuth_value: PreciseDateTime,
        range_values: npt.NDArray[np.floating],
    ) -> npt.NDArray[np.floating]: ...

    def evaluate(
        self,
        azimuth_value: ReferenceAzimuthTimeT,
        range_values: float | npt.NDArray[np.floating],
    ) -> float | npt.NDArray[np.floating]:
        """Evaluate the polynomial at the provided azimuth and range values."""
        azimuth_delta: float = azimuth_value - self.reference_values[0]  # pyright: ignore[reportAssignmentType]
        range_delta = range_values - self.reference_values[1]
        azimuth_delta_, range_delta_ = np.broadcast_arrays(
            azimuth_delta,
            range_delta,
        )
        values = np.polynomial.polynomial.polyval2d(
            azimuth_delta_,
            range_delta_,
            self.coefficient_matrix,
        )
        if isinstance(range_values, np.ndarray):
            return values
        return float(values)


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

    def evaluate(
        self,
        azimuth_value: ReferenceAzimuthTimeT,
        range_values: float | npt.NDArray[np.floating],
    ) -> float | npt.NDArray[np.floating]:
        """Evaluate the polynomial selected by the reference coordinate."""
        if not self._sorted_poly_list:
            msg = "Cannot evaluate an empty PiecewisePolynomial2D"
            raise ValueError(msg)

        idx = bisect.bisect_right(
            self._sorted_poly_list,
            azimuth_value,
            key=lambda poly: poly.reference_values[0],
        )
        selected_poly = self._sorted_poly_list[max(0, idx - 1)]
        return selected_poly.evaluate(azimuth_value, range_values)  # type: ignore[reportArgumentType]


@dataclass(frozen=True)
class DopplerCentroidPoly(PiecewisePolynomial2D[PreciseDateTime]):
    """Doppler centroid piecewise 2D polynomial."""

    @classmethod
    def from_metadata(
        cls: type[DopplerCentroidPoly],
        poly2d_vector: DopplerCentroidVector,
    ) -> DopplerCentroidPoly:
        """Create a Doppler centroid polynomial from product metadata."""
        return cls(
            _sorted_poly_list=[
                Polynomial2D.from_metadata(poly) for poly in poly2d_vector.poly_list
            ],
        )


@dataclass(frozen=True)
class DopplerRatePoly(PiecewisePolynomial2D[PreciseDateTime]):
    """Doppler rate piecewise 2D polynomial."""

    @classmethod
    def from_metadata(
        cls: type[DopplerRatePoly],
        poly2d_vector: DopplerRateVector,
    ) -> DopplerRatePoly:
        """Create a Doppler rate polynomial from product metadata."""
        return cls(
            _sorted_poly_list=[
                Polynomial2D.from_metadata(poly) for poly in poly2d_vector.poly_list
            ],
        )


@dataclass(frozen=True)
class SlantToGroundPoly(PiecewisePolynomial2D[PreciseDateTime]):
    """Slant-to-ground range piecewise 2D polynomial."""

    @classmethod
    def from_metadata(
        cls: type[SlantToGroundPoly],
        poly2d_vector: SlantToGroundVector,
    ) -> SlantToGroundPoly:
        """Create a slant-to-ground polynomial from product metadata."""
        return cls(
            _sorted_poly_list=[
                Polynomial2D.from_metadata(poly) for poly in poly2d_vector.poly_list
            ],
        )


@dataclass(frozen=True)
class GroundToSlantPoly(PiecewisePolynomial2D[PreciseDateTime]):
    """Ground-to-slant range piecewise 2D polynomial."""

    @classmethod
    def from_metadata(
        cls: type[GroundToSlantPoly],
        poly2d_vector: GroundToSlantVector,
    ) -> GroundToSlantPoly:
        """Create a ground-to-slant polynomial from product metadata."""
        return cls(
            _sorted_poly_list=[
                Polynomial2D.from_metadata(poly) for poly in poly2d_vector.poly_list
            ],
        )


@dataclass(frozen=True)
class SlantToIncidencePoly(PiecewisePolynomial2D[PreciseDateTime]):
    """Slant range to incidence angle piecewise 2D polynomial."""

    @classmethod
    def from_metadata(
        cls: type[SlantToIncidencePoly],
        poly2d_vector: SlantToIncidenceVector,
    ) -> SlantToIncidencePoly:
        """Create a slant-to-incidence polynomial from product metadata."""
        return cls(
            _sorted_poly_list=[
                Polynomial2D.from_metadata(poly) for poly in poly2d_vector.poly_list
            ],
        )


@dataclass(frozen=True)
class SlantToElevationPoly(PiecewisePolynomial2D[PreciseDateTime]):
    """Slant range to elevation angle piecewise 2D polynomial."""

    @classmethod
    def from_metadata(
        cls: type[SlantToElevationPoly],
        poly2d_vector: SlantToElevationVector,
    ) -> SlantToElevationPoly:
        """Create a slant-to-elevation polynomial from product metadata."""
        return cls(
            _sorted_poly_list=[
                Polynomial2D.from_metadata(poly) for poly in poly2d_vector.poly_list
            ],
        )


@dataclass(frozen=True)
class TopsAzimuthModulationRatePoly(PiecewisePolynomial2D[PreciseDateTime]):
    """TOPS azimuth modulation rate piecewise 2D polynomial."""

    @classmethod
    def from_metadata(
        cls: type[TopsAzimuthModulationRatePoly],
        poly2d_vector: TopsAzimuthModulationRateVector,
    ) -> TopsAzimuthModulationRatePoly:
        """Create a TOPS azimuth modulation rate polynomial from product metadata."""
        return cls(
            _sorted_poly_list=[
                Polynomial2D.from_metadata(poly) for poly in poly2d_vector.poly_list
            ],
        )


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
        azimuth_value: ReferenceAzimuthTimeT,
        range_values: float | npt.NDArray[np.floating],
    ) -> PolynomialPairEvaluationResult:
        """Evaluate both polynomials at the provided azimuth and range values."""
        az_values = self.azimuth_poly.evaluate(azimuth_value, range_values)  # type: ignore[reportArgumentType]
        rng_values = self.range_poly.evaluate(azimuth_value, range_values)  # type: ignore[reportArgumentType]
        return az_values, rng_values


@dataclass(frozen=True)
class CoregistrationPoly:
    """Piecewise coregistration polynomial pair selection over azimuth references."""

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
        cls: type[CoregistrationPoly],
        poly_vector: CoregPolyVector,
    ) -> CoregistrationPoly:
        """Create a coregistration polynomial from product metadata."""
        return cls(
            _sorted_poly_list=[
                PolynomialPair2D.from_metadata(poly) for poly in poly_vector.poly_list
            ],
        )

    def evaluate(
        self,
        azimuth_value: ReferenceAzimuthTimeT,
        range_values: float | npt.NDArray[np.floating],
    ) -> PolynomialPairEvaluationResult:
        """Evaluate the selected polynomial pair."""
        if not self._sorted_poly_list:
            msg = "Cannot evaluate an empty CoregistrationPoly"
            raise ValueError(msg)

        idx = bisect.bisect_right(
            self._sorted_poly_list,
            azimuth_value,
            key=lambda poly: poly.azimuth_poly.reference_values[0],
        )
        selected_poly = self._sorted_poly_list[max(0, idx - 1)]
        return selected_poly.evaluate(azimuth_value, range_values)


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
