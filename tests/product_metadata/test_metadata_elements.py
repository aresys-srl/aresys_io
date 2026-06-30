# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

import pytest
from perseo_core.timing import PreciseDateTime

from aresys_io.product_metadata import metadata_elements


def test_polynomial_requires_minimum_coefficients() -> None:
    with pytest.raises(ValueError, match="at least 7 coefficients"):
        metadata_elements.DopplerCentroid(
            t_ref_az=PreciseDateTime.from_numeric_datetime(year=2020),
            t_ref_rg=0.005,
            coefficients=[],
        )


def test_coreg_polynomial_requires_exactly_four_coefficients() -> None:
    with pytest.raises(ValueError, match="exactly 4 coefficients"):
        metadata_elements.CoregPoly(
            t_ref_az=PreciseDateTime.from_numeric_datetime(year=2020),
            t_ref_rg=0.005,
            coefficients_az=[1, 2, 3],
            coefficients_rg=[11, 12, 13],
        )


def test_polynomial_vector_class_contract() -> None:
    vector_specs = [
        (metadata_elements.DopplerCentroidVector, metadata_elements.DopplerCentroid),
        (metadata_elements.DopplerRateVector, metadata_elements.DopplerRate),
        (
            metadata_elements.TopsAzimuthModulationRateVector,
            metadata_elements.TopsAzimuthModulationRate,
        ),
        (metadata_elements.SlantToGroundVector, metadata_elements.SlantToGround),
        (metadata_elements.GroundToSlantVector, metadata_elements.GroundToSlant),
        (metadata_elements.SlantToIncidenceVector, metadata_elements.SlantToIncidence),
        (metadata_elements.SlantToElevationVector, metadata_elements.SlantToElevation),
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
