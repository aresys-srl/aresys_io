# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Build the Aresys I/O documentation with zensical."""

import argparse
import datetime
import os
import shutil
import subprocess  # ruff: ignore[suspicious-subprocess-import]
import sys
from pathlib import Path

BUILD_INFO_TEMPLATE = Path("tools") / "build.template.md"
BUILD_INFO_PAGE = Path("docs") / "about" / "build.md"


def short_sha(root: Path) -> str:
    """Return the short hash of the current commit, if available."""
    sha = os.getenv("CI_COMMIT_SHORT_SHA") or os.getenv("GITHUB_SHA", "")[:7]
    if sha:
        return sha

    try:
        return subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],  # ruff: ignore[start-process-with-partial-path]
            cwd=root,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    except subprocess.CalledProcessError:
        return ""


def docs_version() -> str:
    """Return the version of the documentation being built."""
    return (
        os.getenv("DOCS_VERSION")
        or os.getenv("CI_COMMIT_TAG")
        or os.getenv("GITHUB_REF_NAME", "dev")
    )


def write_build_info(root: Path) -> None:
    """Generate the build information page from its template."""
    version = docs_version()
    sha = short_sha(root)
    date = datetime.datetime.now(tz=datetime.UTC).strftime("%Y-%m-%d")

    build_info = (root / BUILD_INFO_TEMPLATE).read_text(encoding="utf-8")
    build_info = (
        build_info.replace("__SHA__", sha).replace("__TAG__", version).replace("__DATE__", date)
    )

    build_info_page = root / BUILD_INFO_PAGE
    build_info_page.parent.mkdir(parents=True, exist_ok=True)
    build_info_page.write_text(build_info, encoding="utf-8")


def build(root: Path) -> None:
    """Build the documentation site with zensical."""
    if (root / "site").exists():
        shutil.rmtree(root / "site")

    stmt = [sys.executable, "-m", "zensical", "build", "-f", str(root / "zensical.toml")]
    subprocess.run(  # ruff: ignore[subprocess-without-shell-equals-true]
        stmt,
        check=True,
    )


def main() -> int:
    """Script for generating the documentation."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skip-build",
        action="store_true",
        help="only generate the build information page, used before deploying with mike",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parent.parent

    write_build_info(root)
    if args.skip_build:
        return 0

    build(root)

    return 0


if __name__ == "__main__":
    sys.exit(main())
