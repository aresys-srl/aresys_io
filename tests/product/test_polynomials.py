# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

from dataclasses import dataclass
from math import isclose

import numpy as np
from perseo_core.timing import PreciseDateTime

from aresys_io.product.polynomials import (
    PiecewisePolynomial2D,
    PiecewisePolynomialPair2D,
    Polynomial2D,
    PolynomialPair2D,
)
from aresys_io.product_metadata.metadata_elements import (
    CoregPoly,
    CoregPolyVector,
    DopplerCentroid,
    DopplerCentroidVector,
    DopplerRate,
)


@dataclass(frozen=True)
class PolyData:
    ref_az: PreciseDateTime
    ref_rg: float
    coefficients: list[float]


@dataclass(frozen=True)
class PolynomialPairData:
    ref_az: PreciseDateTime
    ref_rg: float
    coefficients_az: list[float]
    coefficients_rg: list[float]


POLY_DATA_SORTED_FIRST = PolyData(
    ref_az=PreciseDateTime.from_utc_string("09-JUL-2006 20:59:00.0"),
    ref_rg=8.0,
    coefficients=[5.5, 6.0, 0.0, 0.0, 1.0, 1.0, 0.5],
)

POLY_DATA_SORTED_SECOND = PolyData(
    ref_az=PreciseDateTime.from_utc_string("09-JUL-2006 21:00:00.0"),
    ref_rg=2.0,
    coefficients=[2.5, 2.5, 0.0, -1.0, 0.5, 0.0, 0.0],
)

POLYNOMIAL_PAIR_DATA_SORTED_FIRST = PolynomialPairData(
    ref_az=PreciseDateTime.from_utc_string("09-JUL-2006 20:59:00.0"),
    ref_rg=8.0,
    coefficients_az=[5.5, 6.0, 0.0, 0.0],
    coefficients_rg=[0.5, -2.0, 1.0, 0.0],
)

POLYNOMIAL_PAIR_DATA_SORTED_SECOND = PolynomialPairData(
    ref_az=PreciseDateTime.from_utc_string("09-JUL-2006 21:00:00.0"),
    ref_rg=2.0,
    coefficients_az=[2.5, 2.5, 0.0, -1.0],
    coefficients_rg=[1.0, 0.5, -1.0, 2.0],
)


def _poly_powers(size: int) -> list[tuple[int, int]]:
    return list(
        zip(
            DopplerRate.POWERS_X[:size],
            DopplerRate.POWERS_Y[:size],
            strict=False,
        ),
    )


def _polynomial2d_from_data(poly_data: PolyData) -> Polynomial2D:
    return Polynomial2D(
        reference_values=(poly_data.ref_az, poly_data.ref_rg),
        coefficient_matrix=_poly_matrix(poly_data.coefficients),
    )


def _doppler_rate_from_data(poly_data: PolyData) -> DopplerRate:
    return DopplerRate(
        t_ref_az=poly_data.ref_az,
        t_ref_rg=poly_data.ref_rg,
        coefficients=poly_data.coefficients,
    )


def _doppler_centroid_vector_from_data(poly_data_list: list[PolyData]) -> DopplerCentroidVector:
    vector = DopplerCentroidVector()
    vector.poly_list = [
        DopplerCentroid(
            t_ref_az=poly_data.ref_az,
            t_ref_rg=poly_data.ref_rg,
            coefficients=poly_data.coefficients,
        )
        for poly_data in poly_data_list
    ]
    return vector


def _metadata_polynomial_pair_from_data(poly_data: PolynomialPairData) -> CoregPoly:
    return CoregPoly(
        t_ref_az=poly_data.ref_az,
        t_ref_rg=poly_data.ref_rg,
        coefficients_az=poly_data.coefficients_az,
        coefficients_rg=poly_data.coefficients_rg,
    )


def _polynomial_pair_vector_from_data(
    poly_data_list: list[PolynomialPairData],
) -> CoregPolyVector:
    vector = CoregPolyVector()
    vector.poly_list = [
        _metadata_polynomial_pair_from_data(poly_data) for poly_data in poly_data_list
    ]
    return vector


