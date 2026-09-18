# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Unit tests for Metadata Elements."""

import pytest
from perseo_core.timing import PreciseDateTime

from aresys_io.product.metadata import elements


def test_polynomial_requires_minimum_coefficients() -> None:
    with pytest.raises(ValueError, match="at least 7 coefficients"):
        elements.DopplerCentroid(
            t_ref_az=PreciseDateTime.from_numeric_datetime(year=2020),
            t_ref_rg=0.005,
            coefficients=[],
        )


def test_coreg_polynomial_requires_exactly_four_coefficients() -> None:
    with pytest.raises(ValueError, match="exactly 4 coefficients"):
        elements.CoregPoly(
            t_ref_az=PreciseDateTime.from_numeric_datetime(year=2020),
            t_ref_rg=0.005,
            coefficients_az=[1, 2, 3],
            coefficients_rg=[11, 12, 13],
        )


def test_polynomial_vector_class_contract() -> None:
    vector_specs = [
        (elements.DopplerCentroidVector, elements.DopplerCentroid),
        (elements.DopplerRateVector, elements.DopplerRate),
        (
            elements.TopsAzimuthModulationRateVector,
            elements.TopsAzimuthModulationRate,
        ),
        (elements.SlantToGroundVector, elements.SlantToGround),
        (elements.GroundToSlantVector, elements.GroundToSlant),
        (elements.SlantToIncidenceVector, elements.SlantToIncidence),
        (elements.SlantToElevationVector, elements.SlantToElevation),
    ]

    for vector_cls, poly_cls in vector_specs:
        assert vector_cls.SINGLE_POLY_TYPE is poly_cls

        poly = poly_cls(
            t_ref_az=PreciseDateTime.from_numeric_datetime(year=2020),
            t_ref_rg=0.005,
            coefficients=[1, 2, 3, 4, 5, 6, 7],
        )
        vector = vector_cls(poly_list=[poly])

        assert len(vector.poly_list) == 1
        assert isinstance(vector.poly_list[0], poly_cls)
