#include <pybind11/pybind11.h>
#include "../pricing/black_scholes.h"

namespace py = pybind11;

PYBIND11_MODULE(pricing_cpp, m) {
    m.def("calculate_option_price", &black_scholes_calculator,
        py::arg("S"),
        py::arg("K"),
        py::arg("T"),
        py::arg("r"),
        py::arg("sigma"),
        py::arg("option_type"),
        "Calculate option price using Black-Scholes model");
}
