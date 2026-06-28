#include <algorithm>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <numeric>
#include <sstream>
#include <string>
#include <vector>

struct Coordinate {
    int lon_deg{0};
    int lon_min{0};
    int lat_deg{0};
    int lat_min{0};
};

struct SeedRng {
    double state{0.0};

    auto ran() -> double {
        auto i = static_cast<int>(1061.0 * std::trunc(state * 1048576.0) + 221589.0)
                 % 1048576;
        state = static_cast<double>(i) / 1048576.0;
        return state;
    }

    auto integer(int k) -> int {
        return 1 + static_cast<int>(std::trunc(ran() * static_cast<double>(k)));
    }
};

auto to_decimal_degrees(int degrees, int minutes) -> double {
    return static_cast<double>(degrees) + static_cast<double>(minutes) / 60.0;
}

auto degrees_to_radians(double degrees) -> double {
    return degrees * (M_PI / 180.0);
}

auto great_circle_distance(int i, int j,
                           std::vector<std::vector<int>> const& unused) -> int;

auto build_distance_matrix(std::vector<Coordinate> const& coordinates)
    -> std::vector<std::vector<int>> {
    const auto n = coordinates.size();
    auto dist = std::vector<std::vector<int>>(n, std::vector<int>(n, 0));
    for (auto i = std::size_t{0}; i < n; ++i) {
        for (auto j = i + 1; j < n; ++j) {
            auto lon1 = to_decimal_degrees(coordinates[i].lon_deg,
                                           coordinates[i].lon_min);
            auto lat1 = to_decimal_degrees(coordinates[i].lat_deg,
                                           coordinates[i].lat_min);
            auto lon2 = to_decimal_degrees(coordinates[j].lon_deg,
                                           coordinates[j].lon_min);
            auto lat2 = to_decimal_degrees(coordinates[j].lat_deg,
                                           coordinates[j].lat_min);

            auto b = degrees_to_radians(90.0 - lat1);
            auto c = degrees_to_radians(90.0 - lat2);
            auto a_long = degrees_to_radians(std::fabs(lon1 - lon2));

            auto cos_a = std::cos(b) * std::cos(c)
                         + std::sin(b) * std::sin(c) * std::cos(a_long);
            cos_a = std::clamp(cos_a, -1.0, 1.0);

            auto const earth_radius = 3959.0;
            auto const miles = std::acos(cos_a) * earth_radius;
            auto rounded = static_cast<int>(std::lround(miles));
            dist[i][j] = rounded;
            dist[j][i] = rounded;
        }
    }
    return dist;
}

auto tour_cost(std::vector<int> const& tour,
               std::vector<std::vector<int>> const& dist) -> int {
    auto cost = 0;
    const auto n = tour.size();
    for (auto i = std::size_t{0}; i < n; ++i) {
        auto const a = tour[i];
        auto const b = tour[(i + 1) % n];
        cost += dist[a][b];
    }
    return cost;
}

auto two_opt(std::vector<int>& tour,
             std::vector<std::vector<int>> const& dist) -> void {
    const auto n = tour.size();
    if (n < 4) {
        return;
    }

    auto improved = true;
    while (improved) {
        improved = false;
        for (auto i = std::size_t{0}; i + 2 < n; ++i) {
            for (auto j = i + 2; j < n; ++j) {
                if (i == 0 && j + 1 == n) {
                    continue;
                }

                auto const a = tour[i];
                auto const b = tour[i + 1];
                auto const c = tour[j];
                auto const d = tour[(j + 1) % n];

                auto delta = dist[a][c] + dist[b][d]
                             - dist[a][b] - dist[c][d];
                if (delta < 0) {
                    std::reverse(tour.begin() + static_cast<std::ptrdiff_t>(i + 1),
                                 tour.begin() + static_cast<std::ptrdiff_t>(j + 1));
                    improved = true;
                    break;
                }
            }
            if (improved) {
                break;
            }
        }
    }
}

auto random_tour(int city_count, SeedRng& rng) -> std::vector<int> {
    auto tour = std::vector<int>(city_count);
    std::iota(tour.begin(), tour.end(), 0);

    for (auto i = city_count - 1; i > 1; --i) {
        auto const j = rng.integer(i);
        std::swap(tour[static_cast<std::size_t>(i)],
                  tour[static_cast<std::size_t>(j)]);
    }

    return tour;
}

