# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Translate."""

import warnings
from collections.abc import Sequence
from typing import Protocol, TypeVar

import numpy as np
from perseo_core.timing import PreciseDateTime

from aresys_io.product_metadata import metadata, metadata_elements, models

SECOND_STR = "s"
HERTZ_STR = "Hz"

Poly2DT = TypeVar("Poly2DT", bound=metadata_elements.Poly2D)


class _PolyVectorLike(Protocol):
    poly_list: list[metadata_elements.Poly2D]


class _CoregPolyVectorLike(Protocol):
    poly_list: list[metadata_elements.CoregPoly]


_ENDIANITY_FROM_MODEL: dict[models.Endianity, metadata_elements.RasterByteOrder] = {
    models.Endianity.BIGENDIAN: "BIGENDIAN",
    models.Endianity.LITTLEENDIAN: "LITTLEENDIAN",
}


def translate_endianity_from_model(
    endianity: models.Endianity,
) -> metadata_elements.RasterByteOrder:
    """Translate endianity from model."""
    return _ENDIANITY_FROM_MODEL[endianity]


def translate_endianity_to_model(
    endianity: metadata_elements.RasterByteOrder,
) -> models.Endianity:
    """Translate endianity to model."""
    return models.Endianity(endianity)


def translate_cell_type_from_model(
    cell_type: models.CellTypeVerboseType,
) -> metadata_elements.RasterCellType:
    """Translate cell type from model."""
    if cell_type == models.CellTypeVerboseType.SHORT_COMPLEX:
        return "INT16_COMPLEX"

    if cell_type == models.CellTypeVerboseType.INT_COMPLEX:
        return "INT_COMPLEX"

    return cell_type.value


def translate_cell_type_to_model(
    cell_type: metadata_elements.RasterCellType,
) -> models.CellTypeVerboseType:
    """Translate cell type to model."""
    if cell_type == "INT16_COMPLEX":
        return models.CellTypeVerboseType.SHORT_COMPLEX

    if cell_type == "INT_COMPLEX":
        return models.CellTypeVerboseType.INT_COMPLEX

    return models.CellTypeVerboseType(cell_type)


def translate_orbit_direction_from_model(
    direction: models.AscendingDescendingType,
) -> metadata_elements.OrbitDirection | None:
    """Translate orbit direction from model."""
    if direction == models.AscendingDescendingType.NOT_AVAILABLE:
        return None

    return direction.value


def translate_orbit_direction_to_model(
    direction: metadata_elements.OrbitDirection | None,
) -> models.AscendingDescendingType:
    """Translate orbit direction to model."""
    if direction is not None:
        return models.AscendingDescendingType(direction)
    return models.AscendingDescendingType.NOT_AVAILABLE


_SIDE_LOOKING_FROM_MODEL: dict[models.LeftRightType, metadata_elements.SideLooking] = {
    models.LeftRightType.LEFT: "LEFT",
    models.LeftRightType.RIGHT: "RIGHT",
}


def translate_side_looking_from_model(
    side: models.LeftRightType,
) -> metadata_elements.SideLooking:
    """Translate looking side from model."""
    return _SIDE_LOOKING_FROM_MODEL[side]


def translate_side_looking_to_model(
    side: metadata_elements.SideLooking,
) -> models.LeftRightType:
    """Translate looking side to model."""
    return models.LeftRightType(side)


def translate_polarization_from_model(
    polarization: models.PolarizationType,
) -> metadata_elements.AntennaPolarization:
    """Translate polarization from model."""
    match polarization:
        case models.PolarizationType.H_H:
            return "HH"
        case models.PolarizationType.H_V:
            return "HV"
        case models.PolarizationType.V_H:
            return "VH"
        case models.PolarizationType.V_V:
            return "VV"
        case models.PolarizationType.X_X:
            return "XX"

    msg = f"Unsupported polarization: {polarization}"
    raise ValueError(msg)


def translate_polarization_to_model(
    polarization: metadata_elements.AntennaPolarization,
) -> models.PolarizationType:
    """Translate polarization from model."""
    return models.PolarizationType(f"{polarization[0]}/{polarization[1]}")


_REFERENCE_FRAME_FROM_MODEL: dict[
    models.ReferenceFrameType, metadata_elements.AttitudeReferenceFrame
] = {
    models.ReferenceFrameType.GEOCENTRIC: "GEOCENTRIC",
    models.ReferenceFrameType.GEODETIC: "GEODETIC",
    models.ReferenceFrameType.ZERODOPPLER: "ZERODOPPLER",
}


def translate_reference_frame_from_model(
    frame: models.ReferenceFrameType,
) -> metadata_elements.AttitudeReferenceFrame:
    """Translate reference frame from model."""
    return _REFERENCE_FRAME_FROM_MODEL[frame]


def translate_reference_frame_to_model(
    frame: metadata_elements.AttitudeReferenceFrame,
) -> models.ReferenceFrameType:
    """Translate reference frame to model."""
    return models.ReferenceFrameType(frame)


_ROTATION_ORDER_FROM_MODEL: dict[
    models.RotationOrderType, metadata_elements.AttitudeRotationOrder
] = {
    models.RotationOrderType.YPR: "YPR",
    models.RotationOrderType.YRP: "YRP",
    models.RotationOrderType.PRY: "PRY",
    models.RotationOrderType.PYR: "PYR",
    models.RotationOrderType.RPY: "RPY",
    models.RotationOrderType.RYP: "RYP",
}


def translate_rotation_order_from_model(
    order: models.RotationOrderType,
) -> metadata_elements.AttitudeRotationOrder:
    """Translate rotation order from model."""
    return _ROTATION_ORDER_FROM_MODEL[order]


def translate_rotation_order_to_model(
    order: metadata_elements.AttitudeRotationOrder,
) -> models.RotationOrderType:
    """Translate rotation order to model."""
    return models.RotationOrderType(order)


_ATTITUDE_TYPE_FROM_MODEL: dict[models.AttitudeType, metadata_elements.AttitudeType] = {
    models.AttitudeType.NOMINAL: "NOMINAL",
    models.AttitudeType.REFINED: "REFINED",
}


def translate_attitude_type_from_model(
    attitude_type: models.AttitudeType,
) -> metadata_elements.AttitudeType:
    """Translate attitude type from model."""
    return _ATTITUDE_TYPE_FROM_MODEL[attitude_type]


def translate_attitude_type_to_model(
    attitude_type: metadata_elements.AttitudeType,
) -> models.AttitudeType:
    """Translate attitude type to model."""
    return models.AttitudeType(attitude_type)


def translate_raster_format_type_from_model(
    raster_format: models.RasterFormatType,
) -> metadata_elements.RasterFormat:
    """Translate raster format type from model."""
    if raster_format == models.RasterFormatType.RASTER:
        return "ARESYS_RASTER"
    return raster_format.value


def translate_raster_format_type_to_model(
    raster_format: metadata_elements.RasterFormat,
) -> models.RasterFormatType:
    """Translate raster format type to model.

    Deprecated ``RASTER`` is normalized to ``ARESYS_RASTER`` to avoid writing
    legacy enum values.

    Returns
    -------
    models.RasterFormatType
        Canonical raster format enum.

    Raises
    ------
    RuntimeError
        If the raster format is not supported.
    """
    if raster_format == "ARESYS_GEOTIFF":
        return models.RasterFormatType.ARESYS_GEOTIFF
    if raster_format in {"ARESYS_RASTER", "RASTER"}:
        return models.RasterFormatType.ARESYS_RASTER

    msg = f"Raster format {raster_format} is not supported"
    raise RuntimeError(msg)


def translate_unit_from_model(unit: models.Units) -> str:
    """Translate unit from model."""
    return unit.value


def translate_unit_to_model(unit: str) -> models.Units:
    """Translate unit to model."""
    return models.Units(unit)


def translate_double_with_unit_to_model(value: float, unit: str) -> models.DoubleWithUnit:
    """Create a DoubleWithUnit model."""
    return models.DoubleWithUnit(value=value, unit=translate_unit_to_model(unit))


def translate_str_with_unit_from_model(
    str_with_unit: models.StringWithUnit,
) -> tuple[PreciseDateTime | float, str]:
    """Translate a StringWithUnit model."""
    if str_with_unit.unit == models.Units.UTC:
        value = PreciseDateTime.from_utc_string(str_with_unit.value)
    else:
        value = float(str_with_unit.value)

    return value, translate_unit_from_model(str_with_unit.unit)


