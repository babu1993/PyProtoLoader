import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import os
import tempfile
import types
import shutil
import unittest
from typing import Protocol, runtime_checkable
from pyprotoloader import PyProtoLoader

@runtime_checkable
class DummyProtocol(Protocol):
    def foo(self): ...

class TestPyProtoLoader(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for test modules
        self.test_dir = tempfile.mkdtemp()
        self.module_code = """
class MyClass:
    def foo(self):
        return 'bar'
"""
        self.module_path = os.path.join(self.test_dir, "testmod.py")
        with open(self.module_path, "w") as f:
            f.write(self.module_code)
        self.loader = PyProtoLoader([self.test_dir])

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_load_module(self):
        module_name = os.path.relpath(self.module_path, self.test_dir)[:-3].replace(os.sep, ".")
        module = self.loader.load_module(module_name)
        self.assertTrue(hasattr(module, "MyClass"))

    def test_get_protocol_class(self):
        module_name = os.path.relpath(self.module_path, self.test_dir)[:-3].replace(os.sep, ".")
        module = self.loader.load_module(module_name)
        cls = self.loader.get_protocol_class(module, DummyProtocol)
        self.assertTrue(issubclass(cls, object))
        self.assertEqual(cls.__name__, "MyClass")

    def test_get_protocol_class_with_class_name(self):
        module_name = os.path.relpath(self.module_path, self.test_dir)[:-3].replace(os.sep, ".")
        module = self.loader.load_module(module_name)
        cls = self.loader.get_protocol_class(module, DummyProtocol, class_name="MyClass")
        self.assertEqual(cls.__name__, "MyClass")

    def test_get_protocol_class_invalid_protocol(self):
        module_name = os.path.relpath(self.module_path, self.test_dir)[:-3].replace(os.sep, ".")
        module = self.loader.load_module(module_name)
        with self.assertRaises(ValueError):
            self.loader.get_protocol_class(module, object)

    def test_load_module_not_found(self):
        with self.assertRaises(ImportError):
            self.loader.load_module("nonexistent")

if __name__ == "__main__":
    unittest.main()
