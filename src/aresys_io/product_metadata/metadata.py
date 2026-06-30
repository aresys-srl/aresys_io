# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""MetaData module."""

from __future__ import annotations

import warnings
from dataclasses import dataclass, field
from typing import get_args

from aresys_io.product_metadata import metadata_elements


def get_supported_metadata_elements() -> list[metadata_elements.MetaDataElementName]:
    """Retrieve the list of the supported channel elements.

    Returns
    -------
    list[metadata_elements.MetaDataElementName]
        list of element names.

    """
    return list(get_args(metadata_elements.MetaDataElementName))


@dataclass
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
        supported_elements = get_args(metadata_elements.MetaDataElementName)

        if element_name not in supported_elements:
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

    def get_sampling_constants(self) -> metadata_elements.SamplingConstants:
        """SamplingConstants getter method.

        Returns
        -------
        metadata_elements.SamplingConstants
            SamplingConstants MetaDataElement instance.

        """
        sampling_constants = self.get_element("SamplingConstants")
        assert isinstance(sampling_constants, metadata_elements.SamplingConstants)
        return sampling_constants

    def get_pulse(self) -> metadata_elements.Pulse:
        """Pulse getter method.

        Returns
        -------
        metadata_elements.Pulse
            Pulse MetaDataElement instance.

        """
        pulse = self.get_element("Pulse")
        assert isinstance(pulse, metadata_elements.Pulse)
        return pulse

    def get_raster_info(self) -> metadata_elements.RasterInfo:
        """RasterInfo getter method.

        Returns
        -------
        metadata_elements.RasterInfo
            RasterInfo MetaDataElement instance.

        """
        raster_info = self.get_element("RasterInfo")
        assert isinstance(raster_info, metadata_elements.RasterInfo)
        return raster_info

    def get_dataset_info(self) -> metadata_elements.DataSetInfo:
        """DataSetInfo getter method.

        Returns
        -------
        metadata_elements.DataSetInfo
            DataSetInfo MetaDataElement instance.

        """
        data_set_info = self.get_element("DataSetInfo")
        assert isinstance(data_set_info, metadata_elements.DataSetInfo)
        return data_set_info

    def get_state_vectors(self) -> metadata_elements.StateVectors:
        """StateVectors getter method.

        Returns
        -------
        metadata_elements.StateVectors
            StateVectors MetaDataElement instance.

        """
        state_vectors = self.get_element("StateVectors")
        assert isinstance(state_vectors, metadata_elements.StateVectors)
        return state_vectors

    def get_attitude_info(self) -> metadata_elements.AttitudeInfo:
        """AttitudeInfo getter method.

        Returns
        -------
        metadata_elements.AttitudeInfo
            AttitudeInfo MetaDataElement instance.

        """
        attitude_info = self.get_element("AttitudeInfo")
        assert isinstance(attitude_info, metadata_elements.AttitudeInfo)
        return attitude_info

    def get_acquisition_time_line(self) -> metadata_elements.AcquisitionTimeLine:
        """AcquisitionTimeLine getter method.

        Returns
        -------
        metadata_elements.AcquisitionTimeLine
            AcquisitionTimeLine MetaDataElement instance.

        """
        acquisition_time_line = self.get_element("AcquisitionTimeLine")
        assert isinstance(acquisition_time_line, metadata_elements.AcquisitionTimeLine)
        return acquisition_time_line

    def get_ground_corner_points(self) -> metadata_elements.GroundCornerPoints:
        """GroundCornerPoints getter method.

        Returns
        -------
        metadata_elements.GroundCornerPoints
            GroundCornerPoints MetaDataElement instance.

        """
        ground_corner_points = self.get_element("GroundCornerPoints")
        assert isinstance(ground_corner_points, metadata_elements.GroundCornerPoints)
        return ground_corner_points

    def get_burst_info(self) -> metadata_elements.BurstInfo:
        """BurstInfo getter method.

        Returns
        -------
        metadata_elements.BurstInfo
            BurstInfo MetaDataElement instance.

        """
        burst_info = self.get_element("BurstInfo")
        assert isinstance(burst_info, metadata_elements.BurstInfo)
        return burst_info

    def get_doppler_centroid(self) -> metadata_elements.DopplerCentroidVector:
        """DopplerCentroidVector getter method.

        Returns
        -------
        metadata_elements.DopplerCentroidVector
            DopplerCentroidVector MetaDataElement instance.

        """
        doppler_centroid = self.get_element("DopplerCentroidVector")
        assert isinstance(doppler_centroid, metadata_elements.DopplerCentroidVector)
        return doppler_centroid

    def get_doppler_rate(self) -> metadata_elements.DopplerRateVector:
        """DopplerRateVector getter method.

        Returns
        -------
        metadata_elements.DopplerRateVector
            DopplerRateVector MetaDataElement instance.

        """
        doppler_rate = self.get_element("DopplerRateVector")
        assert isinstance(doppler_rate, metadata_elements.DopplerRateVector)
        return doppler_rate

    def get_tops_azimuth_modulation_rate(
        self,
    ) -> metadata_elements.TopsAzimuthModulationRateVector:
        """TopsAzimuthModulationRateVector getter method.

        Returns
        -------
        metadata_elements.TopsAzimuthModulationRateVector
            TopsAzimuthModulationRateVector MetaDataElement instance.

        """
        tops_azimuth_modulation_rate = self.get_element("TopsAzimuthModulationRateVector")
        assert isinstance(
            tops_azimuth_modulation_rate,
            metadata_elements.TopsAzimuthModulationRateVector,
        )
        return tops_azimuth_modulation_rate

    def get_slant_to_ground(self) -> metadata_elements.SlantToGroundVector:
        """SlantToGroundVector getter method.

        Returns
        -------
        metadata_elements.SlantToGroundVector
            SlantToGroundVector MetaDataElement instance.

        """
        slant_to_ground = self.get_element("SlantToGroundVector")
        assert isinstance(slant_to_ground, metadata_elements.SlantToGroundVector)
        return slant_to_ground

    def get_ground_to_slant(self) -> metadata_elements.GroundToSlantVector:
        """GroundToSlantVector getter method.

        Returns
        -------
        metadata_elements.GroundToSlantVector
            GroundToSlantVector MetaDataElement instance.

        """
        ground_to_slant = self.get_element("GroundToSlantVector")
        assert isinstance(ground_to_slant, metadata_elements.GroundToSlantVector)
        return ground_to_slant

    def get_slant_to_incidence(self) -> metadata_elements.SlantToIncidenceVector:
        """SlantToIncidenceVector getter method.

        Returns
        -------
        metadata_elements.SlantToIncidenceVector
            SlantToIncidenceVector MetaDataElement instance.

        """
        slant_to_incidence = self.get_element("SlantToIncidenceVector")
        assert isinstance(slant_to_incidence, metadata_elements.SlantToIncidenceVector)
        return slant_to_incidence

    def get_slant_to_elevation(self) -> metadata_elements.SlantToElevationVector:
        """SlantToElevationVector getter method.

        Returns
        -------
        metadata_elements.SlantToElevationVector
            SlantToElevationVector MetaDataElement instance.

        """
        slant_to_elevation = self.get_element("SlantToElevationVector")
        assert isinstance(slant_to_elevation, metadata_elements.SlantToElevationVector)
        return slant_to_elevation

    def get_antenna_info(self) -> metadata_elements.AntennaInfo:
        """AntennaInfo getter method.

        Returns
        -------
        metadata_elements.AntennaInfo
            AntennaInfo MetaDataElement instance.

        """
        antenna_info = self.get_element("AntennaInfo")
        assert isinstance(antenna_info, metadata_elements.AntennaInfo)
        return antenna_info

    def get_data_statistics(self) -> metadata_elements.DataStatistics:
        """DataStatistics getter method.

        Returns
        -------
        metadata_elements.DataStatistics
            DataStatistics MetaDataElement instance.

        """
        data_statistics = self.get_element("DataStatistics")
        assert isinstance(data_statistics, metadata_elements.DataStatistics)
        return data_statistics

    def get_swath_info(self) -> metadata_elements.SwathInfo:
        """SwathInfo getter method.

        Returns
        -------
        metadata_elements.SwathInfo
            SwathInfo MetaDataElement instance.

        """
        swath_info = self.get_element("SwathInfo")
        assert isinstance(swath_info, metadata_elements.SwathInfo)
        return swath_info

    def get_coreg_poly(self) -> metadata_elements.CoregPolyVector:
        """CoregPolyVector getter method.

        Returns
        -------
        metadata_elements.CoregPolyVector
            CoregPolyVector MetaDataElement instance.

        """
        coreg_poly = self.get_element("CoregPolyVector")
        assert isinstance(coreg_poly, metadata_elements.CoregPolyVector)
        return coreg_poly


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


