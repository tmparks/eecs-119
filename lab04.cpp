/*
# Programming Assignment 4
## Text formatter

If you look at the handouts for this course carefully, you may notice certain
characteristics that suggest that they are produced with the aid of a machine.
For example, blanks are added between words so all the lines of a paragraph
(except the last one) have exactly the same length, something which is very hard
to do for a human typist.

A program that takes as input a string of text sprinkled with commands about how
to process the text and produces a document as output is called a text formatter.
In this lab you will write the core of a text formatter similar to the one used
to produce the course handouts.

### The basic formatter

Write a program that reads text from an input file and produces output which is
a copy of the input where:

1.  each line starts in the leftmost column of the output page
2.  two words in the same line are separated by exactly one blank
3.  no word is split across lines (hyphenation is too hard a probiem to tackle
    in one week)
4.  each output line contains as many words as possible without exceeding 40
    characters
5.  input lines that start with the character '.' are not printed: these lines
    will contain a formatter command (see below)

You may assume (for this part and all others) that no word will have more than
30 characters (by "word" I mean any sequence of non blank characters). For
example, if • represents a blank and the input file contains:

    This•line•contains•more•than•40•characters
    but•this••••other•••line••••••will•••••••just••fit
    .XX••garbage
    in•the•second•line.••.YY•Here
    is
    additional•••text.

then the output file should contain:

    This•line•contains•more•than•40
    characters•but•this•other•line•will•just
    fit•in•the•second•line.•.YY•Here•is
    additional•text.
*/

#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>

const int MAX_LINE_LENGTH = 40;

void formatText(std::istream &input, std::ostream &output) {
    std::string line;
    std::string currentLine;
    
    while (std::getline(input, line)) {
        // Skip command lines
        if (!line.empty() && line[0] == '.') {
            continue;
        }

        std::istringstream iss(line);
        std::string word;
        
        while (iss >> word) {
            if (currentLine.empty()) {
                currentLine = word;
            } else if (currentLine.length() + 1 + word.length() <= MAX_LINE_LENGTH) {
                currentLine += " " + word;
            } else {
                output << currentLine << std::endl;
                currentLine = word;
            }
        }
    }
    
    // Print any remaining text in the current line
    if (!currentLine.empty()) {
        output << currentLine << std::endl;
    }
}

int main(int argc, char *argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: " << argv[0] << " <input file> <output file>" << std::endl;
        return 1;
    }

    std::ifstream inputFile(argv[1]);
    if (!inputFile) {
        std::cerr << "Error opening input file: " << argv[1] << std::endl;
        return 1;
    }

    std::ofstream outputFile(argv[2]);
    if (!outputFile) {
        std::cerr << "Error opening output file: " << argv[2] << std::endl;
        return 1;
    }

    formatText(inputFile, outputFile);

    inputFile.close();
    outputFile.close();

    return 0;
}
