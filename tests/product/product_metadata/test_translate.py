# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Unit tests for metadata translation functionalities."""

from typing import Literal

import numpy as np
import pytest
from perseo_core.timing import PreciseDateTime

from aresys_io.product.metadata import channel, elements, models, translate


@pytest.mark.parametrize(
    ("model_value", "expected"),
    [
        (models.Endianity.BIGENDIAN, "BIGENDIAN"),
        (models.Endianity.LITTLEENDIAN, "LITTLEENDIAN"),
    ],
)
def test_translate_endianity_from_model(
    model_value: models.Endianity,
    expected: elements.RasterByteOrder,
) -> None:
    assert translate.translate_endianity_from_model(model_value) == expected


@pytest.mark.parametrize(
    ("raw_value", "expected"),
    [
        ("BIGENDIAN", models.Endianity.BIGENDIAN),
        ("LITTLEENDIAN", models.Endianity.LITTLEENDIAN),
    ],
)
def test_translate_endianity_to_model(
    raw_value: elements.RasterByteOrder,
    expected: models.Endianity,
) -> None:
    assert translate.translate_endianity_to_model(raw_value) == expected


@pytest.mark.parametrize(
    ("model_value", "expected"),
    [
        (models.CellTypeVerboseType.FLOAT_COMPLEX, "FLOAT_COMPLEX"),
        (models.CellTypeVerboseType.FLOAT32, "FLOAT32"),
        (models.CellTypeVerboseType.DOUBLE_COMPLEX, "DOUBLE_COMPLEX"),
        (models.CellTypeVerboseType.FLOAT64, "FLOAT64"),
        (models.CellTypeVerboseType.INT16, "INT16"),
        (models.CellTypeVerboseType.SHORT_COMPLEX, "INT16_COMPLEX"),
        (models.CellTypeVerboseType.INT32, "INT32"),
        (models.CellTypeVerboseType.INT_COMPLEX, "INT_COMPLEX"),
        (models.CellTypeVerboseType.INT8, "INT8"),
        (models.CellTypeVerboseType.INT8_COMPLEX, "INT8_COMPLEX"),
        (models.CellTypeVerboseType.CUSTOM, "CUSTOM"),
    ],
)
def test_translate_cell_type_from_model(
    model_value: models.CellTypeVerboseType,
    expected: elements.RasterCellType,
) -> None:
    assert translate.translate_cell_type_from_model(model_value) == expected


@pytest.mark.parametrize(
    ("raw_value", "expected"),
    [
        ("FLOAT_COMPLEX", models.CellTypeVerboseType.FLOAT_COMPLEX),
        ("FLOAT32", models.CellTypeVerboseType.FLOAT32),
        ("DOUBLE_COMPLEX", models.CellTypeVerboseType.DOUBLE_COMPLEX),
        ("FLOAT64", models.CellTypeVerboseType.FLOAT64),
        ("INT16", models.CellTypeVerboseType.INT16),
        ("INT16_COMPLEX", models.CellTypeVerboseType.SHORT_COMPLEX),
        ("INT32", models.CellTypeVerboseType.INT32),
        ("INT_COMPLEX", models.CellTypeVerboseType.INT_COMPLEX),
        ("INT8", models.CellTypeVerboseType.INT8),
        ("INT8_COMPLEX", models.CellTypeVerboseType.INT8_COMPLEX),
        ("CUSTOM", models.CellTypeVerboseType.CUSTOM),
    ],
)
def test_translate_cell_type_to_model(
    raw_value: elements.RasterCellType,
    expected: models.CellTypeVerboseType,
) -> None:
    assert translate.translate_cell_type_to_model(raw_value) == expected


@pytest.mark.parametrize(
    ("model_value", "expected"),
    [
        (models.AscendingDescendingType.ASCENDING, "ASCENDING"),
        (models.AscendingDescendingType.DESCENDING, "DESCENDING"),
        (models.AscendingDescendingType.NOT_AVAILABLE, None),
    ],
)
def test_translate_orbit_direction_from_model(
    model_value: models.AscendingDescendingType,
    expected: elements.OrbitDirection | None,
) -> None:
    assert translate.translate_orbit_direction_from_model(model_value) == expected


@pytest.mark.parametrize(
    ("raw_value", "expected"),
    [
        ("ASCENDING", models.AscendingDescendingType.ASCENDING),
        ("DESCENDING", models.AscendingDescendingType.DESCENDING),
        (None, models.AscendingDescendingType.NOT_AVAILABLE),
    ],
)
def test_translate_orbit_direction_to_model(
    raw_value: elements.OrbitDirection | None,
    expected: models.AscendingDescendingType,
) -> None:
    assert translate.translate_orbit_direction_to_model(raw_value) == expected


@pytest.mark.parametrize(
    ("model_value", "expected"),
    [
        (models.LeftRightType.LEFT, "LEFT"),
        (models.LeftRightType.RIGHT, "RIGHT"),
    ],
)
def test_translate_side_looking_from_model(
    model_value: models.LeftRightType,
    expected: elements.SideLooking,
) -> None:
    assert translate.translate_side_looking_from_model(model_value) == expected


@pytest.mark.parametrize(
    ("raw_value", "expected"),
    [
        ("LEFT", models.LeftRightType.LEFT),
        ("RIGHT", models.LeftRightType.RIGHT),
    ],
)
def test_translate_side_looking_to_model(
    raw_value: elements.SideLooking,
    expected: models.LeftRightType,
) -> None:
    assert translate.translate_side_looking_to_model(raw_value) == expected


@pytest.mark.parametrize(
    ("model_value", "expected"),
    [
        (models.PolarizationType.H_H, "HH"),
        (models.PolarizationType.H_V, "HV"),
        (models.PolarizationType.V_H, "VH"),
        (models.PolarizationType.V_V, "VV"),
        (models.PolarizationType.X_X, "XX"),
    ],
)
def test_translate_polarization_from_model(
    model_value: models.PolarizationType,
    expected: elements.AntennaPolarization,
) -> None:
    assert translate.translate_polarization_from_model(model_value) == expected


@pytest.mark.parametrize(
    ("raw_value", "expected"),
    [
        ("HH", models.PolarizationType.H_H),
        ("HV", models.PolarizationType.H_V),
        ("VH", models.PolarizationType.V_H),
        ("VV", models.PolarizationType.V_V),
        ("XX", models.PolarizationType.X_X),
    ],
)
def test_translate_polarization_to_model(
    raw_value: elements.AntennaPolarization,
    expected: models.PolarizationType,
) -> None:
    assert translate.translate_polarization_to_model(raw_value) == expected


@pytest.mark.parametrize(
    ("model_value", "expected"),
    [
        (models.ReferenceFrameType.GEOCENTRIC, "GEOCENTRIC"),
        (models.ReferenceFrameType.GEODETIC, "GEODETIC"),
        (models.ReferenceFrameType.ZERODOPPLER, "ZERODOPPLER"),
    ],
)
def test_translate_reference_frame_from_model(
    model_value: models.ReferenceFrameType,
    expected: elements.AttitudeReferenceFrame,
) -> None:
    assert translate.translate_reference_frame_from_model(model_value) == expected


@pytest.mark.parametrize(
    ("raw_value", "expected"),
    [
        ("GEOCENTRIC", models.ReferenceFrameType.GEOCENTRIC),
        ("GEODETIC", models.ReferenceFrameType.GEODETIC),
        ("ZERODOPPLER", models.ReferenceFrameType.ZERODOPPLER),
    ],
)
def test_translate_reference_frame_to_model(
    raw_value: elements.AttitudeReferenceFrame,
    expected: models.ReferenceFrameType,
) -> None:
    assert translate.translate_reference_frame_to_model(raw_value) == expected


@pytest.mark.parametrize(
    ("model_value", "expected"),
    [
        (models.RotationOrderType.YPR, "YPR"),
        (models.RotationOrderType.YRP, "YRP"),
        (models.RotationOrderType.RPY, "RPY"),
        (models.RotationOrderType.RYP, "RYP"),
        (models.RotationOrderType.PYR, "PYR"),
        (models.RotationOrderType.PRY, "PRY"),
    ],
)
def test_translate_rotation_order_from_model(
    model_value: models.RotationOrderType,
    expected: elements.AttitudeRotationOrder,
) -> None:
    assert translate.translate_rotation_order_from_model(model_value) == expected


@pytest.mark.parametrize(
    ("raw_value", "expected"),
    [
        ("YPR", models.RotationOrderType.YPR),
        ("YRP", models.RotationOrderType.YRP),
        ("RPY", models.RotationOrderType.RPY),
        ("RYP", models.RotationOrderType.RYP),
        ("PYR", models.RotationOrderType.PYR),
        ("PRY", models.RotationOrderType.PRY),
    ],
)
def test_translate_rotation_order_to_model(
    raw_value: elements.AttitudeRotationOrder,
    expected: models.RotationOrderType,
) -> None:
    assert translate.translate_rotation_order_to_model(raw_value) == expected


@pytest.mark.parametrize(
    ("model_value", "expected"),
    [
        (models.AttitudeType.NOMINAL, "NOMINAL"),
        (models.AttitudeType.REFINED, "REFINED"),
    ],
)
def test_translate_attitude_type_from_model(
    model_value: models.AttitudeType,
    expected: elements.AttitudeType,
) -> None:
    assert translate.translate_attitude_type_from_model(model_value) == expected


@pytest.mark.parametrize(
    ("raw_value", "expected"),
    [
        ("NOMINAL", models.AttitudeType.NOMINAL),
        ("REFINED", models.AttitudeType.REFINED),
    ],
)
def test_translate_attitude_type_to_model(
    raw_value: elements.AttitudeType,
    expected: models.AttitudeType,
) -> None:
    assert translate.translate_attitude_type_to_model(raw_value) == expected


@pytest.mark.parametrize(
    ("model_value", "expected"),
    [
        (models.RasterFormatType.ARESYS_GEOTIFF, "ARESYS_GEOTIFF"),
        (models.RasterFormatType.ARESYS_RASTER, "ARESYS_RASTER"),
        (models.RasterFormatType.RASTER, "ARESYS_RASTER"),
    ],
)
def test_translate_raster_format_type_from_model(
    model_value: models.RasterFormatType,
    expected: elements.RasterFormat,
) -> None:
    assert translate.translate_raster_format_type_from_model(model_value) == expected


@pytest.mark.parametrize(
    ("raw_value", "expected"),
    [
        ("ARESYS_GEOTIFF", models.RasterFormatType.ARESYS_GEOTIFF),
        ("ARESYS_RASTER", models.RasterFormatType.ARESYS_RASTER),
    ],
)
def test_translate_raster_format_type_to_model(
    raw_value: elements.RasterFormat,
    expected: models.RasterFormatType,
) -> None:
    assert translate.translate_raster_format_type_to_model(raw_value) == expected


