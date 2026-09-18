# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Unit tests for metadata polynomials classes."""

from dataclasses import dataclass
from math import isclose

import numpy as np
import pytest
from perseo_core.timing import PreciseDateTime

from aresys_io.product.metadata import (
    CoregistrationPoly,
    DopplerCentroidPoly,
    DopplerRatePoly,
    GroundToSlantPoly,
    PiecewisePolynomial2D,
    Polynomial2D,
    PolynomialPair2D,
    SlantToElevationPoly,
    SlantToGroundPoly,
    SlantToIncidencePoly,
    TopsAzimuthModulationRatePoly,
)
from aresys_io.product.metadata.elements import (
    CoregPoly,
    CoregPolyVector,
    DopplerCentroid,
    DopplerCentroidVector,
    DopplerRate,
    DopplerRateVector,
    GroundToSlant,
    GroundToSlantVector,
    SlantToElevation,
    SlantToElevationVector,
    SlantToGround,
    SlantToGroundVector,
    SlantToIncidence,
    SlantToIncidenceVector,
    TopsAzimuthModulationRate,
    TopsAzimuthModulationRateVector,
)
from aresys_io.product.metadata.polynomials import (
    _coefficients_to_matrix,  # ruff: ignore[import-private-name]
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
    sorted_poly_list: CoregistrationPoly,
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

    sorted_poly_list = DopplerCentroidPoly.from_metadata(poly_list)
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

    sorted_poly_list = DopplerCentroidPoly.from_metadata(poly_list)

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


def test_coregistration_poly_from_metadata() -> None:
    sorted_poly_list = CoregistrationPoly.from_metadata(
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


def test_coregistration_poly_init_and_evaluate() -> None:
    sorted_poly_list = CoregistrationPoly(
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


def test_polynomial2d_equality() -> None:
    p1 = _polynomial2d_from_data(POLY_DATA_SORTED_FIRST)
    p2 = _polynomial2d_from_data(POLY_DATA_SORTED_FIRST)
    p3 = _polynomial2d_from_data(POLY_DATA_SORTED_SECOND)

    assert p1 == p2
    assert p1 != p3
    assert p1 != "not_a_polynomial"


def test_polynomial2d_properties() -> None:
    p = _polynomial2d_from_data(POLY_DATA_SORTED_FIRST)
    assert p.ref_azimuth_time == POLY_DATA_SORTED_FIRST.ref_az
    assert p.ref_range_time == POLY_DATA_SORTED_FIRST.ref_rg


def test_piecewise_init_does_not_mutate_input_list() -> None:
    original = [
        _polynomial2d_from_data(POLY_DATA_SORTED_SECOND),
        _polynomial2d_from_data(POLY_DATA_SORTED_FIRST),
    ]
    PiecewisePolynomial2D(_sorted_poly_list=original)

    # original list must not be sorted in place
    assert original[0].reference_values[0] == POLY_DATA_SORTED_SECOND.ref_az
    assert original[1].reference_values[0] == POLY_DATA_SORTED_FIRST.ref_az


def test_piecewise_evaluate_before_first_reference() -> None:
    poly_list = _doppler_centroid_vector_from_data(
        [POLY_DATA_SORTED_SECOND, POLY_DATA_SORTED_FIRST],
    )
    sorted_poly_list = DopplerCentroidPoly.from_metadata(poly_list)

    # Evaluate before the first polynomial's azimuth time: should pick the first polynomial
    res = sorted_poly_list.evaluate(
        (PreciseDateTime.from_utc_string("09-JUL-2006 20:58:00.0"), 8.0),
    )
    first_poly = _polynomial2d_from_data(POLY_DATA_SORTED_FIRST)
    expected = first_poly.evaluate(
        (PreciseDateTime.from_utc_string("09-JUL-2006 20:58:00.0"), 8.0),
    )
    assert isclose(res, expected)


def test_empty_piecewise_raises_error() -> None:
    empty_poly2d = PiecewisePolynomial2D()
    with pytest.raises(ValueError, match="Cannot evaluate an empty PiecewisePolynomial2D"):
        empty_poly2d.evaluate((PreciseDateTime.now(), 0.0))

    empty_pair = CoregistrationPoly()
    with pytest.raises(ValueError, match="Cannot evaluate an empty CoregistrationPoly"):
        empty_pair.evaluate((PreciseDateTime.now(), 0.0))


def test_polynomial_unhashable() -> None:
    p = _polynomial2d_from_data(POLY_DATA_SORTED_FIRST)
    with pytest.raises(TypeError, match="unhashable"):
        hash(p)

    pair = PolynomialPair2D.from_metadata(
        _metadata_polynomial_pair_from_data(POLYNOMIAL_PAIR_DATA_SORTED_FIRST),
    )
    with pytest.raises(TypeError, match="unhashable"):
        hash(pair)


def test_polynomial2d_equality_matrices() -> None:
    p1 = Polynomial2D(
        reference_values=(POLY_DATA_SORTED_FIRST.ref_az, 1.0),
        coefficient_matrix=np.array([[1.0, 2.0], [3.0, 4.0]]),
    )
    p2 = Polynomial2D(
        reference_values=(POLY_DATA_SORTED_FIRST.ref_az, 1.0),
        coefficient_matrix=np.array([[1.0, 2.0], [3.0, 99.0]]),
    )
    assert p1 != p2


def test_polynomial_pair_equality() -> None:
    pair1 = PolynomialPair2D.from_metadata(
        _metadata_polynomial_pair_from_data(POLYNOMIAL_PAIR_DATA_SORTED_FIRST),
    )
    pair2 = PolynomialPair2D.from_metadata(
        _metadata_polynomial_pair_from_data(POLYNOMIAL_PAIR_DATA_SORTED_FIRST),
    )
    pair3 = PolynomialPair2D.from_metadata(
        _metadata_polynomial_pair_from_data(POLYNOMIAL_PAIR_DATA_SORTED_SECOND),
    )
    assert pair1 == pair2
    assert pair1 != pair3
    assert pair1 != 123


def test_piecewise_input_list_independence() -> None:
    p1 = _polynomial2d_from_data(POLY_DATA_SORTED_FIRST)
    p2 = _polynomial2d_from_data(POLY_DATA_SORTED_SECOND)
    original_list = [p2, p1]
    piecewise = PiecewisePolynomial2D(_sorted_poly_list=original_list)

    # Modifying the original list must not alter the internal list of PiecewisePolynomial2D
    original_list.clear()
    assert len(_sorted_polys(piecewise)) == 2

    pair1 = PolynomialPair2D.from_metadata(
        _metadata_polynomial_pair_from_data(POLYNOMIAL_PAIR_DATA_SORTED_FIRST),
    )
    pair2 = PolynomialPair2D.from_metadata(
        _metadata_polynomial_pair_from_data(POLYNOMIAL_PAIR_DATA_SORTED_SECOND),
    )
    original_pairs = [pair2, pair1]
    piecewise_pairs = CoregistrationPoly(_sorted_poly_list=original_pairs)

    original_pairs.append(pair1)
    assert len(_sorted_polynomial_pairs(piecewise_pairs)) == 2


def test_float_reference_azimuth() -> None:
    # Test Polynomial2D and PiecewisePolynomial2D with float reference azimuth time
    p1 = Polynomial2D(
        reference_values=(10.0, 2.0),
        coefficient_matrix=np.array([[1.0, 2.0]]),  # 1.0 + 2.0 * (rg - 2.0)
    )
    p2 = Polynomial2D(
        reference_values=(20.0, 2.0),
        coefficient_matrix=np.array([[5.0, 0.0]]),  # 5.0
    )

    assert isclose(p1.ref_azimuth_time, 10.0)
    assert isclose(p1.ref_range_time, 2.0)
    assert isclose(p1.evaluate((10.0, 3.0)), 3.0)

    piecewise = PiecewisePolynomial2D(_sorted_poly_list=[p2, p1])
    # Before p1
    assert isclose(piecewise.evaluate((5.0, 3.0)), 3.0)
    # At p1
    assert isclose(piecewise.evaluate((10.0, 3.0)), 3.0)
    # Between p1 and p2 (picks p1)
    assert isclose(piecewise.evaluate((15.0, 3.0)), 3.0)
    # At p2 (picks p2)
    assert isclose(piecewise.evaluate((20.0, 3.0)), 5.0)
    # After p2 (picks p2)
    assert isclose(piecewise.evaluate((25.0, 3.0)), 5.0)


def test_piecewise_pair_boundaries() -> None:
    pair_first = PolynomialPair2D.from_metadata(
        _metadata_polynomial_pair_from_data(POLYNOMIAL_PAIR_DATA_SORTED_FIRST),
    )
    pair_second = PolynomialPair2D.from_metadata(
        _metadata_polynomial_pair_from_data(POLYNOMIAL_PAIR_DATA_SORTED_SECOND),
    )
    piecewise = CoregistrationPoly(_sorted_poly_list=[pair_second, pair_first])

    # Before first
    res_before = piecewise.evaluate(
        (PreciseDateTime.from_utc_string("09-JUL-2006 20:50:00.0"), 8.0),
    )
    res_first_expected = pair_first.evaluate(
        (PreciseDateTime.from_utc_string("09-JUL-2006 20:50:00.0"), 8.0),
    )
    assert isclose(res_before[0], res_first_expected[0])
    assert isclose(res_before[1], res_first_expected[1])

    # Exactly at second
    res_at_second = piecewise.evaluate((POLYNOMIAL_PAIR_DATA_SORTED_SECOND.ref_az, 2.0))
    res_second_expected = pair_second.evaluate((POLYNOMIAL_PAIR_DATA_SORTED_SECOND.ref_az, 2.0))
    assert isclose(res_at_second[0], res_second_expected[0])
    assert isclose(res_at_second[1], res_second_expected[1])

    # After second
    res_after = piecewise.evaluate(
        (PreciseDateTime.from_utc_string("09-JUL-2006 21:10:00.0"), 2.0),
    )
    res_after_expected = pair_second.evaluate(
        (PreciseDateTime.from_utc_string("09-JUL-2006 21:10:00.0"), 2.0),
    )
    assert isclose(res_after[0], res_after_expected[0])
    assert isclose(res_after[1], res_after_expected[1])


def test_coefficients_to_matrix_empty() -> None:
    mat = _coefficients_to_matrix([], (0, 1), (0, 1))
    assert mat.shape == (0, 0)
    assert mat.dtype == float


def _assert_concrete_poly(vector_cls: type, elem_cls: type, poly_cls: type) -> None:
    vector = vector_cls()
    vector.poly_list = [
        elem_cls(
            t_ref_az=POLY_DATA_SORTED_SECOND.ref_az,
            t_ref_rg=POLY_DATA_SORTED_SECOND.ref_rg,
            coefficients=POLY_DATA_SORTED_SECOND.coefficients,
        ),
        elem_cls(
            t_ref_az=POLY_DATA_SORTED_FIRST.ref_az,
            t_ref_rg=POLY_DATA_SORTED_FIRST.ref_rg,
            coefficients=POLY_DATA_SORTED_FIRST.coefficients,
        ),
    ]

    poly_obj = poly_cls.from_metadata(vector)
    assert isinstance(poly_obj, poly_cls)
    assert isinstance(poly_obj, PiecewisePolynomial2D)

    # Elements must be sorted by azimuth reference time
    assert [poly.reference_values[0] for poly in _sorted_polys(poly_obj)] == [
        POLY_DATA_SORTED_FIRST.ref_az,
        POLY_DATA_SORTED_SECOND.ref_az,
    ]

    res = poly_obj.evaluate(
        (PreciseDateTime.from_utc_string("09-JUL-2006 21:00:03.0"), 4.0),
    )
    assert isclose(res, 3.5)


def test_doppler_centroid_poly() -> None:
    _assert_concrete_poly(DopplerCentroidVector, DopplerCentroid, DopplerCentroidPoly)


def test_doppler_rate_poly() -> None:
    _assert_concrete_poly(DopplerRateVector, DopplerRate, DopplerRatePoly)


def test_slant_to_ground_poly() -> None:
    _assert_concrete_poly(SlantToGroundVector, SlantToGround, SlantToGroundPoly)


def test_ground_to_slant_poly() -> None:
    _assert_concrete_poly(GroundToSlantVector, GroundToSlant, GroundToSlantPoly)


def test_slant_to_incidence_poly() -> None:
    _assert_concrete_poly(SlantToIncidenceVector, SlantToIncidence, SlantToIncidencePoly)


def test_slant_to_elevation_poly() -> None:
    _assert_concrete_poly(SlantToElevationVector, SlantToElevation, SlantToElevationPoly)


def test_tops_azimuth_modulation_rate_poly() -> None:
    _assert_concrete_poly(
        TopsAzimuthModulationRateVector,
        TopsAzimuthModulationRate,
        TopsAzimuthModulationRatePoly,
    )
