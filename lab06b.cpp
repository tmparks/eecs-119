//* Write a C++ program for the instructions in the file lab06b.md

#include <iostream>
#include <vector>

using namespace std;

bool is_valid(const vector<int>& cols, int row, int col) {
    for (auto r = 0; r < row; ++r) {
        auto c = cols[r];
        if (c == col || abs(c - col) == abs(r - row))
            return false;
    }
    return true;
}

void solve(int n, int row, vector<int>& cols, vector<vector<int>>& solutions) {
    if (row == n) {
        solutions.push_back(cols);
        return;
    }
    for (auto col = 0; col < n; ++col) {
        if (!is_valid(cols, row, col))
            continue;
        cols[row] = col;
        solve(n, row + 1, cols, solutions);
    }
}

int main() {
    cout << "Enter board size N (4 recommended): ";
    auto n = 4;
    if (!(cin >> n) || n < 1) {
        return 1;
    }

    auto cols = vector<int>(n, -1);
    auto solutions = vector<vector<int>>();
    solve(n, 0, cols, solutions);

    cout << "Found " << solutions.size() << " solution(s) for N=" << n << "\n";
    for (auto const& sol : solutions) {
        for (auto r = 0; r < n; ++r) {
            for (auto c = 0; c < n; ++c)
                cout << (sol[r] == c ? 'Q' : '.') << ' ';
            cout << "\n";
        }
        cout << "\n";
    }

    return 0;
}