---
---
# openvino-python

This is an *unofficial* pip package for OpenVINO on **Windows**.

## How to use

### Installation

Because this library is not registered in PyPI, you can install this library by using the following command:

```bash
pip install openvino-python --extra-index-url=https://masamitsu-murase.github.io/openvino-python/simple/
```

### Environment setting

When you use `openvino` package in Python script, you have to set an environment variable, `PATH`, to include `(python-root)/Library/bin` directory.  
If you use `venv`, you have to set an environment variable, `PATH`, to include `(venv-path)/Library/bin` directory.

## License

Apache License 2.0