@pytest.mark.parametrize(
    ("model_value", "expected"),
    [
        (models.Units.VALUE, ""),
        (models.Units.M, "m"),
        (models.Units.S, "s"),
        (models.Units.J, "j"),
        (models.Units.D_B, "dB"),
        (models.Units.RAD, "rad"),
        (models.Units.DEG, "deg"),
        (models.Units.M_S, "m/s"),
        (models.Units.M_S2, "m/s2"),
        (models.Units.M_S3, "m/s3"),
        (models.Units.M_S4, "m/s4"),
        (models.Units.S_S, "s/s"),
        (models.Units.S_S2, "s/s2"),
        (models.Units.S_S3, "s/s3"),
        (models.Units.S_S4, "s/s4"),
        (models.Units.S_S5, "s/s5"),
        (models.Units.HZ_S, "Hz/s"),
        (models.Units.HZ_S2, "Hz/s2"),
        (models.Units.HZ_S3, "Hz/s3"),
        (models.Units.HZ_S4, "Hz/s4"),
        (models.Units.HZ_S5, "Hz/s5"),
        (models.Units.RAD_S, "rad/s"),
        (models.Units.RAD_S2, "rad/s2"),
        (models.Units.RAD_S3, "rad/s3"),
        (models.Units.RAD_S4, "rad/s4"),
        (models.Units.RAD_S5, "rad/s5"),
        (models.Units.S85, "s85"),
        (models.Units.UTC, "Utc"),
        (models.Units.B, "b"),
        (models.Units.HZ, "Hz"),
        (models.Units.K, "K"),
        (models.Units.S_M, "s/m"),
        (models.Units.S_M2, "s/m2"),
        (models.Units.S_M3, "s/m3"),
        (models.Units.S_M4, "s/m4"),
        (models.Units.DEG_S, "deg/s"),
        (models.Units.DEG_S2, "deg/s2"),
        (models.Units.DEG_S3, "deg/s3"),
        (models.Units.DEG_S4, "deg/s4"),
    ],
)
def test_translate_unit_from_model(
    model_value: models.Units,
    expected: str,
) -> None:
    assert translate.translate_unit_from_model(model_value) == expected


@pytest.mark.parametrize(
    ("raw_value", "expected"),
    [
        ("", models.Units.VALUE),
        ("m", models.Units.M),
        ("s", models.Units.S),
        ("j", models.Units.J),
        ("dB", models.Units.D_B),
        ("rad", models.Units.RAD),
        ("deg", models.Units.DEG),
        ("m/s", models.Units.M_S),
        ("m/s2", models.Units.M_S2),
        ("m/s3", models.Units.M_S3),
        ("m/s4", models.Units.M_S4),
        ("s/s", models.Units.S_S),
        ("s/s2", models.Units.S_S2),
        ("s/s3", models.Units.S_S3),
        ("s/s4", models.Units.S_S4),
        ("s/s5", models.Units.S_S5),
        ("Hz/s", models.Units.HZ_S),
        ("Hz/s2", models.Units.HZ_S2),
        ("Hz/s3", models.Units.HZ_S3),
        ("Hz/s4", models.Units.HZ_S4),
        ("Hz/s5", models.Units.HZ_S5),
        ("rad/s", models.Units.RAD_S),
        ("rad/s2", models.Units.RAD_S2),
        ("rad/s3", models.Units.RAD_S3),
        ("rad/s4", models.Units.RAD_S4),
        ("rad/s5", models.Units.RAD_S5),
        ("s85", models.Units.S85),
        ("Utc", models.Units.UTC),
        ("b", models.Units.B),
        ("Hz", models.Units.HZ),
        ("K", models.Units.K),
        ("s/m", models.Units.S_M),
        ("s/m2", models.Units.S_M2),
        ("s/m3", models.Units.S_M3),
        ("s/m4", models.Units.S_M4),
        ("deg/s", models.Units.DEG_S),
        ("deg/s2", models.Units.DEG_S2),
        ("deg/s3", models.Units.DEG_S3),
        ("deg/s4", models.Units.DEG_S4),
    ],
)
def test_translate_unit_to_model(
    raw_value: str,
    expected: models.Units,
) -> None:
    assert translate.translate_unit_to_model(raw_value) == expected


def test_create_double_with_unit() -> None:
    assert translate.translate_double_with_unit_to_model(5.6, "K") == models.DoubleWithUnit(
        value=5.6,
        unit=models.Units.K,
    )


def test_translate_str_with_unit() -> None:
    assert translate.translate_str_with_unit_from_model(
        models.StringWithUnit(value="01-JAN-2020 00:00:00.000000000000", unit=models.Units.UTC),
    ) == (PreciseDateTime.from_numeric_datetime(year=2020), "Utc")
    assert translate.translate_str_with_unit_from_model(
        models.StringWithUnit(value="2020", unit=models.Units.M),
    ) == (2020, "m")
    assert translate.translate_str_with_unit_to_model(
        PreciseDateTime.from_numeric_datetime(year=2020),
        "Utc",
    ) == models.StringWithUnit(value="01-JAN-2020 00:00:00.000000000000", unit=models.Units.UTC)
    assert translate.translate_str_with_unit_to_model(2020, "m") == models.StringWithUnit(
        value="2020",
        unit=models.Units.M,
    )


def test_translate_dcomplex() -> None:
    assert translate.translate_dcomplex_from_model(  # ruff: ignore[float-equality-comparison]
        models.Dcomplex(real_value=2.3, imaginary_value=-4.3),
    ) == complex(2.3, -4.3)
    assert translate.translate_dcomplex_to_model(complex(2.3, -4.3)) == models.Dcomplex(
        real_value=2.3,
        imaginary_value=-4.3,
    )


class TestRasterInfo:
    @staticmethod
    def assert_equal_raster_info(
        raster_info_a: elements.RasterInfo,
        raster_info_b: elements.RasterInfo,
    ) -> None:
        assert raster_info_a.file_name == raster_info_b.file_name
        assert raster_info_a.lines == raster_info_b.lines
        assert raster_info_a.samples == raster_info_b.samples
        assert raster_info_a.header_offset_bytes == raster_info_b.header_offset_bytes
        assert raster_info_a.row_prefix_bytes == raster_info_b.row_prefix_bytes
        assert raster_info_a.lines_start == raster_info_b.lines_start
        assert raster_info_a.lines_start_unit == raster_info_b.lines_start_unit
        assert raster_info_a.lines_step == raster_info_b.lines_step
        assert raster_info_a.lines_step_unit == raster_info_b.lines_step_unit
        assert raster_info_a.samples_start == raster_info_b.samples_start
        assert raster_info_a.samples_start_unit == raster_info_b.samples_start_unit
        assert raster_info_a.samples_step == raster_info_b.samples_step
        assert raster_info_a.samples_step_unit == raster_info_b.samples_step_unit
        assert raster_info_a.byte_order == raster_info_b.byte_order
        assert raster_info_a.cell_type == raster_info_b.cell_type
        assert raster_info_a.invalid_value == raster_info_b.invalid_value
        assert raster_info_a.format_type == raster_info_b.format_type

    def setup_method(self) -> None:
        self.raster_info_model = models.RasterInfoType(
            file_name="filename.tiff",
            lines=11,
            samples=3,
            header_offset_bytes=50,
            row_prefix_bytes=4,
            byte_order=models.Endianity.BIGENDIAN,
            cell_type=models.CellTypeVerboseType.INT16,
            lines_step=translate.translate_double_with_unit_to_model(0.5, "Hz"),
            samples_step=translate.translate_double_with_unit_to_model(8.5, "m"),
            invalid_value=None,
            lines_start=translate.translate_str_with_unit_to_model(
                PreciseDateTime.from_numeric_datetime(year=2020),
                "Utc",
            ),
            samples_start=translate.translate_str_with_unit_to_model(3.4, "m"),
            raster_format=None,
        )
        self.raster_info_metadata = elements.RasterInfo(
            lines=11,
            samples=3,
            cell_type="INT16",
            file_name="filename.tiff",
            header_offset_bytes=50,
            row_prefix_bytes=4,
            byte_order="BIGENDIAN",
            invalid_value=None,
            format_type=None,
        )
        self.raster_info_metadata.lines_start = PreciseDateTime.from_numeric_datetime(year=2020)
        self.raster_info_metadata.lines_start_unit = "Utc"
        self.raster_info_metadata.lines_step = 0.5
        self.raster_info_metadata.lines_step_unit = "Hz"
        self.raster_info_metadata.samples_start = 3.4
        self.raster_info_metadata.samples_start_unit = "m"
        self.raster_info_metadata.samples_step = 8.5
        self.raster_info_metadata.samples_step_unit = "m"

    def test_translate_raster_info(self) -> None:
        self.assert_equal_raster_info(
            translate.translate_raster_info_from_model(self.raster_info_model),
            self.raster_info_metadata,
        )

        assert (
            translate.translate_raster_info_to_model(self.raster_info_metadata)
            == self.raster_info_model
        )

    def test_translate_raster_info_range_utc_lines_float(self) -> None:
        self.raster_info_model.lines_start = translate.translate_str_with_unit_to_model(
            1000.4,
            "Hz",
        )
        self.raster_info_model.samples_start = translate.translate_str_with_unit_to_model(
            PreciseDateTime.from_numeric_datetime(year=2020),
            "Utc",
        )
        self.raster_info_metadata.lines_start = 1000.4
        self.raster_info_metadata.lines_start_unit = "Hz"
        self.raster_info_metadata.samples_start = PreciseDateTime.from_numeric_datetime(year=2020)
        self.raster_info_metadata.samples_start_unit = "Utc"
        self.assert_equal_raster_info(
            translate.translate_raster_info_from_model(self.raster_info_model),
            self.raster_info_metadata,
        )

        assert (
            translate.translate_raster_info_to_model(self.raster_info_metadata)
            == self.raster_info_model
        )

    def test_translate_raster_info_invalid_value_and_format(self) -> None:
        self.raster_info_model.invalid_value = models.Dcomplex(
            real_value=2.3,
            imaginary_value=-7.8,
        )
        self.raster_info_metadata.invalid_value = complex(2.3, -7.8)

        self.raster_info_model.raster_format = models.RasterFormatType.ARESYS_GEOTIFF
        self.raster_info_metadata.format_type = "ARESYS_GEOTIFF"

        self.assert_equal_raster_info(
            translate.translate_raster_info_from_model(self.raster_info_model),
            self.raster_info_metadata,
        )

        assert (
            translate.translate_raster_info_to_model(self.raster_info_metadata)
            == self.raster_info_model
        )

    def test_filename_change_after_instantiation(self) -> None:
        raster_info = translate.translate_raster_info_from_model(self.raster_info_model)
        new_filename = "test_filename_change.tiff"
        raster_info.file_name = new_filename
        assert raster_info.file_name == new_filename