def translate_str_with_unit_to_model(
    value: PreciseDateTime | float,
    unit: str,
) -> models.StringWithUnit:
    """Translate a StringWithUnit from model."""
    return models.StringWithUnit(value=str(value), unit=translate_unit_to_model(unit))


def translate_dcomplex_to_model(value: complex) -> models.Dcomplex:
    """Translate dcomplex to model."""
    return models.Dcomplex(real_value=value.real, imaginary_value=value.imag)


def translate_dcomplex_from_model(value: models.Dcomplex) -> complex:
    """Translate dcomplex from model."""
    return complex(real=value.real_value, imag=value.imaginary_value)


def translate_raster_info_to_model(
    raster_info: metadata_elements.RasterInfo,
) -> models.RasterInfoType:
    """Translate raster info to model."""
    return models.RasterInfoType(
        number=None,
        total=None,
        file_name=raster_info.file_name,
        lines=raster_info.lines,
        samples=raster_info.samples,
        header_offset_bytes=raster_info.header_offset_bytes,
        row_prefix_bytes=raster_info.row_prefix_bytes,
        byte_order=translate_endianity_to_model(raster_info.byte_order),
        cell_type=translate_cell_type_to_model(raster_info.cell_type),
        lines_step=translate_double_with_unit_to_model(
            raster_info.lines_step,
            raster_info.lines_step_unit,
        ),
        samples_step=translate_double_with_unit_to_model(
            raster_info.samples_step,
            raster_info.samples_step_unit,
        ),
        lines_start=translate_str_with_unit_to_model(
            raster_info.lines_start,
            unit=raster_info.lines_start_unit,
        ),
        samples_start=translate_str_with_unit_to_model(
            raster_info.samples_start,
            unit=raster_info.samples_start_unit,
        ),
        invalid_value=(
            translate_dcomplex_to_model(raster_info.invalid_value)
            if raster_info.invalid_value is not None
            else None
        ),
        raster_format=(
            translate_raster_format_type_to_model(raster_info.format_type)
            if raster_info.format_type is not None
            else None
        ),
    )


def translate_raster_info_from_model(
    raster_info: models.RasterInfoType,
) -> metadata_elements.RasterInfo:
    """Translate raster info from model."""
    lines_start, lines_start_unit = translate_str_with_unit_from_model(raster_info.lines_start)
    samples_start, samples_start_unit = translate_str_with_unit_from_model(
        raster_info.samples_start,
    )

    return metadata_elements.RasterInfo(
        file_name=raster_info.file_name,
        lines=raster_info.lines,
        samples=raster_info.samples,
        header_offset_bytes=raster_info.header_offset_bytes,
        row_prefix_bytes=raster_info.row_prefix_bytes,
        byte_order=translate_endianity_from_model(raster_info.byte_order),
        cell_type=translate_cell_type_from_model(raster_info.cell_type),
        lines_start=lines_start,
        lines_start_unit=lines_start_unit,
        lines_step=raster_info.lines_step.value,
        lines_step_unit=translate_unit_from_model(raster_info.lines_step.unit),
        samples_start=samples_start,
        samples_start_unit=samples_start_unit,
        samples_step=raster_info.samples_step.value,
        samples_step_unit=translate_unit_from_model(raster_info.samples_step.unit),
        invalid_value=(
            translate_dcomplex_from_model(raster_info.invalid_value)
            if raster_info.invalid_value is not None
            else None
        ),
        format_type=(
            translate_raster_format_type_from_model(raster_info.raster_format)
            if raster_info.raster_format is not None
            else None
        ),
    )


def translate_image_quantity_to_model(
    image_quantity: metadata_elements.DataSetImageQuantity,
) -> models.ImageQuantityType:
    """Translate image quantity to model."""
    return models.ImageQuantityType(image_quantity)


_IMAGE_QUANTITY_FROM_MODEL: dict[
    models.ImageQuantityType, metadata_elements.DataSetImageQuantity
] = {
    models.ImageQuantityType.BETA: "BETA",
    models.ImageQuantityType.GAMMA: "GAMMA",
    models.ImageQuantityType.SIGMA: "SIGMA",
}


def translate_image_quantity_from_model(
    image_quantity: models.ImageQuantityType,
) -> metadata_elements.DataSetImageQuantity:
    """Translate image quantity from model."""
    return _IMAGE_QUANTITY_FROM_MODEL[image_quantity]


def translate_dataset_info_from_model(
    info: models.DataSetInfoType,
) -> metadata_elements.DataSetInfo:
    """Translate dataset info from model."""
    return metadata_elements.DataSetInfo(
        sensor_name=info.sensor_name,
        description=info.description.value,
        # XSD field is mandatory, but NOT_AVAILABLE is a legal payload marker.
        # Internally we keep it as None and write it back as NOT_AVAILABLE.
        sense_date=(
            None
            if info.sense_date.value == "NOT_AVAILABLE"
            else PreciseDateTime.from_utc_string(info.sense_date.value)
        ),
        acquisition_mode=info.acquisition_mode.value,
        image_type=info.image_type.value,
        projection=info.projection.value,
        projection_params=(
            info.projection_parameters.value if info.projection_parameters else None
        ),
        image_quantity=(
            translate_image_quantity_from_model(info.image_quantity)
            if info.image_quantity is not None
            else None
        ),
        acquisition_station=info.acquisition_station.value,
        processing_center=info.processing_center.value,
        # XSD field is mandatory, but NOT_AVAILABLE is a legal payload marker.
        # Internally we keep it as None and write it back as NOT_AVAILABLE.
        processing_date=(
            None
            if info.processing_date.value == "NOT_AVAILABLE"
            else PreciseDateTime.from_utc_string(info.processing_date.value)
        ),
        processing_software=info.processing_software.value,
        fc_hz=info.fc_hz.value,
        side_looking=translate_side_looking_from_model(info.side_looking),
        external_calibration_factor=info.external_calibration_factor,
        data_take_id=info.data_take_id,
        projection_params_format=(
            info.projection_parameters.format if info.projection_parameters is not None else None
        ),
        instrument_conf_id=info.instrument_conf_id,
    )


def translate_dataset_info_to_model(
    info: metadata_elements.DataSetInfo,
) -> models.DataSetInfoType:
    """Translate dataset info to model."""
    if info.projection_params is not None and info.projection_params_format is None:
        msg = "Projection parameters format is required when projection parameters is specified"
        raise RuntimeError(
            msg,
        )

    output_proj_params = None
    if info.projection_params is not None:
        assert info.projection_params_format is not None
        output_proj_params = models.DataSetInfoType.ProjectionParameters(
            value=info.projection_params,
            format=info.projection_params_format,
        )

    return models.DataSetInfoType(
        sensor_name=info.sensor_name,
        description=models.DataSetInfoType.Description(value=info.description),
        sense_date=models.DataSetInfoType.SenseDate(
            value="NOT_AVAILABLE" if info.sense_date is None else str(info.sense_date),
        ),
        acquisition_mode=models.DataSetInfoType.AcquisitionMode(value=info.acquisition_mode),
        image_type=models.DataSetInfoType.ImageType(value=info.image_type),
        projection=models.DataSetInfoType.Projection(value=info.projection),
        acquisition_station=models.DataSetInfoType.AcquisitionStation(
            value=info.acquisition_station,
        ),
        processing_center=models.DataSetInfoType.ProcessingCenter(value=info.processing_center),
        processing_date=models.DataSetInfoType.ProcessingDate(
            value="NOT_AVAILABLE" if info.processing_date is None else str(info.processing_date),
        ),
        processing_software=models.DataSetInfoType.ProcessingSoftware(
            value=info.processing_software,
        ),
        fc_hz=models.DataSetInfoType.FcHz(value=info.fc_hz),
        side_looking=translate_side_looking_to_model(info.side_looking),
        external_calibration_factor=info.external_calibration_factor,
        data_take_id=info.data_take_id,
        image_quantity=(
            translate_image_quantity_to_model(info.image_quantity)
            if info.image_quantity is not None
            else None
        ),
        projection_parameters=output_proj_params,
        instrument_conf_id=info.instrument_conf_id,
    )


def translate_geo_point_from_model(
    point: models.PointType,
) -> metadata_elements.GeoPoint:
    """Translate geo point from model."""
    assert len(point.val) == 5

    lat = point.val[0].value
    lon = point.val[1].value
    height = point.val[2].value
    theta_inc = point.val[3].value
    theta_look = point.val[4].value
    return metadata_elements.GeoPoint(
        lat=lat,
        lon=lon,
        height=height,
        theta_inc=theta_inc,
        theta_look=theta_look,
    )


