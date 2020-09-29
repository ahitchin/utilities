import pytest
import sys
from importlib import import_module


@pytest.mark.parametrize(
    "import_path",
    [
        "modules.recursive_namespace",
    ],
)
def test_imports(import_path):
    import_module(import_path)
