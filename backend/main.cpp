#include <iostream>
#include "pricing/black_scholes.h"

int main() {
    double S = 198.85;      // Stock price
    double K = 205;      // Strike price
    double T = 7.0 / 252;  // Time to expiration in years (30 days)
    double r = 0.05;     // Risk-free interest rate (5%)
    double sigma = 0.6373;  // Volatility (20%)
    std::string option_type = "call"; // Option type ("call" or "put")

    double price = black_scholes_calculator(S, K, T, r, sigma, option_type);
    std::cout << "Option Price: " << price << std::endl;

    return 0;
}
