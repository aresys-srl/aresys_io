# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Clean all notebooks from user metadata."""

import argparse
from pathlib import Path

import nbformat


def clean_notebook(path: Path) -> None:
    """Remove execution outputs and environment-specific metadata."""
    nb = nbformat.read(path, as_version=4)

    # Preserve a generic Python kernel specification
    kernelspec = nb.metadata.get("kernelspec", {})
    language = kernelspec.get("language", "python")

    nb.metadata.clear()
    nb.metadata["kernelspec"] = {
        "display_name": "Python 3",
        "language": language,
        "name": "python3",
    }

    for cell in nb.cells:
        # Preserve cell tags
        tags = cell.metadata.get("tags", [])

        cell.metadata.clear()
        if tags:
            cell.metadata["tags"] = tags

        if cell.cell_type == "code":
            cell.outputs = []
            cell.execution_count = None

    nbformat.validate(nb)
    nbformat.write(nb, path)


def main() -> None:
    """Clean notebooks metadata entry point."""
    parser = argparse.ArgumentParser(
        description="Clean Jupyter notebooks from local metadata and execution outputs."
    )
    parser.add_argument(
        "folder",
        type=Path,
        help="Folder containing Jupyter notebooks",
    )
    args = parser.parse_args()

    folder = args.folder

    if not folder.is_dir():
        parser.error(f"Not a valid directory: {folder}")

    notebooks = [
        path for path in folder.rglob("*.ipynb") if ".ipynb_checkpoints" not in path.parts
    ]

    if not notebooks:
        print(f"No notebooks found in {folder}")
        return

    for notebook in notebooks:
        try:
            clean_notebook(notebook)
            print(f"Cleaned: {notebook}")
        except Exception as exc:
            print(f"ERROR: {notebook}: {exc}")

    print(f"\nProcessed {len(notebooks)} notebook(s).")


if __name__ == "__main__":
    main()
