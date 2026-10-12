# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Metadata file IO."""

from pathlib import Path

from aresys_io.core.parsing import parse, serialize
from aresys_io.product.metadata.channel import MetaData
from aresys_io.product.metadata.models import AresysXmlDoc
from aresys_io.product.metadata.translate import (
    translate_metadata_from_model,
    translate_metadata_to_model,
)

__all__ = [
    "parse_metadata",
    "read_metadata",
    "serialize_metadata",
    "write_metadata",
]


def read_metadata(metadata_file: str | Path) -> MetaData:
    """Read metadata from XML file.

    Parameters
    ----------
    metadata_file : str | Path
        path to the xml aresys metadata file.

    Returns
    -------
    MetaData
        Channel metadata
    """
    metadata_content = Path(metadata_file).read_text(encoding="utf-8")
    return parse_metadata(metadata_content)


def write_metadata(metadata_obj: MetaData, metadata_file: str | Path) -> None:
    """Write metadata to XML file.

    Parameters
    ----------
    metadata_obj : MetaData
        Channel metadata.

    metadata_file : str | Path
        path to the xml aresys metadata file
    """
    metadata_content = serialize_metadata(metadata_obj)
    Path(metadata_file).write_text(metadata_content, encoding="utf-8")


def serialize_metadata(metadata_obj: MetaData) -> str:
    """Serialize metadata object.

    Parameters
    ----------
    metadata_obj : MetaData
        Metadata representation object

    Returns
    -------
    str
        serialized metadata as a string (xml format)
    """
    metadata_model = translate_metadata_to_model(metadata_obj)
    return serialize(metadata_model)


def parse_metadata(metadata_content: str) -> MetaData:
    """Parse metadata XML string.

    Parameters
    ----------
    metadata_content : str
        Metadata as string in XML format

    Returns
    -------
    MetaData
        Metadata representation object
    """
    return translate_metadata_from_model(parse(metadata_content, AresysXmlDoc))