@dataclass
class MetaData:
    """Metadata."""

    channels: list[MetaDataChannel] = field(default_factory=list)
    description: str = ""

    def insert_element(
        self,
        element: metadata_elements.MetaDataPydanticModel,
        channel_index: int = 0,
    ) -> None:
        """Insert a new metadata element into the selected metadata channel.

        Parameters
        ----------
        element : metadata_elements.MetaDataPydanticModel
            metadata element to be inserted
        channel_index : int, optional
            metadata channel number where to insert, by default 0.

        """
        self.channels[channel_index].insert_element(element)

    def remove_element(
        self,
        element_type: metadata_elements.MetaDataElementName,
        channel_index: int = 0,
    ) -> None:
        """Remove the specified metadata element from the selected metadata channel.

        Parameters
        ----------
        element_type : metadata_elements.MetaDataElementName
            metadata element name to be removed
        channel_index : int, optional
            metadata channel number where to remove, by default 0.

        """
        self.channels[channel_index].remove_element(element_type)

    def get_sampling_constants(
        self,
        channel_index: int = 0,
    ) -> metadata_elements.SamplingConstants:
        """SamplingConstants getter method.

        Parameters
        ----------
        channel_index : int, optional
            index of the metadata channel, by default 0.

        Returns
        -------
        metadata_elements.SamplingConstants
            SamplingConstants MetaDataElement instance

        """
        return self.channels[channel_index].get_sampling_constants()

    def get_pulse(self, channel_index: int = 0) -> metadata_elements.Pulse:
        """Pulse getter method.

        Parameters
        ----------
        channel_index : int, optional
            index of the metadata channel, by default 0.

        Returns
        -------
        metadata_elements.Pulse
            Pulse MetaDataElement instance

        """
        return self.channels[channel_index].get_pulse()

    def get_raster_info(self, channel_index: int = 0) -> metadata_elements.RasterInfo:
        """RasterInfo getter method.

        Parameters
        ----------
        channel_index : int, optional
            index of the metadata channel, by default 0.

        Returns
        -------
        metadata_elements.RasterInfo
            RasterInfo MetaDataElement instance

        """
        return self.channels[channel_index].get_raster_info()

    def get_dataset_info(self, channel_index: int = 0) -> metadata_elements.DataSetInfo:
        """DataSetInfo getter method.

        Parameters
        ----------
        channel_index : int, optional
            index of the metadata channel, by default 0.

        Returns
        -------
        metadata_elements.DataSetInfo
            DataSetInfo MetaDataElement instance

        """
        return self.channels[channel_index].get_dataset_info()

    def get_state_vectors(self, channel_index: int = 0) -> metadata_elements.StateVectors:
        """StateVectors getter method.

        Parameters
        ----------
        channel_index : int, optional
            index of the metadata channel, by default 0.

        Returns
        -------
        metadata_elements.StateVectors
            StateVectors MetaDataElement instance

        """
        return self.channels[channel_index].get_state_vectors()

    def get_attitude_info(self, channel_index: int = 0) -> metadata_elements.AttitudeInfo:
        """AttitudeInfo getter method.

        Parameters
        ----------
        channel_index : int, optional
            index of the metadata channel, by default 0.

        Returns
        -------
        metadata_elements.AttitudeInfo
            AttitudeInfo MetaDataElement instance

        """
        return self.channels[channel_index].get_attitude_info()

    def get_acquisition_time_line(
        self,
        channel_index: int = 0,
    ) -> metadata_elements.AcquisitionTimeLine:
        """AcquisitionTimeLine getter method.

        Parameters
        ----------
        channel_index : int, optional
            index of the metadata channel, by default 0.

        Returns
        -------
        metadata_elements.AcquisitionTimeLine
            AcquisitionTimeLine MetaDataElement instance

        """
        return self.channels[channel_index].get_acquisition_time_line()

    def get_ground_corner_points(
        self,
        channel_index: int = 0,
    ) -> metadata_elements.GroundCornerPoints:
        """GroundCornerPoints getter method.

        Parameters
        ----------
        channel_index : int, optional
            index of the metadata channel, by default 0.

        Returns
        -------
        metadata_elements.GroundCornerPoints
            GroundCornerPoints MetaDataElement instance

        """
        return self.channels[channel_index].get_ground_corner_points()

    def get_burst_info(self, channel_index: int = 0) -> metadata_elements.BurstInfo:
        """BurstInfo getter method.

        Parameters
        ----------
        channel_index : int, optional
            index of the metadata channel, by default 0.

        Returns
        -------
        metadata_elements.BurstInfo
            BurstInfo MetaDataElement instance

        """
        return self.channels[channel_index].get_burst_info()

    def get_doppler_centroid(
        self,
        channel_index: int = 0,
    ) -> metadata_elements.DopplerCentroidVector:
        """DopplerCentroidVector getter method.

        Parameters
        ----------
        channel_index : int, optional
            index of the metadata channel, by default 0.

        Returns
        -------
        metadata_elements.DopplerCentroidVector
            DopplerCentroidVector MetaDataElement instance

        """
        return self.channels[channel_index].get_doppler_centroid()

    def get_doppler_rate(self, channel_index: int = 0) -> metadata_elements.DopplerRateVector:
        """DopplerRateVector getter method.

        Parameters
        ----------
        channel_index : int, optional
            index of the metadata channel, by default 0.

        Returns
        -------
        metadata_elements.DopplerRateVector
            DopplerRateVector MetaDataElement instance

        """
        return self.channels[channel_index].get_doppler_rate()

    def get_tops_azimuth_modulation_rate(
        self,
        channel_index: int = 0,
    ) -> metadata_elements.TopsAzimuthModulationRateVector:
        """TopsAzimuthModulationRateVector getter method.

        Parameters
        ----------
        channel_index : int, optional
            index of the metadata channel, by default 0.

        Returns
        -------
        metadata_elements.TopsAzimuthModulationRateVector
            TopsAzimuthModulationRateVector MetaDataElement instance

        """
        return self.channels[channel_index].get_tops_azimuth_modulation_rate()

    def get_slant_to_ground(self, channel_index: int = 0) -> metadata_elements.SlantToGroundVector:
        """SlantToGroundVector getter method.

        Parameters
        ----------
        channel_index : int, optional
            index of the metadata channel, by default 0.

        Returns
        -------
        metadata_elements.SlantToGroundVector
            SlantToGroundVector MetaDataElement instance

        """
        return self.channels[channel_index].get_slant_to_ground()

    def get_ground_to_slant(self, channel_index: int = 0) -> metadata_elements.GroundToSlantVector:
        """GroundToSlantVector getter method.

        Parameters
        ----------
        channel_index : int, optional
            index of the metadata channel, by default 0.

        Returns
        -------
        metadata_elements.GroundToSlantVector
            GroundToSlantVector MetaDataElement instance

        """
        return self.channels[channel_index].get_ground_to_slant()

    def get_slant_to_incidence(
        self,
        channel_index: int = 0,
    ) -> metadata_elements.SlantToIncidenceVector:
        """SlantToIncidenceVector getter method.

        Parameters
        ----------
        channel_index : int, optional
            index of the metadata channel, by default 0.

        Returns
        -------
        metadata_elements.SlantToIncidenceVector
            SlantToIncidenceVector MetaDataElement instance

        """
        return self.channels[channel_index].get_slant_to_incidence()

    def get_slant_to_elevation(
        self,
        channel_index: int = 0,
    ) -> metadata_elements.SlantToElevationVector:
        """SlantToElevationVector getter method.

        Parameters
        ----------
        channel_index : int, optional
            index of the metadata channel, by default 0.

        Returns
        -------
        metadata_elements.SlantToElevationVector
            SlantToElevationVector MetaDataElement instance

        """
        return self.channels[channel_index].get_slant_to_elevation()

    def get_antenna_info(self, channel_index: int = 0) -> metadata_elements.AntennaInfo:
        """AntennaInfo getter method.

        Parameters
        ----------
        channel_index : int, optional
            index of the metadata channel, by default 0.

        Returns
        -------
        metadata_elements.AntennaInfo
            AntennaInfo MetaDataElement instance

        """
        return self.channels[channel_index].get_antenna_info()

    def get_data_statistics(self, channel_index: int = 0) -> metadata_elements.DataStatistics:
        """DataStatistics getter method.

        Parameters
        ----------
        channel_index : int, optional
            index of the metadata channel, by default 0.

        Returns
        -------
        metadata_elements.DataStatistics
            DataStatistics MetaDataElement instance

        """
        return self.channels[channel_index].get_data_statistics()

    def get_swath_info(self, channel_index: int = 0) -> metadata_elements.SwathInfo:
        """SwathInfo getter method.

        Parameters
        ----------
        channel_index : int, optional
            index of the metadata channel, by default 0.

        Returns
        -------
        metadata_elements.SwathInfo
            SwathInfo MetaDataElement instance

        """
        return self.channels[channel_index].get_swath_info()

    def get_coreg_poly(self, channel_index: int = 0) -> metadata_elements.CoregPolyVector:
        """CoregPolyVector getter method.

        Parameters
        ----------
        channel_index : int, optional
            index of the metadata channel, by default 0.

        Returns
        -------
        metadata_elements.CoregPolyVector
            CoregPolyVector MetaDataElement instance

        """
        return self.channels[channel_index].get_coreg_poly()