class TestDataSetInfo:
    @staticmethod
    def assert_equal_data_set_info(
        info_a: elements.DataSetInfo,
        info_b: elements.DataSetInfo,
    ) -> None:
        assert info_a.sensor_name == info_b.sensor_name
        assert info_a.description == info_b.description
        assert info_a.acquisition_mode == info_b.acquisition_mode
        assert info_a.image_type == info_b.image_type
        assert info_a.projection == info_b.projection
        assert info_a.acquisition_station == info_b.acquisition_station
        assert info_a.processing_center == info_b.processing_center
        assert info_a.processing_software == info_b.processing_software
        assert info_a.fc_hz == info_b.fc_hz
        assert info_a.external_calibration_factor == info_b.external_calibration_factor
        assert info_a.data_take_id == info_b.data_take_id
        assert info_a.sense_date == info_b.sense_date
        assert info_a.processing_date == info_b.processing_date
        assert info_a.side_looking == info_b.side_looking
        assert info_a.image_quantity == info_b.image_quantity

    def setup_method(self) -> None:
        self.data_set_info_model = models.DataSetInfoType(
            sensor_name="sensor",
            description=models.DataSetInfoType.Description(value="description"),
            sense_date=models.DataSetInfoType.SenseDate(value="01-JAN-2020 00:00:00.000000000000"),
            acquisition_mode=models.DataSetInfoType.AcquisitionMode(value="acquisition_mode"),
            image_type=models.DataSetInfoType.ImageType(value="image_type"),
            projection=models.DataSetInfoType.Projection(value="projection"),
            acquisition_station=models.DataSetInfoType.AcquisitionStation(
                value="acquisition_station",
            ),
            processing_center=models.DataSetInfoType.ProcessingCenter(value="processing_center"),
            processing_date=models.DataSetInfoType.ProcessingDate(
                value="01-JAN-2021 00:00:00.000000000000",
            ),
            processing_software=models.DataSetInfoType.ProcessingSoftware(
                value="processing_software",
            ),
            fc_hz=models.DataSetInfoType.FcHz(value=1000),
            side_looking=models.LeftRightType.LEFT,
            external_calibration_factor=None,
            data_take_id=None,
            instrument_conf_id=15,
        )
        self.data_set_info_metadata = elements.DataSetInfo(
            sensor_name="sensor",
            description="description",
            sense_date=PreciseDateTime.from_numeric_datetime(year=2020),
            acquisition_mode="acquisition_mode",
            image_type="image_type",
            projection="projection",
            acquisition_station="acquisition_station",
            processing_center="processing_center",
            processing_date=PreciseDateTime.from_numeric_datetime(year=2021),
            processing_software="processing_software",
            fc_hz=1000,
            side_looking="LEFT",
        )
        self.data_set_info_metadata.instrument_conf_id = 15

    def test_translate_data_set_info(self) -> None:
        self.assert_equal_data_set_info(
            translate.translate_dataset_info_from_model(self.data_set_info_model),
            self.data_set_info_metadata,
        )

        assert (
            translate.translate_dataset_info_to_model(self.data_set_info_metadata)
            == self.data_set_info_model
        )

    def test_translate_data_set_info_with_dates(self) -> None:
        assert self.data_set_info_model.sense_date is not None
        self.data_set_info_model.sense_date.value = "01-JAN-2022 00:00:00.000000000000"
        self.data_set_info_metadata.sense_date = PreciseDateTime.from_numeric_datetime(year=2022)
        assert self.data_set_info_model.processing_date is not None
        self.data_set_info_model.processing_date.value = "01-JAN-2023 00:00:00.000000000000"
        self.data_set_info_metadata.processing_date = PreciseDateTime.from_numeric_datetime(
            year=2023,
        )

        self.assert_equal_data_set_info(
            translate.translate_dataset_info_from_model(self.data_set_info_model),
            self.data_set_info_metadata,
        )

        assert (
            translate.translate_dataset_info_to_model(self.data_set_info_metadata)
            == self.data_set_info_model
        )

    def test_translate_data_set_info_with_additional_info(self) -> None:
        self.data_set_info_model.external_calibration_factor = 15.2
        self.data_set_info_model.data_take_id = 20
        self.data_set_info_model.image_quantity = models.ImageQuantityType.GAMMA
        self.data_set_info_metadata.external_calibration_factor = 15.2
        self.data_set_info_metadata.data_take_id = 20
        self.data_set_info_metadata.image_quantity = "GAMMA"

        self.assert_equal_data_set_info(
            translate.translate_dataset_info_from_model(self.data_set_info_model),
            self.data_set_info_metadata,
        )

        assert (
            translate.translate_dataset_info_to_model(self.data_set_info_metadata)
            == self.data_set_info_model
        )


def assert_equal_geo_point(
    point_a: elements.GeoPoint,
    point_b: elements.GeoPoint,
) -> None:
    """Assert that geo point are equal."""
    assert point_a.lat == point_b.lat
    assert point_a.lon == point_b.lon
    assert point_a.height == point_b.height
    assert point_a.theta_inc == point_b.theta_inc
    assert point_a.theta_look == point_b.theta_look


def test_translate_geo_point() -> None:
    point_model = models.PointType(
        val=[
            models.PointType.Val(value=0.3),
            models.PointType.Val(value=1.2),
            models.PointType.Val(value=2.1),
            models.PointType.Val(value=3.9),
            models.PointType.Val(value=4.8),
        ],
    )
    point_metadata = elements.GeoPoint(
        lat=0.3,
        lon=1.2,
        height=2.1,
        theta_inc=3.9,
        theta_look=4.8,
    )

    assert_equal_geo_point(translate.translate_geo_point_from_model(point_model), point_metadata)
    assert translate.translate_geo_point_to_model(point_metadata) == point_model


class TestGroundCornerPoints:
    @staticmethod
    def assert_equal_ground_corner_points(
        points_a: elements.GroundCornerPoints,
        points_b: elements.GroundCornerPoints,
    ) -> None:
        assert points_a.easting_grid_size == points_b.easting_grid_size
        assert points_a.northing_grid_size == points_b.northing_grid_size
        assert_equal_geo_point(points_a.center_point, points_b.center_point)
        assert_equal_geo_point(points_a.ne_point, points_b.ne_point)
        assert_equal_geo_point(points_a.nw_point, points_b.nw_point)
        assert_equal_geo_point(points_a.se_point, points_b.se_point)
        assert_equal_geo_point(points_a.sw_point, points_b.sw_point)

    def test_translate_ground_corner_points(self) -> None:
        point_0_model = models.PointType(
            val=[
                models.PointType.Val(value=0.0),
                models.PointType.Val(value=0.0),
                models.PointType.Val(value=0.0),
                models.PointType.Val(value=0.0),
                models.PointType.Val(value=0.0),
            ],
        )
        point_1_model = models.PointType(
            val=[
                models.PointType.Val(value=1.0),
                models.PointType.Val(value=1.0),
                models.PointType.Val(value=1.0),
                models.PointType.Val(value=1.0),
                models.PointType.Val(value=1.0),
            ],
        )
        point_2_model = models.PointType(
            val=[
                models.PointType.Val(value=2.0),
                models.PointType.Val(value=2.0),
                models.PointType.Val(value=2.0),
                models.PointType.Val(value=2.0),
                models.PointType.Val(value=2.0),
            ],
        )
        point_3_model = models.PointType(
            val=[
                models.PointType.Val(value=3.0),
                models.PointType.Val(value=3.0),
                models.PointType.Val(value=3.0),
                models.PointType.Val(value=3.0),
                models.PointType.Val(value=3.0),
            ],
        )
        point_4_model = models.PointType(
            val=[
                models.PointType.Val(value=4.0),
                models.PointType.Val(value=4.0),
                models.PointType.Val(value=4.0),
                models.PointType.Val(value=4.0),
                models.PointType.Val(value=4.0),
            ],
        )

        corners_model = models.GroundCornersPointsType(
            easting_grid_size=models.GroundCornersPointsType.EastingGridSize(value=5.3),
            northing_grid_size=models.GroundCornersPointsType.NorthingGridSize(value=8.1),
            north_west=models.GroundCornersPointsType.NorthWest(point=point_0_model),
            north_east=models.GroundCornersPointsType.NorthEast(point=point_1_model),
            south_west=models.GroundCornersPointsType.SouthWest(point=point_2_model),
            south_east=models.GroundCornersPointsType.SouthEast(point=point_3_model),
            center=models.GroundCornersPointsType.Center(point=point_4_model),
        )

        corners_metadata = elements.GroundCornerPoints()
        corners_metadata.easting_grid_size = 5.3
        corners_metadata.northing_grid_size = 8.1
        corners_metadata.nw_point = translate.translate_geo_point_from_model(point_0_model)
        corners_metadata.ne_point = translate.translate_geo_point_from_model(point_1_model)
        corners_metadata.sw_point = translate.translate_geo_point_from_model(point_2_model)
        corners_metadata.se_point = translate.translate_geo_point_from_model(point_3_model)
        corners_metadata.center_point = translate.translate_geo_point_from_model(point_4_model)

        self.assert_equal_ground_corner_points(
            translate.translate_ground_corner_points_from_model(corners_model),
            corners_metadata,
        )
        assert translate.translate_ground_corner_points_to_model(corners_metadata) == corners_model


class TestSwathInfo:
    @staticmethod
    def assert_equal_swath_info(
        info_a: elements.SwathInfo,
        info_b: elements.SwathInfo,
    ) -> None:
        assert info_a.swath == info_b.swath
        assert info_a.polarization == info_b.polarization
        assert info_a.acquisition_prf == info_b.acquisition_prf
        assert info_a.acquisition_prf_unit == info_b.acquisition_prf_unit
        assert info_a.swath_acquisition_order == info_b.swath_acquisition_order
        assert info_a.rank == info_b.rank
        assert info_a.range_delay_bias == info_b.range_delay_bias
        assert info_a.range_delay_bias_unit == info_b.range_delay_bias_unit
        assert info_a.acquisition_start_time == info_b.acquisition_start_time
        assert info_a.acquisition_start_time_unit == info_b.acquisition_start_time_unit
        assert (
            info_a.azimuth_steering_rate_reference_time
            == info_b.azimuth_steering_rate_reference_time
        )
        assert (
            info_a.azimuth_steering_angle_reference_time
            == info_b.azimuth_steering_angle_reference_time
        )
        assert info_a.az_steering_rate_ref_time_unit == info_b.az_steering_rate_ref_time_unit
        assert info_a.az_steering_angle_ref_time_unit == info_b.az_steering_angle_ref_time_unit
        assert info_a.echoes_per_burst == info_b.echoes_per_burst
        assert info_a.azimuth_steering_rate_pol == info_b.azimuth_steering_rate_pol
        assert info_a.azimuth_steering_angle_pol == info_b.azimuth_steering_angle_pol
        assert info_a.rx_gain == info_b.rx_gain
        assert info_a.channel_delay == info_b.channel_delay

    def test_translate_swath_info_steering_angle(self) -> None:
        swath_info_model = models.SwathInfoType(
            swath=models.SwathInfoType.Swath(value="swath_name"),
            swath_acquisition_order=models.SwathInfoType.SwathAcquisitionOrder(value=4),
            polarization=models.PolarizationType.H_H,
            rank=models.SwathInfoType.Rank(value=15),
            range_delay_bias=models.SwathInfoType.RangeDelayBias(value=0.5, unit=models.Units.S),
            acquisition_start_time=models.SwathInfoType.AcquisitionStartTime(
                value="01-JAN-2020 00:00:00.000000000000",
                unit=models.Units.UTC,
            ),
            azimuth_steering_angle_reference_time=models.DoubleWithUnit(
                value=1.0,
                unit=models.Units.S,
            ),
            azimuth_steering_angle_pol=models.SwathInfoType.AzimuthSteeringAnglePol(
                val=[
                    models.SwathInfoType.AzimuthSteeringAnglePol.Val(value=0.1, n=1),
                    models.SwathInfoType.AzimuthSteeringAnglePol.Val(value=0.2, n=2),
                    models.SwathInfoType.AzimuthSteeringAnglePol.Val(value=0.3, n=3),
                    models.SwathInfoType.AzimuthSteeringAnglePol.Val(value=0.4, n=4),
                ],
            ),
            acquisition_prf=1000.0,
            echoes_per_burst=153,
            channel_delay=0.5,
            rx_gain=85.2,
        )

        swath_info_metadata = elements.SwathInfo(
            swath="swath_name",
            polarization="HH",
            acquisition_start_time=PreciseDateTime.from_utc_string(
                "01-JAN-2020 00:00:00.000000000000",
            ),
            acquisition_prf=1000.0,
        )
        swath_info_metadata.swath_acquisition_order = 4
        swath_info_metadata.rank = 15
        swath_info_metadata.range_delay_bias = 0.5
        swath_info_metadata.azimuth_steering_angle_reference_time = 1.0
        swath_info_metadata.azimuth_steering_angle_pol = (0.1, 0.2, 0.3, 0.4)
        swath_info_metadata.echoes_per_burst = 153
        swath_info_metadata.channel_delay = 0.5
        swath_info_metadata.rx_gain = 85.2

        self.assert_equal_swath_info(
            translate.translate_swath_info_from_model(swath_info_model),
            swath_info_metadata,
        )

        assert translate.translate_swath_info_to_model(swath_info_metadata) == swath_info_model

    def test_translate_swath_info_steering_rate(self) -> None:
        swath_info_model = models.SwathInfoType(
            swath=models.SwathInfoType.Swath(value="swath_name"),
            swath_acquisition_order=models.SwathInfoType.SwathAcquisitionOrder(value=4),
            polarization=models.PolarizationType.H_H,
            rank=models.SwathInfoType.Rank(value=15),
            range_delay_bias=models.SwathInfoType.RangeDelayBias(value=0.5, unit=models.Units.S),
            acquisition_start_time=models.SwathInfoType.AcquisitionStartTime(
                value="01-JAN-2020 00:00:00.000000000000",
                unit=models.Units.UTC,
            ),
            azimuth_steering_rate_reference_time=models.DoubleWithUnit(
                value=1.0,
                unit=models.Units.S,
            ),
            azimuth_steering_rate_pol=models.SwathInfoType.AzimuthSteeringRatePol(
                val=[
                    models.SwathInfoType.AzimuthSteeringRatePol.Val(value=0.1, n=1),
                    models.SwathInfoType.AzimuthSteeringRatePol.Val(value=0.2, n=2),
                    models.SwathInfoType.AzimuthSteeringRatePol.Val(value=0.3, n=3),
                ],
            ),
            acquisition_prf=1000.0,
            echoes_per_burst=153,
            channel_delay=0.5,
            rx_gain=85.2,
        )

        swath_info_metadata = elements.SwathInfo(
            swath="swath_name",
            polarization="HH",
            acquisition_start_time=PreciseDateTime.from_utc_string(
                "01-JAN-2020 00:00:00.000000000000",
            ),
            acquisition_prf=1000.0,
        )
        swath_info_metadata.swath_acquisition_order = 4
        swath_info_metadata.rank = 15
        swath_info_metadata.range_delay_bias = 0.5
        swath_info_metadata.azimuth_steering_rate_reference_time = 1.0
        swath_info_metadata.azimuth_steering_rate_pol = (0.1, 0.2, 0.3)
        swath_info_metadata.echoes_per_burst = 153
        swath_info_metadata.channel_delay = 0.5
        swath_info_metadata.rx_gain = 85.2

        self.assert_equal_swath_info(
            translate.translate_swath_info_from_model(swath_info_model),
            swath_info_metadata,
        )

        assert translate.translate_swath_info_to_model(swath_info_metadata) == swath_info_model


