#pragma once
#include <string>

// Export macro for Windows DLL
#ifdef _WIN32
#define DLL_EXPORT __declspec(dllexport)
#else
#define DLL_EXPORT
#endif

// Core pricing function for binomial tree model
extern "C" {
    DLL_EXPORT double binomial_tree_price(double S,
                                          double K,
                                          double T,
                                          double r,
                                          double sigma,
                                          int steps,
                                          const std::string& option_type,
                                          bool is_american);
}
