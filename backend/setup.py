import sys
from setuptools import setup, Extension
import pybind11

# Set the correct C++ standard flag based on the compiler
extra_args = ['/std:c++17'] if sys.platform == 'win32' else ['-std=c++17']

ext_modules = [
    Extension(
        "pricing_cpp",
        sources=[
            "bindings/pricing_module.cpp",
            "pricing/black_scholes.cpp",
            "pricing/binomial_tree.cpp"
        ],
        include_dirs=[pybind11.get_include(), "pricing"],
        language="c++",
        extra_compile_args=extra_args
    ),
]

setup(
    name="pricing_cpp",
    version="0.1",
    author="Vedaant Mohta",
    description="C++ option pricing models with Python bindings",
    ext_modules=ext_modules,
)