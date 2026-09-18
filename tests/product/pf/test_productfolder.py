# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Unit tests for Product Folder main functionalities."""

from pathlib import Path
from typing import get_args

import pytest

from aresys_io.product.pf.layout import (
    MANIFEST_NAME,
    METADATA_EXTENSION,
    ProductFolderLayout,
    RasterExtension,
)
from aresys_io.product.pf.manifest import Manifest
from aresys_io.product.pf.product_folder import (
    ProductFolder,
    create_product_folder,
    delete_product_folder_content,
    is_valid_product_folder,
    open_product_folder,
    rename_product_folder,
)

PRODUCT_NAMES = ("TEST_SLC_01", "TEST.SLC_01", "TEST-SLC_01")
RENAME_CASES = (
    ("TEST_SLC_01", "NAME_SLC"),
    ("TEST.SLC_01", "NAM.E_SLC"),
    ("TEST-SLC_01", "NAM-E_SLC"),
)
R_EXTENSION: RasterExtension = ".tiff"
QL_PNG = ".png"
QL_JPG = ".jpg"
CHANNELS_INT = [0, 4, 5, 8, 12, 35]
CHANNELS_STR = ["0001", "0009", "0034"]
DESCRIPTION = "example description"


def _check_pf_validity(
    product: ProductFolder,
    path: Path,
    extension: RasterExtension = "",
) -> None:
    """Support function to check ProductFolder validity after creation."""
    assert isinstance(product, ProductFolder)
    assert isinstance(product.manifest, Path)
    assert isinstance(product.path, Path)
    assert isinstance(product.pf_name, str)
    assert isinstance(product.raster_extension, str)
    assert product.path == path
    assert product.pf_name == path.name
    assert product.manifest == path.joinpath(MANIFEST_NAME)
    assert product.raster_extension == extension


def _check_pf_equivalence(pf1: ProductFolder, pf2: ProductFolder) -> None:
    """Checking the equivalence of two PFs."""
    assert pf1.path == pf2.path
    assert pf1.raster_extension == pf2.raster_extension
    assert pf1.pf_name == pf2.pf_name
    assert pf1.manifest == pf2.manifest
    assert pf1.get_config_file() == pf2.get_config_file()
    assert pf1.get_overlay_file() == pf2.get_overlay_file()
    assert pf1.get_channel_metadata(3) == pf2.get_channel_metadata(3)
    assert pf1.get_channel_data(3) == pf2.get_channel_data(3)


@pytest.mark.parametrize("product_name", PRODUCT_NAMES)
def test_pf_creation_private(product_name: str) -> None:
    """Testing ProductFolder object creation, default extension."""
    path = Path(r"C:\Users\user\data").joinpath(product_name)
    product_folder = ProductFolder(path=path)

    assert isinstance(product_folder._layout, ProductFolderLayout)
    assert product_folder._raster_extension in get_args(RasterExtension)
    assert isinstance(product_folder._path, Path)
    assert isinstance(product_folder._manifest, Path)
    assert isinstance(product_folder._pf_name, str)
    assert product_folder._path == path
    assert product_folder._pf_name == product_name
    assert product_folder._manifest == path.joinpath(MANIFEST_NAME)
    assert product_folder._raster_extension == ""


@pytest.mark.parametrize("product_name", PRODUCT_NAMES)
def test_pf_creation_properties(product_name: str) -> None:
    """Testing ProductFolder object creation, default extension."""
    path = Path(r"C:\Users\user\data").joinpath(product_name)
    product_folder = ProductFolder(path=path)
    _check_pf_validity(product=product_folder, path=path)


@pytest.mark.parametrize("product_name", PRODUCT_NAMES)
def test_pf_creation_with_ext(product_name: str) -> None:
    """Testing ProductFolder object creation, with extension."""
    path = Path(r"C:\Users\user\data").joinpath(product_name)
    product_folder = ProductFolder(path=path, raster_extension=R_EXTENSION)
    _check_pf_validity(product=product_folder, path=path, extension=R_EXTENSION)


