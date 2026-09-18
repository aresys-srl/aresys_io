# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Unit tests for Product Folder layout functionalities."""

from pathlib import Path

import pytest

from aresys_io.product.pf.layout import ProductFolderLayout

PRODUCT_NAMES = ["TEST_SLC_01", "TEST.SLC_01"]
DEFAULT_MANIFEST_NAME = "aresys_product"
CHANNEL = 3
BASE_FOLDER = Path(r"C:\Users\user\data")


@pytest.fixture(params=PRODUCT_NAMES)
def case(request: pytest.FixtureRequest) -> tuple[Path, dict[str, Path]]:
    """Provide one product path and expected outputs for each naming variant."""
    product_name = request.param
    path = BASE_FOLDER / product_name
    expected = {
        "manifest": BASE_FOLDER / product_name / DEFAULT_MANIFEST_NAME,
        "config": BASE_FOLDER / product_name / f"{product_name}.config",
        "kmz": BASE_FOLDER / product_name / f"{product_name}.kmz",
        "channel_data_raw": BASE_FOLDER / product_name / f"{product_name}_{CHANNEL:04d}",
        "channel_data_tiff": BASE_FOLDER / product_name / f"{product_name}_{CHANNEL:04d}.tiff",
        "channel_metadata": BASE_FOLDER / product_name / f"{product_name}_{CHANNEL:04d}.xml",
        "channel_quicklook_png": BASE_FOLDER / product_name / f"{product_name}_{CHANNEL:04d}.png",
        "channel_quicklook_jpg": BASE_FOLDER / product_name / f"{product_name}_{CHANNEL:04d}.jpg",
    }
    return path, expected


def test_product_folder_layout_init_defaults(case: tuple[Path, dict[str, Path]]) -> None:
    """Testing object initialization with defaults."""
    path, _ = case
    layout = ProductFolderLayout(path)

    assert isinstance(layout, ProductFolderLayout)
    assert layout._pf_path == path
    assert layout._product_name == path.name


def test_product_folder_layout_generate_manifest(case: tuple[Path, dict[str, Path]]) -> None:
    """Testing generate manifest method."""
    path, expected = case
    assert ProductFolderLayout.generate_manifest_path(path) == expected["manifest"]


def test_product_folder_layout_get_config(case: tuple[Path, dict[str, Path]]) -> None:
    """Testing get config method."""
    path, expected = case
    layout = ProductFolderLayout(path)
    assert layout.get_config_path() == expected["config"]


def test_product_folder_layout_get_kmz(case: tuple[Path, dict[str, Path]]) -> None:
    """Testing get kmz method."""
    path, expected = case
    layout = ProductFolderLayout(path)
    assert layout.get_overlay_path() == expected["kmz"]


def test_product_folder_layout_get_channel_metadata(case: tuple[Path, dict[str, Path]]) -> None:
    """Testing get channel metadata method."""
    path, expected = case
    layout = ProductFolderLayout(path)
    assert layout.get_channel_metadata_path(CHANNEL) == expected["channel_metadata"]


def test_product_folder_layout_get_channel_data_raw(case: tuple[Path, dict[str, Path]]) -> None:
    """Testing get channel data method."""
    path, expected = case
    layout = ProductFolderLayout(path)
    assert layout.get_channel_data_path(CHANNEL, extension="") == expected["channel_data_raw"]


def test_product_folder_layout_get_channel_data_tiff(case: tuple[Path, dict[str, Path]]) -> None:
    """Testing get channel data method."""
    path, expected = case
    layout = ProductFolderLayout(path)
    assert (
        layout.get_channel_data_path(CHANNEL, extension=".tiff") == expected["channel_data_tiff"]
    )


def test_product_folder_layout_get_channel_quicklook_png(
    case: tuple[Path, dict[str, Path]],
) -> None:
    """Testing get channel quicklook method, png format."""
    path, expected = case
    layout = ProductFolderLayout(path)
    assert (
        layout.get_channel_quicklook_path(CHANNEL, extension=".png")
        == expected["channel_quicklook_png"]
    )


def test_product_folder_layout_get_channel_quicklook_jpg(
    case: tuple[Path, dict[str, Path]],
) -> None:
    """Testing get channel quicklook method, jpg format."""
    path, expected = case
    layout = ProductFolderLayout(path)
    assert (
        layout.get_channel_quicklook_path(CHANNEL, extension=".jpg")
        == expected["channel_quicklook_jpg"]
    )


def test_raising_channel_number_error_negative(case: tuple[Path, dict[str, Path]]) -> None:
    """Testing error raising for negative channel numbers."""
    path, _ = case
    layout = ProductFolderLayout(path)
    with pytest.raises(RuntimeError):
        layout.get_channel_quicklook_path(-56, extension=".jpg")


def test_raising_channel_number_error_above_limit(case: tuple[Path, dict[str, Path]]) -> None:
    """Testing error raising for channel number above max limit."""
    path, _ = case
    layout = ProductFolderLayout(path)
    with pytest.raises(RuntimeError):
        layout.get_channel_quicklook_path(10000, extension=".jpg")
