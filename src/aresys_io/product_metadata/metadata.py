# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""MetaData module."""

from __future__ import annotations

import warnings
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from aresys_io.product_metadata import (
    metadata_elements,
)
from aresys_io.product_metadata.create_attitude import (
    create_attitude_from_attitude_info_and_trajectory,
)
from aresys_io.product_metadata.create_orbit import create_trajectory_from_state_vectors
from aresys_io.product_metadata.polynomials import (
    CoregistrationPoly,
    DopplerCentroidPoly,
    DopplerRatePoly,
    GroundToSlantPoly,
    PiecewisePolynomial2D,
    SlantToElevationPoly,
    SlantToGroundPoly,
    SlantToIncidencePoly,
    TopsAzimuthModulationRatePoly,
)

if TYPE_CHECKING:
    from perseo_core.geometry.navigation import CubicSplineTrajectory
    from perseo_core.geometry.pointing import Attitude

__all__ = ["MetaData", "MetaDataChannel", "create_new_metadata"]


@dataclass  # ruff: ignore[too-many-public-methods]
class MetaDataChannel:
    """MetaDataChannel class."""

    content_id: str | None = None
    number: int | None = None
    total: int | None = None
    elements: dict[
        metadata_elements.MetaDataElementName,
        metadata_elements.MetaDataPydanticModel,
    ] = field(default_factory=dict)

    def insert_element(
        self,
        element: metadata_elements.MetaDataPydanticModel,
        *,
        overwrite_ok: bool = False,
    ) -> None:
        """Insert the specified metadata element.

        Parameters
        ----------
        element : metadata_elements.MetaDataPydanticModel
            metadata element to insert
        overwrite_ok : bool
            overwrite existing metadata element of the same type.

        Raises
        ------
        RuntimeError
            if the element is not supported in the current metadata channel
        RuntimeError
            if the element is already present and overwrite_ok is False
        """
        element_name = element.element_name

        if element_name not in metadata_elements.METADATA_ELEMENT_NAMES:
            msg = f"The element {element_name} is not supported in the current metadata channel"
            raise RuntimeError(msg)

        if element_name in self.elements and not overwrite_ok:
            msg = (
                f"The element {element_name} is already present "
                "in the current metadata channel: element not inserted"
            )
            warnings.warn(msg, stacklevel=2)
            return

        self.elements[element_name] = element

    def remove_element(self, element_type: metadata_elements.MetaDataElementName) -> None:
        """Remove specified channel element.

        Parameters
        ----------
        element_type : metadata_elements.MetaDataElementName
            element name.

        """
        self.elements.pop(element_type)

    def get_element(
        self,
        element_type: metadata_elements.MetaDataElementName,
    ) -> metadata_elements.MetaDataPydanticModel:
        """Channel metadata element from element name.

        Parameters
        ----------
        element_type : metadata_elements.MetaDataElementName
            element name.

        Returns
        -------
        metadata_elements.MetaDataPydanticModel
            channel metadata element

        Raises
        ------
        RuntimeError
            if element is not available in the current metadata channel

        """
        element = self.elements.get(element_type)
        if element is None:
            msg = f"The element {element_type} is not available in the current metadata channel"
            raise RuntimeError(msg)

        return element

    @property
    def sampling_constants(self) -> metadata_elements.SamplingConstants:
        """SamplingConstants.

        Returns
        -------
        metadata_elements.SamplingConstants
            SamplingConstants metadata element.

        """
        sampling_constants = self.get_element("SamplingConstants")
        assert isinstance(sampling_constants, metadata_elements.SamplingConstants)
        return sampling_constants

    @property
    def pulse(self) -> metadata_elements.Pulse:
        """Pulse.

        Returns
        -------
        metadata_elements.Pulse
            Pulse metadata element.

        """
        pulse = self.get_element("Pulse")
        assert isinstance(pulse, metadata_elements.Pulse)
        return pulse

    @property
    def raster_info(self) -> metadata_elements.RasterInfo:
        """RasterInfo.

        Returns
        -------
        metadata_elements.RasterInfo
            RasterInfo metadata element.

        """
        raster_info = self.get_element("RasterInfo")
        assert isinstance(raster_info, metadata_elements.RasterInfo)
        return raster_info

    @property
    def data_set_info(self) -> metadata_elements.DataSetInfo:
        """DataSetInfo.

        Returns
        -------
        metadata_elements.DataSetInfo
            DataSetInfo metadata element.

        """
        data_set_info = self.get_element("DataSetInfo")
        assert isinstance(data_set_info, metadata_elements.DataSetInfo)
        return data_set_info

    @property
    def state_vector_data(self) -> metadata_elements.StateVectors:
        """StateVectors.

        Returns
        -------
        metadata_elements.StateVectors
            StateVectors metadata element.

        """
        state_vectors = self.get_element("StateVectors")
        assert isinstance(state_vectors, metadata_elements.StateVectors)
        return state_vectors

    @property
    def attitude_info(self) -> metadata_elements.AttitudeInfo:
        """AttitudeInfo.

        Returns
        -------
        metadata_elements.AttitudeInfo
            AttitudeInfo metadata element.

        """
        attitude_info = self.get_element("AttitudeInfo")
        assert isinstance(attitude_info, metadata_elements.AttitudeInfo)
        return attitude_info

    @property
    def acquisition_time_line(self) -> metadata_elements.AcquisitionTimeLine:
        """AcquisitionTimeLine.

        Returns
        -------
        metadata_elements.AcquisitionTimeLine
            AcquisitionTimeLine metadata element.

        """
        acquisition_time_line = self.get_element("AcquisitionTimeLine")
        assert isinstance(acquisition_time_line, metadata_elements.AcquisitionTimeLine)
        return acquisition_time_line

    @property
    def ground_corner_points(self) -> metadata_elements.GroundCornerPoints:
        """GroundCornerPoints.

        Returns
        -------
        metadata_elements.GroundCornerPoints
            GroundCornerPoints metadata element.

        """
        ground_corner_points = self.get_element("GroundCornerPoints")
        assert isinstance(ground_corner_points, metadata_elements.GroundCornerPoints)
        return ground_corner_points

    @property
    def burst_info(self) -> metadata_elements.BurstInfo:
        """BurstInfo.

        Returns
        -------
        metadata_elements.BurstInfo
            BurstInfo metadata element.

        """
        burst_info = self.get_element("BurstInfo")
        assert isinstance(burst_info, metadata_elements.BurstInfo)
        return burst_info

    @property
    def doppler_centroid(self) -> metadata_elements.DopplerCentroidVector:
        """DopplerCentroidVector.

        Returns
        -------
        metadata_elements.DopplerCentroidVector
            DopplerCentroidVector metadata element.

        """
        doppler_centroid = self.get_element("DopplerCentroidVector")
        assert isinstance(doppler_centroid, metadata_elements.DopplerCentroidVector)
        return doppler_centroid

    @property
    def doppler_rate(self) -> metadata_elements.DopplerRateVector:
        """DopplerRateVector.

        Returns
        -------
        metadata_elements.DopplerRateVector
            DopplerRateVector metadata element.

        """
        doppler_rate = self.get_element("DopplerRateVector")
        assert isinstance(doppler_rate, metadata_elements.DopplerRateVector)
        return doppler_rate

    @property
    def tops_azimuth_modulation_rate(
        self,
    ) -> metadata_elements.TopsAzimuthModulationRateVector:
        """TopsAzimuthModulationRateVector.

        Returns
        -------
        metadata_elements.TopsAzimuthModulationRateVector
            TopsAzimuthModulationRateVector metadata element.

        """
        tops_azimuth_modulation_rate = self.get_element("TopsAzimuthModulationRateVector")
        assert isinstance(
            tops_azimuth_modulation_rate,
            metadata_elements.TopsAzimuthModulationRateVector,
        )
        return tops_azimuth_modulation_rate

    @property
    def slant_to_ground(self) -> metadata_elements.SlantToGroundVector:
        """SlantToGroundVector.

        Returns
        -------
        metadata_elements.SlantToGroundVector
            SlantToGroundVector metadata element.

        """
        slant_to_ground = self.get_element("SlantToGroundVector")
        assert isinstance(slant_to_ground, metadata_elements.SlantToGroundVector)
        return slant_to_ground

    @property
    def ground_to_slant(self) -> metadata_elements.GroundToSlantVector:
        """GroundToSlantVector.

        Returns
        -------
        metadata_elements.GroundToSlantVector
            GroundToSlantVector metadata element.

        """
        ground_to_slant = self.get_element("GroundToSlantVector")
        assert isinstance(ground_to_slant, metadata_elements.GroundToSlantVector)
        return ground_to_slant

    @property
    def slant_to_incidence(self) -> metadata_elements.SlantToIncidenceVector:
        """SlantToIncidenceVector.

        Returns
        -------
        metadata_elements.SlantToIncidenceVector
            SlantToIncidenceVector metadata element.

        """
        slant_to_incidence = self.get_element("SlantToIncidenceVector")
        assert isinstance(slant_to_incidence, metadata_elements.SlantToIncidenceVector)
        return slant_to_incidence

    @property
    def slant_to_elevation(self) -> metadata_elements.SlantToElevationVector:
        """SlantToElevationVector.

        Returns
        -------
        metadata_elements.SlantToElevationVector
            SlantToElevationVector metadata element.

        """
        slant_to_elevation = self.get_element("SlantToElevationVector")
        assert isinstance(slant_to_elevation, metadata_elements.SlantToElevationVector)
        return slant_to_elevation

    @property
    def antenna_info(self) -> metadata_elements.AntennaInfo:
        """AntennaInfo.

        Returns
        -------
        metadata_elements.AntennaInfo
            AntennaInfo metadata element.

        """
        antenna_info = self.get_element("AntennaInfo")
        assert isinstance(antenna_info, metadata_elements.AntennaInfo)
        return antenna_info

    @property
    def data_statistics(self) -> metadata_elements.DataStatistics:
        """DataStatistics.

        Returns
        -------
        metadata_elements.DataStatistics
            DataStatistics metadata element.

        """
        data_statistics = self.get_element("DataStatistics")
        assert isinstance(data_statistics, metadata_elements.DataStatistics)
        return data_statistics

    @property
    def swath_info(self) -> metadata_elements.SwathInfo:
        """SwathInfo.

        Returns
        -------
        metadata_elements.SwathInfo
            SwathInfo metadata element.

        """
        swath_info = self.get_element("SwathInfo")
        assert isinstance(swath_info, metadata_elements.SwathInfo)
        return swath_info

    @property
    def coreg_poly(self) -> metadata_elements.CoregPolyVector:
        """CoregPolyVector.

        Returns
        -------
        metadata_elements.CoregPolyVector
            CoregPolyVector metadata element.

        """
        coreg_poly = self.get_element("CoregPolyVector")
        assert isinstance(coreg_poly, metadata_elements.CoregPolyVector)
        return coreg_poly

    def trajectory(self) -> CubicSplineTrajectory:
        """Create a CubicSplineTrajectory from the state vector data."""
        return create_trajectory_from_state_vectors(self.state_vector_data)

    def attitude(self) -> Attitude:
        """Create an Attitude object from the attitude data."""
        return create_attitude_from_attitude_info_and_trajectory(
            self.trajectory(), self.attitude_info
        )

    def doppler_centroid_poly(self) -> DopplerCentroidPoly:
        """Create a DopplerCentroidPoly from the doppler centroid metadata element."""
        return DopplerCentroidPoly.from_metadata(self.doppler_centroid)

    def doppler_rate_poly(self) -> DopplerRatePoly:
        """Create a DopplerRatePoly from the doppler rate metadata element."""
        return DopplerRatePoly.from_metadata(self.doppler_rate)

    def tops_azimuth_modulation_rate_poly(self) -> TopsAzimuthModulationRatePoly:
        """Create a TopsAzimuthModulationRatePoly from the tops azimuth rate metadata element."""
        return TopsAzimuthModulationRatePoly.from_metadata(self.tops_azimuth_modulation_rate)

    def ground_to_slant_poly(self) -> GroundToSlantPoly:
        """Create a GroundToSlantPoly from the ground to slant metadata element."""
        return GroundToSlantPoly.from_metadata(self.ground_to_slant)

    def slant_to_ground_poly(self) -> SlantToGroundPoly:
        """Create a SlantToGroundPoly from the slant to ground metadata element."""
        return SlantToGroundPoly.from_metadata(self.slant_to_ground)

    def slant_to_incidence_poly(self) -> SlantToIncidencePoly:
        """Create a SlantToIncidencePoly from the slant to incidence metadata element."""
        return SlantToIncidencePoly.from_metadata(self.slant_to_incidence)

    def slant_to_elevation_poly(self) -> SlantToElevationPoly:
        """Create a SlantToElevationPoly from the slant to elevation metadata element."""
        return SlantToElevationPoly.from_metadata(self.slant_to_elevation)

    def coregistration_poly(self) -> CoregistrationPoly:
        """Create a CoregistrationPoly from the coreg_poly metadata element."""
        return CoregistrationPoly.from_metadata(self.coreg_poly)