@pytest.mark.parametrize("product_name", PRODUCT_NAMES)
def test_pf_get_channels_list_error(product_name: str) -> None:
    """Testing ProductFolder get_channel_list method raising error."""
    path = Path(r"C:\Users\user\data").joinpath(product_name)
    product_folder = ProductFolder(path=path)
    with pytest.raises(RuntimeError):
        product_folder.get_channels_list()


@pytest.mark.parametrize("product_name", PRODUCT_NAMES)
def test_pf_get_channels_list_empty(tmp_path: Path, product_name: str) -> None:
    """Testing ProductFolder get_channel_list, empty list."""
    path = tmp_path.joinpath(product_name)
    path.mkdir()
    product_folder = ProductFolder(path=path)
    Manifest().write(product_folder.manifest)

    channels = product_folder.get_channels_list()

    assert isinstance(channels, list)
    assert len(channels) == 0


@pytest.mark.parametrize("product_name", PRODUCT_NAMES)
def test_pf_get_channels_list(tmp_path: Path, product_name: str) -> None:
    """Testing ProductFolder get_channel_list."""
    path = tmp_path.joinpath(product_name)
    path.mkdir()
    product_folder = ProductFolder(path=path)
    Manifest().write(product_folder.manifest)

    file_list = [product_folder.get_channel_data(c) for c in CHANNELS_INT]
    metadata_list = [product_folder.get_channel_metadata(c) for c in CHANNELS_INT]
    for file_path, metadata_path in zip(file_list, metadata_list, strict=False):
        Path(file_path).write_text("", encoding="utf-8")
        Path(metadata_path).write_text("", encoding="utf-8")

    channels = product_folder.get_channels_list()

    assert isinstance(channels, list)
    assert len(channels) == len(CHANNELS_INT)
    assert sorted(channels) == sorted(CHANNELS_INT)


@pytest.mark.parametrize("product_name", PRODUCT_NAMES)
def test_pf_get_channels_list_ext(tmp_path: Path, product_name: str) -> None:
    """Testing ProductFolder get_channel_list, with extension."""
    path = tmp_path.joinpath(product_name)
    path.mkdir()
    product_folder = ProductFolder(path=path, raster_extension=R_EXTENSION)
    Manifest(datafile_extension=R_EXTENSION).write(product_folder.manifest)

    file_list = [product_folder.get_channel_data(c) for c in CHANNELS_INT]
    metadata_list = [product_folder.get_channel_metadata(c) for c in CHANNELS_INT]
    for file_path, metadata_path in zip(file_list, metadata_list, strict=False):
        Path(file_path).write_text("", encoding="utf-8")
        Path(metadata_path).write_text("", encoding="utf-8")

    channels = product_folder.get_channels_list()

    assert isinstance(channels, list)
    assert len(channels) == len(CHANNELS_INT)
    assert sorted(channels) == sorted(CHANNELS_INT)


@pytest.mark.parametrize("product_name", PRODUCT_NAMES)
def test_create_product_folder_no_ext(tmp_path: Path, product_name: str) -> None:
    """Testing creation of a product folder."""
    path = tmp_path.joinpath(product_name)
    product_folder = create_product_folder(pf_path=path)
    _check_pf_validity(product_folder, path)


@pytest.mark.parametrize("product_name", PRODUCT_NAMES)
def test_create_product_folder_ext(tmp_path: Path, product_name: str) -> None:
    """Testing creation of a product folder, with extension."""
    path = tmp_path.joinpath(product_name)
    product_folder = create_product_folder(pf_path=path, raster_extension=R_EXTENSION)
    _check_pf_validity(product_folder, path, extension=R_EXTENSION)


@pytest.mark.parametrize("product_name", PRODUCT_NAMES)
def test_create_product_folder_description(tmp_path: Path, product_name: str) -> None:
    """Testing creation of a product folder, with description."""
    path = tmp_path.joinpath(product_name)
    product_folder = create_product_folder(
        pf_path=path,
        raster_extension=R_EXTENSION,
        description=DESCRIPTION,
    )

    manifest = Manifest.from_file(product_folder.manifest)
    assert manifest.description == DESCRIPTION
    _check_pf_validity(product_folder, path, extension=R_EXTENSION)


