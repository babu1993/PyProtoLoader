import os
from importlib.util import spec_from_file_location, module_from_spec
from inspect import getmembers, isclass
from typing import List


class PyProtoLoader:
    """
    Dynamically loads Python modules from specified directories and provides utilities
    to retrieve classes implementing a given protocol.
    """
    def __init__(self, paths: List[str]):
        """
        Initialize the loader with a list of directory paths to search for Python modules.

        Args:
            paths (List[str]): List of directory paths to search for `.py` files.
        """
        self.paths = paths
        self.specs = {}
        for path in paths:
            for p, _, filenames in os.walk(path):
                if p.endswith("__pycache__"):
                    continue
                for filename in filenames:
                    if filename.endswith(".py"):
                        file_path = os.path.join(p, filename)
                        module_path = os.path.relpath(file_path, path)
                        spec = spec_from_file_location(filename[:-3], file_path)
                        if spec:
                            self.specs[module_path[:-3].replace(os.sep, ".")] = {"spec": spec,
                                                                                 "path": module_path,
                                                                                 "is_loaded": False, "module": None}


    def load_module(self, module_name: str, reload: bool = False):
        """
        Load a module by name. Optionally reload if already loaded.

        Args:
            module_name (str): Name of the module to load (without `.py` extension).
            reload (bool): Whether to reload the module if already loaded.

        Returns:
            module: The loaded Python module.

        Raises:
            ImportError: If the module is not found in the specified paths.
        """
        if module_name in self.specs:
            spec_info = self.specs[module_name]
            spec = spec_info["spec"]
            module = module_from_spec(spec)
            if not reload and spec_info["is_loaded"]:
                return spec_info["module"]
            else:
                spec.loader.exec_module(module)
                spec_info["module"] = module
                spec_info["is_loaded"] = True
            return module
        else:
            raise ImportError(f"Module {module_name} not found in specified paths.")

    @staticmethod
    def get_protocol_class(module, protocol, class_name=None):
        """
        Retrieve the first class in the module that implements the given protocol.

        Args:
            module: The Python module to search.
            protocol: The protocol class to check against.
            class_name (str, optional): Specific class name to match. If None, returns the first match.

        Returns:
            class: The class implementing the protocol.

        Raises:
            ValueError: If the protocol is invalid or no implementing class is found.
        """
        if getattr(protocol, "_is_protocol", False) and getattr(protocol, "_is_runtime_protocol", False):
            for name, obj in getmembers(module, isclass):
                if isinstance(obj, protocol):
                    if class_name and name != class_name:
                        continue
                    return obj
            raise ValueError(f"No class {class_name if class_name else ""} implementing {protocol} found in module {module.__name__}.")
        else:
            raise ValueError(f"{protocol} is not a valid protocol class. "
                             f"Ensure it is decorated with @protocol and @runtime_protocol.")
