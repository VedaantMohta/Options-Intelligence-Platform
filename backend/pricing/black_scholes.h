#ifndef BLACK_SCHOLES_H
#define BLACK_SCHOLES_H

#include <string>

// Calculates the Black-Scholes price for a call or put option
double black_scholes_calculator(double S, double K, double T, double r, double sigma, const std::string& option_type);

double normal_cdf(double x);

#endif // BLACK_SCHOLES_H
