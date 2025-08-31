// Programming Assignment 3: A simple interactive game

/*
Pick-up-stones is a simple game to play and implement. Here's a simple
explanation of the game: Twenty-one stones are put in a pile and players take
turns removing 1, 2 or 3 stones from the pile. The last player to pick up a
stone from the pile loses. Even though it sounds easy to play, it might not be
easy to win every time you play. Your task is to implement this game so that you
can play against the computer (your program). Your program should employ some
clever algorithm so that it could win against a naive player. It does not have
to win all the time in order to get most of the credit. However, you will get
full credit if you write a program that is impossible to beat.

Hint: In order to make your program win all the time, the other player must go
first.
*/

#include <iostream>
#include <cstdlib>
#include <ctime>

using namespace std;

int main() {
    int stones = 21; // Initial number of stones
    int playerMove, computerMove;

    cout << "Welcome to the Pick-up-stones game!" << endl;
    cout << "There are 21 stones in the pile." << endl;
    cout << "You can pick 1, 2, or 3 stones on your turn." << endl;
    cout << "The player who picks the last stone loses." << endl;
    cout << "You will go first." << endl;

    while (stones > 0) {
        // Player's turn
        do {
            cout << "There are " << stones << " stones left." << endl;
            cout << "How many stones do you want to pick (1, 2, or 3)? ";
            cin >> playerMove;
        } while (playerMove < 1 || playerMove > 3 || playerMove > stones);

        stones -= playerMove;
        if (stones == 0) {
            cout << "You picked the last stone. You lose!" << endl;
            break;
        }

        // Computer's turn
        computerMove = (4 - playerMove) % 4; // Optimal move
        if (computerMove == 0) computerMove = 1; // If player picks 3, pick 1

        stones -= computerMove;
        cout << "Computer picks " << computerMove << " stone(s)." << endl;

        if (stones == 0) {
            cout << "Computer picked the last stone. Computer loses!" << endl;
            break;
        }
    }

    return 0;
}
