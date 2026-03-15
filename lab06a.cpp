//* Translate the PASCAL program described in the file lab06a.md into C++
//* then find and fix the bugs

//* Fix the bugs in the file lab06a.cpp

#include <iostream>
#include <vector>

using namespace std;

const int MAX_SIZE = 15;

void swap_elements(vector<int>& n, int& left, int& right) {
    int temp = n[left];
    n[left] = n[right];
    n[right] = temp;
    left++;
    right--;
}

void quicksort(vector<int>& n, int low, int high) {
    if (low < high) {
        // Lomuto partition: choose pivot as n[high]
        int pivot = n[high];
        int i = low - 1;
        for (int j = low; j < high; j++) {
            if (n[j] <= pivot) {
                i++;
                // Simple swap without modifying indices
                int temp = n[i];
                n[i] = n[j];
                n[j] = temp;
            }
        }
        // Swap pivot to correct position
        int temp = n[i + 1];
        n[i + 1] = n[high];
        n[high] = temp;
        int pi = i + 1;
        quicksort(n, low, pi - 1);
        quicksort(n, pi + 1, high);
    }
}

int main() {
    cout << "I can sort arrays of size up to " << MAX_SIZE << endl;
    cout << "how large an array would you like me to sort? " << endl;
    int arraysize;
    cin >> arraysize;
    if (arraysize > MAX_SIZE || arraysize < 1) {
        cout << "Invalid size" << endl;
        return 1;
    }
    vector<int> n(arraysize);
    cout << "now enter the elements of your array, all on one line " << endl;
    for (int k = 0; k < arraysize; k++) {
        cin >> n[k];
    }
    quicksort(n, 0, arraysize - 1);
    cout << "sorted numbers are " << endl;
    for (int k = 0; k < arraysize; k++) {
        cout << n[k] << " ";
    }
    cout << endl;
    return 0;
}
