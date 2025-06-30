#include "binomial_tree.h"
#include <cmath>
#include <string>
#include <iostream>
#include <vector>
#include <algorithm>

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
    if (p < 0.0 || p > 1.0) return -2.0;
    double discount = std::exp(-r * dt);

    std::vector<double> option_values(steps + 1);

    if (option_type == "call") {
        for (int i = 0; i < steps + 1; i++) {
            double final_price = S * std::pow(u, i) * std::pow(d, steps - i);
            option_values[i] = std::max(final_price - K, 0.0);
        }
    } else if (option_type == "put") {
        for (int i = 0; i < steps + 1; i++) {
            double final_price = S * std::pow(u, i) * std::pow(d, steps - i);
            option_values[i] = std::max(K - final_price, 0.0);
        }
    } else {
        return -1;
    }

     if (is_american) {
        if (option_type == "call") {
            // Path 1: American Call
            for (int i = steps - 1; i >= 0; --i) {
                for (int j = 0; j <= i; ++j) {
                    double curr_price = S * pow(u, j) * pow(d, i - j);
                    double exercise_value = curr_price - K;
                    option_values[j] = std::max(discount * (p * option_values[j + 1] + (1 - p) * option_values[j]), exercise_value);
                }
            }
        } else {
            // Path 2: American Put
            for (int i = steps - 1; i >= 0; --i) {
                for (int j = 0; j <= i; ++j) {
                    double curr_price = S * pow(u, j) * pow(d, i - j);
                    double exercise_value = K - curr_price;
                    option_values[j] = std::max(discount * (p * option_values[j + 1] + (1 - p) * option_values[j]), exercise_value);
                }
            }
        }
    } else {
        // Path 3 & 4: European (Call or Put) - the logic is identical
        for (int i = steps - 1; i >= 0; --i) {
            for (int j = 0; j <= i; ++j) {
                option_values[j] = discount * (p * option_values[j + 1] + (1 - p) * option_values[j]);
            }
        }
    }

    return option_values[0];
}