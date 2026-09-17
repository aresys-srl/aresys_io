# SPDX-FileCopyrightText: Aresys S.r.l. <info@aresys.it>
# SPDX-License-Identifier: MIT

"""Build the Aresys I/O documentation with zensical."""

import datetime
import os
import shutil
import subprocess  # ruff: ignore[suspicious-subprocess-import]
import sys
from pathlib import Path


def main() -> int:
    """Script for generating the documentation."""
    root = Path(__file__).resolve().parent.parent

    if (root / "site").exists():
        shutil.rmtree(root / "site")

    tag = os.getenv("CI_COMMIT_TAG") or os.getenv("GITHUB_REF_NAME", "dev")
    sha = os.getenv("CI_COMMIT_SHORT_SHA")
    if sha is None:
        try:
            sha = subprocess.run(
                ["git", "rev-parse", "--short", "HEAD"],  # ruff: ignore[start-process-with-partial-path]
                cwd=root,
                capture_output=True,
                text=True,
                check=True,
            ).stdout.strip()
        except subprocess.CalledProcessError:
            sha = ""
    date = datetime.datetime.now(tz=datetime.UTC).strftime("%Y-%m-%d")
    doc_name = f"{date}-{tag}-{sha}-html-doc"

    build_info_template = root / "docs" / "about" / "build.template.md"
    build_info = build_info_template.read_text(encoding="utf-8")
    build_info = (
        build_info.replace("__SHA__", sha).replace("__TAG__", tag).replace("__DATE__", date)
    )
    build_info_template.with_name("build.md").write_text(build_info, encoding="utf-8")
    build_info_template.unlink()

    stmt = [sys.executable, "-m", "zensical", "build", "-f", str(root / "zensical.toml")]
    subprocess.run(  # ruff: ignore[subprocess-without-shell-equals-true]
        stmt,
        check=True,
    )

    if os.getenv("CI") == "true":
        shutil.make_archive(f"documentation-{doc_name}", "zip", root_dir=root, base_dir="site")

    return 0


if __name__ == "__main__":
    sys.exit(main())