auto print_tour(std::vector<int> const& tour) -> void {
    for (auto const city : tour) {
        std::cout << (city + 1) << " ";
    }
    std::cout << '\n';
}

auto show_usage(char const* program_name) -> void {
    std::cout << "Usage: " << program_name
              << " [seed] [city-count] [trials]\n"
                 "  seed        : floating point value between 0 and 1\n"
                 "  city-count  : 10 or 52 (default 52)\n"
                 "  trials      : number of random starts (default 3)\n";
}

auto main(int argc, char* argv[]) -> int {
    const auto coordinates = std::vector<Coordinate>{
        {74, 1, 40, 47},
        {75, 55, 42, 6},
        {80, 0, 40, 27},
        {75, 15, 41, 34},
        {82, 33, 35, 36},
        {74, 39, 40, 21},
        {122, 54, 47, 2},
        {81, 31, 41, 5},
        {122, 10, 37, 26},
        {78, 38, 35, 47},
        {75, 32, 39, 9},
        {73, 56, 42, 49},
        {111, 56, 33, 26},
        {131, 42, 55, 22},
        {86, 18, 32, 21},
        {83, 19, 36, 51},
        {77, 6, 38, 53},
        {98, 29, 29, 25},
        {104, 59, 39, 45},
        {121, 30, 38, 35},
        {71, 23, 41, 53},
        {80, 9, 26, 0},
        {84, 23, 33, 46},
        {76, 18, 36, 51},
        {94, 23, 40, 24},
        {91, 22, 39, 42},
        {83, 3, 42, 20},
        {88, 26, 42, 35},
        {92, 17, 30, 0},
        {73, 52, 41, 9},
        {78, 14, 39, 37},
        {93, 58, 44, 19},
        {95, 23, 29, 45},
        {111, 37, 42, 39},
        {74, 45, 41, 48},
        {89, 39, 39, 49},
        {155, 5, 19, 44},
        {86, 23, 35, 51},
        {111, 40, 40, 14},
        {68, 0, 46, 52},
        {106, 13, 41, 54},
        {96, 55, 35, 20},
        {67, 6, 18, 23},
        {110, 28, 40, 11},
        {100, 4, 45, 44},
        {98, 52, 48, 7},
        {91, 51, 33, 56},
        {80, 50, 32, 41},
        {77, 9, 39, 5},
        {120, 12, 45, 0},
    };

    if (argc > 4) {
        show_usage(argv[0]);
        return 1;
    }

    auto seed = 0.123456;
    auto city_count = 52;
    auto trials = 3;

    if (argc >= 2) {
        seed = std::stod(argv[1]);
        if (seed <= 0.0 || seed >= 1.0) {
            std::cerr << "Seed must be greater than 0 and less than 1.\n";
            return 1;
        }
    }

    if (argc >= 3) {
        city_count = std::stoi(argv[2]);
        if (city_count != 10 && city_count != 52) {
            std::cerr << "City count must be 10 or 52.\n";
            return 1;
        }
    }

    if (argc == 4) {
        trials = std::stoi(argv[3]);
        if (trials < 1) {
            std::cerr << "Trials must be positive.\n";
            return 1;
        }
    }

    const auto active_coordinates =
        std::vector<Coordinate>(coordinates.begin(),
                                coordinates.begin() + city_count);
    const auto dist = build_distance_matrix(active_coordinates);

    std::cout << "Computed " << city_count << "-city distance matrix.\n";

    auto best_cost = std::numeric_limits<int>::max();
    auto best_tour = std::vector<int>{};

    for (auto t = 0; t < trials; ++t) {
        auto rng = SeedRng{seed + static_cast<double>(t) * 0.1234};
        auto tour = random_tour(city_count, rng);
        two_opt(tour, dist);
        auto const cost = tour_cost(tour, dist);

        std::cout << "Trial " << (t + 1) << " seed="
                  << std::fixed << std::setprecision(6)
                  << (seed + static_cast<double>(t) * 0.1234)
                  << " cost=" << cost << '\n';

        if (cost < best_cost) {
            best_cost = cost;
            best_tour = tour;
        }
    }

    std::cout << "Best cost = " << best_cost << '\n';
    std::cout << "Best tour (1-based city numbers):\n";
    print_tour(best_tour);

    return 0;
}
