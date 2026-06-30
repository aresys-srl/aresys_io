# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Unit tests for manifest functionalities."""

from pathlib import Path
from tempfile import TemporaryDirectory
from typing import get_args

from aresys_io.product.manifest import Manifest, RasterExtension
from aresys_io.product.productfolder_layout import MANIFEST_NAME


def test_manifest_no_ext() -> None:
    """Testing Manifest dataclass."""
    manifest = Manifest()
    assert manifest.version == "2.1"
    assert manifest.description is None
    assert manifest.datafile_extension in get_args(RasterExtension)
    assert manifest.datafile_extension == ""


def test_manifest_no_ext_with_description() -> None:
    """Testing Manifest dataclass."""
    description = "ProductFolder initialized by aresys_io"
    manifest = Manifest(description=description)
    assert manifest.version == "2.1"
    assert manifest.description == description
    assert manifest.datafile_extension in get_args(RasterExtension)
    assert manifest.datafile_extension == ""


def test_manifest_ext() -> None:
    """Testing Manifest dataclass, with extension."""
    manifest = Manifest(datafile_extension=".tiff")
    assert manifest.version == "2.1"
    assert manifest.description is None
    assert manifest.datafile_extension in get_args(RasterExtension)
    assert manifest.datafile_extension == ".tiff"


def test_manifest_write() -> None:
    """Testing Manifest dump to disk."""
    with TemporaryDirectory() as temp_dir:
        manifest_path = Path(temp_dir).joinpath(MANIFEST_NAME)
        assert not manifest_path.exists()
        Manifest().write(manifest_path)
        assert manifest_path.exists()
        assert manifest_path.is_file()


def test_manifest_read() -> None:
    """Testing Manifest dump to disk."""
    with TemporaryDirectory() as temp_dir:
        manifest_path = Path(temp_dir).joinpath(MANIFEST_NAME)
        description = "ProductFolder initialized by aresys_io"
        Manifest(description=description).write(manifest_path)
        manifest = Manifest.from_file(manifest_path)
        assert isinstance(manifest, Manifest)
        assert manifest.version == "2.1"
        assert manifest.description == description
        assert manifest.datafile_extension in get_args(RasterExtension)
        assert manifest.datafile_extension == ""


def test_manifest_read_ext() -> None:
    """Testing Manifest dump to disk, with extension."""
    with TemporaryDirectory() as temp_dir:
        manifest_path = Path(temp_dir).joinpath(MANIFEST_NAME)
        Manifest(datafile_extension=".tiff").write(manifest_path)
        manifest = Manifest.from_file(manifest_path)
        assert isinstance(manifest, Manifest)
        assert manifest.version == "2.1"
        assert manifest.description is None
        assert manifest.datafile_extension in get_args(RasterExtension)
        assert manifest.datafile_extension == ".tiff"
