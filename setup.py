from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
import subprocess
import os
from pathlib import Path


class CMakeExtension(Extension):
    def __init__(self, name, sourcedir="", **kwargs):
        super().__init__(name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    def build_extension(self, ext: CMakeExtension) -> None:
        build_tmp = Path(self.build_temp)
        build_tmp.mkdir(parents=True, exist_ok=True)
        extdir = Path(self.get_ext_fullpath(ext.name)).parent.absolute()

        config = "Debug" if self.debug else "Release"
        cmake_args = [
            f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={extdir}",  # ビルド出力先
            f"-DCMAKE_BUILD_TYPE={config}",
        ]
        build_args = ["--config", config, "--", "-j4"]

        subprocess.run(["cmake", ext.sourcedir] + cmake_args, cwd=build_tmp, check=True)
        subprocess.run(["cmake", "--build", "."] + build_args, cwd=build_tmp, check=True)

        self._move_shared_library(extdir, build_tmp)

    def _move_shared_library(self, extdir: Path, build_tmp: Path):
        """共有ライブラリ (libcmark.so) をパッケージディレクトリにコピー"""
        shared_lib = build_tmp / "libcmark.so"
        if not shared_lib.exists():
            raise RuntimeError(f"{shared_lib} does not exist. Check your CMake setup.")

        target_lib = extdir / "libcmark.so"
        shared_lib.replace(target_lib)
        print(f"Copied {shared_lib} -> {target_lib}")


setup(
    name="pymark",
    version="0.1.0",
    description="A Python markdown parser",
    author="tuna2134",
    author_email="me@tuna2134.dev",
    packages=["pymark"],
    ext_modules=[CMakeExtension("pymark._pymark")],
    cmdclass={"build_ext": CMakeBuild},
    package_data={
        "pymark": ["libcmark.so"],
    },
    zip_safe=False,
)