@pytest.mark.parametrize("product_name", PRODUCT_NAMES)
def test_create_product_folder_overwrite(tmp_path: Path, product_name: str) -> None:
    """Testing creation of a product folder, with overwrite."""
    path = tmp_path.joinpath(product_name)
    product_folder = create_product_folder(pf_path=path)
    _check_pf_validity(product_folder, path)

    product_folder_ovwr = create_product_folder(pf_path=path, overwrite_ok=True)
    _check_pf_validity(product_folder_ovwr, path)


@pytest.mark.parametrize("product_name", PRODUCT_NAMES)
def test_create_product_folder_no_overwrite_error(tmp_path: Path, product_name: str) -> None:
    """Testing creation of a product folder already existing but no overwrite."""
    path = tmp_path.joinpath(product_name)
    path.mkdir()
    with pytest.raises(RuntimeError):
        create_product_folder(pf_path=path)


@pytest.mark.parametrize("product_name", PRODUCT_NAMES)
def test_create_product_folder_overwrite_not_valid_error(
    tmp_path: Path,
    product_name: str,
) -> None:
    """Testing overwrite on an existing invalid product folder."""
    path = tmp_path.joinpath(product_name)
    product_folder = create_product_folder(pf_path=path)
    product_folder.manifest.unlink()
    with pytest.raises(RuntimeError):
        create_product_folder(pf_path=path, overwrite_ok=True)


@pytest.mark.parametrize("product_name", PRODUCT_NAMES)
def test_open_product_folder_no_ext(tmp_path: Path, product_name: str) -> None:
    """Testing opening a product folder."""
    path = tmp_path.joinpath(product_name)
    pf_created = create_product_folder(pf_path=path)

    pf_opened = open_product_folder(pf_path=path)

    _check_pf_validity(pf_created, path)
    _check_pf_validity(pf_opened, path)
    _check_pf_equivalence(pf_created, pf_opened)


@pytest.mark.parametrize("product_name", PRODUCT_NAMES)
def test_open_product_folder_ext(tmp_path: Path, product_name: str) -> None:
    """Testing opening a product folder, with extension."""
    path = tmp_path.joinpath(product_name)
    pf_created = create_product_folder(pf_path=path, raster_extension=R_EXTENSION)

    pf_opened = open_product_folder(pf_path=path)

    _check_pf_validity(pf_created, path, extension=R_EXTENSION)
    _check_pf_validity(pf_opened, path, extension=R_EXTENSION)
    _check_pf_equivalence(pf_created, pf_opened)


def test_open_product_folder_not_found_error(tmp_path: Path) -> None:
    """Testing opening a product folder, not existent."""
    with pytest.raises(RuntimeError):
        open_product_folder(pf_path=tmp_path.joinpath("missing_pf"))


def test_open_product_folder_invalid_pf_error(tmp_path: Path) -> None:
    """Testing opening an existing path that is not a valid product folder."""
    with pytest.raises(RuntimeError):
        open_product_folder(pf_path=tmp_path)


@pytest.mark.parametrize(("product_name", "new_name"), RENAME_CASES)
def test_rename_product_folder_no_ext_no_ql(
    tmp_path: Path,
    product_name: str,
    new_name: str,
) -> None:
    """Testing rename_product_folder function."""
    path = tmp_path.joinpath(product_name)
    create_product_folder(pf_path=path)

    for channel in CHANNELS_STR:
        path.joinpath(product_name + "_" + channel).write_text("", encoding="utf-8")
        path.joinpath(product_name + "_" + channel + METADATA_EXTENSION).write_text(
            "",
            encoding="utf-8",
        )

    new_pf = path.with_name(new_name)
    assert not new_pf.exists()

    rename_product_folder(current_folder=path, new_folder=new_pf)

    new = open_product_folder(new_pf)
    ch_list = new.get_channels_list()
    assert ch_list == [int(c) for c in CHANNELS_STR]


