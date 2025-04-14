#pragma once
#include <string>

#ifdef _WIN32
#define DLL_EXPORT __declspec(dllexport)
#else
#define DLL_EXPORT
#endif

double normal_cdf(double x);

extern "C" {
    DLL_EXPORT double black_scholes_calculator(double S, 
                                                double K, 
                                                double T, 
                                                double r, 
                                                double sigma, 
                                                const std::string& option_type);
}


