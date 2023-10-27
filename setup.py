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
		#aise Exception(build_tmp)
		extdir = Path(self.get_ext_fullpath(ext.name))
		config = "Debug" if self.debug else "Release"
		cmake_args = [
			"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=" + str(extdir.parent.absolute()),
			"-DCMAKE_BUILD_TYPE=" + config,
		]
		build_args = [
            '--config', config,
            '--', '-j4'
        ]
		subprocess.run(["cmake", ext.sourcedir] + cmake_args, cwd=build_tmp, check=True)
		subprocess.run(["cmake", "--build", "."] + build_args, cwd=build_tmp, check=True)
		ext.libraries = ["cmark"]
		ext.include_dirs = [str(build_tmp)]
		ext.library_dirs = [str(build_tmp)]


setup(
	name="pymark",
	version="0.1.0",
	description="A Python markdown parser",
	author="tuna2134",
	author_email="me@tuna2134.dev",
	ext_modules=[CMakeExtension("pymark")],
	cmdclass={"build_ext": CMakeBuild},
	zip_safe=False,
)