def _sorted_polynomial_pairs(
    sorted_poly_list: PiecewisePolynomialPair2D,
) -> list[PolynomialPair2D]:
    return sorted_poly_list._sorted_poly_list


def _sorted_polys(sorted_poly_list: PiecewisePolynomial2D) -> list[Polynomial2D]:
    return sorted_poly_list._sorted_poly_list


def _poly_matrix(coefficients: list[float]) -> np.ndarray:
    selected_powers = _poly_powers(len(coefficients))
    coefficient_matrix = np.zeros(
        (
            max(power_x for power_x, _ in selected_powers) + 1,
            max(power_y for _, power_y in selected_powers) + 1,
        ),
        dtype=float,
    )
    for coefficient, (power_x, power_y) in zip(coefficients, selected_powers, strict=False):
        coefficient_matrix[power_x, power_y] = coefficient
    return coefficient_matrix


def test_init() -> None:
    polynomial2d = _polynomial2d_from_data(POLY_DATA_SORTED_FIRST)

    assert polynomial2d.reference_values[0] == POLY_DATA_SORTED_FIRST.ref_az
    assert polynomial2d.reference_values[1] == POLY_DATA_SORTED_FIRST.ref_rg
    assert np.array_equal(
        polynomial2d.coefficient_matrix,
        _poly_matrix(POLY_DATA_SORTED_FIRST.coefficients),
    )


def test_evaluate() -> None:
    polynomial2d = _polynomial2d_from_data(POLY_DATA_SORTED_SECOND)

    result = polynomial2d.evaluate(
        (PreciseDateTime.from_utc_string("09-JUL-2006 21:00:03.0"), 4.0),
    )

    assert isclose(result, 3.5)


def test_from_metadata() -> None:
    poly = _doppler_rate_from_data(POLY_DATA_SORTED_SECOND)

    polynomial2d = Polynomial2D.from_metadata(poly)

    assert polynomial2d.reference_values == (
        POLY_DATA_SORTED_SECOND.ref_az,
        POLY_DATA_SORTED_SECOND.ref_rg,
    )
    assert np.array_equal(
        polynomial2d.coefficient_matrix,
        _poly_matrix(POLY_DATA_SORTED_SECOND.coefficients),
    )


def test_sorted_poly_list_from_metadata() -> None:
    poly_list = _doppler_centroid_vector_from_data(
        [POLY_DATA_SORTED_SECOND, POLY_DATA_SORTED_FIRST],
    )

    sorted_poly_list = PiecewisePolynomial2D.from_metadata(poly_list)
    sorted_polys = _sorted_polys(sorted_poly_list)

    assert np.array_equal(
        sorted_polys[0].coefficient_matrix,
        _poly_matrix(POLY_DATA_SORTED_FIRST.coefficients),
    )
    assert np.array_equal(
        sorted_polys[1].coefficient_matrix,
        _poly_matrix(POLY_DATA_SORTED_SECOND.coefficients),
    )


def test_from_metadata_sorts_and_selects_previous_poly() -> None:
    poly_list = _doppler_centroid_vector_from_data(
        [POLY_DATA_SORTED_SECOND, POLY_DATA_SORTED_FIRST],
    )

    sorted_poly_list = PiecewisePolynomial2D.from_metadata(poly_list)

    assert [poly.reference_values[0] for poly in _sorted_polys(sorted_poly_list)] == [
        POLY_DATA_SORTED_FIRST.ref_az,
        POLY_DATA_SORTED_SECOND.ref_az,
    ]
    assert isclose(
        sorted_poly_list.evaluate(
            (PreciseDateTime.from_utc_string("09-JUL-2006 21:00:03.0"), 4.0),
        ),
        3.5,
    )
    assert isclose(
        sorted_poly_list.evaluate(
            (PreciseDateTime.from_utc_string("09-JUL-2006 20:59:07.0"), 4.0),
        ),
        61.5,
    )


