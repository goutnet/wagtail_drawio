"""
Wagtail DrawIO init file
This code is distributed under the MIT License, see the LICENSE file
"""


# Automatic version from the changelog
def package_information():
    """get a tuple (name, version) from the changelog"""
    if package_information.name is None:
        import os  # pylint: disable=import-outside-toplevel
        import re  # pylint: disable=import-outside-toplevel

        with open(
            os.path.join(os.path.dirname(__file__), "changelog.txt"), encoding="utf-8"
        ) as changelog:
            matches = re.compile(r"([^ ]+) \(([^\)]+)\) .*").match(
                changelog.readline()
            )  # pylint: disable=invalid-name
            package_information.name = str(matches[1].replace("-", "_"))
            package_information.version = str(matches[2])

    return (package_information.name, package_information.version)


package_information.name = None
package_information.version = None


def __getattr__(name: str) -> any:

    if name == "__version__":
        return package_information()[1]

    if name == "__name__":
        return package_information()[0]

    raise AttributeError(f"module does not contain {name}")