def translate_geo_point_to_model(point: metadata_elements.GeoPoint) -> models.PointType:
    """Translate geo point to model."""
    return models.PointType(
        val=[
            models.PointType.Val(value=point.lat),
            models.PointType.Val(value=point.lon),
            models.PointType.Val(value=point.height),
            models.PointType.Val(value=point.theta_inc),
            models.PointType.Val(value=point.theta_look),
        ],
    )


def translate_ground_corner_points_from_model(
    corners: models.GroundCornersPointsType,
) -> metadata_elements.GroundCornerPoints:
    """Translate ground corner points from model."""
    corners_metadata = metadata_elements.GroundCornerPoints()
    corners_metadata.easting_grid_size = corners.easting_grid_size.value
    corners_metadata.northing_grid_size = corners.northing_grid_size.value
    corners_metadata.nw_point = translate_geo_point_from_model(corners.north_west.point)
    corners_metadata.ne_point = translate_geo_point_from_model(corners.north_east.point)
    corners_metadata.sw_point = translate_geo_point_from_model(corners.south_west.point)
    corners_metadata.se_point = translate_geo_point_from_model(corners.south_east.point)
    corners_metadata.center_point = translate_geo_point_from_model(corners.center.point)
    return corners_metadata


def translate_ground_corner_points_to_model(
    corners: metadata_elements.GroundCornerPoints,
) -> models.GroundCornersPointsType:
    """Translate ground corner points."""
    return models.GroundCornersPointsType(
        easting_grid_size=models.GroundCornersPointsType.EastingGridSize(
            value=corners.easting_grid_size,
        ),
        northing_grid_size=models.GroundCornersPointsType.NorthingGridSize(
            value=corners.northing_grid_size,
        ),
        north_west=models.GroundCornersPointsType.NorthWest(
            point=translate_geo_point_to_model(corners.nw_point),
        ),
        north_east=models.GroundCornersPointsType.NorthEast(
            point=translate_geo_point_to_model(corners.ne_point),
        ),
        south_west=models.GroundCornersPointsType.SouthWest(
            point=translate_geo_point_to_model(corners.sw_point),
        ),
        south_east=models.GroundCornersPointsType.SouthEast(
            point=translate_geo_point_to_model(corners.se_point),
        ),
        center=models.GroundCornersPointsType.Center(
            point=translate_geo_point_to_model(corners.center_point),
        ),
    )


def translate_swath_info_from_model(
    info: models.SwathInfoType,
) -> metadata_elements.SwathInfo:
    """Translate swath info from model."""
    # azimuth steering options
    assert (
        # steering rate
        info.azimuth_steering_rate_reference_time is not None
        and info.azimuth_steering_rate_pol is not None
    ) or (
        # steering
        info.azimuth_steering_angle_reference_time is not None
        and info.azimuth_steering_angle_pol is not None
    )

    swath_info_metadata = metadata_elements.SwathInfo(
        swath=info.swath.value,
        polarization=translate_polarization_from_model(info.polarization),
        acquisition_start_time=PreciseDateTime.from_utc_string(info.acquisition_start_time.value),
        acquisition_prf=info.acquisition_prf,
    )
    swath_info_metadata.swath_acquisition_order = info.swath_acquisition_order.value
    swath_info_metadata.rank = info.rank.value
    swath_info_metadata.range_delay_bias = info.range_delay_bias.value
    if info.azimuth_steering_rate_reference_time is not None:
        swath_info_metadata.azimuth_steering_rate_reference_time = (
            info.azimuth_steering_rate_reference_time.value
        )
        assert info.azimuth_steering_rate_pol is not None
        assert len(info.azimuth_steering_rate_pol.val) == 3
        val_0, val_1, val_2 = info.azimuth_steering_rate_pol.val
        swath_info_metadata.azimuth_steering_rate_pol = (val_0.value, val_1.value, val_2.value)
    if info.azimuth_steering_angle_reference_time is not None:
        swath_info_metadata.azimuth_steering_angle_reference_time = (
            info.azimuth_steering_angle_reference_time.value
        )
        assert info.azimuth_steering_angle_pol is not None
        assert len(info.azimuth_steering_angle_pol.val) == 4
        val_0, val_1, val_2, val_3 = info.azimuth_steering_angle_pol.val
        swath_info_metadata.azimuth_steering_angle_pol = (
            val_0.value,
            val_1.value,
            val_2.value,
            val_3.value,
        )
    swath_info_metadata.echoes_per_burst = info.echoes_per_burst
    swath_info_metadata.channel_delay = info.channel_delay
    swath_info_metadata.rx_gain = info.rx_gain

    return swath_info_metadata


def translate_swath_info_to_model(
    info: metadata_elements.SwathInfo,
) -> models.SwathInfoType:
    """Translate swath info to model."""
    polarization = models.PolarizationType(f"{info.polarization[0]}/{info.polarization[1]}")

    return models.SwathInfoType(
        swath=models.SwathInfoType.Swath(value=info.swath),
        swath_acquisition_order=models.SwathInfoType.SwathAcquisitionOrder(
            value=info.swath_acquisition_order,
        ),
        polarization=polarization,
        rank=models.SwathInfoType.Rank(value=info.rank),
        range_delay_bias=models.SwathInfoType.RangeDelayBias(
            value=info.range_delay_bias,
            unit=translate_unit_to_model(info.range_delay_bias_unit),
        ),
        acquisition_start_time=models.SwathInfoType.AcquisitionStartTime(
            value=str(info.acquisition_start_time),
            unit=translate_unit_to_model(info.acquisition_start_time_unit),
        ),
        azimuth_steering_angle_reference_time=(
            models.DoubleWithUnit(
                value=info.azimuth_steering_angle_reference_time,
                unit=translate_unit_to_model(info.az_steering_angle_ref_time_unit),
            )
            if info.azimuth_steering_angle_reference_time is not None
            else None
        ),
        azimuth_steering_angle_pol=(
            models.SwathInfoType.AzimuthSteeringAnglePol(
                val=[
                    models.SwathInfoType.AzimuthSteeringAnglePol.Val(
                        value=info.azimuth_steering_angle_pol[0],
                        n=1,
                    ),
                    models.SwathInfoType.AzimuthSteeringAnglePol.Val(
                        value=info.azimuth_steering_angle_pol[1],
                        n=2,
                    ),
                    models.SwathInfoType.AzimuthSteeringAnglePol.Val(
                        value=info.azimuth_steering_angle_pol[2],
                        n=3,
                    ),
                    models.SwathInfoType.AzimuthSteeringAnglePol.Val(
                        value=info.azimuth_steering_angle_pol[3],
                        n=4,
                    ),
                ],
            )
            if info.azimuth_steering_angle_pol is not None
            else None
        ),
        azimuth_steering_rate_reference_time=(
            models.DoubleWithUnit(
                value=info.azimuth_steering_rate_reference_time,
                unit=translate_unit_to_model(info.az_steering_rate_ref_time_unit),
            )
            if info.azimuth_steering_rate_reference_time is not None
            else None
        ),
        azimuth_steering_rate_pol=(
            models.SwathInfoType.AzimuthSteeringRatePol(
                val=[
                    models.SwathInfoType.AzimuthSteeringRatePol.Val(
                        value=info.azimuth_steering_rate_pol[0],
                        n=1,
                    ),
                    models.SwathInfoType.AzimuthSteeringRatePol.Val(
                        value=info.azimuth_steering_rate_pol[1],
                        n=2,
                    ),
                    models.SwathInfoType.AzimuthSteeringRatePol.Val(
                        value=info.azimuth_steering_rate_pol[2],
                        n=3,
                    ),
                ],
            )
            if info.azimuth_steering_rate_pol is not None
            else None
        ),
        acquisition_prf=info.acquisition_prf,
        echoes_per_burst=info.echoes_per_burst,
        channel_delay=info.channel_delay,
        rx_gain=info.rx_gain,
    )


def translate_sampling_constants_from_model(
    constants: models.SamplingConstantsType,
) -> metadata_elements.SamplingConstants:
    """Translate sampling constants from model."""
    return metadata_elements.SamplingConstants(
        frg_hz=constants.frg_hz.value,
        brg_hz=constants.brg_hz.value,
        faz_hz=constants.faz_hz.value,
        baz_hz=constants.baz_hz.value,
    )