def test_init_sorts_poly_list() -> None:
    sorted_poly_list = PiecewisePolynomial2D(
        _sorted_poly_list=[
            _polynomial2d_from_data(POLY_DATA_SORTED_SECOND),
            _polynomial2d_from_data(POLY_DATA_SORTED_FIRST),
        ],
    )
    sorted_polys = _sorted_polys(sorted_poly_list)

    assert np.array_equal(
        sorted_polys[0].coefficient_matrix,
        _poly_matrix(POLY_DATA_SORTED_FIRST.coefficients),
    )
    assert np.array_equal(
        sorted_polys[1].coefficient_matrix,
        _poly_matrix(POLY_DATA_SORTED_SECOND.coefficients),
    )


def test_polynomial_pair_from_metadata() -> None:
    polynomial_pair = PolynomialPair2D.from_metadata(
        _metadata_polynomial_pair_from_data(POLYNOMIAL_PAIR_DATA_SORTED_SECOND),
    )

    assert polynomial_pair.ref_azimuth_time == POLYNOMIAL_PAIR_DATA_SORTED_SECOND.ref_az
    assert polynomial_pair.ref_range_time == POLYNOMIAL_PAIR_DATA_SORTED_SECOND.ref_rg
    assert np.array_equal(
        polynomial_pair.azimuth_poly.coefficient_matrix,
        _poly_matrix(POLYNOMIAL_PAIR_DATA_SORTED_SECOND.coefficients_az),
    )
    assert np.array_equal(
        polynomial_pair.range_poly.coefficient_matrix,
        _poly_matrix(POLYNOMIAL_PAIR_DATA_SORTED_SECOND.coefficients_rg),
    )


def test_polynomial_pair_evaluate() -> None:
    polynomial_pair = PolynomialPair2D.from_metadata(
        _metadata_polynomial_pair_from_data(POLYNOMIAL_PAIR_DATA_SORTED_SECOND),
    )

    azimuth_result, range_result = polynomial_pair.evaluate(
        (PreciseDateTime.from_utc_string("09-JUL-2006 21:00:03.0"), 4.0),
    )

    assert isclose(azimuth_result, 1.5)
    assert isclose(range_result, 11.0)


def test_piecewise_polynomial_pair_from_metadata() -> None:
    sorted_poly_list = PiecewisePolynomialPair2D.from_metadata(
        _polynomial_pair_vector_from_data(
            [POLYNOMIAL_PAIR_DATA_SORTED_SECOND, POLYNOMIAL_PAIR_DATA_SORTED_FIRST],
        ),
    )

    sorted_polys = _sorted_polynomial_pairs(sorted_poly_list)

    assert np.array_equal(
        sorted_polys[0].azimuth_poly.coefficient_matrix,
        _poly_matrix(POLYNOMIAL_PAIR_DATA_SORTED_FIRST.coefficients_az),
    )
    assert np.array_equal(
        sorted_polys[1].range_poly.coefficient_matrix,
        _poly_matrix(POLYNOMIAL_PAIR_DATA_SORTED_SECOND.coefficients_rg),
    )


def test_piecewise_polynomial_pair_init_and_evaluate() -> None:
    sorted_poly_list = PiecewisePolynomialPair2D(
        _sorted_poly_list=[
            PolynomialPair2D.from_metadata(
                _metadata_polynomial_pair_from_data(POLYNOMIAL_PAIR_DATA_SORTED_SECOND),
            ),
            PolynomialPair2D.from_metadata(
                _metadata_polynomial_pair_from_data(POLYNOMIAL_PAIR_DATA_SORTED_FIRST),
            ),
        ],
    )

    assert [poly.ref_azimuth_time for poly in _sorted_polynomial_pairs(sorted_poly_list)] == [
        POLYNOMIAL_PAIR_DATA_SORTED_FIRST.ref_az,
        POLYNOMIAL_PAIR_DATA_SORTED_SECOND.ref_az,
    ]
    azimuth_result, range_result = sorted_poly_list.evaluate(
        (PreciseDateTime.from_utc_string("09-JUL-2006 21:00:03.0"), 4.0),
    )
    assert isclose(azimuth_result, 1.5)
    assert isclose(range_result, 11.0)

    azimuth_result, range_result = sorted_poly_list.evaluate(
        (PreciseDateTime.from_utc_string("09-JUL-2006 20:59:07.0"), 4.0),
    )
    assert isclose(azimuth_result, -18.5)
    assert isclose(range_result, 15.5)
