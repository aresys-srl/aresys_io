# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

from dataclasses import dataclass
from pathlib import Path
from tempfile import TemporaryDirectory
from types import GeneratorType

import pytest

from aresys_io.product import channel_iteration, create_product_folder
from aresys_io.product_metadata import MetaData, SwathPolarization

swaths = ["S1", "S2", "S3"]
pols = ["H/H", "V/V", "V/H", "H/V"]

_xml = """
<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<AresysXmlDoc xmlns:at="aresysTypes">
  <NumberOfChannels>1</NumberOfChannels>
  <VersionNumber>2.1</VersionNumber>
  <Description/>
  <Channel Number="1" Total="1">
    <RasterInfo>
      <FileName>iSLC_0001</FileName>
      <Lines>42878</Lines>
      <Samples>1210</Samples>
      <HeaderOffsetBytes>0</HeaderOffsetBytes>
      <RowPrefixBytes>0</RowPrefixBytes>
      <ByteOrder>LITTLEENDIAN</ByteOrder>
      <CellType>FLOAT_COMPLEX</CellType>
      <LinesStep unit="s">0.000679478160138531</LinesStep>
      <SamplesStep unit="s">1.32183907894041e-07</SamplesStep>
      <LinesStart unit="Utc">01-JAN-2017 06:03:05.415896855135</LinesStart>
      <SamplesStart unit="s">0.004821408040426434886</SamplesStart>
    </RasterInfo>
    <SwathInfo>
      <Swath>XXXX</Swath>
      <SwathAcquisitionOrder>0</SwathAcquisitionOrder>
      <Polarization>YYYY</Polarization>
      <Rank>7</Rank>
      <RangeDelayBias>0</RangeDelayBias>
      <AcquisitionStartTime>01-JAN-2017 06:03:05.418499000000</AcquisitionStartTime>
      <AzimuthSteeringRateReferenceTime unit="s">0</AzimuthSteeringRateReferenceTime>
      <AzimuthSteeringRatePol>
        <val N="1">0</val>
        <val N="2">0</val>
        <val N="3">0</val>
      </AzimuthSteeringRatePol>
      <AcquisitionPRF>1471.71764843203</AcquisitionPRF>
      <EchoesPerBurst>42878</EchoesPerBurst>
      <RxGain>1</RxGain>
    </SwathInfo>
  </Channel>
</AresysXmlDoc>
"""


def convert_pol(pol: str) -> SwathPolarization:
    """Convert polarization string to the format used in the metadata."""
    mapping: dict[str, SwathPolarization] = {
        "H/H": "HH",
        "V/V": "VV",
        "V/H": "VH",
        "H/V": "HV",
        "X/X": "XX",
    }
    swath_pol = mapping.get(pol)
    if swath_pol is None:
        msg = f"Invalid polarization: {pol}"
        raise ValueError(msg)
    return swath_pol


@dataclass(frozen=True)
class ChannelTestData:
    """Container for reusable channel iteration test data."""

    pol_xml: list[str]
    filter_pol: channel_iteration.SwathIDFilter
    filter_swt: channel_iteration.SwathIDFilter
    filter_both: channel_iteration.SwathIDFilter


@pytest.fixture
def channel_test_data() -> ChannelTestData:
    """Common test data for channel iteration tests."""
    pol_xml = [
        _xml.replace("<Polarization>YYYY</Polarization>", f"<Polarization>{p}</Polarization>")
        for p in pols
    ]
    return ChannelTestData(
        pol_xml=pol_xml,
        filter_pol=channel_iteration.SwathIDFilter(polarization=convert_pol(pols[1])),
        filter_swt=channel_iteration.SwathIDFilter(swath=swaths[1]),
        filter_both=channel_iteration.SwathIDFilter(
            polarization=convert_pol(pols[1]),
            swath=swaths[1],
        ),
    )


def _create_product_with_channels(
    tmpdir: str,
    channel_xml_contents: list[str],
) -> channel_iteration.ProductFolder:
    """Create a product folder and populate channels with raster placeholders."""
    product_path = Path(tmpdir, "test_product")
    pf = create_product_folder(product_path)
    channel_paths = [
        product_path.joinpath(pf.pf_name + f"_000{c + 1}.xml")
        for c in range(len(channel_xml_contents))
    ]
    for item, content in zip(channel_paths, channel_xml_contents, strict=False):
        item.write_text(content)
        item.with_suffix("").write_bytes(b"")
    return pf


def test_iter_channels_generator_no_filter(channel_test_data: ChannelTestData) -> None:
    """Testing iter_channels_generator function, no filter."""
    with TemporaryDirectory() as tmpdir:
        pf = _create_product_with_channels(tmpdir, channel_test_data.pol_xml)
        out = channel_iteration.iter_channels_generator(product=pf)

        assert isinstance(out, GeneratorType)
        for idx, item in enumerate(out):
            assert isinstance(item, tuple)
            assert isinstance(item[0], int)
            assert isinstance(item[1], MetaData)
            assert item[1].swath_info.polarization == pols[idx].replace("/", "")