def translate_sampling_constants_to_model(
    constants: metadata_elements.SamplingConstants,
) -> models.SamplingConstantsType:
    """Translate sampling constants to model."""
    return models.SamplingConstantsType(
        frg_hz=models.SamplingConstantsType.FrgHz(
            value=constants.frg_hz,
            unit=translate_unit_to_model(HERTZ_STR),
        ),
        brg_hz=models.SamplingConstantsType.BrgHz(
            value=constants.brg_hz,
            unit=translate_unit_to_model(HERTZ_STR),
        ),
        faz_hz=models.SamplingConstantsType.FazHz(
            value=constants.faz_hz,
            unit=translate_unit_to_model(HERTZ_STR),
        ),
        baz_hz=models.SamplingConstantsType.BazHz(
            value=constants.baz_hz,
            unit=translate_unit_to_model(HERTZ_STR),
        ),
    )


def translate_acquisition_time_line_from_model(
    time_line: models.AcquisitionTimelineType,
) -> metadata_elements.AcquisitionTimeLine:
    """Translate acquisition time line from model."""
    if time_line.swl_changes_number:
        assert time_line.swl_changes_azimuthtimes is not None
        assert time_line.swl_changes_values is not None
        swl_changes_azimuth_times = [
            element.value for element in time_line.swl_changes_azimuthtimes.val
        ] or None
        swl_changes_values = [
            element.value for element in time_line.swl_changes_values.val
        ] or None
    else:
        swl_changes_azimuth_times = None
        swl_changes_values = None

    if time_line.prf_changes_number:
        assert time_line.prf_changes_azimuthtimes is not None
        assert time_line.prf_changes_values is not None
        prf_changes_azimuth_times = [
            element.value for element in time_line.prf_changes_azimuthtimes.val
        ] or None
        prf_changes_values = [
            element.value for element in time_line.prf_changes_values.val
        ] or None
    else:
        prf_changes_azimuth_times = None
        prf_changes_values = None

    output_time_line = metadata_elements.AcquisitionTimeLine(
        missing_lines=[element.value for element in time_line.missing_lines_azimuthtimes.val]
        or [],
        swst_changes=list(
            zip(
                [element.value for element in time_line.swst_changes_azimuthtimes.val] or [],
                [element.value for element in time_line.swst_changes_values.val] or [],
                strict=True,
            ),
        ),
        noise_packet=[element.value for element in time_line.noise_packets_azimuthtimes.val] or [],
        internal_calibration=[
            element.value for element in time_line.internal_calibration_azimuthtimes.val
        ]
        or [],
        swl_changes=list(
            zip(swl_changes_azimuth_times or [], swl_changes_values or [], strict=True),
        ),
        prf_changes=list(
            zip(prf_changes_azimuth_times or [], prf_changes_values or [], strict=True),
        ),
        chirp_period=time_line.chirp_period,
    )

    if time_line.duplicated_lines_number is not None:
        assert time_line.duplicated_lines_azimuthtimes is not None
        output_time_line.duplicated_lines = [
            element.value for element in time_line.duplicated_lines_azimuthtimes.val
        ] or []

    return output_time_line


def translate_acquisition_time_line_to_model(
    time_line: metadata_elements.AcquisitionTimeLine,
) -> models.AcquisitionTimelineType:
    """Translate acquisition time line from model."""
    missing_lines_azimuth_times = models.AcquisitionTimelineType.MissingLinesAzimuthtimes(
        val=[
            models.AcquisitionTimelineType.MissingLinesAzimuthtimes.Val(
                value=value,
                unit=translate_unit_to_model(SECOND_STR),
            )
            for value in time_line.missing_lines
        ],
    )

    swst_changes_azimuth_times = models.AcquisitionTimelineType.SwstChangesAzimuthtimes(
        val=[
            models.AcquisitionTimelineType.SwstChangesAzimuthtimes.Val(
                value=azimuth_time,
                unit=translate_unit_to_model(SECOND_STR),
            )
            for azimuth_time, _ in time_line.swst_changes
        ],
    )
    swst_changes_values = models.AcquisitionTimelineType.SwstChangesValues(
        val=[
            models.AcquisitionTimelineType.SwstChangesValues.Val(
                value=value,
                unit=translate_unit_to_model(SECOND_STR),
            )
            for _, value in time_line.swst_changes
        ],
    )

    noise_packets_azimuthtimes = models.AcquisitionTimelineType.NoisePacketsAzimuthtimes(
        val=[
            models.AcquisitionTimelineType.NoisePacketsAzimuthtimes.Val(
                value=value,
                unit=translate_unit_to_model(SECOND_STR),
            )
            for value in time_line.noise_packet
        ],
    )

    internal_calibration_azimuthtimes = (
        models.AcquisitionTimelineType.InternalCalibrationAzimuthtimes(
            val=[
                models.AcquisitionTimelineType.InternalCalibrationAzimuthtimes.Val(
                    value=value,
                    unit=translate_unit_to_model(SECOND_STR),
                )
                for value in time_line.internal_calibration
            ],
        )
    )

    swl_changes_azimuth_times, swl_changes_values = (
        None,
        None,
    )
    if len(time_line.swl_changes) > 0:
        swl_changes_azimuth_times = models.AcquisitionTimelineType.SwlChangesAzimuthtimes(
            val=[
                models.AcquisitionTimelineType.SwlChangesAzimuthtimes.Val(
                    value=azimuth_time,
                    unit=translate_unit_to_model(SECOND_STR),
                )
                for azimuth_time, _ in time_line.swl_changes
            ],
        )
        swl_changes_values = models.AcquisitionTimelineType.SwlChangesValues(
            val=[
                models.AcquisitionTimelineType.SwlChangesValues.Val(
                    value=value,
                    unit=translate_unit_to_model(SECOND_STR),
                )
                for _, value in time_line.swl_changes
            ],
        )

    prf_changes_azimuth_times, prf_changes_values = (
        None,
        None,
    )
    if len(time_line.prf_changes) > 0:
        prf_changes_azimuth_times = models.AcquisitionTimelineType.PrfChangesAzimuthtimes(
            val=[
                models.AcquisitionTimelineType.PrfChangesAzimuthtimes.Val(
                    value=azimuth_time,
                    unit=translate_unit_to_model(SECOND_STR),
                )
                for azimuth_time, _ in time_line.prf_changes
            ],
        )
        prf_changes_values = models.AcquisitionTimelineType.PrfChangesValues(
            val=[
                models.AcquisitionTimelineType.PrfChangesValues.Val(
                    value=value,
                    unit=translate_unit_to_model(HERTZ_STR),
                )
                for _, value in time_line.prf_changes
            ],
        )

    duplicated_lines_azimuthtimes = None
    if len(time_line.duplicated_lines) > 0:
        duplicated_lines_azimuthtimes = models.AcquisitionTimelineType.DuplicatedLinesAzimuthtimes(
            val=[
                models.AcquisitionTimelineType.DuplicatedLinesAzimuthtimes.Val(
                    value=value,
                    unit=translate_unit_to_model(SECOND_STR),
                )
                for value in time_line.duplicated_lines
            ],
        )

    return models.AcquisitionTimelineType(
        missing_lines_number=len(missing_lines_azimuth_times.val),
        missing_lines_azimuthtimes=missing_lines_azimuth_times,
        swst_changes_number=len(swst_changes_azimuth_times.val),
        swst_changes_azimuthtimes=swst_changes_azimuth_times,
        swst_changes_values=swst_changes_values,
        noise_packets_number=len(noise_packets_azimuthtimes.val),
        noise_packets_azimuthtimes=noise_packets_azimuthtimes,
        internal_calibration_number=len(internal_calibration_azimuthtimes.val),
        internal_calibration_azimuthtimes=internal_calibration_azimuthtimes,
        swl_changes_number=len(swl_changes_azimuth_times.val)
        if swl_changes_azimuth_times is not None
        else None,
        swl_changes_azimuthtimes=swl_changes_azimuth_times,
        swl_changes_values=swl_changes_values,
        duplicated_lines_number=len(duplicated_lines_azimuthtimes.val)
        if duplicated_lines_azimuthtimes is not None
        else None,
        duplicated_lines_azimuthtimes=duplicated_lines_azimuthtimes,
        prf_changes_number=len(prf_changes_azimuth_times.val)
        if prf_changes_azimuth_times is not None
        else None,
        prf_changes_azimuthtimes=prf_changes_azimuth_times,
        prf_changes_values=prf_changes_values,
        chirp_period=time_line.chirp_period,
    )