@pytest.mark.parametrize(("product_name", "new_name"), RENAME_CASES)
def test_rename_product_folder_ext_no_ql(
    tmp_path: Path,
    product_name: str,
    new_name: str,
) -> None:
    """Testing rename_product_folder function."""
    path = tmp_path.joinpath(product_name)
    create_product_folder(pf_path=path, raster_extension=R_EXTENSION)

    for channel in CHANNELS_STR:
        path.joinpath(product_name + "_" + channel + R_EXTENSION).write_text(
            "",
            encoding="utf-8",
        )
        path.joinpath(product_name + "_" + channel + METADATA_EXTENSION).write_text(
            "",
            encoding="utf-8",
        )

    new_pf = path.with_name(new_name)
    assert not new_pf.exists()

    rename_product_folder(current_folder=path, new_folder=new_pf)

    new = open_product_folder(new_pf)
    ch_list = new.get_channels_list()
    assert ch_list == [int(c) for c in CHANNELS_STR]


@pytest.mark.parametrize(("product_name", "new_name"), RENAME_CASES)
def test_rename_product_folder_ext_ql(
    tmp_path: Path,
    product_name: str,
    new_name: str,
) -> None:
    """Testing rename_product_folder function."""
    path = tmp_path.joinpath(product_name)
    create_product_folder(pf_path=path, raster_extension=R_EXTENSION)

    for channel in CHANNELS_STR:
        path.joinpath(product_name + "_" + channel + R_EXTENSION).write_text(
            "",
            encoding="utf-8",
        )
        path.joinpath(product_name + "_" + channel + METADATA_EXTENSION).write_text(
            "",
            encoding="utf-8",
        )
        path.joinpath(product_name + "_" + channel + QL_JPG).write_text(
            "",
            encoding="utf-8",
        )

    new_pf = path.with_name(new_name)
    assert not new_pf.exists()

    rename_product_folder(current_folder=path, new_folder=new_pf)

    new = open_product_folder(new_pf)
    ch_list = new.get_channels_list()
    assert ch_list == [int(c) for c in CHANNELS_STR]
    for channel in CHANNELS_STR:
        assert new_pf.joinpath(new_name + "_" + channel + R_EXTENSION).exists()
        assert new_pf.joinpath(new_name + "_" + channel + QL_JPG).exists()
        assert new_pf.joinpath(new_name + "_" + channel + METADATA_EXTENSION).exists()


@pytest.mark.parametrize(("product_name", "new_name"), RENAME_CASES)
def test_rename_product_folder_other_files(
    tmp_path: Path,
    product_name: str,
    new_name: str,
) -> None:
    """Testing rename_product_folder function."""
    path = tmp_path.joinpath(product_name)
    create_product_folder(pf_path=path)

    for channel in CHANNELS_STR:
        path.joinpath(product_name + "_" + channel).write_text("", encoding="utf-8")
        path.joinpath(product_name + "_" + channel + METADATA_EXTENSION).write_text(
            "",
            encoding="utf-8",
        )

    path.joinpath("report.xml").write_text("", encoding="utf-8")
    path.joinpath("info.txt").write_text("", encoding="utf-8")
    path.joinpath("test.dat").write_text("", encoding="utf-8")

    new_pf = path.with_name(new_name)
    assert not new_pf.exists()

    rename_product_folder(current_folder=path, new_folder=new_pf)

    new = open_product_folder(new_pf)
    ch_list = new.get_channels_list()
    assert ch_list == [int(c) for c in CHANNELS_STR]
    assert new_pf.joinpath("report.xml").exists()
    assert new_pf.joinpath("info.txt").exists()
    assert new_pf.joinpath("test.dat").exists()


@pytest.mark.parametrize(("product_name", "new_name"), RENAME_CASES)
def test_rename_product_folder_error_existing_new_pf(
    tmp_path: Path,
    product_name: str,
    new_name: str,
) -> None:
    """Testing rename_product_folder error when destination folder already exists."""
    path = tmp_path.joinpath(product_name)
    create_product_folder(pf_path=path, raster_extension=R_EXTENSION)

    new_pf = path.with_name(new_name)
    new_pf.mkdir()

    with pytest.raises(RuntimeError):
        rename_product_folder(current_folder=path, new_folder=new_pf)