class TestSamplingConstants:
    @staticmethod
    def assert_equal_sampling_constants(
        constants_a: elements.SamplingConstants,
        constants_b: elements.SamplingConstants,
    ) -> None:
        assert constants_a.frg_hz == constants_b.frg_hz
        assert constants_a.brg_hz == constants_b.brg_hz
        assert constants_a.faz_hz == constants_b.faz_hz
        assert constants_a.baz_hz == constants_b.baz_hz

    def test_translate_sampling_constants(self) -> None:
        constants_model = models.SamplingConstantsType(
            frg_hz=models.SamplingConstantsType.FrgHz(value=150.0, unit=models.Units.HZ),
            brg_hz=models.SamplingConstantsType.BrgHz(value=120.0, unit=models.Units.HZ),
            faz_hz=models.SamplingConstantsType.FazHz(value=2000.0, unit=models.Units.HZ),
            baz_hz=models.SamplingConstantsType.BazHz(value=1500.0, unit=models.Units.HZ),
        )

        constants_metadata = elements.SamplingConstants(
            frg_hz=150.0,
            brg_hz=120.0,
            faz_hz=2000.0,
            baz_hz=1500.0,
        )

        self.assert_equal_sampling_constants(
            translate.translate_sampling_constants_from_model(constants_model),
            constants_metadata,
        )

        assert (
            translate.translate_sampling_constants_to_model(constants_metadata) == constants_model
        )


class TestAcquisitionTimeLine:
    @staticmethod
    def assert_equal_acquisition_time_line(
        time_line_a: elements.AcquisitionTimeLine,
        time_line_b: elements.AcquisitionTimeLine,
    ) -> None:
        assert time_line_a.missing_lines == time_line_b.missing_lines
        assert time_line_a.swst_changes == time_line_b.swst_changes
        assert time_line_a.noise_packet == time_line_b.noise_packet
        assert time_line_a.internal_calibration == time_line_b.internal_calibration
        assert time_line_a.swl_changes == time_line_b.swl_changes
        assert time_line_a.prf_changes == time_line_b.prf_changes
        assert time_line_a.duplicated_lines == time_line_b.duplicated_lines
        assert time_line_a.chirp_period == time_line_b.chirp_period

    def setup_method(self) -> None:
        self.time_line_metadata = elements.AcquisitionTimeLine()
        self.time_line_model = models.AcquisitionTimelineType(
            missing_lines_number=0,
            missing_lines_azimuthtimes=models.AcquisitionTimelineType.MissingLinesAzimuthtimes(),
            swst_changes_number=0,
            swst_changes_azimuthtimes=models.AcquisitionTimelineType.SwstChangesAzimuthtimes(),
            swst_changes_values=models.AcquisitionTimelineType.SwstChangesValues(),
            noise_packets_number=0,
            noise_packets_azimuthtimes=models.AcquisitionTimelineType.NoisePacketsAzimuthtimes(),
            internal_calibration_number=0,
            internal_calibration_azimuthtimes=models.AcquisitionTimelineType.InternalCalibrationAzimuthtimes(),
        )

    def test_translate_acquisition_time_line(self) -> None:
        assert (
            translate.translate_acquisition_time_line_to_model(self.time_line_metadata)
            == self.time_line_model
        )

        self.assert_equal_acquisition_time_line(
            translate.translate_acquisition_time_line_from_model(self.time_line_model),
            self.time_line_metadata,
        )

    def test_translate_acquisition_time_line_with_changes(self) -> None:
        self.time_line_metadata.missing_lines = [0.0, 1.1, 2.1]
        self.time_line_metadata.swst_changes = [(0.0, 0.005), (1.2, 0.0051)]
        self.time_line_metadata.noise_packet = [0.0, 5.5, 15.2, 16.2]
        self.time_line_metadata.internal_calibration = [0.0, 2.3, 4.8, 6.9, 15.2]

        self.time_line_model.missing_lines_number = 3
        self.time_line_model.missing_lines_azimuthtimes = (
            models.AcquisitionTimelineType.MissingLinesAzimuthtimes(
                val=[
                    models.AcquisitionTimelineType.MissingLinesAzimuthtimes.Val(
                        value=0.0,
                        unit=models.Units.S,
                    ),
                    models.AcquisitionTimelineType.MissingLinesAzimuthtimes.Val(
                        value=1.1,
                        unit=models.Units.S,
                    ),
                    models.AcquisitionTimelineType.MissingLinesAzimuthtimes.Val(
                        value=2.1,
                        unit=models.Units.S,
                    ),
                ],
            )
        )
        self.time_line_model.swst_changes_number = 2
        self.time_line_model.swst_changes_azimuthtimes = (
            models.AcquisitionTimelineType.SwstChangesAzimuthtimes(
                val=[
                    models.AcquisitionTimelineType.SwstChangesAzimuthtimes.Val(
                        value=0.0,
                        unit=models.Units.S,
                    ),
                    models.AcquisitionTimelineType.SwstChangesAzimuthtimes.Val(
                        value=1.2,
                        unit=models.Units.S,
                    ),
                ],
            )
        )
        self.time_line_model.swst_changes_values = (
            models.AcquisitionTimelineType.SwstChangesValues(
                val=[
                    models.AcquisitionTimelineType.SwstChangesValues.Val(
                        value=0.005,
                        unit=models.Units.S,
                    ),
                    models.AcquisitionTimelineType.SwstChangesValues.Val(
                        value=0.0051,
                        unit=models.Units.S,
                    ),
                ],
            )
        )
        self.time_line_model.noise_packets_number = 4
        self.time_line_model.noise_packets_azimuthtimes = (
            models.AcquisitionTimelineType.NoisePacketsAzimuthtimes(
                val=[
                    models.AcquisitionTimelineType.NoisePacketsAzimuthtimes.Val(
                        value=0.0,
                        unit=models.Units.S,
                    ),
                    models.AcquisitionTimelineType.NoisePacketsAzimuthtimes.Val(
                        value=5.5,
                        unit=models.Units.S,
                    ),
                    models.AcquisitionTimelineType.NoisePacketsAzimuthtimes.Val(
                        value=15.2,
                        unit=models.Units.S,
                    ),
                    models.AcquisitionTimelineType.NoisePacketsAzimuthtimes.Val(
                        value=16.2,
                        unit=models.Units.S,
                    ),
                ],
            )
        )
        self.time_line_model.internal_calibration_number = 5

        self.time_line_model.internal_calibration_azimuthtimes = (
            models.AcquisitionTimelineType.InternalCalibrationAzimuthtimes(
                val=[
                    models.AcquisitionTimelineType.InternalCalibrationAzimuthtimes.Val(
                        value=0.0,
                        unit=models.Units.S,
                    ),
                    models.AcquisitionTimelineType.InternalCalibrationAzimuthtimes.Val(
                        value=2.3,
                        unit=models.Units.S,
                    ),
                    models.AcquisitionTimelineType.InternalCalibrationAzimuthtimes.Val(
                        value=4.8,
                        unit=models.Units.S,
                    ),
                    models.AcquisitionTimelineType.InternalCalibrationAzimuthtimes.Val(
                        value=6.9,
                        unit=models.Units.S,
                    ),
                    models.AcquisitionTimelineType.InternalCalibrationAzimuthtimes.Val(
                        value=15.2,
                        unit=models.Units.S,
                    ),
                ],
            )
        )

        assert (
            translate.translate_acquisition_time_line_to_model(self.time_line_metadata)
            == self.time_line_model
        )

        self.assert_equal_acquisition_time_line(
            translate.translate_acquisition_time_line_from_model(self.time_line_model),
            self.time_line_metadata,
        )

    def test_translate_acquisition_time_line_with_optional_changes(self) -> None:
        self.time_line_metadata.duplicated_lines = [0.0, 1.1, 2.1]
        self.time_line_metadata.swl_changes = [(0.0, 0.005), (1.2, 0.0051)]
        self.time_line_metadata.prf_changes = [
            (0.0, 1000.0),
            (2.0, 1200.0),
            (3.0, 1400.0),
            (4.0, 1500.0),
        ]
        self.time_line_metadata.chirp_period = "Chirp period"

        self.time_line_model.duplicated_lines_number = 3
        self.time_line_model.duplicated_lines_azimuthtimes = (
            models.AcquisitionTimelineType.DuplicatedLinesAzimuthtimes(
                val=[
                    models.AcquisitionTimelineType.DuplicatedLinesAzimuthtimes.Val(
                        value=0.0,
                        unit=models.Units.S,
                    ),
                    models.AcquisitionTimelineType.DuplicatedLinesAzimuthtimes.Val(
                        value=1.1,
                        unit=models.Units.S,
                    ),
                    models.AcquisitionTimelineType.DuplicatedLinesAzimuthtimes.Val(
                        value=2.1,
                        unit=models.Units.S,
                    ),
                ],
            )
        )

        self.time_line_model.swl_changes_number = 2
        self.time_line_model.swl_changes_azimuthtimes = (
            models.AcquisitionTimelineType.SwlChangesAzimuthtimes(
                val=[
                    models.AcquisitionTimelineType.SwlChangesAzimuthtimes.Val(
                        value=0.0,
                        unit=models.Units.S,
                    ),
                    models.AcquisitionTimelineType.SwlChangesAzimuthtimes.Val(
                        value=1.2,
                        unit=models.Units.S,
                    ),
                ],
            )
        )
        self.time_line_model.swl_changes_values = models.AcquisitionTimelineType.SwlChangesValues(
            val=[
                models.AcquisitionTimelineType.SwlChangesValues.Val(
                    value=0.005,
                    unit=models.Units.S,
                ),
                models.AcquisitionTimelineType.SwlChangesValues.Val(
                    value=0.0051,
                    unit=models.Units.S,
                ),
            ],
        )

        self.time_line_model.prf_changes_number = 4
        self.time_line_model.prf_changes_azimuthtimes = (
            models.AcquisitionTimelineType.PrfChangesAzimuthtimes(
                val=[
                    models.AcquisitionTimelineType.PrfChangesAzimuthtimes.Val(
                        value=0.0,
                        unit=models.Units.S,
                    ),
                    models.AcquisitionTimelineType.PrfChangesAzimuthtimes.Val(
                        value=2.0,
                        unit=models.Units.S,
                    ),
                    models.AcquisitionTimelineType.PrfChangesAzimuthtimes.Val(
                        value=3.0,
                        unit=models.Units.S,
                    ),
                    models.AcquisitionTimelineType.PrfChangesAzimuthtimes.Val(
                        value=4.0,
                        unit=models.Units.S,
                    ),
                ],
            )
        )
        self.time_line_model.prf_changes_values = models.AcquisitionTimelineType.PrfChangesValues(
            val=[
                models.AcquisitionTimelineType.PrfChangesValues.Val(
                    value=1000.0,
                    unit=models.Units.HZ,
                ),
                models.AcquisitionTimelineType.PrfChangesValues.Val(
                    value=1200.0,
                    unit=models.Units.HZ,
                ),
                models.AcquisitionTimelineType.PrfChangesValues.Val(
                    value=1400.0,
                    unit=models.Units.HZ,
                ),
                models.AcquisitionTimelineType.PrfChangesValues.Val(
                    value=1500.0,
                    unit=models.Units.HZ,
                ),
            ],
        )

        self.time_line_model.chirp_period = "Chirp period"

        assert (
            translate.translate_acquisition_time_line_to_model(self.time_line_metadata)
            == self.time_line_model
        )

        self.assert_equal_acquisition_time_line(
            translate.translate_acquisition_time_line_from_model(self.time_line_model),
            self.time_line_metadata,
        )


