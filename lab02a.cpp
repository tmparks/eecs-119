/*
Write a program that reads a file containing text and writes one number for each
line of text according to the rules given below. In these rules "word" means any
sequence of consecutive non-blank characters.

(1) The output text should consist of the same number of lines as the input text.
(2) Each line of the output contains the number of characters in the longest word
    on that line of the input.
(3) If any line of the input text is blank, the progran may crash in a merciless
    fashion.

To illustrate, if the input file contains:

    Just some silly text an example of
    what your program is supposed to do.
    More:
    so you know what to do with it.

the program should produce the following output:

    7
    8
    5
    4
*/

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