def translate_attitude_from_model(
    attitude: models.AttitudeInfoType,
) -> metadata_elements.AttitudeInfo:
    """Translate attitude from model."""
    yaw = [element.value for element in attitude.yaw_deg.val]
    pitch = [element.value for element in attitude.pitch_deg.val]
    roll = [element.value for element in attitude.roll_deg.val]

    expected_records = attitude.n_ypr_n.value
    if (
        len(yaw) != expected_records
        or len(pitch) != expected_records
        or len(roll) != expected_records
    ):
        msg = (
            "AttitudeInfo n_ypr_n must match the number of yaw/pitch/roll samples "
            f"(expected {expected_records}, "
            f"got yaw={len(yaw)}, pitch={len(pitch)}, roll={len(roll)})"
        )
        raise ValueError(msg)

    return metadata_elements.AttitudeInfo(
        ypr_deg=np.asarray(list(zip(yaw, pitch, roll, strict=True)), dtype=np.float64),
        reference_time=PreciseDateTime.from_utc_string(attitude.t_ref_utc),
        time_step=attitude.dt_ypr_s.value,
        reference_frame=translate_reference_frame_from_model(attitude.reference_frame),
        rotation_order=translate_rotation_order_from_model(attitude.rotation_order),
        attitude_type=translate_attitude_type_from_model(attitude.attitude_type),
    )


def translate_attitude_to_model(
    attitude: metadata_elements.AttitudeInfo,
) -> models.AttitudeInfoType:
    """Translate attitude to model."""
    yaw_values = attitude.ypr_deg[:, 0]
    pitch_values = attitude.ypr_deg[:, 1]
    roll_values = attitude.ypr_deg[:, 2]

    return models.AttitudeInfoType(
        t_ref_utc=str(attitude.reference_time),
        dt_ypr_s=models.AttitudeInfoType.DtYprS(value=attitude.time_step),
        n_ypr_n=models.AttitudeInfoType.NYprN(value=int(attitude.ypr_deg.shape[0])),
        yaw_deg=models.AttitudeInfoType.YawDeg(
            val=[
                models.AttitudeInfoType.YawDeg.Val(value=float(yaw), n=index + 1)
                for index, yaw in enumerate(yaw_values)
            ],
        ),
        pitch_deg=models.AttitudeInfoType.PitchDeg(
            val=[
                models.AttitudeInfoType.PitchDeg.Val(value=float(pitch), n=index + 1)
                for index, pitch in enumerate(pitch_values)
            ],
        ),
        roll_deg=models.AttitudeInfoType.RollDeg(
            val=[
                models.AttitudeInfoType.RollDeg.Val(value=float(roll), n=index + 1)
                for index, roll in enumerate(roll_values)
            ],
        ),
        reference_frame=translate_reference_frame_to_model(attitude.reference_frame),
        rotation_order=translate_rotation_order_to_model(attitude.rotation_order),
        attitude_type=translate_attitude_type_to_model(attitude.attitude_type),
    )


def _fill_lines_per_burst_list(
    changes: list[models.BurstInfoType.LinesPerBurstChangeList.Lines],
    burst_number: int,
) -> list[int]:
    """Fill lines per burst list."""
    sorted_changes = sorted(
        ((change.from_burst, change.value) for change in changes),
        reverse=True,
    )
    return [
        next(v for k, v in sorted_changes if k <= burst_index + 1)
        for burst_index in range(burst_number)
    ]


def translate_burst_info_from_model(
    info: models.BurstInfoType,
) -> metadata_elements.BurstInfo:
    """Translate burst info from model."""
    output_info = metadata_elements.BurstInfo(
        burst_repetition_frequency=info.burst_repetition_frequency.value,
    )
    if info.lines_per_burst is not None:
        lines_per_burst = info.number_of_bursts * [info.lines_per_burst]
    else:
        assert info.lines_per_burst_change_list
        lines_per_burst = _fill_lines_per_burst_list(
            info.lines_per_burst_change_list.lines,
            info.number_of_bursts,
        )

    assert len(info.burst) == info.number_of_bursts
    for burst, lines in zip(info.burst, lines_per_burst, strict=True):
        output_info.bursts.append(
            metadata_elements.Burst(
                range_start_time=burst.range_start_time.value,
                azimuth_start_time=PreciseDateTime.from_utc_string(burst.azimuth_start_time.value),
                lines=lines,
                burst_center_azimuth_shift=(
                    burst.burst_center_azimuth_shift.value
                    if burst.burst_center_azimuth_shift is not None
                    else None
                ),
            ),
        )

    return output_info


def translate_burst_info_to_model(
    info: metadata_elements.BurstInfo,
) -> models.BurstInfoType:
    """Translate burst info to model."""
    changes = {
        index: burst.lines
        for index, burst in enumerate(info.bursts)
        if index == 0 or burst.lines != info.bursts[index - 1].lines
    }

    change_list = models.BurstInfoType.LinesPerBurstChangeList(
        lines=[
            models.BurstInfoType.LinesPerBurstChangeList.Lines(
                value=lines,
                from_burst=from_burst + 1,
            )
            for from_burst, lines in changes.items()
        ],
    )

    burst_list = []
    for index, burst in enumerate(info.bursts):
        burst_model = models.BurstType(
            range_start_time=models.DoubleWithUnit(
                value=burst.range_start_time,
                unit=models.Units.S,
            ),
            azimuth_start_time=models.StringWithUnit(
                value=str(burst.azimuth_start_time),
                unit=models.Units.UTC,
            ),
            burst_center_azimuth_shift=(
                models.DoubleWithUnit(value=burst.burst_center_azimuth_shift, unit=models.Units.S)
                if burst.burst_center_azimuth_shift is not None
                else None
            ),
            n=index + 1,
        )
        burst_list.append(burst_model)

    return models.BurstInfoType(
        number_of_bursts=len(info.bursts),
        burst_repetition_frequency=models.DoubleWithUnit(
            value=info.burst_repetition_frequency,
            unit=models.Units.HZ,
        ),
        lines_per_burst=None,  # Lines per burst is considered deprecated
        lines_per_burst_change_list=change_list,
        burst=burst_list,
    )


def translate_state_vectors_from_model(
    state_vectors: models.StateVectorDataType,
) -> metadata_elements.StateVectors:
    """Translate state vectors from model."""
    number_of_state_vectors = state_vectors.n_sv_n.value
    if (
        len(state_vectors.p_sv_m.val) != len(state_vectors.v_sv_m_os.val)
        or len(state_vectors.v_sv_m_os.val) != number_of_state_vectors * 3
    ):
        msg = (
            "StateVectorData components do not match n_sv_n "
            f"(expected {number_of_state_vectors * 3}, "
            f"got p={len(state_vectors.p_sv_m.val)}, "
            f"v={len(state_vectors.v_sv_m_os.val)})"
        )
        raise ValueError(msg)

    positions = np.zeros((number_of_state_vectors, 3), dtype=np.float64)
    velocities = np.zeros((number_of_state_vectors, 3), dtype=np.float64)

    for index, (pos, vel) in enumerate(
        zip(state_vectors.p_sv_m.val, state_vectors.v_sv_m_os.val, strict=True),
    ):
        assert pos.n == index + 1
        assert vel.n == index + 1
        state_vector_index = index // 3
        component_index = index % 3

        positions[state_vector_index, component_index] = pos.value
        velocities[state_vector_index, component_index] = vel.value

    anx_position = None
    if state_vectors.ascending_node_coords is not None:
        assert len(state_vectors.ascending_node_coords.val) == 3
        coord_x, coord_y, coord_z = state_vectors.ascending_node_coords.val
        anx_position = (coord_x.value, coord_y.value, coord_z.value)

    anx_time = None
    if state_vectors.ascending_node_time is not None:
        anx_time = PreciseDateTime.from_utc_string(state_vectors.ascending_node_time)

    # NOT_AVAILABLE is legal in the XML schema; map it to None in metadata.
    orbit_number = (
        None if state_vectors.orbit_number == "NOT_AVAILABLE" else int(state_vectors.orbit_number)
    )
    # NOT_AVAILABLE is legal in the XML schema; map it to None in metadata.
    track_number = None if state_vectors.track == "NOT_AVAILABLE" else int(state_vectors.track)

    output_sv = metadata_elements.StateVectors(
        position_vector=positions,
        velocity_vector=velocities,
        reference_time=PreciseDateTime.from_utc_string(state_vectors.t_ref_utc),
        time_step=state_vectors.dt_sv_s.value,
        orbit_number=orbit_number,
        track_number=track_number,
        anx_time=anx_time,
        anx_position=anx_position,
    )

    expected_orbit_direction = (
        models.AscendingDescendingType.ASCENDING
        if velocities[0, 2] > 0
        else models.AscendingDescendingType.DESCENDING
    )

    if state_vectors.orbit_direction != expected_orbit_direction:
        msg = (
            "StateVectorData orbit_direction does not agree with velocity sign "
            f"(orbit_direction={state_vectors.orbit_direction.value}, "
            f"inferred={expected_orbit_direction.value})"
        )
        warnings.warn(msg, UserWarning, stacklevel=2)

        output_sv.annotated_orbit_direction = (
            None
            if state_vectors.orbit_direction is models.AscendingDescendingType.NOT_AVAILABLE
            else state_vectors.orbit_direction.value
        )

    return output_sv


