# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Unit tests for metadata accessors."""

from aresys_io.product import MetaDataElementName
from aresys_io.product.metadata.io import parse_metadata

METADATA = """<?xml version="1.0" encoding="utf-8"?>
<AresysXmlDoc>
    <NumberOfChannels>1</NumberOfChannels>
    <VersionNumber>2.1</VersionNumber>
    <Description/>
    <Channel Number="1" Total="1">
        <RasterInfo>
            <FileName>GRD_0001</FileName>
            <Lines>8951</Lines>
            <Samples>2215</Samples>
            <HeaderOffsetBytes>150</HeaderOffsetBytes>
            <RowPrefixBytes>20</RowPrefixBytes>
            <ByteOrder>LITTLEENDIAN</ByteOrder>
            <CellType>FLOAT32</CellType>
            <LinesStep unit="s">0.00325489654798287</LinesStep>
            <SamplesStep unit="m">25.0</SamplesStep>
            <LinesStart unit="Utc">11-JAN-2017 05:06:05.420354672133</LinesStart>
            <SamplesStart unit="m">0.0</SamplesStart>
        </RasterInfo>
        <DataSetInfo>
            <SensorName>BIOMASS</SensorName>
            <Description>NOT_AVAILABLE - AZIMUTH FOCUSED RANGE COMPENSATED</Description>
            <SenseDate>NOT_AVAILABLE</SenseDate>
            <AcquisitionMode>STRIPMAP</AcquisitionMode>
            <ImageType>MULTILOOK</ImageType>
            <Projection>GROUND RANGE</Projection>
            <AcquisitionStation>NOT_AVAILABLE</AcquisitionStation>
            <ProcessingCenter>NOT_AVAILABLE</ProcessingCenter>
            <ProcessingDate>10-FEB-2023 18:59:39.063638000000</ProcessingDate>
            <ProcessingSoftware>GSS</ProcessingSoftware>
            <fc_hz>435000000.0</fc_hz>
            <SideLooking>LEFT</SideLooking>
        </DataSetInfo>
        <SwathInfo>
            <Swath>S2</Swath>
            <SwathAcquisitionOrder>9</SwathAcquisitionOrder>
            <Polarization>H/H</Polarization>
            <Rank>8</Rank>
            <RangeDelayBias unit="s">0.05</RangeDelayBias>
            <AcquisitionStartTime unit="Utc">11-JAN-2017 05:06:05.420354672133</AcquisitionStartTime>
            <AzimuthSteeringRateReferenceTime unit="s">-2.3</AzimuthSteeringRateReferenceTime>
            <AzimuthSteeringRatePol>
                <val N="1">45.0</val>
                <val N="2">42.0</val>
                <val N="3">43.0</val>
            </AzimuthSteeringRatePol>
            <AcquisitionPRF>20.0</AcquisitionPRF>
            <EchoesPerBurst>30</EchoesPerBurst>
        </SwathInfo>
        <SamplingConstants>
            <frg_hz unit="Hz">10.0</frg_hz>
            <Brg_hz unit="Hz">20.0</Brg_hz>
            <faz_hz unit="Hz">30.0</faz_hz>
            <Baz_hz unit="Hz">40.0</Baz_hz>
        </SamplingConstants>
        <DataStatistics>
            <NumSamples>19826458</NumSamples>
            <MaxI>2676823552.0</MaxI>
            <MinI>83823.4921875</MinI>
            <MaxQ>0.0</MaxQ>
            <MinQ>0.0</MinQ>
            <SumI>89122400845249.0</SumI>
            <SumQ>0.0</SumQ>
            <Sum2I>7.00840507541525E20</Sum2I>
            <Sum2Q>0.0</Sum2Q>
            <StdDevI>3891349.90059871</StdDevI>
            <StdDevQ>0.0</StdDevQ>
        </DataStatistics>
        <StateVectorData>
            <OrbitNumber>NOT_AVAILABLE</OrbitNumber>
            <Track>7</Track>
            <OrbitDirection>ASCENDING</OrbitDirection>
            <pSV_m>
                <val N="1">5317607.32991368</val>
                <val N="2">610604.181576807</val>
                <val N="3">4577936.42495716</val>
                <val N="4">5313024.92248479</val>
                <val N="5">608285.759542598</val>
                <val N="6">4583546.68380492</val>
            </pSV_m>
            <vSV_mOs>
                <val N="1">-4579.23071779759</val>
                <val N="2">-2318.41093794023</val>
                <val N="3">5612.88065438087</val>
                <val N="4">-4585.59543140451</val>
                <val N="5">-2318.43362350978</val>
                <val N="6">5607.64864044348</val>
            </vSV_mOs>
            <t_ref_Utc>11-JAN-2017 05:05:55.374776000000</t_ref_Utc>
            <dtSV_s unit="s">0.99999999962462</dtSV_s>
            <nSV_n>2</nSV_n>
        </StateVectorData>
        <SlantToGround Number="1" Total="1">
            <pol>
                <val N="1" unit="m">0.0279764859084441</val>
                <val N="2" unit="m/s">332392355.238117</val>
                <val N="3" unit="m/s">0.0</val>
                <val N="4" unit="m/s2">0.0</val>
                <val N="5" unit="m/s2">-147100378880.014</val>
                <val N="6" unit="m/s3">148771445722789.0</val>
                <val N="7" unit="m/s4">-1.18791374851972E17</val>
            </pol>
            <trg0_s unit="s">0.00498119194829745</trg0_s>
            <taz0_Utc unit="Utc">11-JAN-2017 05:06:19.987644172630</taz0_Utc>
        </SlantToGround>
        <GroundToSlant Number="1" Total="1">
            <pol>
                <val N="1" unit="s">0.00498119195039857</val>
                <val N="2" unit="s/m">3.00835380687427E-09</val>
                <val N="3" unit="s/m">0.0</val>
                <val N="4" unit="s/m2">0.0</val>
                <val N="5" unit="s/m2">4.02534653514271E-15</val>
                <val N="6" unit="s/m3">-2.45577629676765E-21</val>
                <val N="7" unit="s/m4">1.03753668287902E-28</val>
            </pol>
            <trg0_s unit="s">0.0</trg0_s>
            <taz0_Utc unit="Utc">11-JAN-2017 05:06:05.420354672133</taz0_Utc>
        </GroundToSlant>
        <AttitudeInfo>
            <t_ref_Utc>11-JAN-2017 05:05:55.374776000000</t_ref_Utc>
            <dtYPR_s>0.99999999962462</dtYPR_s>
            <nYPR_n>3</nYPR_n>
            <yaw_deg>
                <val N="1">6.01545966886107E-06</val>
                <val N="2">1.72217492445588E-05</val>
                <val N="3">2.15186524627847E-05</val>
            </yaw_deg>
            <pitch_deg>
                <val N="1">2.76923549635297E-06</val>
                <val N="2">7.98225683167924E-06</val>
                <val N="3">9.98095451338142E-06</val>
            </pitch_deg>
            <roll_deg>
                <val N="1">25.9269230465147</val>
                <val N="2">25.9265262380572</val>
                <val N="3">25.9261295216853</val>
            </roll_deg>
            <referenceFrame>ZERODOPPLER</referenceFrame>
            <rotationOrder>YPR</rotationOrder>
            <AttitudeType>NOMINAL</AttitudeType>
        </AttitudeInfo>
        <Pulse>
            <Direction>UP</Direction>
            <PulseLength unit="s">-1.0</PulseLength>
            <Bandwidth unit="Hz">-1.0</Bandwidth>
            <PulseEnergy unit="j">-1.0</PulseEnergy>
            <PulseSamplingRate unit="Hz">-1.0</PulseSamplingRate>
            <PulseStartFrequency unit="Hz">0.5</PulseStartFrequency>
            <PulseStartPhase unit="rad">0.785398163397448</PulseStartPhase>
        </Pulse>
    </Channel>
</AresysXmlDoc>
"""  # ruff: ignore[line-too-long]

