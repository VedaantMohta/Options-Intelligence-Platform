from setuptools import setup, Extension
import pybind11

ext_modules = [
    Extension(
        "pricing_cpp",
        sources=["bindings/pricing_module.cpp", "pricing/black_scholes.cpp"],
        include_dirs=[
            pybind11.get_include(),
            "pricing"
        ],
        language="c++",
        extra_compile_args=["-std=c++17"],
    ),
]

setup(
    name="pricing_cpp",
    version="0.1",
    ext_modules=ext_modules,
)