class TestAttitudeInfo:
    @staticmethod
    def assert_equal_attitude_info(
        attitude_a: elements.AttitudeInfo,
        attitude_b: elements.AttitudeInfo,
    ) -> None:
        assert attitude_a.reference_frame == attitude_b.reference_frame
        assert attitude_a.rotation_order == attitude_b.rotation_order
        assert attitude_a.ypr_deg.shape[0] == attitude_b.ypr_deg.shape[0]
        assert attitude_a.attitude_type == attitude_b.attitude_type

        np.testing.assert_allclose(attitude_a.ypr_deg, attitude_b.ypr_deg)

        assert attitude_a.reference_time == attitude_b.reference_time
        assert attitude_a.time_step == attitude_b.time_step

    def setup_method(self) -> None:
        self.attitude_model = models.AttitudeInfoType(
            t_ref_utc="01-JAN-2023 00:00:00.000000000000",
            dt_ypr_s=models.AttitudeInfoType.DtYprS(value=1.5),
            n_ypr_n=models.AttitudeInfoType.NYprN(value=3),
            yaw_deg=models.AttitudeInfoType.YawDeg(
                val=[
                    models.AttitudeInfoType.YawDeg.Val(value=0.5, n=1),
                    models.AttitudeInfoType.YawDeg.Val(value=1.0, n=2),
                    models.AttitudeInfoType.YawDeg.Val(value=1.5, n=3),
                ],
            ),
            pitch_deg=models.AttitudeInfoType.PitchDeg(
                val=[
                    models.AttitudeInfoType.PitchDeg.Val(value=-0.5, n=1),
                    models.AttitudeInfoType.PitchDeg.Val(value=-1.0, n=2),
                    models.AttitudeInfoType.PitchDeg.Val(value=-1.5, n=3),
                ],
            ),
            roll_deg=models.AttitudeInfoType.RollDeg(
                val=[
                    models.AttitudeInfoType.RollDeg.Val(value=30.2, n=1),
                    models.AttitudeInfoType.RollDeg.Val(value=31.2, n=2),
                    models.AttitudeInfoType.RollDeg.Val(value=32.2, n=3),
                ],
            ),
            reference_frame=models.ReferenceFrameType.ZERODOPPLER,
            rotation_order=models.RotationOrderType.PRY,
            attitude_type=models.AttitudeType.REFINED,
        )

        self.attitude_metadata = elements.AttitudeInfo(
            ypr_deg=np.asarray(
                [[0.5, -0.5, 30.2], [1.0, -1.0, 31.2], [1.5, -1.5, 32.2]],
                dtype=np.float64,
            ),
            reference_time=PreciseDateTime.from_numeric_datetime(year=2023),
            time_step=1.5,
            reference_frame="ZERODOPPLER",
            rotation_order="PRY",
            attitude_type="REFINED",
        )

    def test_translate_attitude_info(self) -> None:
        self.assert_equal_attitude_info(
            translate.translate_attitude_from_model(self.attitude_model),
            self.attitude_metadata,
        )

        assert translate.translate_attitude_to_model(self.attitude_metadata) == self.attitude_model

    def test_translate_attitude_info_rejects_inconsistent_n_ypr_n(self) -> None:
        self.attitude_model.n_ypr_n = models.AttitudeInfoType.NYprN(value=2)

        with pytest.raises(ValueError, match=r".*"):
            translate.translate_attitude_from_model(self.attitude_model)


class TestBurstInfo:
    @staticmethod
    def assert_equal_burst(
        burst_a: elements.Burst,
        burst_b: elements.Burst,
    ) -> None:
        assert burst_a.range_start_time == burst_b.range_start_time
        assert burst_a.azimuth_start_time == burst_b.azimuth_start_time
        assert burst_a.burst_center_azimuth_shift == burst_b.burst_center_azimuth_shift
        assert burst_a.lines == burst_b.lines

    def assert_equal_burst_info(
        self,
        info_a: elements.BurstInfo,
        info_b: elements.BurstInfo,
    ) -> None:
        assert info_a.burst_repetition_frequency == info_b.burst_repetition_frequency
        assert len(info_a.bursts) == len(info_b.bursts)
        for burst_a, burst_b in zip(info_a.bursts, info_b.bursts, strict=True):
            self.assert_equal_burst(burst_a, burst_b)

    def setup_method(self) -> None:
        self.burst_info_metadata = elements.BurstInfo(
            burst_repetition_frequency=20.5,
            bursts=[
                elements.Burst(
                    range_start_time=0.005,
                    azimuth_start_time=PreciseDateTime.from_numeric_datetime(year=2021),
                    lines=1520,
                ),
                elements.Burst(
                    range_start_time=0.0055,
                    azimuth_start_time=PreciseDateTime.from_numeric_datetime(year=2023),
                    lines=1520,
                ),
            ],
        )

        burst_model_one = models.BurstType(
            range_start_time=models.DoubleWithUnit(value=0.005, unit=models.Units.S),
            azimuth_start_time=models.StringWithUnit(
                value="01-JAN-2021 00:00:00.000000000000",
                unit=models.Units.UTC,
            ),
            n=1,
        )
        burst_model_two = models.BurstType(
            range_start_time=models.DoubleWithUnit(value=0.0055, unit=models.Units.S),
            azimuth_start_time=models.StringWithUnit(
                value="01-JAN-2023 00:00:00.000000000000",
                unit=models.Units.UTC,
            ),
            n=2,
        )

        self.burst_info_model = models.BurstInfoType(
            number_of_bursts=2,
            lines_per_burst=None,
            lines_per_burst_change_list=models.BurstInfoType.LinesPerBurstChangeList(
                lines=[
                    models.BurstInfoType.LinesPerBurstChangeList.Lines(value=1520, from_burst=1),
                ],
            ),
            burst_repetition_frequency=models.DoubleWithUnit(value=20.5, unit=models.Units.HZ),
            burst=[burst_model_one, burst_model_two],
        )

    def test_translate_burst_info(self) -> None:
        self.assert_equal_burst_info(
            translate.translate_burst_info_from_model(self.burst_info_model),
            self.burst_info_metadata,
        )

        assert (
            translate.translate_burst_info_to_model(self.burst_info_metadata)
            == self.burst_info_model
        )

    def test_translate_burst_info_different_lines_and_shift(self) -> None:
        self.burst_info_model.burst.append(
            models.BurstType(
                range_start_time=models.DoubleWithUnit(value=0.008, unit=models.Units.S),
                azimuth_start_time=models.StringWithUnit(
                    value="01-JAN-2022 00:00:00.000000000000",
                    unit=models.Units.UTC,
                ),
                n=3,
                burst_center_azimuth_shift=models.DoubleWithUnit(value=0.56, unit=models.Units.S),
            ),
        )
        self.burst_info_model.number_of_bursts = 3
        assert self.burst_info_model.lines_per_burst_change_list is not None
        self.burst_info_model.lines_per_burst_change_list.lines.append(
            models.BurstInfoType.LinesPerBurstChangeList.Lines(value=2000, from_burst=3),
        )

        self.burst_info_metadata.bursts.append(
            elements.Burst(
                range_start_time=0.008,
                azimuth_start_time=PreciseDateTime.from_numeric_datetime(year=2022),
                lines=2000,
                burst_center_azimuth_shift=0.56,
            ),
        )

        self.assert_equal_burst_info(
            translate.translate_burst_info_from_model(self.burst_info_model),
            self.burst_info_metadata,
        )

        assert (
            translate.translate_burst_info_to_model(self.burst_info_metadata)
            == self.burst_info_model
        )


