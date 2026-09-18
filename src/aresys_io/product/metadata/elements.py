# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""MetaData elements module."""

from __future__ import annotations

from typing import Any, ClassVar, Generic, Literal, TypeVar, get_args

import numpy as np
import numpy.typing as npt
from perseo_core.timing import PreciseDateTime
from pydantic import BaseModel, Field, PrivateAttr, field_validator, model_validator

__all__ = [
    "METADATA_ELEMENT_NAMES",
    "AcquisitionTimeLine",
    "AntennaInfo",
    "AntennaPolarization",
    "AttitudeInfo",
    "AttitudeReferenceFrame",
    "AttitudeRotationOrder",
    "AttitudeType",
    "Burst",
    "CoregPoly",
    "CoregPolyVector",
    "DataBlockStatistic",
    "DataSetImageQuantity",
    "DataSetInfo",
    "DataStatistics",
    "DopplerCentroid",
    "DopplerCentroidVector",
    "DopplerRate",
    "DopplerRateVector",
    "GeoPoint",
    "GroundCornerPoints",
    "GroundToSlant",
    "GroundToSlantVector",
    "MetaDataElementName",
    "OrbitDirection",
    "Poly2D",
    "Pulse",
    "PulseDirection",
    "RasterByteOrder",
    "RasterCellType",
    "RasterFormat",
    "RasterInfo",
    "SamplingConstants",
    "SideLooking",
    "SlantToElevation",
    "SlantToElevationVector",
    "SlantToGround",
    "SlantToGroundVector",
    "SlantToIncidence",
    "SlantToIncidenceVector",
    "StateVectors",
    "SwathInfo",
    "SwathPolarization",
    "TopsAzimuthModulationRate",
    "TopsAzimuthModulationRateVector",
]


RasterByteOrder = Literal["BIGENDIAN", "LITTLEENDIAN"]
RasterCellType = Literal[
    "INT8",
    "INT16",
    "INT32",
    "FLOAT32",
    "FLOAT64",
    "INT8_COMPLEX",
    "INT16_COMPLEX",
    "INT_COMPLEX",
    "FLOAT_COMPLEX",
    "DOUBLE_COMPLEX",
    "CUSTOM",
]
RasterFormat = Literal["ARESYS_RASTER", "ARESYS_GEOTIFF"]
OrbitDirection = Literal["ASCENDING", "DESCENDING"]
SideLooking = Literal["RIGHT", "LEFT"]
PulseDirection = Literal["UP", "DOWN"]
DataSetImageQuantity = Literal["BETA", "SIGMA", "GAMMA"]
SwathPolarization = Literal["HH", "HV", "VH", "VV", "XX"]
AntennaPolarization = Literal["HH", "HV", "VH", "VV", "XX"]
AttitudeReferenceFrame = Literal["GEOCENTRIC", "GEODETIC", "ZERODOPPLER"]
AttitudeRotationOrder = Literal["YPR", "YRP", "PRY", "PYR", "RYP", "RPY"]
AttitudeType = Literal["NOMINAL", "REFINED"]

MetaDataElementName = Literal[
    "RasterInfo",
    "DataSetInfo",
    "SwathInfo",
    "SamplingConstants",
    "AcquisitionTimeLine",
    "BurstInfo",
    "StateVectors",
    "AttitudeInfo",
    "Pulse",
    "GroundCornerPoints",
    "DopplerCentroidVector",
    "DopplerRateVector",
    "TopsAzimuthModulationRateVector",
    "SlantToGroundVector",
    "GroundToSlantVector",
    "SlantToIncidenceVector",
    "SlantToElevationVector",
    "AntennaInfo",
    "DataStatistics",
    "CoregPolyVector",
]
METADATA_ELEMENT_NAMES: set[MetaDataElementName] = set(get_args(MetaDataElementName))


class MetaDataPydanticModel(BaseModel):
    """Base Pydantic model for metadata elements."""

    model_config = {
        "arbitrary_types_allowed": True,
        "populate_by_name": True,
        "validate_assignment": True,
    }

    @property
    def element_name(self) -> MetaDataElementName:
        """The element name."""
        return self.__class__.__name__  # pyrefly: ignore[bad-return]  # pyright: ignore[reportReturnType]