def test_iter_channels_generator_filter(channel_test_data: ChannelTestData) -> None:
    """Testing iter_channels_generator function, with filter."""
    with TemporaryDirectory() as tmpdir:
        pf = _create_product_with_channels(tmpdir, channel_test_data.pol_xml)
        out = channel_iteration.iter_channels_generator(
            product=pf,
            filter_func=channel_test_data.filter_pol,
        )

        assert isinstance(out, GeneratorType)
        for item in out:
            assert isinstance(item, tuple)
            assert isinstance(item[0], int)
            assert isinstance(item[1], MetaData)
            assert item[1].swath_info.polarization == pols[1].replace("/", "")


def test_iter_channels_generator_filter_1(channel_test_data: ChannelTestData) -> None:
    """Testing iter_channels_generator function, with filter."""
    with TemporaryDirectory() as tmpdir:
        pf = _create_product_with_channels(tmpdir, channel_test_data.pol_xml)
        out = channel_iteration.iter_channels_generator(
            product=pf,
            filter_func=channel_test_data.filter_pol,
        )

        assert isinstance(out, GeneratorType)
        for item in out:
            assert isinstance(item, tuple)
            assert isinstance(item[0], int)
            assert isinstance(item[1], MetaData)
            assert item[1].swath_info.polarization == pols[1].replace("/", "")


def test_iter_channels_generator_filter_2(channel_test_data: ChannelTestData) -> None:
    """Testing iter_channels_generator function, with filter."""
    with TemporaryDirectory() as tmpdir:
        swath_xml = [
            content.replace("<Swath>XXXX</Swath>", f"<Swath>{swaths[1]}</Swath>")
            for content in channel_test_data.pol_xml
        ]
        pf = _create_product_with_channels(tmpdir, swath_xml)
        out = channel_iteration.iter_channels_generator(
            product=pf,
            filter_func=channel_test_data.filter_swt,
        )

        assert isinstance(out, GeneratorType)
        for item in out:
            assert isinstance(item, tuple)
            assert isinstance(item[0], int)
            assert isinstance(item[1], MetaData)
            assert item[1].swath_info.swath == swaths[1]


def test_iter_channels_generator_filter_3(channel_test_data: ChannelTestData) -> None:
    """Testing iter_channels_generator function, with filter."""
    with TemporaryDirectory() as tmpdir:
        swath_xml = [
            content.replace("<Swath>XXXX</Swath>", f"<Swath>{swaths[1]}</Swath>")
            for content in channel_test_data.pol_xml
        ]
        pf = _create_product_with_channels(tmpdir, swath_xml)
        out = channel_iteration.iter_channels_generator(
            product=pf,
            filter_func=channel_test_data.filter_both,
        )

        assert isinstance(out, GeneratorType)
        for item in out:
            assert isinstance(item, tuple)
            assert isinstance(item[0], int)
            assert isinstance(item[1], MetaData)
            assert item[1].swath_info.polarization == pols[1].replace("/", "")
            assert item[1].swath_info.swath == swaths[1]


def test_iter_channels_generator_filter_4(channel_test_data: ChannelTestData) -> None:
    """Testing iter_channels_generator function, with filter."""
    with TemporaryDirectory() as tmpdir:
        swath_xml = [
            content.replace("<Swath>XXXX</Swath>", f"<Swath>{swaths[1]}</Swath>")
            for content in channel_test_data.pol_xml
        ]
        pf = _create_product_with_channels(tmpdir, swath_xml)
        out = channel_iteration.iter_channels_generator(
            product=pf,
            filter_func=channel_iteration.SwathIDFilter(
                polarization=[convert_pol(pol) for pol in pols[:2]],
            ),
        )

        assert isinstance(out, GeneratorType)
        count = 0
        for idx, item in enumerate(out):
            assert isinstance(item, tuple)
            assert isinstance(item[0], int)
            assert isinstance(item[1], MetaData)
            assert item[1].swath_info.polarization == pols[idx].replace("/", "")
            count += 1
        assert count == 2