class TestStateVectors:
    @staticmethod
    def assert_equal_state_vectors(
        sv_a: elements.StateVectors,
        sv_b: elements.StateVectors,
    ) -> None:
        assert sv_a.anx_position == sv_b.anx_position
        assert sv_a.anx_time == sv_b.anx_time
        assert sv_a.orbit_direction == sv_b.orbit_direction
        assert sv_a.orbit_number == sv_b.orbit_number
        assert sv_a.reference_time == sv_b.reference_time
        assert sv_a.position_vector.shape[0] == sv_b.position_vector.shape[0]
        assert sv_a.time_step == sv_b.time_step
        assert sv_a.track_number == sv_b.track_number

        assert sv_a.position_vector.shape == sv_b.position_vector.shape
        for pos_a, pos_b in zip(sv_a.position_vector, sv_b.position_vector, strict=False):
            for comp_a, comp_b in zip(pos_a, pos_b, strict=False):
                assert comp_a == comp_b

        assert sv_a.velocity_vector.shape == sv_b.velocity_vector.shape
        for vel_a, vel_b in zip(sv_a.velocity_vector, sv_b.velocity_vector, strict=False):
            for comp_a, comp_b in zip(vel_a, vel_b, strict=False):
                assert comp_a == comp_b

    def setup_method(self) -> None:
        self.state_vectors_model = models.StateVectorDataType(
            p_sv_m=models.StateVectorDataType.PSvM(
                val=[
                    models.StateVectorDataType.PSvM.Val(value=1.2, n=1),
                    models.StateVectorDataType.PSvM.Val(value=2.3, n=2),
                    models.StateVectorDataType.PSvM.Val(value=3.4, n=3),
                    models.StateVectorDataType.PSvM.Val(value=4.5, n=4),
                    models.StateVectorDataType.PSvM.Val(value=5.6, n=5),
                    models.StateVectorDataType.PSvM.Val(value=6.7, n=6),
                ],
            ),
            v_sv_m_os=models.StateVectorDataType.VSvMOs(
                val=[
                    models.StateVectorDataType.VSvMOs.Val(value=11.2, n=1),
                    models.StateVectorDataType.VSvMOs.Val(value=12.3, n=2),
                    models.StateVectorDataType.VSvMOs.Val(value=13.4, n=3),
                    models.StateVectorDataType.VSvMOs.Val(value=14.5, n=4),
                    models.StateVectorDataType.VSvMOs.Val(value=15.6, n=5),
                    models.StateVectorDataType.VSvMOs.Val(value=16.7, n=6),
                ],
            ),
            orbit_number="NOT_AVAILABLE",
            track="NOT_AVAILABLE",
            orbit_direction=models.AscendingDescendingType.ASCENDING,
            t_ref_utc="01-JAN-2020 00:00:00.000000000000",
            dt_sv_s=models.StateVectorDataType.DtSvS(value=1.2, unit=models.Units.S),
            n_sv_n=models.StateVectorDataType.NSvN(value=2),
        )

        positions = np.zeros(shape=(2, 3))
        positions[0, :] = [1.2, 2.3, 3.4]
        positions[1, :] = [4.5, 5.6, 6.7]

        velocities = np.zeros(shape=(2, 3))
        velocities[0, :] = [11.2, 12.3, 13.4]
        velocities[1, :] = [14.5, 15.6, 16.7]

        self.state_vectors_metadata = elements.StateVectors(
            position_vector=positions,
            velocity_vector=velocities,
            reference_time=PreciseDateTime.from_numeric_datetime(year=2020),
            time_step=1.2,
        )

    def test_translate_state_vectors(self) -> None:
        assert (
            translate.translate_state_vectors_to_model(self.state_vectors_metadata)
            == self.state_vectors_model
        )
        self.assert_equal_state_vectors(
            translate.translate_state_vectors_from_model(self.state_vectors_model),
            self.state_vectors_metadata,
        )

    def test_translate_state_vectors_anx(self) -> None:
        self.state_vectors_metadata = self.state_vectors_metadata.model_copy(
            update={
                "anx_time": PreciseDateTime.from_numeric_datetime(year=2019),
                "anx_position": (1, 2, 3),
            },
        )
        self.state_vectors_model.ascending_node_coords = (
            models.StateVectorDataType.AscendingNodeCoords(
                val=[
                    models.StateVectorDataType.AscendingNodeCoords.Val(value=1),
                    models.StateVectorDataType.AscendingNodeCoords.Val(value=2),
                    models.StateVectorDataType.AscendingNodeCoords.Val(value=3),
                ],
            )
        )
        self.state_vectors_model.ascending_node_time = "01-JAN-2019 00:00:00.000000000000"

        assert (
            translate.translate_state_vectors_to_model(self.state_vectors_metadata)
            == self.state_vectors_model
        )
        self.assert_equal_state_vectors(
            translate.translate_state_vectors_from_model(self.state_vectors_model),
            self.state_vectors_metadata,
        )

    def test_translate_state_vectors_auxiliary_info(self) -> None:
        self.state_vectors_metadata.orbit_number = 5
        self.state_vectors_metadata.track_number = 10
        self.state_vectors_model.orbit_number = "5"
        self.state_vectors_model.track = "10"

        assert (
            translate.translate_state_vectors_to_model(self.state_vectors_metadata)
            == self.state_vectors_model
        )
        self.assert_equal_state_vectors(
            translate.translate_state_vectors_from_model(self.state_vectors_model),
            self.state_vectors_metadata,
        )

    def test_translate_state_vectors_orbit_direction_mismatch(self) -> None:
        self.state_vectors_model.orbit_direction = models.AscendingDescendingType.DESCENDING

        with pytest.warns(UserWarning, match=r".*"):
            state_vectors = translate.translate_state_vectors_from_model(self.state_vectors_model)

        state_vectors_model = translate.translate_state_vectors_to_model(state_vectors)
        assert state_vectors_model == self.state_vectors_model

        assert state_vectors.annotated_orbit_direction == "DESCENDING"
        assert state_vectors.orbit_direction == "ASCENDING"

    def test_translate_state_vectors_annotated_orbit_not_available(self) -> None:
        self.state_vectors_model.orbit_direction = models.AscendingDescendingType.NOT_AVAILABLE

        with pytest.warns(UserWarning, match=r".*"):
            state_vectors = translate.translate_state_vectors_from_model(self.state_vectors_model)
        assert state_vectors.annotated_orbit_direction is None
        assert state_vectors.orbit_direction == "ASCENDING"

        state_vectors_model = translate.translate_state_vectors_to_model(state_vectors)
        assert state_vectors_model == self.state_vectors_model


def assert_equal_poly2d(
    poly_a: elements.Poly2D,
    poly_b: elements.Poly2D,
) -> None:
    assert poly_a.coefficients == poly_b.coefficients
    assert poly_a.t_ref_az == poly_b.t_ref_az
    assert poly_a.t_ref_rg == poly_b.t_ref_rg


def test_translate_polynomial() -> None:
    poly_metadata = elements.Poly2D(
        t_ref_az=PreciseDateTime.from_numeric_datetime(year=2020),
        t_ref_rg=0.005,
        coefficients=[1, 2, 3, 4, 5, 6, 7],
    )
    poly_model = models.PolyType(
        pol=models.PolyType.Pol(
            val=[
                models.PolyType.Pol.Val(value=1, n=1, unit=models.Units.VALUE),
                models.PolyType.Pol.Val(value=2, n=2, unit=models.Units.VALUE),
                models.PolyType.Pol.Val(value=3, n=3, unit=models.Units.VALUE),
                models.PolyType.Pol.Val(value=4, n=4, unit=models.Units.VALUE),
                models.PolyType.Pol.Val(value=5, n=5, unit=models.Units.VALUE),
                models.PolyType.Pol.Val(value=6, n=6, unit=models.Units.VALUE),
                models.PolyType.Pol.Val(value=7, n=7, unit=models.Units.VALUE),
            ],
        ),
        trg0_s=models.PolyType.Trg0S(value=0.005, unit=models.Units.S),
        taz0_utc=models.PolyType.Taz0Utc(
            value="01-JAN-2020 00:00:00.000000000000",
            unit=models.Units.UTC,
        ),
    )

    assert_equal_poly2d(
        translate.translate_polynomial_from_model(poly_model, elements.Poly2D),
        poly_metadata,
    )
    assert translate.translate_polynomial_to_model(poly_metadata) == poly_model


PieceWisePolynomials2D = elements.DopplerCentroidVector | elements.DopplerRateVector


class TestPoly2DList:
    @staticmethod
    def assert_equal_poly_list(
        poly_list_a: PieceWisePolynomials2D, poly_list_b: PieceWisePolynomials2D
    ) -> None:
        assert type(poly_list_a) is type(poly_list_b)

        for poly_a, poly_b in zip(poly_list_a.poly_list, poly_list_b.poly_list, strict=False):
            assert type(poly_a) is type(poly_b)
            assert poly_a.coefficients == poly_b.coefficients
            assert poly_a.t_ref_az == poly_b.t_ref_az
            assert poly_a.t_ref_rg == poly_b.t_ref_rg

    def test_translate_doppler_centroid(self) -> None:
        doppler_centroid_metadata = elements.DopplerCentroidVector(
            poly_list=[
                elements.DopplerCentroid(
                    t_ref_az=PreciseDateTime.from_numeric_datetime(year=2020),
                    t_ref_rg=0.005,
                    coefficients=[1, 2, 3, 4, 5, 6, 7],
                ),
            ],
        )

        doppler_centroid_model = [
            models.PolyType(
                number=1,
                total=1,
                pol=models.PolyType.Pol(
                    val=[
                        models.PolyType.Pol.Val(value=1, n=1, unit=models.Units.HZ),
                        models.PolyType.Pol.Val(value=2, n=2, unit=models.Units.HZ_S),
                        models.PolyType.Pol.Val(value=3, n=3, unit=models.Units.HZ_S),
                        models.PolyType.Pol.Val(value=4, n=4, unit=models.Units.HZ_S2),
                        models.PolyType.Pol.Val(value=5, n=5, unit=models.Units.HZ_S2),
                        models.PolyType.Pol.Val(value=6, n=6, unit=models.Units.HZ_S3),
                        models.PolyType.Pol.Val(value=7, n=7, unit=models.Units.HZ_S4),
                    ],
                ),
                trg0_s=models.PolyType.Trg0S(value=0.005, unit=models.Units.S),
                taz0_utc=models.PolyType.Taz0Utc(
                    value="01-JAN-2020 00:00:00.000000000000",
                    unit=models.Units.UTC,
                ),
            ),
        ]

        assert (
            translate.translate_polynomial_list_to_model(doppler_centroid_metadata.poly_list)
            == doppler_centroid_model
        )
        self.assert_equal_poly_list(
            elements.DopplerCentroidVector(
                poly_list=[
                    translate.translate_polynomial_from_model(
                        poly,
                        elements.DopplerCentroidVector.SINGLE_POLY_TYPE,
                    )
                    for poly in doppler_centroid_model
                ],
            ),
            doppler_centroid_metadata,
        )

    def test_translate_doppler_centroid_all_orders(self) -> None:
        doppler_centroid_metadata = elements.DopplerCentroidVector(
            poly_list=[
                elements.DopplerCentroid(
                    t_ref_az=PreciseDateTime.from_numeric_datetime(year=2020),
                    t_ref_rg=0.005,
                    coefficients=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                ),
            ],
        )

        doppler_centroid_model = [
            models.PolyType(
                number=1,
                total=1,
                pol=models.PolyType.Pol(
                    val=[
                        models.PolyType.Pol.Val(value=1, n=1, unit=models.Units.HZ),
                        models.PolyType.Pol.Val(value=2, n=2, unit=models.Units.HZ_S),
                        models.PolyType.Pol.Val(value=3, n=3, unit=models.Units.HZ_S),
                        models.PolyType.Pol.Val(value=4, n=4, unit=models.Units.HZ_S2),
                        models.PolyType.Pol.Val(value=5, n=5, unit=models.Units.HZ_S2),
                        models.PolyType.Pol.Val(value=6, n=6, unit=models.Units.HZ_S3),
                        models.PolyType.Pol.Val(value=7, n=7, unit=models.Units.HZ_S4),
                        models.PolyType.Pol.Val(value=8, n=8, unit=models.Units.HZ_S5),
                        models.PolyType.Pol.Val(value=9, n=9, unit=models.Units.HZ_S6),
                        models.PolyType.Pol.Val(value=10, n=10, unit=models.Units.HZ_S7),
                        models.PolyType.Pol.Val(value=11, n=11, unit=models.Units.HZ_S8),
                    ],
                ),
                trg0_s=models.PolyType.Trg0S(value=0.005, unit=models.Units.S),
                taz0_utc=models.PolyType.Taz0Utc(
                    value="01-JAN-2020 00:00:00.000000000000",
                    unit=models.Units.UTC,
                ),
            ),
        ]

        assert (
            translate.translate_polynomial_list_to_model(doppler_centroid_metadata.poly_list)
            == doppler_centroid_model
        )
        self.assert_equal_poly_list(
            elements.DopplerCentroidVector(
                poly_list=[
                    translate.translate_polynomial_from_model(
                        poly,
                        elements.DopplerCentroidVector.SINGLE_POLY_TYPE,
                    )
                    for poly in doppler_centroid_model
                ],
            ),
            doppler_centroid_metadata,
        )

    def test_translate_doppler_rate(self) -> None:
        doppler_rate_metadata = elements.DopplerRateVector(
            poly_list=[
                elements.DopplerRate(
                    t_ref_az=PreciseDateTime.from_numeric_datetime(year=2020),
                    t_ref_rg=0.005,
                    coefficients=[1, 2, 3, 4, 5, 6, 7],
                ),
            ],
        )

        doppler_rate_model = [
            models.PolyType(
                number=1,
                total=1,
                pol=models.PolyType.Pol(
                    val=[
                        models.PolyType.Pol.Val(value=1, n=1, unit=models.Units.HZ_S),
                        models.PolyType.Pol.Val(value=2, n=2, unit=models.Units.HZ_S2),
                        models.PolyType.Pol.Val(value=3, n=3, unit=models.Units.HZ_S2),
                        models.PolyType.Pol.Val(value=4, n=4, unit=models.Units.HZ_S3),
                        models.PolyType.Pol.Val(value=5, n=5, unit=models.Units.HZ_S3),
                        models.PolyType.Pol.Val(value=6, n=6, unit=models.Units.HZ_S4),
                        models.PolyType.Pol.Val(value=7, n=7, unit=models.Units.HZ_S5),
                    ],
                ),
                trg0_s=models.PolyType.Trg0S(value=0.005, unit=models.Units.S),
                taz0_utc=models.PolyType.Taz0Utc(
                    value="01-JAN-2020 00:00:00.000000000000",
                    unit=models.Units.UTC,
                ),
            ),
        ]

        assert (
            translate.translate_polynomial_list_to_model(doppler_rate_metadata.poly_list)
            == doppler_rate_model
        )
        self.assert_equal_poly_list(
            elements.DopplerRateVector(
                poly_list=[
                    translate.translate_polynomial_from_model(
                        poly,
                        elements.DopplerRateVector.SINGLE_POLY_TYPE,
                    )
                    for poly in doppler_rate_model
                ],
            ),
            doppler_rate_metadata,
        )

    def test_translate_doppler_rate_all_orders(self) -> None:
        doppler_rate_metadata = elements.DopplerRateVector(
            poly_list=[
                elements.DopplerRate(
                    t_ref_az=PreciseDateTime.from_numeric_datetime(year=2020),
                    t_ref_rg=0.005,
                    coefficients=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                ),
            ],
        )

        doppler_rate_model = [
            models.PolyType(
                number=1,
                total=1,
                pol=models.PolyType.Pol(
                    val=[
                        models.PolyType.Pol.Val(value=1, n=1, unit=models.Units.HZ_S),
                        models.PolyType.Pol.Val(value=2, n=2, unit=models.Units.HZ_S2),
                        models.PolyType.Pol.Val(value=3, n=3, unit=models.Units.HZ_S2),
                        models.PolyType.Pol.Val(value=4, n=4, unit=models.Units.HZ_S3),
                        models.PolyType.Pol.Val(value=5, n=5, unit=models.Units.HZ_S3),
                        models.PolyType.Pol.Val(value=6, n=6, unit=models.Units.HZ_S4),
                        models.PolyType.Pol.Val(value=7, n=7, unit=models.Units.HZ_S5),
                        models.PolyType.Pol.Val(value=8, n=8, unit=models.Units.HZ_S6),
                        models.PolyType.Pol.Val(value=9, n=9, unit=models.Units.HZ_S7),
                        models.PolyType.Pol.Val(value=10, n=10, unit=models.Units.HZ_S8),
                        models.PolyType.Pol.Val(value=11, n=11, unit=models.Units.HZ_S9),
                    ],
                ),
                trg0_s=models.PolyType.Trg0S(value=0.005, unit=models.Units.S),
                taz0_utc=models.PolyType.Taz0Utc(
                    value="01-JAN-2020 00:00:00.000000000000",
                    unit=models.Units.UTC,
                ),
            ),
        ]

        assert (
            translate.translate_polynomial_list_to_model(doppler_rate_metadata.poly_list)
            == doppler_rate_model
        )
        self.assert_equal_poly_list(
            elements.DopplerRateVector(
                poly_list=[
                    translate.translate_polynomial_from_model(
                        poly,
                        elements.DopplerRateVector.SINGLE_POLY_TYPE,
                    )
                    for poly in doppler_rate_model
                ],
            ),
            doppler_rate_metadata,
        )


