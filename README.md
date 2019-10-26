[![Build Status](https://dev.azure.com/masamitsu-murase/openvino_python/_apis/build/status/masamitsu-murase.openvino-python?branchName=master)](https://dev.azure.com/masamitsu-murase/openvino_python/_build/latest?definitionId=15&branchName=master)

# openvino-python

This is an *unofficial* pip package for OpenVINO on Windows.

## How to use

### Required files

You need both [openvino-python](https://github.com/masamitsu-murase/openvino-python) and [openvino-rt](https://github.com/masamitsu-murase/openvino-rt) to use OpenVINO.  
Please download them in "releases" pages, [openvino-python](https://github.com/masamitsu-murase/openvino-python/releases) and [openvino-rt](https://github.com/masamitsu-murase/openvino-rt/releases)

### Installation

You can install `openvino-rt` using `pip` command as follows:

```bash
$ pip install openvino_rt-XXXX-py3-none-win_amd64.whl
```

Then, install `openvino-python`.  

```bash
$ pip install openvino_python-XXXX-cp3x-cp3xm-win_amd64.whl
```

Because openvino-python depends on openvino-rt, you have to install openvino-rt first.

### Environment setting

When you use `openvino` package in Python script, you have to set an environment variable, `PATH`, to include `(python-root)/Library/bin` directory.

## Note

When you call `add_cpu_extension` to specify `cpu_extension.dll`, you can use either `cpu_extension_avx2.dll` or `cpu_extension_sse.dll`.  
Because this package does not have `cpu_extension.dll`, you cannot choose it.

For example, you can use `cpu_extension_avx2.dll` as follows:
```python
from openvino.inference_engine import IEPlugin

plugin = IEPlugin(device="CPU", plugin_dirs=None)
plugin.add_cpu_extension('cpu_extension_avx2.dll')
```

## License

Apache License 2.0
