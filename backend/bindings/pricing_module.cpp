#include <pybind11/pybind11.h>
#include "../pricing/black_scholes.h"
#include "../pricing/binomial_tree.h"

namespace py = pybind11;

PYBIND11_MODULE(pricing_cpp, m) {
    m.def(
        "binomial_tree_calculator", 
        &binomial_tree_calculator,
        py::arg("S"),
        py::arg("K"),
        py::arg("T"),
        py::arg("r"),
        py::arg("sigma"),
        py::arg("steps") = 100,
        py::arg("option_type"),
        py::arg("is_american") = false,
        "Calculate option price using Binomial Tree model"
    );
    
    m.def(
        "black_scholes_calculator", 
        &black_scholes_calculator,
        py::arg("S"),
        py::arg("K"),
        py::arg("T"),
        py::arg("r"),
        py::arg("sigma"),
        py::arg("option_type"),
        "Calculate option price using Black-Scholes model");
}