@pytest.mark.parametrize(("product_name", "new_name"), RENAME_CASES)
def test_rename_product_folder_error_missing_source(
    tmp_path: Path,
    product_name: str,
    new_name: str,
) -> None:
    """Testing rename_product_folder error when source folder does not exist."""
    path = tmp_path.joinpath(product_name)
    new_pf = path.with_name(new_name)

    with pytest.raises(RuntimeError):
        rename_product_folder(current_folder=path, new_folder=new_pf)


@pytest.mark.parametrize(("product_name", "new_name"), RENAME_CASES)
def test_rename_product_folder_error_source_is_file(
    tmp_path: Path,
    product_name: str,
    new_name: str,
) -> None:
    """Testing rename_product_folder error when source path is a file."""
    path = tmp_path.joinpath(product_name + ".xml")
    path.write_text("", encoding="utf-8")
    new_pf = path.with_name(new_name)

    with pytest.raises(RuntimeError):
        rename_product_folder(current_folder=path, new_folder=new_pf)


@pytest.mark.parametrize("product_name", PRODUCT_NAMES)
def test_delete_product_folder_no_ext_no_ql(tmp_path: Path, product_name: str) -> None:
    """Testing delete_product_folder function."""
    path = tmp_path.joinpath(product_name)
    pf_created = create_product_folder(pf_path=path)

    for channel in CHANNELS_STR:
        path.joinpath(product_name + "_" + channel).write_text("", encoding="utf-8")
        path.joinpath(product_name + "_" + channel + METADATA_EXTENSION).write_text(
            "",
            encoding="utf-8",
        )

    delete_product_folder_content(pf_created)
    assert not path.exists()


@pytest.mark.parametrize("product_name", PRODUCT_NAMES)
def test_delete_product_folder_ext_no_ql(tmp_path: Path, product_name: str) -> None:
    """Testing delete_product_folder function."""
    path = tmp_path.joinpath(product_name)
    pf_created = create_product_folder(pf_path=path, raster_extension=R_EXTENSION)

    for channel in CHANNELS_STR:
        path.joinpath(product_name + "_" + channel + R_EXTENSION).write_text(
            "",
            encoding="utf-8",
        )
        path.joinpath(product_name + "_" + channel + METADATA_EXTENSION).write_text(
            "",
            encoding="utf-8",
        )

    delete_product_folder_content(pf_created)
    assert not path.exists()


@pytest.mark.parametrize("product_name", PRODUCT_NAMES)
def test_delete_product_folder_ext_ql(tmp_path: Path, product_name: str) -> None:
    """Testing delete_product_folder function."""
    path = tmp_path.joinpath(product_name)
    pf_created = create_product_folder(pf_path=path, raster_extension=R_EXTENSION)
    ql_files = []

    for channel in CHANNELS_STR:
        path.joinpath(product_name + "_" + channel + R_EXTENSION).write_text(
            "",
            encoding="utf-8",
        )
        ql = path.joinpath(product_name + "_" + channel + QL_JPG)
        ql_files.append(ql)
        ql.write_text("", encoding="utf-8")
        path.joinpath(product_name + "_" + channel + METADATA_EXTENSION).write_text(
            "",
            encoding="utf-8",
        )

    delete_product_folder_content(pf_created)

    res_files = [f.name for f in pf_created.path.iterdir()]
    res_files_expected = [f.name for f in ql_files] + ["aresys_product"]

    assert path.exists()
    assert path.is_dir()
    assert len(res_files) == len(res_files_expected)
    assert sorted(res_files) == sorted(res_files_expected)


@pytest.mark.parametrize("product_name", PRODUCT_NAMES)
def test_delete_product_folder_other_files(tmp_path: Path, product_name: str) -> None:
    """Testing delete_product_folder function."""
    path = tmp_path.joinpath(product_name)
    pf_created = create_product_folder(pf_path=path, raster_extension=R_EXTENSION)

    for channel in CHANNELS_STR:
        path.joinpath(product_name + "_" + channel + R_EXTENSION).write_text(
            "",
            encoding="utf-8",
        )
        path.joinpath(product_name + "_" + channel + METADATA_EXTENSION).write_text(
            "",
            encoding="utf-8",
        )

    path.joinpath("report.txt").write_text("", encoding="utf-8")

    delete_product_folder_content(pf_created)

    res_files = [f.name for f in pf_created.path.iterdir()]
    res_files_expected = ["aresys_product", "report.txt"]

    assert path.exists()
    assert path.is_dir()
    assert path.joinpath("report.txt").exists()
    assert len(res_files) == len(res_files_expected)
    assert sorted(res_files) == sorted(res_files_expected)