def assert_equal_coreg_poly(
    poly_a: elements.CoregPoly,
    poly_b: elements.CoregPoly,
) -> None:
    assert poly_a.coefficients_az == poly_b.coefficients_az
    assert poly_a.coefficients_rg == poly_b.coefficients_rg
    assert poly_a.t_ref_az == poly_b.t_ref_az
    assert poly_a.t_ref_rg == poly_b.t_ref_rg


def test_translate_coreg_polynomial() -> None:
    poly_metadata = elements.CoregPoly(
        t_ref_az=PreciseDateTime.from_numeric_datetime(year=2020),
        t_ref_rg=0.005,
        coefficients_az=[1, 2, 3, 4],
        coefficients_rg=[11, 12, 13, 14],
    )
    poly_model = models.PolyCoregType(
        pol_az=models.PolyCoregType.PolAz(
            val=[
                models.PolyCoregType.PolAz.Val(value=1, n=1),
                models.PolyCoregType.PolAz.Val(value=2, n=2),
                models.PolyCoregType.PolAz.Val(value=3, n=3),
                models.PolyCoregType.PolAz.Val(value=4, n=4),
            ],
        ),
        pol_rg=models.PolyCoregType.PolRg(
            val=[
                models.PolyCoregType.PolRg.Val(value=11, n=1),
                models.PolyCoregType.PolRg.Val(value=12, n=2),
                models.PolyCoregType.PolRg.Val(value=13, n=3),
                models.PolyCoregType.PolRg.Val(value=14, n=4),
            ],
        ),
        trg0_s=models.PolyCoregType.Trg0S(value=0.005, unit=models.Units.S),
        taz0_utc=models.PolyCoregType.Taz0Utc(
            value="01-JAN-2020 00:00:00.000000000000",
            unit=models.Units.UTC,
        ),
    )

    assert_equal_coreg_poly(
        translate.translate_coreg_polynomial_from_model(poly_model),
        poly_metadata,
    )
    assert translate.translate_coreg_polynomial_to_model(poly_metadata) == poly_model


class TestCoregPolyList:
    @staticmethod
    def assert_equal_poly_list(
        poly_list_a: elements.CoregPolyVector,
        poly_list_b: elements.CoregPolyVector,
    ) -> None:
        assert type(poly_list_a) is type(poly_list_b)

        for poly_a, poly_b in zip(poly_list_a.poly_list, poly_list_b.poly_list, strict=False):
            assert type(poly_a) is type(poly_b)
            poly_a: elements.CoregPoly
            poly_b: elements.CoregPoly
            assert poly_a.coefficients_az == poly_b.coefficients_az
            assert poly_a.coefficients_rg == poly_b.coefficients_rg
            assert poly_a.t_ref_az == poly_b.t_ref_az
            assert poly_a.t_ref_rg == poly_b.t_ref_rg

    def test_translate_coreg_poly(self) -> None:
        coreg_poly_metadata = elements.CoregPolyVector(
            poly_list=[
                elements.CoregPoly(
                    t_ref_az=PreciseDateTime.from_numeric_datetime(year=2020),
                    t_ref_rg=0.005,
                    coefficients_az=[1, 2, 3, 4],
                    coefficients_rg=[11, 12, 13, 14],
                ),
            ],
        )

        coreg_poly_model = [
            models.PolyCoregType(
                number=1,
                total=1,
                pol_az=models.PolyCoregType.PolAz(
                    val=[
                        models.PolyCoregType.PolAz.Val(value=1, n=1),
                        models.PolyCoregType.PolAz.Val(value=2, n=2),
                        models.PolyCoregType.PolAz.Val(value=3, n=3),
                        models.PolyCoregType.PolAz.Val(value=4, n=4),
                    ],
                ),
                pol_rg=models.PolyCoregType.PolRg(
                    val=[
                        models.PolyCoregType.PolRg.Val(value=11, n=1),
                        models.PolyCoregType.PolRg.Val(value=12, n=2),
                        models.PolyCoregType.PolRg.Val(value=13, n=3),
                        models.PolyCoregType.PolRg.Val(value=14, n=4),
                    ],
                ),
                trg0_s=models.PolyCoregType.Trg0S(value=0.005, unit=models.Units.S),
                taz0_utc=models.PolyCoregType.Taz0Utc(
                    value="01-JAN-2020 00:00:00.000000000000",
                    unit=models.Units.UTC,
                ),
            ),
        ]

        assert (
            translate.translate_coreg_polynomial_list_to_model(coreg_poly_metadata.poly_list)
            == coreg_poly_model
        )
        self.assert_equal_poly_list(
            translate.translate_coreg_polynomial_list_from_model(coreg_poly_model),
            coreg_poly_metadata,
        )


def test_translate_slant_to_incidence_units() -> None:
    poly_metadata = elements.SlantToIncidence(
        t_ref_az=PreciseDateTime.from_numeric_datetime(year=2020),
        t_ref_rg=0.005,
        coefficients=[1, 2, 3, 4, 5, 6, 7],
    )

    poly_model = translate.translate_polynomial_to_model(poly_metadata)

    assert poly_model.pol.val[0].unit == models.Units.DEG
    assert poly_model.pol.val[1].unit == models.Units.DEG_S


def test_translate_polynomial_preserves_all_supported_orders() -> None:
    poly_metadata = elements.Poly2D(
        t_ref_az=PreciseDateTime.from_numeric_datetime(year=2020),
        t_ref_rg=0.005,
        coefficients=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
    )

    poly_model = translate.translate_polynomial_to_model(poly_metadata)

    assert len(poly_model.pol.val) == 11
    assert [val.value for val in poly_model.pol.val] == poly_metadata.coefficients


class TestDataStatistics:
    @staticmethod
    def assert_equal_data_statistics(
        stat_a: elements.DataStatistics,
        stat_b: elements.DataStatistics,
    ) -> None:
        assert stat_a.num_samples == stat_b.num_samples
        assert stat_a.max_i == stat_b.max_i
        assert stat_a.max_q == stat_b.max_q
        assert stat_a.min_i == stat_b.min_i
        assert stat_a.min_q == stat_b.min_q
        assert stat_a.sum_i == stat_b.sum_i
        assert stat_a.sum_q == stat_b.sum_q
        assert stat_a.sum_2_i == stat_b.sum_2_i
        assert stat_a.sum_2_q == stat_b.sum_2_q
        assert stat_a.std_dev_i == stat_b.std_dev_i
        assert stat_a.std_dev_q == stat_b.std_dev_q
        assert len(stat_a.statistics_list) == len(stat_b.statistics_list)
        for block_a, block_b in zip(stat_a.statistics_list, stat_b.statistics_list, strict=False):
            assert block_a.num_samples == block_b.num_samples
            assert block_a.max_i == block_b.max_i
            assert block_a.max_q == block_b.max_q
            assert block_a.min_i == block_b.min_i
            assert block_a.min_q == block_b.min_q
            assert block_a.sum_i == block_b.sum_i
            assert block_a.sum_q == block_b.sum_q
            assert block_a.sum_2_i == block_b.sum_2_i
            assert block_a.sum_2_q == block_b.sum_2_q

    def setup_method(self) -> None:
        self.stat_metadata = elements.DataStatistics(
            num_samples=5,
            max_i=2.1,
            min_i=-2.0,
            max_q=8.5,
            min_q=-9.6,
            sum_i=20.2,
            sum_q=-5.2,
            sum_2_i=50.0,
            sum_2_q=81,
            std_dev_i=5.0,
            std_dev_q=6.4,
        )

        self.stat_model = models.DataStatisticsType(
            num_samples=models.DataStatisticsType.NumSamples(value=5),
            max_i=models.DataStatisticsType.MaxI(value=2.1),
            min_i=models.DataStatisticsType.MinI(value=-2.0),
            max_q=models.DataStatisticsType.MaxQ(value=8.5),
            min_q=models.DataStatisticsType.MinQ(value=-9.6),
            sum_i=models.DataStatisticsType.SumI(value=20.2),
            sum_q=models.DataStatisticsType.SumQ(value=-5.2),
            sum2_i=models.DataStatisticsType.Sum2I(value=50.0),
            sum2_q=models.DataStatisticsType.Sum2Q(value=81),
            std_dev_i=models.DataStatisticsType.StdDevI(value=5.0),
            std_dev_q=models.DataStatisticsType.StdDevQ(value=6.4),
        )

    def test_translate_data_statistics(self) -> None:
        self.assert_equal_data_statistics(
            translate.translate_data_statistics_from_model(self.stat_model),
            self.stat_metadata,
        )
        assert translate.translate_data_statistics_to_model(self.stat_metadata) == self.stat_model


