//* Write a C++ program for the instructions in the file lab05.md

#include <bits/stdc++.h>
using namespace std;

int main() {
    const int ROWS = 56;
    const int COLS = 130;
    vector<string> page(ROWS, string(COLS, ' '));

    double penR = 1.0;
    double penC = 1.0;
    double vchange = 0.0;
    double hchange = 0.0;

    auto clearPage = [&]() {
        for (int r = 0; r < ROWS; r++) {
            page[r].assign(COLS, ' ');
        }
    };

    auto putStar = [&](double r, double c) {
        int rr = (int)round(r);
        int cc = (int)round(c);
        if (rr >= 1 && rr <= ROWS && cc >= 1 && cc <= COLS) {
            // row 1 is bottom, internal index 0 is bottom
            page[rr - 1][cc - 1] = '*';
        }
    };

    auto doPrint = [&]() {
        // print row 56 first (top) down to row 1 (bottom)
        for (int r = ROWS - 1; r >= 0; r--) {
            cout << page[r] << "\n";
        }
    };

    clearPage();

    string tok;
    while (cin >> tok) {
        if (tok.empty()) continue;
        string cmd;
        for (char ch : tok) cmd.push_back(toupper((unsigned char)ch));
        char c = cmd[0];

        if (c == 'M') { // MOVE or MCHANGE? only MOVE exists
            // MOVE n m
            double n, m;
            if (!(cin >> n >> m)) break;
            penR = n;
            penC = m;
        } else if (c == 'V') { // VCHANGE
            double n;
            if (!(cin >> n)) break;
            vchange = n;
        } else if (c == 'H') { // HCHANGE
            double n;
            if (!(cin >> n)) break;
            hchange = n;
        } else if (c == 'S') { // STEP
            double n;
            if (!(cin >> n)) break;
            int steps = (int)round(n);
            if (steps < 0) steps = 0;
            for (int i = 0; i < steps; i++) {
                penR += vchange;
                penC += hchange;
                putStar(penR, penC);
            }
        } else if (c == 'P') { // PRINT
            doPrint();
        } else if (c == 'E') { // ERASE
            clearPage();
        } else {
            // unknown command: ignore (consume any following numeric tokens? not needed)
        }
    }

    return 0;
}