class RasterInfo(MetaDataPydanticModel):
    """Raster metadata container based on Pydantic public fields."""

    file_name: str = ""
    lines: int
    samples: int
    header_offset_bytes: int = 0
    row_prefix_bytes: int = 0
    byte_order: RasterByteOrder = "LITTLEENDIAN"
    cell_type: RasterCellType
    lines_start: float | PreciseDateTime = 0.0
    lines_start_unit: str = ""
    lines_step: float = 0.0
    lines_step_unit: str = ""
    samples_start: float | PreciseDateTime = 0.0
    samples_start_unit: str = ""
    samples_step: float = 0.0
    samples_step_unit: str = ""
    invalid_value: float | complex | None = None
    format_type: RasterFormat | None = None

    @property
    def azimuth_axis(self) -> npt.NDArray:
        """The azimuth axis of the raster.

        Returns
        -------
        npt.NDArray
            The azimuth axis of the raster.

        """
        return np.arange(0, self.lines, 1) * self.lines_step + self.lines_start  # pyrefly: ignore[unsupported-operation]

    @property
    def range_axis(self) -> npt.NDArray:
        """The range axis of the raster.

        Returns
        -------
        npt.NDArray
            The range axis of the raster.

        """
        return np.arange(0, self.samples, 1) * self.samples_step + self.samples_start  # pyrefly: ignore[unsupported-operation]

    @property
    def lines_start_date(self) -> PreciseDateTime:
        """The start date of the lines.

        Returns
        -------
        PreciseDateTime
            The start date of the lines.

        Raises
        ------
        TypeError
            If the lines start is not a PreciseDateTime.

        """
        if not isinstance(self.lines_start, PreciseDateTime):
            msg = "The lines start is not a PreciseDateTime"
            raise TypeError(msg)
        return self.lines_start

    @property
    def samples_start_date(self) -> PreciseDateTime:
        """The start date of the samples.

        Returns
        -------
        PreciseDateTime
            The start date of the samples.

        Raises
        ------
        TypeError
            If the samples start is not a PreciseDateTime.

        """
        if not isinstance(self.samples_start, PreciseDateTime):
            msg = "The samples start is not a PreciseDateTime"
            raise TypeError(msg)
        return self.samples_start


class DataSetInfo(MetaDataPydanticModel):
    """Dataset metadata container based on Pydantic public fields."""

    sensor_name: str
    description: str
    sense_date: PreciseDateTime | None = None
    acquisition_mode: str
    image_type: str
    projection: str
    projection_params: str | None = None
    projection_params_format: str | None = None
    image_quantity: DataSetImageQuantity | None = None
    acquisition_station: str
    processing_center: str
    processing_date: PreciseDateTime | None = None
    processing_software: str
    fc_hz: float
    side_looking: SideLooking
    external_calibration_factor: float | None = None
    data_take_id: int | None = None
    instrument_conf_id: int | None = None


class GeoPoint(MetaDataPydanticModel):
    """GeoPoint class."""

    lat: float = 0.0
    lon: float = 0.0
    height: float = 0.0
    theta_inc: float = 0.0
    theta_look: float = 0.0

    def to_list(self) -> list[float]:
        """Retrieve the geo point as a list:  [lat, lon, height, theta_inc, theta_look]."""
        return [self.lat, self.lon, self.height, self.theta_inc, self.theta_look]


class GroundCornerPoints(MetaDataPydanticModel):
    """GroundCornerPoint class."""

    easting_grid_size: float = 0.0
    northing_grid_size: float = 0.0
    nw_point: GeoPoint = Field(default_factory=GeoPoint)
    ne_point: GeoPoint = Field(default_factory=GeoPoint)
    sw_point: GeoPoint = Field(default_factory=GeoPoint)
    se_point: GeoPoint = Field(default_factory=GeoPoint)
    center_point: GeoPoint = Field(default_factory=GeoPoint)

    @property
    def geo_points(self) -> list[GeoPoint]:
        """Geo points as a list:  [nw_point, ne_point, sw_point, se_point, center_point]."""
        return [self.nw_point, self.ne_point, self.sw_point, self.se_point, self.center_point]


