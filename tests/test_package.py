"""
Test that the package is correctly structured for pip install from GitHub or PyPI.
"""

import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_readme_exists():
    assert os.path.isfile(os.path.join(ROOT, "README.md")), "README.md is missing"


def test_license_exists():
    assert os.path.isfile(os.path.join(ROOT, "LICENSE")), "LICENSE is missing"


def test_requirements_txt_exists():
    assert os.path.isfile(
        os.path.join(ROOT, "requirements.txt")
    ), "requirements.txt is missing"


def test_changelog_exists():
    assert os.path.isfile(
        os.path.join(ROOT, "wagtail_drawio", "changelog.txt")
    ), "wagtail_drawio/changelog.txt is missing"


def test_package_version_parseable():
    """The version must be derivable from the changelog without errors."""
    import wagtail_drawio

    version = wagtail_drawio.__version__
    assert version, "Package version is empty"
    # Must follow PEP 440 (X.Y.Z)
    parts = version.split(".")
    assert len(parts) >= 2, f"Version '{version}' does not look like X.Y[.Z]"
    for part in parts:
        assert part.isdigit(), f"Version component '{part}' is not numeric"


def test_package_name_parseable():
    import wagtail_drawio

    name = wagtail_drawio.__name__
    assert name, "Package name is empty"
    assert "_" in name or name.isalpha(), f"Unexpected package name: '{name}'"


def test_pip_check():
    """pip check verifies installed dependencies are consistent."""
    result = subprocess.run(
        [sys.executable, "-m", "pip", "check"],
        capture_output=True,
        text=True,
    )
    assert (
        result.returncode == 0
    ), f"pip check failed:\n{result.stdout}\n{result.stderr}"


def test_package_builds():
    """Verify the package can be built as a source distribution without errors."""
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "build",
            "--sdist",
            "--outdir",
            "/tmp/wagtail_drawio_build_test",
        ],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    assert (
        result.returncode == 0
    ), f"Package build failed:\n{result.stdout}\n{result.stderr}"
    # At least one .tar.gz must have been produced
    import glob

    artifacts = glob.glob("/tmp/wagtail_drawio_build_test/*.tar.gz")
    assert artifacts, "No .tar.gz produced by build"