def translate_state_vectors_to_model(
    state_vectors: metadata_elements.StateVectors,
) -> models.StateVectorDataType:
    """Translate state vectors to model."""
    if state_vectors.position_vector.shape != state_vectors.velocity_vector.shape:
        msg = "Position and velocity arrays must have the same shape"
        raise ValueError(msg)

    position = models.StateVectorDataType.PSvM()
    velocity = models.StateVectorDataType.VSvMOs()
    for index, (pos, vel) in enumerate(
        zip(state_vectors.position_vector, state_vectors.velocity_vector, strict=False),
    ):
        offset = index * 3
        for component, (pos_comp, vel_comp) in enumerate(zip(pos, vel, strict=False)):
            index_current = offset + component + 1

            position.val.append(
                models.StateVectorDataType.PSvM.Val(value=float(pos_comp), n=index_current),
            )
            velocity.val.append(
                models.StateVectorDataType.VSvMOs.Val(value=float(vel_comp), n=index_current),
            )

    state_vectors_model = models.StateVectorDataType(
        p_sv_m=position,
        v_sv_m_os=velocity,
        orbit_number=(
            "NOT_AVAILABLE"
            if state_vectors.orbit_number is None
            else str(state_vectors.orbit_number)
        ),
        track=(
            "NOT_AVAILABLE"
            if state_vectors.track_number is None
            else str(state_vectors.track_number)
        ),
        orbit_direction=translate_orbit_direction_to_model(
            state_vectors.annotated_orbit_direction
        ),
        t_ref_utc=str(state_vectors.reference_time),
        dt_sv_s=models.StateVectorDataType.DtSvS(
            value=state_vectors.time_step,
            unit=models.Units.S,
        ),
        n_sv_n=models.StateVectorDataType.NSvN(value=int(state_vectors.position_vector.shape[0])),
    )

    if state_vectors.anx_position is not None:
        state_vectors_model.ascending_node_coords = models.StateVectorDataType.AscendingNodeCoords(
            val=[
                models.StateVectorDataType.AscendingNodeCoords.Val(
                    value=state_vectors.anx_position[0],
                ),
                models.StateVectorDataType.AscendingNodeCoords.Val(
                    value=state_vectors.anx_position[1],
                ),
                models.StateVectorDataType.AscendingNodeCoords.Val(
                    value=state_vectors.anx_position[2],
                ),
            ],
        )

    if state_vectors.anx_time is not None:
        state_vectors_model.ascending_node_time = str(state_vectors.anx_time)

    return state_vectors_model


def translate_polynomial_from_model(
    poly: models.PolyType,
    specific_type: type[Poly2DT],
) -> Poly2DT:
    """Translate polynomial from model."""
    return specific_type(
        t_ref_az=PreciseDateTime.from_utc_string(poly.taz0_utc.value),
        t_ref_rg=poly.trg0_s.value,
        coefficients=[elem.value for elem in poly.pol.val],
    )


def translate_polynomial_to_model(poly: metadata_elements.Poly2D) -> models.PolyType:
    """Translate polynomial to model."""
    if len(poly.coefficients) > len(poly.UNITS):
        msg = (
            f"Polynomial has {len(poly.coefficients)} coefficients but only "
            f"{len(poly.UNITS)} units are defined"
        )
        raise ValueError(msg)

    return models.PolyType(
        pol=models.PolyType.Pol(
            val=[
                models.PolyType.Pol.Val(
                    value=coeff,
                    unit=translate_unit_to_model(unit),
                    n=index + 1,
                )
                for index, (coeff, unit) in enumerate(
                    zip(poly.coefficients, poly.UNITS, strict=False),
                )
            ],
        ),
        trg0_s=models.PolyType.Trg0S(value=poly.t_ref_rg, unit=models.Units.S),
        taz0_utc=models.PolyType.Taz0Utc(value=str(poly.t_ref_az), unit=models.Units.UTC),
    )


def translate_polynomial_list_to_model(
    poly_list: Sequence[metadata_elements.Poly2D],
) -> list[models.PolyType]:
    """Translate polynomial list from model."""

    def _add_number_and_total(
        poly: models.PolyType,
        number: int,
        total: int,
    ) -> models.PolyType:
        poly.number = number
        poly.total = total
        return poly

    return [
        _add_number_and_total(
            translate_polynomial_to_model(poly),
            index + 1,
            len(poly_list),
        )
        for index, poly in enumerate(poly_list)
    ]


def translate_coreg_polynomial_from_model(
    poly: models.PolyCoregType,
) -> metadata_elements.CoregPoly:
    """Translate coregistration polynomial from model."""
    return metadata_elements.CoregPoly(
        t_ref_az=PreciseDateTime.from_utc_string(poly.taz0_utc.value),
        t_ref_rg=poly.trg0_s.value,
        coefficients_az=[elem.value for elem in poly.pol_az.val],
        coefficients_rg=[elem.value for elem in poly.pol_rg.val],
    )


def translate_coreg_polynomial_to_model(
    poly: metadata_elements.CoregPoly,
) -> models.PolyCoregType:
    """Translate coregistration polynomial to model."""
    if poly.coefficients_az is None:
        msg = "Azimuth Coefficients are required in Coreg Polynomial: cannot be 'None'"
        raise RuntimeError(
            msg,
        )

    if poly.coefficients_rg is None:
        msg = "Range Coefficients are required in Coreg Polynomial: cannot be 'None'"
        raise RuntimeError(msg)

    return models.PolyCoregType(
        pol_az=models.PolyCoregType.PolAz(
            val=[
                models.PolyCoregType.PolAz.Val(value=coeff, n=index + 1)
                for index, coeff in enumerate(poly.coefficients_az)
            ],
        ),
        pol_rg=models.PolyCoregType.PolRg(
            val=[
                models.PolyCoregType.PolRg.Val(value=coeff, n=index + 1)
                for index, coeff in enumerate(poly.coefficients_rg)
            ],
        ),
        trg0_s=models.PolyCoregType.Trg0S(value=poly.t_ref_rg, unit=models.Units.S),
        taz0_utc=models.PolyCoregType.Taz0Utc(value=str(poly.t_ref_az), unit=models.Units.UTC),
    )


def translate_coreg_polynomial_list_from_model(
    poly_list: list[models.PolyCoregType],
) -> metadata_elements.CoregPolyVector:
    """Translate coregistration polynomial list from model."""
    return metadata_elements.CoregPolyVector(
        poly_list=[translate_coreg_polynomial_from_model(poly) for poly in poly_list],
    )


def translate_coreg_polynomial_list_to_model(
    poly_list: list[metadata_elements.CoregPoly],
) -> list[models.PolyCoregType]:
    """Translate coregistration polynomial list to model."""

    def _add_number_and_total(
        poly: models.PolyCoregType,
        number: int,
        total: int,
    ) -> models.PolyCoregType:
        poly.number = number
        poly.total = total
        return poly

    return [
        _add_number_and_total(
            translate_coreg_polynomial_to_model(poly),
            number=index + 1,
            total=len(poly_list),
        )
        for index, poly in enumerate(poly_list)
    ]


