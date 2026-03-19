//* Translate the PASCAL program described in the file lab06c.md into C++

//* Remove unused variables in the file lab06c.cpp

#include <iostream>

using namespace std;

auto g(int x) -> int;

auto f(int x) -> int {
    if (x > 100)
        return x - 10;
    else
        return g(f(x + 11));
}

auto g(int x) -> int {
    if (x > 100)
        return x - 10;
    else
        return f(g(x + 11));
}

int main() {
    cout << "on what input would you like me to run the function\n";
    auto arg = 0;
    cin >> arg;
    cout << "f(" << arg << ") = " << f(arg) << "\n";
    return 0;
}