def test_iter_channels_generator_filter_5(channel_test_data: ChannelTestData) -> None:
    """Testing iter_channels_generator function, with filter."""
    with TemporaryDirectory() as tmpdir:
        swath_xml = [
            content.replace("<Swath>XXXX</Swath>", f"<Swath>{swaths[1]}</Swath>")
            for content in channel_test_data.pol_xml
        ]
        pf = _create_product_with_channels(tmpdir, swath_xml)
        out = channel_iteration.iter_channels_generator(
            product=pf,
            filter_func=channel_iteration.SwathIDFilter(
                polarization=[convert_pol(pol) for pol in pols[:2]],
                swath=swaths[1],
            ),
        )

        assert isinstance(out, GeneratorType)
        count = 0
        for idx, item in enumerate(out):
            assert isinstance(item, tuple)
            assert isinstance(item[0], int)
            assert isinstance(item[1], MetaData)
            assert item[1].swath_info.polarization == pols[idx].replace("/", "")
            assert item[1].swath_info.swath == swaths[1]
            count += 1
        assert count == 2


def test_iter_channels_filter_1(channel_test_data: ChannelTestData) -> None:
    """Testing iter_channels function, with filter."""
    with TemporaryDirectory() as tmpdir:
        pf = _create_product_with_channels(tmpdir, channel_test_data.pol_xml)
        out = channel_iteration.iter_channels(product=pf, polarization=convert_pol(pols[2]))

        assert isinstance(out, GeneratorType)
        count = 0
        for item in out:
            assert isinstance(item, tuple)
            assert isinstance(item[0], int)
            assert isinstance(item[1], MetaData)
            assert item[1].swath_info.polarization == pols[2].replace("/", "")
            count += 1
        assert count == 1


def test_iter_channels_filter_2(channel_test_data: ChannelTestData) -> None:
    """Testing iter_channels function, with filter."""
    with TemporaryDirectory() as tmpdir:
        swath_xml = [
            content.replace("<Swath>XXXX</Swath>", f"<Swath>{swaths[2]}</Swath>")
            for content in channel_test_data.pol_xml
        ]
        pf = _create_product_with_channels(tmpdir, swath_xml)
        out = channel_iteration.iter_channels(product=pf, swath=swaths[2])

        assert isinstance(out, GeneratorType)
        for item in out:
            assert isinstance(item, tuple)
            assert isinstance(item[0], int)
            assert isinstance(item[1], MetaData)
            assert item[1].swath_info.swath == swaths[2]


def test_iter_channels_filter_3(channel_test_data: ChannelTestData) -> None:
    """Testing iter_channels function, with filter."""
    with TemporaryDirectory() as tmpdir:
        swath_xml = [
            content.replace("<Swath>XXXX</Swath>", f"<Swath>{swaths[2]}</Swath>")
            for content in channel_test_data.pol_xml
        ]
        pf = _create_product_with_channels(tmpdir, swath_xml)
        out = channel_iteration.iter_channels(
            product=pf,
            polarization=convert_pol(pols[3]),
            swath=swaths[2],
        )

        assert isinstance(out, GeneratorType)
        count = 0
        for item in out:
            assert isinstance(item, tuple)
            assert isinstance(item[0], int)
            assert isinstance(item[1], MetaData)
            assert item[1].swath_info.polarization == pols[3].replace("/", "")
            assert item[1].swath_info.swath == swaths[2]
            count += 1
        assert count == 1


def test_iter_channels_filter_4(channel_test_data: ChannelTestData) -> None:
    """Testing iter_channels function, with filter."""
    with TemporaryDirectory() as tmpdir:
        swath_xml = [
            content.replace("<Swath>XXXX</Swath>", f"<Swath>{swaths[2]}</Swath>")
            for content in channel_test_data.pol_xml
        ]
        pf = _create_product_with_channels(tmpdir, swath_xml)
        out = channel_iteration.iter_channels(
            product=pf,
            polarization=[convert_pol(pol) for pol in pols[:3]],
        )

        assert isinstance(out, GeneratorType)
        count = 0
        for idx, item in enumerate(out):
            assert isinstance(item, tuple)
            assert isinstance(item[0], int)
            assert isinstance(item[1], MetaData)
            assert item[1].swath_info.polarization == pols[idx].replace("/", "")
            count += 1
        assert count == 3


def test_iter_channels_filter_5(channel_test_data: ChannelTestData) -> None:
    """Testing iter_channels function, with filter."""
    with TemporaryDirectory() as tmpdir:
        swath_xml = [
            content.replace("<Swath>XXXX</Swath>", f"<Swath>{swaths[2]}</Swath>")
            for content in channel_test_data.pol_xml
        ]
        pf = _create_product_with_channels(tmpdir, swath_xml)
        out = channel_iteration.iter_channels(
            product=pf,
            polarization=[convert_pol(pol) for pol in pols[:2]],
            swath=swaths[2],
        )

        assert isinstance(out, GeneratorType)
        count = 0
        for idx, item in enumerate(out):
            assert isinstance(item, tuple)
            assert isinstance(item[0], int)
            assert isinstance(item[1], MetaData)
            assert item[1].swath_info.polarization == pols[idx].replace("/", "")
            assert item[1].swath_info.swath == swaths[2]
            count += 1
        assert count == 2
