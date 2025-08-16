/*
Write a program that reads a sequence of integers from a file and prints the two
largest different values among them. Your program should assume that the
sequence of integers is preceded by another integer telling how many elements
there are in the sequence. Thus when given the input:

    7 1 - 3 6 4 3 6 5

your program should produce the following output

        Largest value in the sequence: 6
        Next largest value: 5

This is because the initial seven just tells that there are seven numbers
following it (note that the second six was ignored: we want the two largest
different values).

You can assume that there will be at least two different values among the
numbers in the sequence, that is, an input like

        5 4 4 4 4 4

will not occur.
*/

#include <iostream>
#include <fstream>
#include <limits>
#include <vector>       // For std::vector
#include <algorithm>    // For std::sort

int main() {
    std::ifstream inputFile("input.txt");
    if (!inputFile) {
        std::cerr << "Error opening file." << std::endl;
        return 1;
    }

    int n;
    inputFile >> n; // Read the number of elements
    if (n < 2) {
        std::cerr << "There must be at least two numbers in the sequence." << std::endl;
        return 1;
    }

    std::vector<int> numbers(n);
    for (int i = 0; i < n; ++i) {
        inputFile >> numbers[i];
    }

    // Sort the numbers in descending order and remove duplicates
    std::sort(numbers.begin(), numbers.end(), std::greater<int>());
    auto last = std::unique(numbers.begin(), numbers.end());
    numbers.erase(last, numbers.end());

    if (numbers.size() < 2) {
        std::cerr << "Not enough different values found." << std::endl;
        return 1;
    }

    // Output the two largest different values
    std::cout << "Largest value in the sequence: " << numbers[0] << std::endl;
    std::cout << "Next largest value: " << numbers[1] << std::endl;

    return 0;
}
// Note: Make sure to create an input.txt file with the appropriate content for testing.
// The input file should contain the sequence of integers as described in the problem statement.
// For example, the content of input.txt could be:
// 7 1 -3 6 4 3 6 5
// This will produce the expected output when the program is run.
// The program reads the integers from the file, sorts them, removes duplicates,
// and then prints the two largest different values.
// Ensure that the input file is in the same directory as the executable or provide the correct path
// to the input file in the code.
// The program uses C++20 features such as std::vector and std::sort, so ensure your compiler supports C++20.
// To compile the program, you can use a command like:
// g++ -std=c++20 lab01b.cpp -o lab01b
// Then run the program with:
// ./lab01b
// This will read from input.txt and display the results as specified.
// If you want to change the input, simply edit the input.txt file with the desired sequence of integers.
// The program is designed to handle various sequences of integers, ensuring that it always finds
// the two largest different values as long as there are at least two distinct integers in the input.
// The program is efficient and straightforward, making it easy to understand and modify if needed.
// It uses standard C++ libraries for file handling, input/output, and algorithms, ensuring portability
// across different systems that support C++20.
// Make sure to test the program with various inputs to verify its correctness and robustness.
// You can also extend the program to handle more complex scenarios or additional features as needed.
// This code is a complete solution to the problem statement provided, ensuring that it meets the requirements
// and handles edge cases appropriately.
