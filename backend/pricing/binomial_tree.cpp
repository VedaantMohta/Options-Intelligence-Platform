#include "binomial_tree.h"
#include <cmath>
#include <string>
#include <iostream>
#include <vector>

extern "C" DLL_EXPORT double binomial_tree_calculator(double S,
                                                      double K,
                                                      double T,
                                                      double r,
                                                      double sigma,
                                                      int steps,
                                                      const std::string &option_type,
                                                      bool is_american) {
    double dt = T / steps;
    double u = std::exp(sigma * std::sqrt(dt));
    double d = 1.0 / u;
    double p = (std::exp(r * dt) - d) / (u-d);
    double discount = std::exp(-r * dt);

    std::vector<double> option_values(steps + 1);

}