def translate_data_statistics_from_model(
    stat: models.DataStatisticsType,
) -> metadata_elements.DataStatistics:
    """Translate data statistics from model."""
    stat_metadata = metadata_elements.DataStatistics(
        num_samples=stat.num_samples.value,
        max_i=stat.max_i.value,
        min_i=stat.min_i.value,
        max_q=stat.max_q.value,
        min_q=stat.min_q.value,
        sum_i=stat.sum_i.value,
        sum_q=stat.sum_q.value,
        sum_2_i=stat.sum2_i.value,
        sum_2_q=stat.sum2_q.value,
        std_dev_i=stat.std_dev_i.value,
        std_dev_q=stat.std_dev_q.value,
    )

    if stat.statistics_list is not None:
        for block_stat in stat.statistics_list.data_block_statistic:
            stat_metadata.statistics_list.append(
                metadata_elements.DataBlockStatistic(
                    num_samples=block_stat.num_samples.value,
                    max_i=block_stat.max_i.value,
                    min_i=block_stat.min_i.value,
                    max_q=block_stat.max_q.value,
                    min_q=block_stat.min_q.value,
                    sum_i=block_stat.sum_i.value,
                    sum_q=block_stat.sum_q.value,
                    sum_2_i=block_stat.sum2_i.value,
                    sum_2_q=block_stat.sum2_q.value,
                    line_start=block_stat.line_start,
                    line_stop=block_stat.line_stop,
                ),
            )

    return stat_metadata


def translate_data_statistics_to_model(
    stat: metadata_elements.DataStatistics,
) -> models.DataStatisticsType:
    """Translate data statistics to model."""
    stat_model = models.DataStatisticsType(
        num_samples=models.DataStatisticsType.NumSamples(value=stat.num_samples),
        max_i=models.DataStatisticsType.MaxI(value=stat.max_i),
        min_i=models.DataStatisticsType.MinI(value=stat.min_i),
        max_q=models.DataStatisticsType.MaxQ(value=stat.max_q),
        min_q=models.DataStatisticsType.MinQ(value=stat.min_q),
        sum_i=models.DataStatisticsType.SumI(value=stat.sum_i),
        sum_q=models.DataStatisticsType.SumQ(value=stat.sum_q),
        sum2_i=models.DataStatisticsType.Sum2I(value=stat.sum_2_i),
        sum2_q=models.DataStatisticsType.Sum2Q(value=stat.sum_2_q),
        std_dev_i=models.DataStatisticsType.StdDevI(value=stat.std_dev_i),
        std_dev_q=models.DataStatisticsType.StdDevQ(value=stat.std_dev_q),
    )
    if stat.statistics_list:
        stat_model.statistics_list = models.DataStatisticsType.StatisticsList()
        for block in stat.statistics_list:
            stat_model.statistics_list.data_block_statistic.append(
                models.DataBlockStatisticsType(
                    num_samples=models.DataBlockStatisticsType.NumSamples(value=block.num_samples),
                    max_i=models.DataBlockStatisticsType.MaxI(value=block.max_i),
                    min_i=models.DataBlockStatisticsType.MinI(value=block.min_i),
                    max_q=models.DataBlockStatisticsType.MaxQ(value=block.max_q),
                    min_q=models.DataBlockStatisticsType.MinQ(value=block.min_q),
                    sum_i=models.DataBlockStatisticsType.SumI(value=block.sum_i),
                    sum_q=models.DataBlockStatisticsType.SumQ(value=block.sum_q),
                    sum2_i=models.DataBlockStatisticsType.Sum2I(value=block.sum_2_i),
                    sum2_q=models.DataBlockStatisticsType.Sum2Q(value=block.sum_2_q),
                    line_start=block.line_start,
                    line_stop=block.line_stop,
                ),
            )

    return stat_model


def translate_sensor_names_from_model(name: models.SensorNamesType) -> str:
    """Translate sensor name from model."""
    return name.value


def translate_sensor_names_to_model(name: str) -> models.SensorNamesType:
    """Translate sensor name to model."""
    return models.SensorNamesType(name)


def translate_antenna_info_from_model(
    info: models.AntennaInfoType,
) -> metadata_elements.AntennaInfo:
    """Translate antenna info from model."""
    return metadata_elements.AntennaInfo(
        sensor_name=translate_sensor_names_from_model(info.sensor_name),
        acquisition_mode=info.acquisition_mode.value,
        acquisition_beam=info.beam_name,
        polarization=translate_polarization_from_model(info.polarization),
        lines_per_pattern=info.lines_per_pattern,
    )


def translate_antenna_info_to_model(
    info: metadata_elements.AntennaInfo,
) -> models.AntennaInfoType:
    """Translate antenna info to model."""
    return models.AntennaInfoType(
        sensor_name=models.SensorNamesType(
            info.sensor_name if info.sensor_name is not None else "NOT SET",
        ),
        acquisition_mode=models.AcquisitionModeType(info.acquisition_mode),
        beam_name=info.acquisition_beam,
        polarization=translate_polarization_to_model(info.polarization),
        lines_per_pattern=info.lines_per_pattern,
    )


_PULSE_DIRECTION_FROM_MODEL: dict[models.PulseTypeDirection, metadata_elements.PulseDirection] = {
    models.PulseTypeDirection.UP: "UP",
    models.PulseTypeDirection.DOWN: "DOWN",
}


def translate_pulse_direction_from_model(
    direction: models.PulseTypeDirection,
) -> metadata_elements.PulseDirection:
    """Translate pulse direction from model."""
    return _PULSE_DIRECTION_FROM_MODEL[direction]


def translate_pulse_direction_to_model(
    direction: metadata_elements.PulseDirection,
) -> models.PulseTypeDirection:
    """Translate pulse direction to model."""
    return models.PulseTypeDirection(direction)


def translate_pulse_from_model(pulse: models.PulseType) -> metadata_elements.Pulse:
    """Translate pulse from model."""
    return metadata_elements.Pulse(
        pulse_length=pulse.pulse_length.value,
        bandwidth=pulse.bandwidth.value,
        pulse_sampling_rate=pulse.pulse_sampling_rate.value,
        pulse_energy=pulse.pulse_energy.value,
        pulse_start_frequency=(
            pulse.pulse_start_frequency.value if pulse.pulse_start_frequency is not None else None
        ),
        pulse_start_phase=(
            pulse.pulse_start_phase.value if pulse.pulse_start_phase is not None else None
        ),
        pulse_direction=(
            translate_pulse_direction_from_model(pulse.direction)
            if pulse.direction is not None
            else None
        ),
    )


def translate_pulse_to_model(pulse: metadata_elements.Pulse) -> models.PulseType:
    """Translate pulse to model."""
    return models.PulseType(
        pulse_length=models.DoubleWithUnit(value=pulse.pulse_length, unit=models.Units.S),
        bandwidth=models.DoubleWithUnit(value=pulse.bandwidth, unit=models.Units.HZ),
        pulse_energy=models.DoubleWithUnit(value=pulse.pulse_energy, unit=models.Units.J),
        pulse_sampling_rate=models.DoubleWithUnit(
            value=pulse.pulse_sampling_rate,
            unit=models.Units.HZ,
        ),
        pulse_start_frequency=(
            models.DoubleWithUnit(
                value=pulse.pulse_start_frequency,
                unit=models.Units.HZ,
            )
            if pulse.pulse_start_frequency is not None
            else None
        ),
        pulse_start_phase=(
            models.DoubleWithUnit(
                value=pulse.pulse_start_phase,
                unit=models.Units.RAD,
            )
            if pulse.pulse_start_phase is not None
            else None
        ),
        direction=(
            translate_pulse_direction_to_model(pulse.pulse_direction)
            if pulse.pulse_direction is not None
            else None
        ),
    )


def _translate_poly_list_from_model(
    poly_list: list[models.PolyType],
    specific_type: type[Poly2DT],
) -> list[Poly2DT]:
    """Translate a model polynomial list into metadata polynomials."""
    return [translate_polynomial_from_model(poly, specific_type) for poly in poly_list]


def _translate_doppler_centroid_vector_from_model(
    poly_list: list[models.PolyType],
) -> metadata_elements.DopplerCentroidVector:
    """Translate a Doppler centroid vector from model."""
    return metadata_elements.DopplerCentroidVector(
        poly_list=_translate_poly_list_from_model(
            poly_list,
            metadata_elements.DopplerCentroidVector.SINGLE_POLY_TYPE,
        ),
    )


def _translate_doppler_rate_vector_from_model(
    poly_list: list[models.PolyType],
) -> metadata_elements.DopplerRateVector:
    """Translate a Doppler rate vector from model."""
    return metadata_elements.DopplerRateVector(
        poly_list=_translate_poly_list_from_model(
            poly_list,
            metadata_elements.DopplerRateVector.SINGLE_POLY_TYPE,
        ),
    )


