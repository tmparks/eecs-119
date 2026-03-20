//* Write a C++ program for the instructions in the file lab07.md

#include <iostream>
#include <vector>
#include <fstream>

using namespace std;

const int MAX_ROWS = 100;
const int MAX_COLS = 100;

auto picture = vector<vector<int>>(MAX_ROWS, vector<int>(MAX_COLS, 0));
auto visited = vector<vector<bool>>(MAX_ROWS, vector<bool>(MAX_COLS, false));
auto rows = 0;
auto cols = 0;

void print_picture() {
    for (auto r = 0; r < rows; ++r) {
        for (auto c = 0; c < cols; ++c) {
            cout << (picture[r][c] == 1 ? '*' : '-');
        }
        cout << "\n";
    }
    cout << "\n";
}

void print_picture_by_region(int min_size, int max_size) {
    for (auto r = 0; r < rows; ++r) {
        for (auto c = 0; c < cols; ++c) {
            auto region_id = picture[r][c];
            if (region_id > 0 && region_id <= max_size + 1000 && region_id > min_size + 1000) {
                cout << '*';
            } else {
                cout << '-';
            }
        }
        cout << "\n";
    }
    cout << "\n";
}

auto dfs(int r, int c, int region_id) -> int {
    if (r < 0 || r >= rows || c < 0 || c >= cols || visited[r][c] || picture[r][c] == 0)
        return 0;
    
    visited[r][c] = true;
    picture[r][c] = region_id;
    
    auto size = 1;
    size += dfs(r - 1, c, region_id);
    size += dfs(r + 1, c, region_id);
    size += dfs(r, c - 1, region_id);
    size += dfs(r, c + 1, region_id);
    
    return size;
}

int main() {
    cout << "Enter number of rows: ";
    cin >> rows;
    cout << "Enter number of columns: ";
    cin >> cols;
    cin.ignore();
    
    for (auto r = 0; r < rows; ++r) {
        auto line = "";
        getline(cin, line);
        for (auto c = 0; c < cols && c < line.size(); ++c) {
            picture[r][c] = (line[c] == '*' ? 1 : 0);
        }
    }
    
    cout << "\nOriginal Picture:\n";
    print_picture();
    
    auto region_id = 1;
    auto region_sizes = vector<int>();
    auto edge_regions = vector<bool>();
    
    for (auto r = 0; r < rows; ++r) {
        for (auto c = 0; c < cols; ++c) {
            if (picture[r][c] == 1 && !visited[r][c]) {
                auto size = dfs(r, c, region_id + 1000);
                region_sizes.push_back(size);
                
                auto touches_edge = false;
                for (auto rr = 0; rr < rows; ++rr) {
                    for (auto cc = 0; cc < cols; ++cc) {
                        if (picture[rr][cc] == region_id + 1000) {
                            if (rr == 0 || rr == rows - 1 || cc == 0 || cc == cols - 1) {
                                touches_edge = true;
                            }
                        }
                    }
                }
                edge_regions.push_back(touches_edge);
                region_id++;
            }
        }
    }
    
    cout << "Part 1: Number of distinct dark regions: " << region_sizes.size() << "\n\n";
    
    auto edge_count = 0;
    for (auto touches : edge_regions) {
        if (touches) edge_count++;
    }
    cout << "Part 2: Number of regions touching the edge: " << edge_count << "\n\n";
    
    cout << "Part 3: Pictures by region size:\n\n";
    
    cout << "Regions with 1-20 pixels:\n";
    for (auto r = 0; r < rows; ++r) {
        for (auto c = 0; c < cols; ++c) {
            auto rid = picture[r][c] - 1000;
            if (rid > 0 && rid <= region_sizes.size() && region_sizes[rid - 1] >= 1 && region_sizes[rid - 1] <= 20) {
                cout << '*';
            } else {
                cout << '-';
            }
        }
        cout << "\n";
    }
    cout << "\n";
    
    cout << "Regions with 21-40 pixels:\n";
    for (auto r = 0; r < rows; ++r) {
        for (auto c = 0; c < cols; ++c) {
            auto rid = picture[r][c] - 1000;
            if (rid > 0 && rid <= region_sizes.size() && region_sizes[rid - 1] >= 21 && region_sizes[rid - 1] <= 40) {
                cout << '*';
            } else {
                cout << '-';
            }
        }
        cout << "\n";
    }
    cout << "\n";
    
    cout << "Regions with 41-80 pixels:\n";
    for (auto r = 0; r < rows; ++r) {
        for (auto c = 0; c < cols; ++c) {
            auto rid = picture[r][c] - 1000;
            if (rid > 0 && rid <= region_sizes.size() && region_sizes[rid - 1] >= 41 && region_sizes[rid - 1] <= 80) {
                cout << '*';
            } else {
                cout << '-';
            }
        }
        cout << "\n";
    }
    cout << "\n";
    
    cout << "Regions with 80+ pixels:\n";
    for (auto r = 0; r < rows; ++r) {
        for (auto c = 0; c < cols; ++c) {
            auto rid = picture[r][c] - 1000;
            if (rid > 0 && rid <= region_sizes.size() && region_sizes[rid - 1] > 80) {
                cout << '*';
            } else {
                cout << '-';
            }
        }
        cout << "\n";
    }
    cout << "\n";
    
    return 0;
}