ACCESSOR_NAMES = (
    "raster_info",
    "dataset_info",
    "swath_info",
    "sampling_constants",
    "state_vectors",
    "attitude_info",
    "slant_to_ground",
    "ground_to_slant",
    "data_statistics",
    "pulse",
)

FIELD_NAMES: list[MetaDataElementName] = [
    "RasterInfo",
    "DataSetInfo",
    "SwathInfo",
    "SamplingConstants",
    "StateVectors",
    "AttitudeInfo",
    "SlantToGroundVector",
    "GroundToSlantVector",
    "DataStatistics",
    "Pulse",
]
FIELD_NAMES_NOT: list[MetaDataElementName] = [
    "DopplerCentroidVector",
    "AntennaInfo",
    "CoregPolyVector",
]


def test_metadata_element_access_is_consistent() -> None:
    """Accessing an element directly matches accessing it through channel zero."""
    metadata = parse_metadata(METADATA)
    channel = metadata[0]

    for accessor_name in ACCESSOR_NAMES:
        assert getattr(metadata, accessor_name) is getattr(channel, accessor_name)


def test_metadata_element_in_channel() -> None:
    """Check if the element is available in the metadata channel."""
    metadata = parse_metadata(METADATA)
    channel = metadata[0]

    for name in FIELD_NAMES:
        assert name in channel

    for name in FIELD_NAMES_NOT:
        assert name not in channel


def test_metadata_element_in_metadata() -> None:
    """Check if the element is available in the metadata channel."""
    metadata = parse_metadata(METADATA)

    for name in FIELD_NAMES:
        assert name in metadata

    for name in FIELD_NAMES_NOT:
        assert name not in metadata