class SwathInfo(MetaDataPydanticModel):
    """SwathInfo class."""

    swath: str
    swath_acquisition_order: int = 0
    polarization: SwathPolarization
    rank: int = 0
    range_delay_bias: float = 0.0
    range_delay_bias_unit: ClassVar[str] = "s"
    acquisition_start_time: PreciseDateTime
    acquisition_start_time_unit: ClassVar[str] = "Utc"
    azimuth_steering_angle_reference_time: float | None = None
    az_steering_angle_ref_time_unit: ClassVar[str] = "s"
    azimuth_steering_angle_pol: tuple[float, float, float, float] | None = None
    azimuth_steering_rate_reference_time: float | None = 0.0
    az_steering_rate_ref_time_unit: ClassVar[str] = "s"
    azimuth_steering_rate_pol: tuple[float, float, float] | None = (0.0, 0.0, 0.0)
    acquisition_prf: float = 0.0
    acquisition_prf_unit: ClassVar[str] = "Hz"
    echoes_per_burst: int = 0
    channel_delay: float | None = None
    rx_gain: float | None = None

    @model_validator(mode="after")
    def _enforce_steering_exclusivity(self) -> SwathInfo:
        # Usage of __setattr__ is necessary to avoid recursive validation
        if self.azimuth_steering_angle_reference_time is not None:
            object.__setattr__(self, "azimuth_steering_rate_reference_time", None)  # ruff: ignore[unnecessary-dunder-call]
        elif self.azimuth_steering_rate_reference_time is not None:
            object.__setattr__(self, "azimuth_steering_angle_reference_time", None)  # ruff: ignore[unnecessary-dunder-call]

        if self.azimuth_steering_angle_pol is not None:
            object.__setattr__(self, "azimuth_steering_rate_pol", None)  # ruff: ignore[unnecessary-dunder-call]
        elif self.azimuth_steering_rate_pol is not None:
            object.__setattr__(self, "azimuth_steering_angle_pol", None)  # ruff: ignore[unnecessary-dunder-call]

        return self


class SamplingConstants(MetaDataPydanticModel):
    """SamplingConstants class."""

    frg_hz: float
    brg_hz: float
    faz_hz: float
    baz_hz: float


class AcquisitionTimeLine(MetaDataPydanticModel):
    """AcquisitionTimeLine class."""

    missing_lines: list[float] = Field(default_factory=list)
    swst_changes: list[tuple[float, float]] = Field(default_factory=list)
    noise_packet: list[float] = Field(default_factory=list)
    internal_calibration: list[float] = Field(default_factory=list)
    swl_changes: list[tuple[float, float]] = Field(default_factory=list)
    prf_changes: list[tuple[float, float]] = Field(default_factory=list)
    duplicated_lines: list[float] = Field(default_factory=list)
    chirp_period: str | None = None