@pytest.mark.parametrize(
    ("model_value", "expected"),
    [
        (models.SensorNamesType.NOT_SET, "NOT SET"),
        (models.SensorNamesType.ASAR, "ASAR"),
        (models.SensorNamesType.PALSAR, "PALSAR"),
        (models.SensorNamesType.ERS1, "ERS1"),
        (models.SensorNamesType.ERS2, "ERS2"),
        (models.SensorNamesType.RADARSAT, "RADARSAT"),
        (models.SensorNamesType.TERRASARX, "TERRASARX"),
        (models.SensorNamesType.SENTINEL1, "SENTINEL1"),
        (models.SensorNamesType.SENTINEL1_A, "SENTINEL1A"),
        (models.SensorNamesType.SENTINEL1_B, "SENTINEL1B"),
        (models.SensorNamesType.SENTINEL1_C, "SENTINEL1C"),
        (models.SensorNamesType.SENTINEL1_D, "SENTINEL1D"),
        (models.SensorNamesType.SAOCOM, "SAOCOM"),
        (models.SensorNamesType.SAOCOM_1_A, "SAOCOM-1A"),
        (models.SensorNamesType.SAOCOM_1_B, "SAOCOM-1B"),
        (models.SensorNamesType.UAVSAR, "UAVSAR"),
    ],
)
def test_translate_sensor_name_from_model(
    model_value: models.SensorNamesType,
    expected: str,
) -> None:
    assert translate.translate_sensor_names_from_model(model_value) == expected


@pytest.mark.parametrize(
    ("raw_value", "expected"),
    [
        ("NOT SET", models.SensorNamesType.NOT_SET),
        ("ASAR", models.SensorNamesType.ASAR),
        ("PALSAR", models.SensorNamesType.PALSAR),
        ("ERS1", models.SensorNamesType.ERS1),
        ("ERS2", models.SensorNamesType.ERS2),
        ("RADARSAT", models.SensorNamesType.RADARSAT),
        ("TERRASARX", models.SensorNamesType.TERRASARX),
        ("SENTINEL1", models.SensorNamesType.SENTINEL1),
        ("SENTINEL1A", models.SensorNamesType.SENTINEL1_A),
        ("SENTINEL1B", models.SensorNamesType.SENTINEL1_B),
        ("SENTINEL1C", models.SensorNamesType.SENTINEL1_C),
        ("SENTINEL1D", models.SensorNamesType.SENTINEL1_D),
        ("SAOCOM", models.SensorNamesType.SAOCOM),
        ("SAOCOM-1A", models.SensorNamesType.SAOCOM_1_A),
        ("SAOCOM-1B", models.SensorNamesType.SAOCOM_1_B),
        ("UAVSAR", models.SensorNamesType.UAVSAR),
    ],
)
def test_translate_sensor_name_to_model(
    raw_value: str,
    expected: models.SensorNamesType,
) -> None:
    assert translate.translate_sensor_names_to_model(raw_value) == expected


def assert_equal_antenna_info(
    info_a: elements.AntennaInfo,
    info_b: elements.AntennaInfo,
) -> None:
    assert info_a.sensor_name == info_b.sensor_name
    assert info_a.polarization == info_b.polarization
    assert info_a.acquisition_mode == info_b.acquisition_mode
    assert info_a.acquisition_beam == info_b.acquisition_beam
    assert info_a.lines_per_pattern == info_b.lines_per_pattern


def test_translate_antenna_info() -> None:
    info_model = models.AntennaInfoType(
        sensor_name=models.SensorNamesType.NOT_SET,
        acquisition_mode=models.AcquisitionModeType.STRIPMAP,
        beam_name="S2",
        polarization=models.PolarizationType.H_H,
    )
    info_metadata = elements.AntennaInfo(
        sensor_name="NOT SET",
        acquisition_mode="STRIPMAP",
        acquisition_beam="S2",
        polarization="HH",
    )

    assert translate.translate_antenna_info_to_model(info_metadata) == info_model
    assert_equal_antenna_info(
        translate.translate_antenna_info_from_model(info_model),
        info_metadata,
    )

    info_model.lines_per_pattern = 4
    info_metadata.lines_per_pattern = 4

    assert translate.translate_antenna_info_to_model(info_metadata) == info_model
    assert_equal_antenna_info(
        translate.translate_antenna_info_from_model(info_model),
        info_metadata,
    )


@pytest.mark.parametrize(
    ("raw_value", "expected"),
    [
        ("DOWN", models.PulseTypeDirection.DOWN),
        ("UP", models.PulseTypeDirection.UP),
    ],
)
def test_translate_pulse_direction_to_model(
    raw_value: elements.PulseDirection,
    expected: models.PulseTypeDirection,
) -> None:
    assert translate.translate_pulse_direction_to_model(raw_value) == expected


@pytest.mark.parametrize(
    ("model_value", "expected"),
    [
        (models.PulseTypeDirection.DOWN, "DOWN"),
        (models.PulseTypeDirection.UP, "UP"),
    ],
)
def test_translate_pulse_direction_from_model(
    model_value: models.PulseTypeDirection,
    expected: str,
) -> None:
    assert translate.translate_pulse_direction_from_model(model_value) == expected


def assert_equal_pulse(pulse_a: elements.Pulse, pulse_b: elements.Pulse) -> None:
    assert pulse_a.pulse_length == pulse_b.pulse_length
    assert pulse_a.bandwidth == pulse_b.bandwidth
    assert pulse_a.pulse_energy == pulse_b.pulse_energy
    assert pulse_a.pulse_sampling_rate == pulse_b.pulse_sampling_rate
    assert pulse_a.pulse_start_frequency == pulse_b.pulse_start_frequency
    assert pulse_a.pulse_start_phase == pulse_b.pulse_start_phase
    assert pulse_a.pulse_direction == pulse_b.pulse_direction


def test_translate_pulse() -> None:
    pulse_metadata = elements.Pulse(
        pulse_length=0.005,
        bandwidth=100000.5,
        pulse_sampling_rate=120000.5,
        pulse_energy=0.0,
    )

    pulse_model = models.PulseType(
        pulse_length=models.DoubleWithUnit(value=0.005, unit=models.Units.S),
        bandwidth=models.DoubleWithUnit(value=100000.5, unit=models.Units.HZ),
        pulse_sampling_rate=models.DoubleWithUnit(value=120000.5, unit=models.Units.HZ),
        pulse_energy=models.DoubleWithUnit(value=0.0, unit=models.Units.J),
    )

    assert translate.translate_pulse_to_model(pulse_metadata) == pulse_model
    assert_equal_pulse(translate.translate_pulse_from_model(pulse_model), pulse_metadata)


def test_translate_pulse_additional_data() -> None:
    pulse_metadata = elements.Pulse(
        pulse_length=0.005,
        bandwidth=100000.5,
        pulse_sampling_rate=120000.6,
        pulse_energy=56,
        pulse_start_frequency=-8,
        pulse_start_phase=-0.5,
        pulse_direction="DOWN",
    )

    pulse_model = models.PulseType(
        direction=models.PulseTypeDirection.DOWN,
        pulse_length=models.DoubleWithUnit(value=0.005, unit=models.Units.S),
        bandwidth=models.DoubleWithUnit(value=100000.5, unit=models.Units.HZ),
        pulse_energy=models.DoubleWithUnit(value=56, unit=models.Units.J),
        pulse_sampling_rate=models.DoubleWithUnit(value=120000.6, unit=models.Units.HZ),
        pulse_start_frequency=models.DoubleWithUnit(value=-8, unit=models.Units.HZ),
        pulse_start_phase=models.DoubleWithUnit(value=-0.5, unit=models.Units.RAD),
    )

    assert translate.translate_pulse_to_model(pulse_metadata) == pulse_model
    assert_equal_pulse(translate.translate_pulse_from_model(pulse_model), pulse_metadata)


class TestMetadata:
    def setup_method(self) -> None:
        self.metadata_obj = channel.MetaData(description="Description")

        mdc = channel.MetaDataChannel()
        raster_info = models.RasterInfoType(
            file_name="filename.tiff",
            lines=11,
            samples=3,
            header_offset_bytes=50,
            row_prefix_bytes=4,
            byte_order=models.Endianity.BIGENDIAN,
            cell_type=models.CellTypeVerboseType.INT16,
            lines_step=translate.translate_double_with_unit_to_model(0.5, "Hz"),
            samples_step=translate.translate_double_with_unit_to_model(8.5, "m"),
            invalid_value=None,
            lines_start=translate.translate_str_with_unit_to_model(
                PreciseDateTime.from_numeric_datetime(year=2020),
                "Utc",
            ),
            samples_start=translate.translate_str_with_unit_to_model(3.4, "m"),
            raster_format=None,
        )

        mdc.insert_element(translate.translate_raster_info_from_model(raster_info))
        self.metadata_obj.channels.append(mdc)

        self.model_obj = models.AresysXmlDoc(
            number_of_channels=1,
            version_number=2.1,
            description="Description",
        )
        channel_model = models.AresysXmlDoc.Channel(number=1, total=1)
        channel_model.raster_info = raster_info
        self.model_obj.channel.append(channel_model)

    def test_translate_metadata(self) -> None:
        assert translate.translate_metadata_to_model(self.metadata_obj) == self.model_obj
        assert (
            translate.translate_metadata_to_model(
                translate.translate_metadata_from_model(self.model_obj),
            )
            == self.model_obj
        )

    def test_translate_metadata_sub_channels(self) -> None:
        channel_two_model = models.AresysXmlDoc.Channel(number=2, total=2)
        channel_two_model.pulse = translate.translate_pulse_to_model(
            elements.Pulse(
                pulse_length=0.5,
                bandwidth=80,
                pulse_sampling_rate=90,
                pulse_energy=0.0,
            ),
        )
        self.model_obj.channel[0].total = 2
        self.model_obj.channel.append(channel_two_model)
        self.model_obj.number_of_channels = 2

        channel_two_metadata = channel.MetaDataChannel()
        channel_two_metadata.insert_element(
            elements.Pulse(
                pulse_length=0.5,
                bandwidth=80,
                pulse_sampling_rate=90,
                pulse_energy=0.0,
            ),
        )
        self.metadata_obj.channels.append(channel_two_metadata)

        assert translate.translate_metadata_to_model(self.metadata_obj) == self.model_obj
        assert (
            translate.translate_metadata_to_model(
                translate.translate_metadata_from_model(self.model_obj),
            )
            == self.model_obj
        )


@pytest.mark.parametrize(
    ("raw_value", "expected"),
    [
        ("BETA", models.ImageQuantityType.BETA),
        ("SIGMA", models.ImageQuantityType.SIGMA),
        ("GAMMA", models.ImageQuantityType.GAMMA),
    ],
)
def test_translate_image_quantity_to_model(
    raw_value: Literal["BETA", "GAMMA", "SIGMA"],
    expected: models.ImageQuantityType,
) -> None:
    assert translate.translate_image_quantity_to_model(raw_value) == expected


@pytest.mark.parametrize(
    ("model_value", "expected"),
    [
        (models.ImageQuantityType.BETA, "BETA"),
        (models.ImageQuantityType.SIGMA, "SIGMA"),
        (models.ImageQuantityType.GAMMA, "GAMMA"),
    ],
)
def test_translate_image_quantity_from_model(
    model_value: models.ImageQuantityType,
    expected: str,
) -> None:
    assert translate.translate_image_quantity_from_model(model_value) == expected
