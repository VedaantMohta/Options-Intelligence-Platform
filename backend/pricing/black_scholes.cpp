#include "black_scholes.h"
#include <cmath>
#include <string>

double black_scholes_calculator(double S, 
                                double K, 
                                double T, 
                                double r, 
                                double sigma, 
                                const std::string& option_type) {
    double d1 = (std::log(S/K) + (r + (sigma * sigma)/2) * T) / (sigma * std::sqrt(T));
    double d2 = d1 - sigma * std::sqrt(T);

    double option_price;
    if (option_type == "call") {
        option_price = S * normal_cdf(d1) - K * exp(-r * T) * normal_cdf(d2);
    } else if (option_type == "put") {
        option_price = K * exp(-r * T) * normal_cdf(-d2) - S * normal_cdf(-d1);
    } else {
        return -1;
    }

    return option_price;
}

double normal_cdf(double x) {
    return 0.5 * std::erf(x / std::sqrt(2)) + 0.5;
}