def _translate_tops_azimuth_modulation_rate_vector_from_model(
    poly_list: list[models.PolyType],
) -> metadata_elements.TopsAzimuthModulationRateVector:
    """Translate a TOPS azimuth modulation rate vector from model."""
    return metadata_elements.TopsAzimuthModulationRateVector(
        poly_list=_translate_poly_list_from_model(
            poly_list,
            metadata_elements.TopsAzimuthModulationRateVector.SINGLE_POLY_TYPE,
        ),
    )


def _translate_slant_to_ground_vector_from_model(
    poly_list: list[models.PolyType],
) -> metadata_elements.SlantToGroundVector:
    """Translate a slant-to-ground vector from model."""
    return metadata_elements.SlantToGroundVector(
        poly_list=_translate_poly_list_from_model(
            poly_list,
            metadata_elements.SlantToGroundVector.SINGLE_POLY_TYPE,
        ),
    )


def _translate_ground_to_slant_vector_from_model(
    poly_list: list[models.PolyType],
) -> metadata_elements.GroundToSlantVector:
    """Translate a ground-to-slant vector from model."""
    return metadata_elements.GroundToSlantVector(
        poly_list=_translate_poly_list_from_model(
            poly_list,
            metadata_elements.GroundToSlantVector.SINGLE_POLY_TYPE,
        ),
    )


def _translate_slant_to_incidence_vector_from_model(
    poly_list: list[models.PolyType],
) -> metadata_elements.SlantToIncidenceVector:
    """Translate a slant-to-incidence vector from model."""
    return metadata_elements.SlantToIncidenceVector(
        poly_list=_translate_poly_list_from_model(
            poly_list,
            metadata_elements.SlantToIncidenceVector.SINGLE_POLY_TYPE,
        ),
    )


def _translate_slant_to_elevation_vector_from_model(
    poly_list: list[models.PolyType],
) -> metadata_elements.SlantToElevationVector:
    """Translate a slant-to-elevation vector from model."""
    return metadata_elements.SlantToElevationVector(
        poly_list=_translate_poly_list_from_model(
            poly_list,
            metadata_elements.SlantToElevationVector.SINGLE_POLY_TYPE,
        ),
    )


def _translate_poly_vector_to_model(vector: _PolyVectorLike) -> list[models.PolyType]:
    """Translate a polynomial metadata vector into a model list."""
    return translate_polynomial_list_to_model(vector.poly_list)


def _translate_coreg_poly_vector_to_model(
    vector: _CoregPolyVectorLike,
) -> list[models.PolyCoregType]:
    """Translate a coregistration polynomial vector into a model list."""
    return translate_coreg_polynomial_list_to_model(vector.poly_list)


CHANNEL_FIELDS_FROM_MODEL = (
    ("raster_info", translate_raster_info_from_model),
    ("data_set_info", translate_dataset_info_from_model),
    ("swath_info", translate_swath_info_from_model),
    ("sampling_constants", translate_sampling_constants_from_model),
    ("acquisition_time_line", translate_acquisition_time_line_from_model),
    ("data_statistics", translate_data_statistics_from_model),
    ("burst_info", translate_burst_info_from_model),
    ("state_vector_data", translate_state_vectors_from_model),
    ("doppler_centroid", _translate_doppler_centroid_vector_from_model),
    ("doppler_rate", _translate_doppler_rate_vector_from_model),
    (
        "tops_azimuth_modulation_rate",
        _translate_tops_azimuth_modulation_rate_vector_from_model,
    ),
    ("slant_to_ground", _translate_slant_to_ground_vector_from_model),
    ("ground_to_slant", _translate_ground_to_slant_vector_from_model),
    ("slant_to_incidence", _translate_slant_to_incidence_vector_from_model),
    ("slant_to_elevation", _translate_slant_to_elevation_vector_from_model),
    ("attitude_info", translate_attitude_from_model),
    ("ground_corner_points", translate_ground_corner_points_from_model),
    ("pulse", translate_pulse_from_model),
    ("coreg_poly", translate_coreg_polynomial_list_from_model),
    ("antenna_info", translate_antenna_info_from_model),
)


CHANNEL_FIELDS_TO_MODEL = (
    ("RasterInfo", "raster_info", translate_raster_info_to_model),
    ("SamplingConstants", "sampling_constants", translate_sampling_constants_to_model),
    ("Pulse", "pulse", translate_pulse_to_model),
    ("SwathInfo", "swath_info", translate_swath_info_to_model),
    ("DataSetInfo", "data_set_info", translate_dataset_info_to_model),
    ("StateVectors", "state_vector_data", translate_state_vectors_to_model),
    ("AttitudeInfo", "attitude_info", translate_attitude_to_model),
    ("AcquisitionTimeLine", "acquisition_time_line", translate_acquisition_time_line_to_model),
    ("GroundCornerPoints", "ground_corner_points", translate_ground_corner_points_to_model),
    ("BurstInfo", "burst_info", translate_burst_info_to_model),
    ("DopplerCentroidVector", "doppler_centroid", _translate_poly_vector_to_model),
    ("DopplerRateVector", "doppler_rate", _translate_poly_vector_to_model),
    (
        "TopsAzimuthModulationRateVector",
        "tops_azimuth_modulation_rate",
        _translate_poly_vector_to_model,
    ),
    ("SlantToGroundVector", "slant_to_ground", _translate_poly_vector_to_model),
    ("GroundToSlantVector", "ground_to_slant", _translate_poly_vector_to_model),
    ("SlantToElevationVector", "slant_to_elevation", _translate_poly_vector_to_model),
    ("SlantToIncidenceVector", "slant_to_incidence", _translate_poly_vector_to_model),
    ("AntennaInfo", "antenna_info", translate_antenna_info_to_model),
    ("DataStatistics", "data_statistics", translate_data_statistics_to_model),
    ("CoregPolyVector", "coreg_poly", _translate_coreg_poly_vector_to_model),
)


def translate_metadata_channel_from_model(
    channel: models.AresysXmlDoc.Channel,
) -> metadata.MetaDataChannel:
    """Translate a metadata channel model into the corresponding object."""
    mdc = metadata.MetaDataChannel(
        content_id=channel.content_id,
        number=channel.number,
        total=channel.total,
    )

    for field_name, translator in CHANNEL_FIELDS_FROM_MODEL:
        if (value := getattr(channel, field_name)) is not None:
            mdc.insert_element(translator(value))

    return mdc


def translate_metadata_from_model(
    model: models.AresysXmlDoc,
) -> metadata.MetaData:
    """Translate metadata model into corresponding object.

    Parameters
    ----------
    model : models.AresysXmlDoc
        xsdata model

    Returns
    -------
    metadata.MetaData
        metadata object
    """
    output_metadata = metadata.MetaData(description=model.description)

    for channel in model.channel:
        output_metadata.channels.append(translate_metadata_channel_from_model(channel))

    return output_metadata


def translate_metadata_channel_to_model(
    metadata_channel: metadata.MetaDataChannel,
    number: int,
    total: int,
) -> models.AresysXmlDoc.Channel:
    """Translate a metadata channel into the corresponding model."""
    channel_model = models.AresysXmlDoc.Channel(
        number=number,
        total=total,
        content_id=metadata_channel.content_id,
    )

    for element_name, field_name, translator in CHANNEL_FIELDS_TO_MODEL:
        if element_name in metadata_channel.elements:
            setattr(channel_model, field_name, translator(getattr(metadata_channel, field_name)))

    return channel_model


def translate_metadata_to_model(
    metadata_obj: metadata.MetaData,
) -> models.AresysXmlDoc:
    """Translate metadata model into corresponding object.

    Parameters
    ----------
    metadata_obj : metadata.MetaData
        metadata object

    Returns
    -------
    models.AresysXmlDoc
        xsdata model
    """
    metadata_model = models.AresysXmlDoc(
        number_of_channels=len(metadata_obj.channels),
        version_number=2.1,
        description=metadata_obj.description,
    )

    for channel_number, metadata_channel in enumerate(metadata_obj.channels, start=1):
        metadata_model.channel.append(
            translate_metadata_channel_to_model(
                metadata_channel=metadata_channel,
                number=metadata_channel.number
                if metadata_channel.number is not None
                else channel_number,
                total=metadata_channel.total
                if metadata_channel.total is not None
                else len(metadata_obj.channels),
            ),
        )

    return metadata_model
