//* Write a C++ program for the instructions in the file lab07.md

#include <iostream>
#include <vector>
#include <string>
#include <queue>
#include <array>      // needed for std::array
#include <algorithm>  // needed for std::find

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

auto is_enclosed_region(int region_code) -> bool {
    auto seen = vector<vector<bool>>(rows, vector<bool>(cols, false));
    queue<pair<int,int>> q;
    bool touches_border = false;

    for (auto r = 0; r < rows; ++r) {
        for (auto c = 0; c < cols; ++c) {
            if (picture[r][c] != region_code) continue;
            array<pair<int,int>,4> ncoords{ pair{r-1,c}, pair{r+1,c}, pair{r,c-1}, pair{r,c+1} };
            for (auto [nr,nc] : ncoords) {
                if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) {
                    touches_border = true;
                    continue;
                }
                if (picture[nr][nc] != 0) continue;
                if (seen[nr][nc]) continue;
                seen[nr][nc] = true;
                q.push({nr,nc});
            }
        }
    }

    if (touches_border) return false;

    while (!q.empty()) {
        auto [r,c] = q.front(); q.pop();
        if (r == 0 || r == rows - 1 || c == 0 || c == cols - 1) {
            return false;
        }
        array<pair<int,int>,4> ncoords{ pair{r-1,c}, pair{r+1,c}, pair{r,c-1}, pair{r,c+1} };
        for (auto [nr,nc] : ncoords) {
            if (nr < 0 || nr >= rows || nc < 0 || nc >= cols) continue;
            if (seen[nr][nc]) continue;
            if (picture[nr][nc] != 0) continue;
            seen[nr][nc] = true;
            q.push({nr,nc});
        }
    }

    return true;
}

int main() {
    cout << "Enter number of rows: ";
    cin >> rows;
    cout << "Enter number of columns: ";
    cin >> cols;
    cin.ignore();

    for (auto r = 0; r < rows; ++r) {
        auto line = string();
        getline(cin, line);
        for (auto c = 0; c < cols && c < static_cast<int>(line.size()); ++c) {
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

    auto print_by_size = [&](int lo, int hi, bool infinity = false) {
        for (auto r = 0; r < rows; ++r) {
            for (auto c = 0; c < cols; ++c) {
                auto rid = picture[r][c] - 1000;
                if (rid > 0 && rid <= static_cast<int>(region_sizes.size())) {
                    auto sz = region_sizes[rid - 1];
                    if (infinity ? sz > lo : (sz >= lo && sz <= hi)) {
                        cout << '*';
                        continue;
                    }
                }
                cout << '-';
            }
            cout << "\n";
        }
        cout << "\n";
    };

    cout << "Regions with 1-20 pixels:\n";   print_by_size(1, 20);
    cout << "Regions with 21-40 pixels:\n";  print_by_size(21, 40);
    cout << "Regions with 41-80 pixels:\n";  print_by_size(41, 80);
    cout << "Regions with 80+ pixels:\n";    print_by_size(80, 0, true);

    cout << "Part 4: Regions totally surrounded by another dark region:\n";
    auto surrounded_region_ids = vector<int>();
    for (auto idx = 0; idx < static_cast<int>(region_sizes.size()); ++idx) {
        if (edge_regions[idx]) continue;
        auto region_code = idx + 1 + 1000;
        if (is_enclosed_region(region_code)) {
            surrounded_region_ids.push_back(region_code);
        }
    }

    auto enclosed_picture = vector<vector<char>>(rows, vector<char>(cols, '-'));
    for (auto r = 0; r < rows; ++r) {
        for (auto c = 0; c < cols; ++c) {
            auto rc = picture[r][c];
            if (find(surrounded_region_ids.begin(), surrounded_region_ids.end(), rc) != surrounded_region_ids.end()) {
                enclosed_picture[r][c] = '*';
            }
        }
    }
    for (auto r = 0; r < rows; ++r) {
        for (auto c = 0; c < cols; ++c) {
            cout << enclosed_picture[r][c];
        }
        cout << "\n";
    }
    cout << "\n";

    return 0;
}