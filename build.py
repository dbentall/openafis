from distutils.command.build_ext import build_ext
from distutils.core import Distribution, Extension
import shutil
from pathlib import Path

from Cython.Build import cythonize


cython_dir = Path("src") / "openafis"
include_dirs = [str(cython_dir), "lib", "3rdparty"]

extension = Extension(
    "openafis",
    [str(p) for p in cython_dir.glob("*.pyx")],
    include_dirs=include_dirs,
    extra_compile_args=["-O3", "-std=c++17"],
)

ext_modules = cythonize([extension], include_path=include_dirs, language_level=3)
dist = Distribution({"ext_modules": ext_modules})
cmd = build_ext(dist)
cmd.ensure_finalized()
cmd.run()

for output in cmd.get_outputs():
    shutil.copyfile(output, cython_dir / Path(output).name)
