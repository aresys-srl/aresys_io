# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Generate XML parser models from project XSD files."""

import subprocess
import sys
from pathlib import Path

LICENSE_HEADER = """# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""
MODULE_DOCSTRING = '"""Generated module."""\n\n'

ROOT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT_DIR / "src"
XSD_DIR = ROOT_DIR / "xsd"
XSDATA_CONFIG = XSD_DIR / ".xsdata.xml"


def prepend_license_header(filename: Path) -> None:
    """Prepend project license header to generated Python modules."""
    body = filename.read_text(encoding="utf-8")

    while body.startswith(LICENSE_HEADER):
        body = body[len(LICENSE_HEADER) :]

    for quote in ('"""', "'''"):
        if body.startswith(quote):
            end = body.find(quote, len(quote))
            if end != -1:
                body = body[end + len(quote) :].lstrip("\n")
            break

    fixed_content = f"{LICENSE_HEADER}{MODULE_DOCSTRING}{body}"
    filename.write_text(fixed_content, encoding="utf-8")


def format_generated_package(python_executable: str, package: str) -> None:
    """Apply import sorting and formatting to generated package files."""
    package_dir = SRC_DIR / Path(*package.split("."))

    for generated_file in package_dir.glob("*.py"):
        prepend_license_header(generated_file)

    subprocess.run(
        [
            python_executable,
            "-m",
            "ruff",
            "check",
            "--fix",
            str(package_dir),
        ],
        check=True,
    )
    subprocess.run([python_executable, "-m", "ruff", "format", str(package_dir)], check=True)


def main() -> None:
    """Generate XML parser models for metadata files."""
    packages = [
        ("aresys_io.product.metadata.models", "aresys_generic_metadata.xsd"),
        ("aresys_io.point_target.models"),
        (
            "aresys_io.sarsystem.models",
            "sarsystem",
        ),
    ]

    for package, xsd_file_or_folder in packages:
        subprocess.run(
            [
                sys.executable,
                "-m",
                "xsdata",
                "generate",
                "--package",
                package,
                "--structure-style",
                "filenames",
                "--config",
                str(XSDATA_CONFIG),
                str(XSD_DIR / xsd_file_or_folder),
            ],
            cwd=SRC_DIR,
            check=True,
        )
        format_generated_package(sys.executable, package)


if __name__ == "__main__":
    main()