@pytest.mark.parametrize("product_name", PRODUCT_NAMES)
def test_is_valid_product_folder_no_files(tmp_path: Path, product_name: str) -> None:
    """Testing is_valid_product_folder for folders with only manifest."""
    path = tmp_path.joinpath(product_name)
    create_product_folder(pf_path=path)
    assert is_valid_product_folder(path)


@pytest.mark.parametrize("product_name", PRODUCT_NAMES)
def test_is_valid_product_folder_no_ql(tmp_path: Path, product_name: str) -> None:
    """Testing is_valid_product_folder with channels and metadata only."""
    path = tmp_path.joinpath(product_name)
    create_product_folder(pf_path=path)

    for channel in CHANNELS_STR:
        path.joinpath(product_name + "_" + channel).write_text("", encoding="utf-8")
        path.joinpath(product_name + "_" + channel + METADATA_EXTENSION).write_text(
            "",
            encoding="utf-8",
        )

    assert is_valid_product_folder(path)


@pytest.mark.parametrize("product_name", PRODUCT_NAMES)
def test_is_valid_product_folder(tmp_path: Path, product_name: str) -> None:
    """Testing is_valid_product_folder with channels, metadata and quicklooks."""
    path = tmp_path.joinpath(product_name)
    create_product_folder(pf_path=path, raster_extension=R_EXTENSION)

    for channel in CHANNELS_STR:
        path.joinpath(product_name + "_" + channel + R_EXTENSION).write_text(
            "",
            encoding="utf-8",
        )
        path.joinpath(product_name + "_" + channel + QL_JPG).write_text(
            "",
            encoding="utf-8",
        )
        path.joinpath(product_name + "_" + channel + METADATA_EXTENSION).write_text(
            "",
            encoding="utf-8",
        )

    assert is_valid_product_folder(path)


@pytest.mark.parametrize("product_name", PRODUCT_NAMES)
def test_is_valid_product_folder_other_file(tmp_path: Path, product_name: str) -> None:
    """Testing is_valid_product_folder with additional unrelated files."""
    path = tmp_path.joinpath(product_name)
    create_product_folder(pf_path=path, raster_extension=R_EXTENSION)

    for channel in CHANNELS_STR:
        path.joinpath(product_name + "_" + channel + R_EXTENSION).write_text(
            "",
            encoding="utf-8",
        )
        path.joinpath(product_name + "_" + channel + QL_JPG).write_text(
            "",
            encoding="utf-8",
        )
        path.joinpath(product_name + "_" + channel + METADATA_EXTENSION).write_text(
            "",
            encoding="utf-8",
        )

    path.joinpath("report.txt").write_text("", encoding="utf-8")
    assert is_valid_product_folder(path)


@pytest.mark.parametrize("product_name", PRODUCT_NAMES)
def test_is_valid_product_folder_error(tmp_path: Path, product_name: str) -> None:
    """Testing invalid folder when some metadata files are missing."""
    path = tmp_path.joinpath(product_name)
    create_product_folder(pf_path=path, raster_extension=R_EXTENSION)

    for channel in CHANNELS_STR:
        path.joinpath(product_name + "_" + channel + R_EXTENSION).write_text(
            "",
            encoding="utf-8",
        )
        path.joinpath(product_name + "_" + channel + QL_JPG).write_text(
            "",
            encoding="utf-8",
        )
        if int(channel) % 2 == 1:
            path.joinpath(product_name + "_" + channel + METADATA_EXTENSION).write_text(
                "",
                encoding="utf-8",
            )

    assert not is_valid_product_folder(path)
