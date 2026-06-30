# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Manifest module."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import get_args

from lxml import etree

from aresys_io.product.productfolder_layout import RasterExtension

_VERSION = "2.1"


@dataclass
class Manifest:
    """Product folder manifest document dataclass."""

    version: str = _VERSION
    description: str | None = None
    datafile_extension: RasterExtension = ""

    def write(self, file_path: str | Path) -> None:
        """Write manifest file to disk.

        Parameters
        ----------
        file_path : Union[str, Path]
            path of the file to be written, comprehensive of file name.
        """
        file_path = Path(file_path)

        manifest_xml = etree.Element("AresysProductManifest")
        manifest_xml.set("Version", self.version)
        if self.description is not None:
            etree.SubElement(manifest_xml, "ProductDescription").text = self.description

        assert self.datafile_extension is not None
        etree.SubElement(manifest_xml, "DataFileExtension").text = self.datafile_extension

        tree = etree.ElementTree(manifest_xml)
        tree.write(
            str(file_path),
            pretty_print=True,
            xml_declaration=True,
            encoding="utf-8",
        )

    @staticmethod
    def from_file(file_path: str | Path) -> Manifest:
        """Read manifest xml document from file.

        Parameters
        ----------
        file_path : Union[str, Path]
            path to the xml manifest file.

        Returns
        -------
        Manifest
            Manifest dataclass containing all the info from loaded file

        Raises
        ------
        RuntimeError
            if the input file does not exist
        ValueError
            if the raster extension found in the manifest is not valid
        """
        file_path = Path(file_path)

        if not file_path.is_file():
            msg = "Input file does not exist"
            raise RuntimeError(msg)

        # casting Path to string when loading due to bug with PosixPath on Linux
        manifest_root = etree.parse(str(file_path)).getroot()
        version = manifest_root.values()[0]
        try:
            description = manifest_root.find("ProductDescription").text
        except AttributeError:
            description = None
        try:
            extension = manifest_root.find("DataFileExtension").text
        except AttributeError:
            extension = ""

        extension = extension if extension is not None else ""
        if extension not in get_args(RasterExtension):
            msg = f"Invalid raster extension found in manifest: {extension}"
            raise ValueError(msg)

        return Manifest(version=version, description=description, datafile_extension=extension)
