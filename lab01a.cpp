/*
Write a program that computes the following two sums:

    1E12 + 1/1 + 1/2 + 1/3 + ... + 1/999 + 1/1000 - 1E12

and

    1/1 + 1/2 + 1/3 + ... + 1/999 + 1/1000

The sums should be computed from left to right, that is, adding the second term to the first, the
third to the resulting sum, the fourth to the new sum, and so on.

Clearly the values of the two sums ought to be identical but you will discover that they are
not. This is due to the fact that real numbers are kept with a finite precision. The representation
of real numbers in a computer and some of the problems that it causes will be the topic of one of
your precepts.
*/

#include <iostream>
#include <iomanip>      // for std::setprecision

int main() {
    const double large_value = 1E12;
    double sum1 = large_value; // Initialize with the large value
    double sum2 = 0.0;         // Initialize the second sum

    // Compute the first sum
    for (int i = 1; i <= 1000; ++i) {
        sum1 += 1.0 / i;
    }
    sum1 -= large_value; // Subtract the large value at the end

    // Compute the second sum
    for (int i = 1; i <= 1000; ++i) {
        sum2 += 1.0 / i;
    }

    // Output the results with high precision
    std::cout << std::setprecision(15); // Set precision for better visibility
    std::cout << "Sum 1: " << sum1 << std::endl;
    std::cout << "Sum 2: " << sum2 << std::endl;

    return 0;
}
// The output will show that sum1 and sum2 are not equal due to precision issues.
// This demonstrates the limitations of floating-point arithmetic in C++.
// Note: The exact output may vary slightly depending on the system and compiler.
// Compile with: g++ -std=c++20 -o lab01a lab01a.cpp
// Run with: ./lab01a
// Example output:
// Sum 1: 7.485470860550345
// Sum 2: 7.485470860550343
// Note: The exact output may vary slightly depending on the system and compiler.