class AttitudeInfo(MetaDataPydanticModel):
    """AttitudeInfo class."""

    ypr_deg: npt.NDArray[np.float64]
    reference_time: PreciseDateTime
    time_step: float
    reference_frame: AttitudeReferenceFrame
    rotation_order: AttitudeRotationOrder
    attitude_type: AttitudeType = "NOMINAL"

    @field_validator("ypr_deg", mode="before")
    @classmethod
    def _validate_ypr_deg(cls, value: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        if not isinstance(value, np.ndarray):
            msg = "Attitude ypr_deg must be a NumPy ndarray"
            raise TypeError(msg)
        if value.dtype != np.float64:
            msg = "Attitude ypr_deg must have dtype float64"
            raise ValueError(msg)
        if value.ndim != 2 or value.shape[1] != 3:
            msg = "Attitude angles must be a (N, 3) array with columns [yaw, pitch, roll]"
            raise ValueError(msg)
        return value

    @property
    def times(self) -> npt.NDArray:
        """The time axis of the attitude data.

        Returns
        -------
        npt.NDArray
            The time axis of the attitude data.

        """
        return np.arange(self.ypr_deg.shape[0]) * self.time_step + self.reference_time  # pyrefly: ignore[unsupported-operation]


class Burst(MetaDataPydanticModel):
    """Single burst metadata."""

    range_start_time: float
    azimuth_start_time: PreciseDateTime
    lines: int
    burst_center_azimuth_shift: float | None = None


class BurstInfo(MetaDataPydanticModel):
    """Burst info metadata container."""

    burst_repetition_frequency: float = 0.0
    bursts: list[Burst] = Field(default_factory=list)

    @property
    def lines_per_burst(self) -> int:
        """The number of lines per burst if constant, raise otherwise."""
        if not self.bursts:
            msg = "No bursts available"
            raise ValueError(msg)
        first = self.bursts[0].lines
        if any(burst.lines != first for burst in self.bursts):
            msg = "Lines per burst are not constant across bursts"
            raise ValueError(msg)
        return first

    def get_burst_roi(
        self,
        burst_index: int,
        raster_info: RasterInfo,
        range_interval: tuple[int, int] | None = None,
    ) -> list[int]:
        """Get the region of interest for a specific burst.

        Parameters
        ----------
        burst_index : int
            Index of the burst to retrieve the ROI for.
        raster_info : RasterInfo
            Raster information for the product.
        range_interval : tuple[int, int] | None, optional
            Range of interest in the format (start, end), by default None.

        Returns
        -------
        list[int]
            The region of interest for the specified burst.

        Raises
        ------
        ValueError
            If the burst index is not valid.
        """
        if range_interval is None:
            range_interval = (0, raster_info.samples)

        if burst_index < 0 or burst_index >= len(self.bursts):
            msg = "Not valid burst index"
            raise ValueError(msg)

        first_line = 0
        for i_burst in range(burst_index):
            first_line += self.bursts[i_burst].lines

        return [first_line, range_interval[0], self.bursts[burst_index].lines, range_interval[1]]


class StateVectors(MetaDataPydanticModel):
    """State vectors metadata container."""

    position_vector: npt.NDArray[np.float64]
    velocity_vector: npt.NDArray[np.float64]
    reference_time: PreciseDateTime
    time_step: float
    orbit_number: int | None = None
    track_number: int | None = None
    anx_time: PreciseDateTime | None = None
    anx_position: tuple[float, float, float] | None = None
    _annotated_orbit_direction: OrbitDirection | None = PrivateAttr()

    @property
    def annotated_orbit_direction(self) -> OrbitDirection | None:
        """Annotated orbit direction.

        Might be different from the orbit direction which is derived from velocity.
        """
        return self._annotated_orbit_direction

    @annotated_orbit_direction.setter
    def annotated_orbit_direction(self, value: OrbitDirection | None) -> None:
        self._annotated_orbit_direction = value

    def model_post_init(self, _: Any) -> None:  # ruff: ignore[any-type]
        """Post-initialization for the model."""
        self._annotated_orbit_direction = self.orbit_direction

    @field_validator("position_vector", "velocity_vector", mode="before")
    @classmethod
    def _validate_state_vector_array(
        cls,
        value: npt.NDArray[np.float64],
    ) -> npt.NDArray[np.float64]:
        if not isinstance(value, np.ndarray):
            msg = "State vectors must be NumPy ndarrays"
            raise TypeError(msg)
        if value.dtype != np.float64:
            msg = "State vectors must have dtype float64"
            raise ValueError(msg)
        if value.ndim != 2 or value.shape[1] != 3:
            msg = "State vectors must be a (N, 3) array"
            raise ValueError(msg)
        if value.shape[0] == 0:
            msg = "State vectors cannot be empty"
            raise ValueError(msg)
        return value

    @field_validator("orbit_number", "track_number")
    @classmethod
    def _validate_positive_optional_int(cls, value: int | None) -> int | None:
        if value is not None and value <= 0:
            msg = "Orbit and track numbers must be positive when provided"
            raise ValueError(msg)
        return value

    @property
    def orbit_direction(self) -> OrbitDirection:
        """Orbit direction inferred from the first velocity vector."""
        if self.velocity_vector[0, 2] > 0:
            return "ASCENDING"
        return "DESCENDING"

    @property
    def num_state_vectors(self) -> int:
        """Number of state vectors."""
        return self.position_vector.shape[0]

    @property
    def times(self) -> npt.NDArray:
        """The time axis of the state vector data.

        Returns
        -------
        npt.NDArray
            The time axis of the state vector data.

        """
        return np.arange(self.position_vector.shape[0]) * self.time_step + self.reference_time  # pyrefly: ignore[unsupported-operation]


ReferenceAzimuthTimeT = TypeVar("ReferenceAzimuthTimeT", PreciseDateTime, float)


class Poly2D(MetaDataPydanticModel, Generic[ReferenceAzimuthTimeT]):
    """Base class for Poly2D format."""

    POWERS_X: ClassVar[tuple[int, ...]] = (0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0)
    POWERS_Y: ClassVar[tuple[int, ...]] = (0, 1, 0, 1, 2, 3, 4, 5, 6, 7, 8)
    UNITS: ClassVar[tuple[str, ...]] = 11 * ("",)

    t_ref_az: ReferenceAzimuthTimeT
    t_ref_rg: float
    coefficients: list[float] = Field(default_factory=list)

    @field_validator("coefficients")
    @classmethod
    def _validate_coefficients(cls, value: list[float]) -> list[float]:
        if len(value) < 7:
            msg = "Polynomial must contain at least 7 coefficients"
            raise ValueError(msg)
        if len(value) > len(cls.POWERS_X):
            msg = "the size of coefficients and powers must agree"
            raise ValueError(msg)
        return value


class DopplerCentroid(Poly2D):
    """DopplerCentroid class."""

    UNITS = (
        "Hz",
        "Hz/s",
        "Hz/s",
        "Hz/s2",
        "Hz/s2",
        "Hz/s3",
        "Hz/s4",
        "Hz/s5",
        "Hz/s6",
        "Hz/s7",
        "Hz/s8",
    )


class DopplerCentroidVector(MetaDataPydanticModel):
    """List of DopplerCentroid poly."""

    SINGLE_POLY_TYPE: ClassVar[type[DopplerCentroid]] = DopplerCentroid
    poly_list: list[DopplerCentroid] = Field(default_factory=list)


class DopplerRate(Poly2D):
    """DopplerRate class."""

    UNITS = (
        "Hz/s",
        "Hz/s2",
        "Hz/s2",
        "Hz/s3",
        "Hz/s3",
        "Hz/s4",
        "Hz/s5",
        "Hz/s6",
        "Hz/s7",
        "Hz/s8",
        "Hz/s9",
    )


class DopplerRateVector(MetaDataPydanticModel):
    """list of DopplerRate poly."""

    SINGLE_POLY_TYPE: ClassVar[type[DopplerRate]] = DopplerRate
    poly_list: list[DopplerRate] = Field(default_factory=list)


class TopsAzimuthModulationRate(Poly2D):
    """TopsAzimuthModulationRate class."""

    UNITS = (
        "Hz",
        "Hz/s",
        "Hz/s",
        "Hz/s2",
        "Hz/s2",
        "Hz/s3",
        "Hz/s4",
        "Hz/s5",
        "Hz/s6",
        "Hz/s7",
        "Hz/s8",
    )


class TopsAzimuthModulationRateVector(MetaDataPydanticModel):
    """List of TopsAzimuthModulationRate poly."""

    SINGLE_POLY_TYPE: ClassVar[type[TopsAzimuthModulationRate]] = TopsAzimuthModulationRate
    poly_list: list[TopsAzimuthModulationRate] = Field(default_factory=list)


class SlantToGround(Poly2D):
    """SlantToGround class."""

    UNITS = (
        "m",
        "m/s",
        "m/s",
        "m/s2",
        "m/s2",
        "m/s3",
        "m/s4",
        "m/s5",
        "m/s6",
        "m/s7",
        "m/s8",
    )


class SlantToGroundVector(MetaDataPydanticModel):
    """List of SlantToGround poly."""

    SINGLE_POLY_TYPE: ClassVar[type[SlantToGround]] = SlantToGround
    poly_list: list[SlantToGround] = Field(default_factory=list)


class GroundToSlant(Poly2D):
    """GroundToSlant class."""

    UNITS = (
        "s",
        "s/m",
        "s/m",
        "s/m2",
        "s/m2",
        "s/m3",
        "s/m4",
        "s/m5",
        "s/m6",
        "s/m7",
        "s/m8",
    )


class GroundToSlantVector(MetaDataPydanticModel):
    """List of GroundToSlant poly."""

    SINGLE_POLY_TYPE: ClassVar[type[GroundToSlant]] = GroundToSlant
    poly_list: list[GroundToSlant] = Field(default_factory=list)


class SlantToIncidence(Poly2D):
    """SlantToIncidence class."""

    UNITS = (
        "deg",
        "deg/s",
        "deg/s",
        "deg/s2",
        "deg/s2",
        "deg/s3",
        "deg/s4",
        "deg/s5",
        "deg/s6",
        "deg/s7",
        "deg/s8",
    )


class SlantToIncidenceVector(MetaDataPydanticModel):
    """List of SlantToIncidence poly."""

    SINGLE_POLY_TYPE: ClassVar[type[SlantToIncidence]] = SlantToIncidence
    poly_list: list[SlantToIncidence] = Field(default_factory=list)


class SlantToElevation(Poly2D):
    """SlantToElevation class."""

    UNITS = (
        "deg",
        "deg/s",
        "deg/s",
        "deg/s2",
        "deg/s2",
        "deg/s3",
        "deg/s4",
        "deg/s5",
        "deg/s6",
        "deg/s7",
        "deg/s8",
    )


class SlantToElevationVector(MetaDataPydanticModel):
    """List of SlantToElevation poly."""

    SINGLE_POLY_TYPE: ClassVar[type[SlantToElevation]] = SlantToElevation
    poly_list: list[SlantToElevation] = Field(default_factory=list)


class AntennaInfo(MetaDataPydanticModel):
    """Antenna pattern metadata container."""

    sensor_name: str | None = None
    acquisition_mode: str
    acquisition_beam: str
    polarization: AntennaPolarization
    lines_per_pattern: int | None = None


class DataBlockStatistic(MetaDataPydanticModel):
    """Statistics computed over a data block."""

    num_samples: int
    max_i: float
    min_i: float
    max_q: float
    min_q: float
    sum_i: float
    sum_q: float
    sum_2_i: float
    sum_2_q: float
    line_start: int
    line_stop: int


class DataStatistics(MetaDataPydanticModel):
    """Statistics computed over full data."""

    num_samples: int
    max_i: float
    min_i: float
    max_q: float
    min_q: float
    sum_i: float
    sum_q: float
    sum_2_i: float
    sum_2_q: float
    std_dev_i: float
    std_dev_q: float
    statistics_list: list[DataBlockStatistic] = Field(default_factory=list)


class CoregPoly(MetaDataPydanticModel):
    """Coregistration polynomials metadata container."""

    t_ref_az: PreciseDateTime
    t_ref_rg: float
    coefficients_az: list[float] = Field(default_factory=list)
    coefficients_rg: list[float] = Field(default_factory=list)

    @field_validator("coefficients_az", "coefficients_rg")
    @classmethod
    def _validate_coefficients(cls, value: list[float]) -> list[float]:
        if len(value) != 4:
            msg = "Coreg polynomial must contain exactly 4 coefficients"
            raise ValueError(msg)
        return value


class CoregPolyVector(MetaDataPydanticModel):
    """List of CoregPoly."""

    SINGLE_POLY_TYPE: ClassVar[type[CoregPoly]] = CoregPoly
    poly_list: list[CoregPoly] = Field(default_factory=list)


class Pulse(MetaDataPydanticModel):
    """Pulse class."""

    pulse_length: float
    bandwidth: float
    pulse_sampling_rate: float
    pulse_energy: float
    pulse_start_frequency: float | None = None
    pulse_start_phase: float | None = None
    pulse_direction: PulseDirection | None = None
