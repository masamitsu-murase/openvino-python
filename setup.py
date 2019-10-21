from distutils.errors import DistutilsSetupError
from distutils.file_util import copy_file
import os.path
from pathlib import Path
from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext


class PrebuiltExtension(Extension):
    def __init__(self, name, sources, *args, **kw):
        if len(sources) != 1:
            raise DistutilsSetupError(
                "PrebuiltExtension can accept only one source.")
        super(PrebuiltExtension, self).__init__(name, sources, *args, **kw)


class copy_ext(build_ext):
    def run(self):
        for extension in self.extensions:
            if not isinstance(extension, PrebuiltExtension):
                raise DistutilsSetupError(
                    "copy_ext can accept PrebuiltExtension only")
            src = extension.sources[0]
            dst = self.get_ext_fullpath(extension.name)
            copy_file(src, dst, verbose=self.verbose, dry_run=self.dry_run)


def find_prebuilt_extensions(base_dir, ext_pattern):
    extensions = []
    for path in Path(base_dir).glob(ext_pattern):
        relpath = path.relative_to(base_dir)
        if relpath.parent != ".":
            package_names = str(relpath.parent).split(os.path.sep)
        else:
            package_names = []
        package_names.append(path.name.split(".", 1)[0])
        name = ".".join(package_names)
        extensions.append(PrebuiltExtension(name, sources=[str(path)]))
    return extensions


version = "2019.3.334"

setup(
    name="openvino_python",
    author="Masamitsu MURASE",
    author_email="masamitsu.murase@gmail.com",
    url="https://github.com/masamitsu-murase/openvino-python",
    version=version,
    description="OpenVINO Python binding",
    cmdclass={"build_ext": copy_ext},
    ext_modules=find_prebuilt_extensions("src", "**/*.pyd"),
    packages=find_packages("src"),
    package_dir={"": "src"},
    zip_safe=False,
    install_requires=["openvino_rt=={}".format(version)],
)
