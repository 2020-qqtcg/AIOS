from importlib.util import find_spec
from importlib.metadata import metadata, PackageNotFoundError

def is_swebench_available():
    return _is_package_available("swebench")

def _is_package_available(pkg_name, metadata_name=None):
    # Check we're not importing a "pkg_name" directory somewhere but the actual library by trying to grab the version
    package_exists = find_spec(pkg_name) is not None
    if package_exists:
        try:
            # Some libraries have different names in the metadata
            metadata(pkg_name if metadata_name is None else metadata_name)
            return True
        except PackageNotFoundError:
            return False
