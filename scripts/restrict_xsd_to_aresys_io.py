# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Restrict BrickSAR XSD files to aresys_io usage."""

import io
import xml.etree.ElementTree as ET
from pathlib import Path

import click

UNUSED_TAGS = [
    "ProductType",
    "OrderingType",
    "ScanSARSlcSwathType",
    "ScanSARRgcSwathType",
    "ScanSARRawSwathType",
    "SlcSwathType",
    "RgcSwathType",
    "RawSwathType",
    "GeometryParamsType",
    "GridType",
    "PolySARType",
    "FileListType",
    "SensorAttitudeType",
    "ROIType",
]


def remove_unused_types(xsd_file_in: Path, xsd_file_out: Path) -> None:
    """Remove unused types from the input XSD file and write the result to the output XSD file."""
    tree = ET.parse(xsd_file_in)
    root = tree.getroot()
    children = list(root)

    def unused_child(child: ET.Element) -> bool:
        return child.attrib.get("name") in UNUSED_TAGS

    for child in filter(unused_child, children):
        root.remove(child)

    with io.BytesIO() as intermediate_xsd:
        tree.write(
            intermediate_xsd,
            encoding="utf-8",
            xml_declaration=True,
            default_namespace=None,
            method="xml",
        )
        file_content = intermediate_xsd.getvalue().replace(
            b"<xs:schema", b'<xs:schema xmlns:at="aresysTypes"'
        )

        xsd_file_out.write_bytes(file_content)


def remove_roi_type(xsd_file_in: Path, xsd_file_out: Path) -> None:
    """Remove ROIType from the input XSD file and write the result to the output XSD file."""
    lines_out = []
    for line in xsd_file_in.read_text(encoding="utf-8").splitlines():
        if "ROIType" in line:
            continue
        lines_out.append(line)

    xsd_file_out.write_text("\n".join(lines_out), encoding="utf-8")


def restrict_xsd_to_aresys_io(bricksar_dir: Path, destination_dir: Path) -> None:
    """Restrict the BrickSAR XSD files to aresys_io usage."""
    bricksar_xsd_product_dir = bricksar_dir.joinpath("doc", "xsd", "products")
    input_aresys_types_xsd = bricksar_xsd_product_dir.joinpath("aresysTypes.xsd")
    input_aresys_metadata_xsd = bricksar_xsd_product_dir.joinpath("aresys_generic_metadata.xsd")

    destination_dir.mkdir(parents=True, exist_ok=True)

    restricted_aresys_types = destination_dir.joinpath("aresysTypes.xsd")
    local_aresys_metadata = destination_dir.joinpath("aresys_generic_metadata.xsd")

    remove_unused_types(input_aresys_types_xsd, restricted_aresys_types)
    remove_roi_type(input_aresys_metadata_xsd, local_aresys_metadata)


@click.command()
@click.option(
    "--input-bricksar-dir",
    nargs=1,
    type=click.Path(exists=True, dir_okay=True, file_okay=False),
    required=True,
)
@click.option(
    "--output-aresys-io-xsd-dir",
    nargs=1,
    type=click.Path(dir_okay=True),
    required=True,
)
def main(input_bricksar_dir: str, output_aresys_io_xsd_dir: str) -> None:
    """Restrict BrickSAR XSD files to aresys_io usage."""
    click.echo(f"Input BrickSAR directory: {input_bricksar_dir}")
    click.echo(f"Output XSD directory: {output_aresys_io_xsd_dir}")
    restrict_xsd_to_aresys_io(Path(input_bricksar_dir), Path(output_aresys_io_xsd_dir))


if __name__ == "__main__":
    main()
