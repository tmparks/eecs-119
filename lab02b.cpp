// Programming Assignment 2: Part Two

#include <iostream>
#include <iomanip>
#include <cmath>
#include <limits>       // For std::numeric_limits

int main() {
    double x = 0.0;
    std::cout << "Enter a value for x (0 < x <= 1): ";
    std::cin >> x;

    if (std::cin.fail()) {
        std::cerr << "Error: Invalid input. Please enter a numeric value for x." << std::endl;
        return 1;
    }

    if (x <= 0 || x > 1) {
        std::cerr << "Error: x must be greater than 0 and less than or equal to 1." << std::endl;
        return 1;
    }

    double I_x = 0.0; // The computed value of I(x)
    double term; // The current term in the series
    int n; // Term index
    const double tolerance = 1E-6; // Stopping condition for the term value
    const int max_iterations = 15; // Maximum number of iterations

    double x_power; // x^(2n+1), initially for n=0
    double factorial; // n! for current n

    bool stopped_due_to_small_term = false;

    // Initialize variables before the loop
    term = x; // The first term (n=0)
    x_power = x; // x^(2n+1), initially for n=0
    factorial = 1.0; // n! for current n

    for (n = 0; n < max_iterations; ++n) {
        I_x += term;

        // Compute the next term in the series
        factorial *= (n + 1); // Update factorial for next n
        x_power *= x * x; // Update x_power for next n: x^(2n+1) = x^(2n-1+1) * x^2 (multiplying by x*x advances the exponent by 2)

        int sign = (n % 2 == 0) ? -1 : 1;
        double numerator = sign * x_power;
        double denominator = factorial * (2 * (n + 1) + 1);
        term = numerator / denominator;

        if (std::abs(term) < tolerance) {
            stopped_due_to_small_term = true;
            break;
        }
    }

    if (stopped_due_to_small_term) {
        std::cout << "Stopped due to small term: " << term << std::endl;
    } else {
        std::cout << "Stopped after reaching maximum iterations: " << max_iterations << std::endl;
    }

    std::cout << std::fixed << std::setprecision(8);
    std::cout << "Computed value of I(" << x << ") = " << I_x << std::endl;
    std::cout << "Last term computed: " << term << std::endl;

    return 0;
}
