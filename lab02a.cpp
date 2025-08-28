// Programming Assignment 2: Part One

#include <iostream>
#include <fstream>
#include <string>
#include <sstream>      // For std::stringstream
#include <cctype>      // For std::isspace
#include <limits>      // For std::numeric_limits

int main() {
    std::ifstream inputFile("lab02a.txt"); // Change to your input file
    if (!inputFile) {
        std::cerr << "Error opening file." << std::endl;
        return 1;
    }

    std::string line;
    while (std::getline(inputFile, line)) {
        std::istringstream lineStream(line);
        std::string word;
        int maxLength = 0;

        while (lineStream >> word) {
            if (word.length() > static_cast<size_t>(maxLength)) {
                maxLength = word.length();
            }
        }

        std::cout << maxLength << std::endl;
    }

    return 0;
}
