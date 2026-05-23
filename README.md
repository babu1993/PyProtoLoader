# PyProtoLoader

PyProtoLoader is a utility for dynamically loading Python modules from specified directories and retrieving classes that implement a given protocol (PEP 544). It is especially useful for plugin systems, dynamic class discovery, and protocol-based architectures.

## Features
- Dynamically load Python modules from one or more directories
- Retrieve classes that implement a specified protocol (including runtime-checkable protocols)
- Reload modules on demand
- Simple API for integration into larger projects

## Installation
PyProtoLoader is a pure Python package. Install from PyPI.

```bash
pip install pyprotoloader
```

## Usage

### 1. Basic Example
```python
from pyprotoloader import PyProtoLoader
from typing import Protocol, runtime_checkable

@runtime_checkable
class MyProtocol(Protocol):
    def foo(self): ...

# Initialize loader with a list of directories to search
loader = PyProtoLoader(["/path/to/plugins"])

# Load a module by name (without .py extension)
module = loader.load_module("plugin_module")

# Retrieve the class implementing the protocol
cls = loader.get_protocol_class(module, MyProtocol)

# Instantiate and use
instance = cls()
instance.foo()
```

### 2. With Class Name
```python
cls = loader.get_protocol_class(module, MyProtocol, class_name="MyClass")
```

## API
### `PyProtoLoader(paths: List[str])`
Initializes the loader with a list of directory paths to search for `.py` files.

### `load_module(module_name: str, reload: bool = False)`
Loads a module by name. Optionally reloads if already loaded.

### `get_protocol_class(module, protocol, class_name=None)`
Retrieves the first class in the module that implements the given protocol. Optionally specify a class name.

## Testing
Unit tests are provided in the `tests/` directory. To run tests:

```bash
python3 -m unittest discover -s tests
```

## License
This project is licensed under the terms of the MIT license. See the LICENSE file for details.
