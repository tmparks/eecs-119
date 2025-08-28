// Programming Assignment 3: A simulation of a predator prey system

#include <iostream>
#include <iomanip>
#include <cmath>
#include <limits>       // For std::numeric_limits

double newrabbits(double oldrabbits, double oldcoyotes) {
    double births = 0.2 * oldrabbits;
    double starvation_deaths = 0.00002 * oldrabbits * oldrabbits;
    double other_deaths = oldcoyotes * oldrabbits * 45.0 / 10000.0;
    return oldrabbits + births - starvation_deaths - other_deaths;
}

double newcoyotes(double oldrabbits, double oldcoyotes) {
    double births = 0.08 * oldcoyotes;
    double starvation_deaths = oldcoyotes * (250.0 / oldrabbits);
    return oldcoyotes + births - starvation_deaths;
}

//* Print a line of the form:
//* if rabbit blanks < coyote blanks:  m |        'r'        'c'
//* if rabbit blanks > coyote blanks:  m |        'c'        'r'
//* if rabbit blanks == coyote blanks: m |             'x'
//* Remember that the 'r' or 'c' character replaces a blank!
void printline(int month, double rabbits, double coyotes) {
    int rabbit_blanks = static_cast<int>(std::round(rabbits / 100.0));
    int coyote_blanks = static_cast<int>(std::round(coyotes * 2.0));
    std::cout << std::setw(4) << month << " |";
    if (rabbit_blanks < coyote_blanks) {
        std::cout << std::string(rabbit_blanks, ' ') << 'r'
                  << std::string(coyote_blanks - rabbit_blanks - 1, ' ') << 'c' << std::endl;
    } else if (rabbit_blanks > coyote_blanks) {
        std::cout << std::string(coyote_blanks, ' ') << 'c'
                  << std::string(rabbit_blanks - coyote_blanks - 1, ' ') << 'r' << std::endl;
    } else {
        std::cout << std::string(rabbit_blanks, ' ') << 'x' << std::endl;
    }
}

int main() {
    const int max_months = 300;
    const double change_threshold = 0.01; // 1%
    
    double rabbits = 10.0; // Initial rabbit population
    double coyotes = 0.0;  // Initial coyote population
    
    std::cout << "Month | Population" << std::endl;
    std::cout << "-------------------" << std::endl;
    
    for (int month = 0; month <= max_months; ++month) {
        if (month % 3 == 0) {
            printline(month, rabbits, coyotes);
        }
        
        //* Introduce coyotes in month 50
        if (month == 50) {
            coyotes = 10.0;
        }
        double new_rabbits = newrabbits(rabbits, coyotes);
        double new_coyotes = newcoyotes(rabbits, coyotes);
        double rabbit_change = new_rabbits - rabbits;
        double coyote_change = new_coyotes - coyotes;
        rabbits = new_rabbits;
        coyotes = new_coyotes;
        if (rabbits < 0) rabbits = 0;
        if (coyotes < 0) coyotes = 0;
        if (month > 0) {
            if (std::abs(rabbit_change) / rabbits < change_threshold &&
                std::abs(coyote_change) / coyotes < change_threshold) {
                break;
            }
        }
    }
    std::cout << "Final populations after simulation:" << std::endl;
    std::cout << "Rabbits: " << std::fixed << std::setprecision(2) << rabbits << std::endl;
    std::cout << "Coyotes: " << std::fixed << std::setprecision(2) << coyotes << std::endl;
    return 0;
}