def create_new_metadata(
    num_metadata_channels: int = 1,
    description: str | None = None,
) -> MetaData:
    """Create a new empty MetaData object with the selected number of channels.

    Parameters
    ----------
    num_metadata_channels : int, optional
        number of metadata channels, by default 1
    description : str, optional
        metadata description, by default None.

    Returns
    -------
    MetaData
        new empty MetaData object
    """
    return MetaData(
        description=description or "",
        channels=[MetaDataChannel() for _ in range(num_metadata_channels)],
    )


@dataclass  # ruff: ignore[too-many-public-methods]
class MetaData:
    """Metadata."""

    channels: list[MetaDataChannel] = field(default_factory=list)
    description: str = ""

    def __getitem__(self, index: int) -> MetaDataChannel:
        """Retrieve the metadata channel at the specified index."""
        return self.channels[index]

    def insert_element(
        self,
        element: metadata_elements.MetaDataPydanticModel,
    ) -> None:
        """Insert a new metadata element into the first metadata channel.

        Parameters
        ----------
        element : metadata_elements.MetaDataPydanticModel
            metadata element to be inserted into the first metadata channel.

        """
        self.channels[0].insert_element(element)

    def remove_element(
        self,
        element_type: metadata_elements.MetaDataElementName,
    ) -> None:
        """Remove the specified metadata element from the first metadata channel.

        Parameters
        ----------
        element_type : metadata_elements.MetaDataElementName
            metadata element name to be removed from the first metadata channel.

        """
        self.channels[0].remove_element(element_type)

    @property
    def sampling_constants(self) -> metadata_elements.SamplingConstants:
        """SamplingConstants from the first metadata channel.

        Returns
        -------
        metadata_elements.SamplingConstants
            SamplingConstants metadata element from the first metadata channel.

        """
        return self.channels[0].sampling_constants

    @property
    def pulse(self) -> metadata_elements.Pulse:
        """Pulse from the first metadata channel.

        Returns
        -------
        metadata_elements.Pulse
            Pulse metadata element from the first metadata channel.

        """
        return self.channels[0].pulse

    @property
    def raster_info(self) -> metadata_elements.RasterInfo:
        """RasterInfo from the first metadata channel.

        Returns
        -------
        metadata_elements.RasterInfo
            RasterInfo metadata element from the first metadata channel.

        """
        return self.channels[0].raster_info

    @property
    def data_set_info(self) -> metadata_elements.DataSetInfo:
        """DataSetInfo from the first metadata channel.

        Returns
        -------
        metadata_elements.DataSetInfo
            DataSetInfo metadata element from the first metadata channel.

        """
        return self.channels[0].data_set_info

    @property
    def state_vector_data(self) -> metadata_elements.StateVectors:
        """StateVectors from the first metadata channel.

        Returns
        -------
        metadata_elements.StateVectors
            StateVectors metadata element from the first metadata channel.

        """
        return self.channels[0].state_vector_data

    @property
    def attitude_info(self) -> metadata_elements.AttitudeInfo:
        """AttitudeInfo from the first metadata channel.

        Returns
        -------
        metadata_elements.AttitudeInfo
            AttitudeInfo metadata element from the first metadata channel.

        """
        return self.channels[0].attitude_info

    @property
    def acquisition_time_line(self) -> metadata_elements.AcquisitionTimeLine:
        """AcquisitionTimeLine from the first metadata channel.

        Returns
        -------
        metadata_elements.AcquisitionTimeLine
            AcquisitionTimeLine metadata element from the first metadata channel.

        """
        return self.channels[0].acquisition_time_line

    @property
    def ground_corner_points(self) -> metadata_elements.GroundCornerPoints:
        """GroundCornerPoints from the first metadata channel.

        Returns
        -------
        metadata_elements.GroundCornerPoints
            GroundCornerPoints metadata element from the first metadata channel.

        """
        return self.channels[0].ground_corner_points

    @property
    def burst_info(self) -> metadata_elements.BurstInfo:
        """BurstInfo from the first metadata channel.

        Returns
        -------
        metadata_elements.BurstInfo
            BurstInfo metadata element from the first metadata channel.

        """
        return self.channels[0].burst_info

    @property
    def doppler_centroid(self) -> metadata_elements.DopplerCentroidVector:
        """DopplerCentroidVector from the first metadata channel.

        Returns
        -------
        metadata_elements.DopplerCentroidVector
            DopplerCentroidVector metadata element from the first metadata channel.

        """
        return self.channels[0].doppler_centroid

    @property
    def doppler_rate(self) -> metadata_elements.DopplerRateVector:
        """DopplerRateVector from the first metadata channel.

        Returns
        -------
        metadata_elements.DopplerRateVector
            DopplerRateVector metadata element from the first metadata channel.

        """
        return self.channels[0].doppler_rate

    @property
    def tops_azimuth_modulation_rate(self) -> metadata_elements.TopsAzimuthModulationRateVector:
        """TopsAzimuthModulationRateVector from the first metadata channel.

        Returns
        -------
        metadata_elements.TopsAzimuthModulationRateVector
            TopsAzimuthModulationRateVector metadata element from the first metadata channel.

        """
        return self.channels[0].tops_azimuth_modulation_rate

    @property
    def slant_to_ground(self) -> metadata_elements.SlantToGroundVector:
        """SlantToGroundVector from the first metadata channel.

        Returns
        -------
        metadata_elements.SlantToGroundVector
            SlantToGroundVector metadata element from the first metadata channel.

        """
        return self.channels[0].slant_to_ground

    @property
    def ground_to_slant(self) -> metadata_elements.GroundToSlantVector:
        """GroundToSlantVector from the first metadata channel.

        Returns
        -------
        metadata_elements.GroundToSlantVector
            GroundToSlantVector metadata element from the first metadata channel.

        """
        return self.channels[0].ground_to_slant

    @property
    def slant_to_incidence(self) -> metadata_elements.SlantToIncidenceVector:
        """SlantToIncidenceVector from the first metadata channel.

        Returns
        -------
        metadata_elements.SlantToIncidenceVector
            SlantToIncidenceVector metadata element from the first metadata channel.

        """
        return self.channels[0].slant_to_incidence

    @property
    def slant_to_elevation(self) -> metadata_elements.SlantToElevationVector:
        """SlantToElevationVector from the first metadata channel.

        Returns
        -------
        metadata_elements.SlantToElevationVector
            SlantToElevationVector metadata element from the first metadata channel.

        """
        return self.channels[0].slant_to_elevation

    @property
    def antenna_info(self) -> metadata_elements.AntennaInfo:
        """AntennaInfo from the first metadata channel.

        Returns
        -------
        metadata_elements.AntennaInfo
            AntennaInfo metadata element from the first metadata channel.

        """
        return self.channels[0].antenna_info

    @property
    def data_statistics(self) -> metadata_elements.DataStatistics:
        """DataStatistics from the first metadata channel.

        Returns
        -------
        metadata_elements.DataStatistics
            DataStatistics metadata element from the first metadata channel.

        """
        return self.channels[0].data_statistics

    @property
    def swath_info(self) -> metadata_elements.SwathInfo:
        """SwathInfo from the first metadata channel.

        Returns
        -------
        metadata_elements.SwathInfo
            SwathInfo metadata element from the first metadata channel.

        """
        return self.channels[0].swath_info

    @property
    def coreg_poly(self) -> metadata_elements.CoregPolyVector:
        """CoregPolyVector from the first metadata channel.

        Returns
        -------
        metadata_elements.CoregPolyVector
            CoregPolyVector metadata element from the first metadata channel.

        """
        return self.channels[0].coreg_poly

    def trajectory(self) -> CubicSplineTrajectory:
        """CubicSplineTrajectory from the first metadata channel.

        Returns
        -------
        CubicSplineTrajectory
            CubicSplineTrajectory metadata element from the first metadata channel.

        """
        return self.channels[0].trajectory()

    def attitude(self) -> Attitude:
        """Attitude from the first metadata channel.

        Returns
        -------
        Attitude
            Attitude metadata element from the first metadata channel.

        """
        return self.channels[0].attitude()

    def doppler_centroid_poly(self) -> PiecewisePolynomial2D:
        """Create a PiecewisePolynomial2D from the first metadata channel's doppler centroid.

        Returns
        -------
        PiecewisePolynomial2D
            PiecewisePolynomial2D metadata element from the first metadata channel.

        """
        return self.channels[0].doppler_centroid_poly()

    def doppler_rate_poly(self) -> PiecewisePolynomial2D:
        """Create a PiecewisePolynomial2D from the first metadata channel's doppler rate.

        Returns
        -------
        PiecewisePolynomial2D
            PiecewisePolynomial2D metadata element from the first metadata channel.

        """
        return self.channels[0].doppler_rate_poly()

    def tops_azimuth_modulation_rate_poly(self) -> PiecewisePolynomial2D:
        """Create a PiecewisePolynomial2D from the first metadata channel's tops azimuth mod rate.

        Returns
        -------
        PiecewisePolynomial2D
            PiecewisePolynomial2D metadata element from the first metadata channel.

        """
        return self.channels[0].tops_azimuth_modulation_rate_poly()

    def ground_to_slant_poly(self) -> PiecewisePolynomial2D:
        """Create a PiecewisePolynomial2D from the first metadata channel's ground to slant range.

        Returns
        -------
        PiecewisePolynomial2D
            PiecewisePolynomial2D metadata element from the first metadata channel.

        """
        return self.channels[0].ground_to_slant_poly()

    def slant_to_ground_poly(self) -> PiecewisePolynomial2D:
        """Create a PiecewisePolynomial2D from the first metadata channel's slant to ground range.

        Returns
        -------
        PiecewisePolynomial2D
            PiecewisePolynomial2D metadata element from the first metadata channel.

        """
        return self.channels[0].slant_to_ground_poly()

    def slant_to_incidence_poly(self) -> PiecewisePolynomial2D:
        """Create a PiecewisePolynomial2D from the first metadata channel's slant to incidence.

        Returns
        -------
        PiecewisePolynomial2D
            PiecewisePolynomial2D metadata element from the first metadata channel.

        """
        return self.channels[0].slant_to_incidence_poly()

    def slant_to_elevation_poly(self) -> PiecewisePolynomial2D:
        """Create a PiecewisePolynomial2D from the first metadata channel's slant to elevation.

        Returns
        -------
        PiecewisePolynomial2D
            PiecewisePolynomial2D metadata element from the first metadata channel.

        """
        return self.channels[0].slant_to_elevation_poly()

    def coregistration_poly(self) -> CoregistrationPoly:
        """Create a CoregistrationPoly from the first metadata channel's coregistration.

        Returns
        -------
        CoregistrationPoly
            CoregistrationPoly metadata element from the first metadata channel.

        """
        return self.channels[0].coregistration_poly()
