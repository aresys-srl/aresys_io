# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Unit tests for metadata_io functionalities."""

from pathlib import Path

import pytest
from perseo_core.timing import PreciseDateTime

from aresys_io.product_metadata import metadata
from aresys_io.product_metadata.metadata_elements import RasterInfo
from aresys_io.product_metadata.metadata_io import (
    read_metadata,
    write_metadata,
)
from aresys_io.product_metadata.translate import translate_metadata_to_model

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
  </Channel>
</AresysXmlDoc>
"""


def assert_equal_metadata(
    metadata_a: metadata.MetaData,
    metadata_b: metadata.MetaData,
) -> None:
    model_a = translate_metadata_to_model(metadata_a)
    model_b = translate_metadata_to_model(metadata_b)
    assert model_a == model_b


@pytest.fixture
def metadata_obj() -> metadata.MetaData:
    metadata_object = metadata.MetaData(description="")

    channel = metadata.MetaDataChannel()
    channel.number = 1
    channel.total = 1

    raster_info = RasterInfo(
        lines=8951,
        samples=2215,
        cell_type="FLOAT32",
        file_name="GRD_0001",
        header_offset_bytes=150,
        row_prefix_bytes=20,
        byte_order="LITTLEENDIAN",
        invalid_value=None,
        format_type=None,
    )
    raster_info.lines_start = PreciseDateTime.from_utc_string(
        "11-JAN-2017 05:06:05.420354672133",
    )
    raster_info.lines_start_unit = "Utc"
    raster_info.lines_step = 0.00325489654798287
    raster_info.lines_step_unit = "s"
    raster_info.samples_start = 0.0
    raster_info.samples_start_unit = "m"
    raster_info.samples_step = 25.0
    raster_info.samples_step_unit = "m"
    channel.insert_element(raster_info)

    metadata_object.channels.append(channel)
    return metadata_object


def test_read(tmp_path: Path, metadata_obj: metadata.MetaData) -> None:
    metadata_file = tmp_path / "metadata.xml"
    metadata_file.write_text(METADATA, encoding="utf-8")
    assert_equal_metadata(read_metadata(metadata_file), metadata_obj)


def test_write(tmp_path: Path, metadata_obj: metadata.MetaData) -> None:
    metadata_file = tmp_path / "metadata.xml"
    write_metadata(metadata_obj, metadata_file)
    assert metadata_file.read_text(encoding="utf-8") == METADATA


def test_create() -> None:
    """Testing create_new_metadata."""
    meta = metadata.create_new_metadata(10, "test")
    assert meta.description == "test"
    assert len(meta.channels) == 10
    assert meta.description == "test"

    assert len(meta.channels) == 10
