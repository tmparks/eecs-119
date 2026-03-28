#include <iostream>
#include <vector>
#include <list>
#include <string>
#include <sstream>
#include <cmath>
#include <algorithm>
#include <limits>

struct Point {
    double x{0.0};
    double y{0.0};
};

struct Polygon {
    std::list<Point> points{};
};

struct Scene {
    std::vector<Polygon> polygons{};
};

auto distance(const Point& a, const Point& b) -> double {
    auto dx = a.x - b.x;
    auto dy = a.y - b.y;
    return std::sqrt(dx * dx + dy * dy);
}

auto distance_to_segment(const Point& p, const Point& a, const Point& b) -> double {
    auto abx = b.x - a.x;
    auto aby = b.y - a.y;
    auto apx = p.x - a.x;
    auto apy = p.y - a.y;
    auto ab2 = abx * abx + aby * aby;
    if (ab2 == 0.0) {
        return distance(p, a);
    }
    auto proj = (apx * abx + apy * aby) / ab2;
    if (proj < 0.0) {
        return distance(p, a);
    }
    if (proj > 1.0) {
        return distance(p, b);
    }
    auto px = a.x + proj * abx;
    auto py = a.y + proj * aby;
    return distance(p, {px, py});
}

auto is_inside(const Point& p, const Polygon& poly) -> bool {
    auto count = 0;
    if (poly.points.empty()) {
        return false;
    }
    auto it = poly.points.begin();
    auto prev = *it;
    ++it;
    for (; it != poly.points.end(); ++it) {
        auto curr = *it;
        if ((prev.y <= p.y && curr.y > p.y) || (prev.y > p.y && curr.y <= p.y)) {
            auto denom = curr.y - prev.y;
            if (denom != 0.0) {
                auto xinters = prev.x + (p.y - prev.y) / denom * (curr.x - prev.x);
                if (p.x < xinters) {
                    ++count;
                }
            }
        }
        prev = curr;
    }
    // close the polygon
    auto curr = *poly.points.begin();
    if ((prev.y <= p.y && curr.y > p.y) || (prev.y > p.y && curr.y <= p.y)) {
        auto denom = curr.y - prev.y;
        if (denom != 0.0) {
            auto xinters = prev.x + (p.y - prev.y) / denom * (curr.x - prev.x);
            if (p.x < xinters) {
                ++count;
            }
        }
    }
    return count % 2 == 1;
}

auto distance_to_polygon(const Point& p, const Polygon& poly) -> double {
    if (is_inside(p, poly)) {
        return 0.0;
    }
    auto min_dist = std::numeric_limits<double>::max();
    if (poly.points.empty()) {
        return min_dist;
    }
    auto it = poly.points.begin();
    auto prev = *it;
    ++it;
    for (; it != poly.points.end(); ++it) {
        min_dist = std::min(min_dist, distance_to_segment(p, prev, *it));
        prev = *it;
    }
    // close the polygon
    min_dist = std::min(min_dist, distance_to_segment(p, prev, *poly.points.begin()));
    return min_dist;
}

auto main() -> int {
    Scene scene{};
    Polygon rect{};
    rect.points = {{0.0, 0.0}, {100.0, 0.0}, {100.0, 100.0}, {0.0, 100.0}};
    scene.polygons.push_back(rect);

    auto line = std::string{};
    while (std::getline(std::cin, line)) {
        auto iss = std::istringstream{line};
        auto cmd = std::string{};
        iss >> cmd;
        if (cmd == "q") {
            break;
        } else if (cmd == "h") {
            std::cout << "Commands:\n";
            std::cout << "A n x1 y1 ... xn yn - add polygon\n";
            std::cout << "D x1 y1 - delete closest polygon\n";
            std::cout << "a x1 y1 - add point to closest polygon\n";
            std::cout << "d x1 y1 - delete closest point\n";
            std::cout << "F x1 y1 - find closest polygon\n";
            std::cout << "f x1 y1 - find closest point\n";
            std::cout << "L n - list polygons with n vertices\n";
            std::cout << "L * - list all polygons\n";
            std::cout << "C n - list polygons with n vertices and vertices\n";
            std::cout << "C * - list all polygons and vertices\n";
            std::cout << "l - list all vertices\n";
            std::cout << "h - help\n";
            std::cout << "q - quit\n";
        } else if (cmd == "A") {
            auto n = 0;
            iss >> n;
            auto poly = Polygon{};
            for (auto i = 0; i < n; ++i) {
                auto x = 0.0;
                auto y = 0.0;
                iss >> x >> y;
                poly.points.push_back({x, y});
            }
            scene.polygons.push_back(poly);
        } else if (cmd == "D") {
            auto x = 0.0;
            auto y = 0.0;
            iss >> x >> y;
            auto p = Point{x, y};
            if (scene.polygons.empty()) {
                std::cout << "No polygons to delete.\n";
                continue;
            }
            auto closest_idx = size_t{0};
            auto min_dist = distance_to_polygon(p, scene.polygons[0]);
            for (auto i = size_t{1}; i < scene.polygons.size(); ++i) {
                auto d = distance_to_polygon(p, scene.polygons[i]);
                if (d < min_dist) {
                    min_dist = d;
                    closest_idx = i;
                }
            }
            if (scene.polygons.size() == 1) {
                std::cout << "Warning: Deleting the only polygon.\n";
            }
            scene.polygons.erase(scene.polygons.begin() + static_cast<std::ptrdiff_t>(closest_idx));
        } else if (cmd == "a") {
            auto x = 0.0;
            auto y = 0.0;
            iss >> x >> y;
            auto p = Point{x, y};
            if (scene.polygons.empty()) {
                std::cout << "No polygons.\n";
                continue;
            }
            auto closest_idx = size_t{0};
            auto min_dist = distance_to_polygon(p, scene.polygons[0]);
            for (auto i = size_t{1}; i < scene.polygons.size(); ++i) {
                auto d = distance_to_polygon(p, scene.polygons[i]);
                if (d < min_dist) {
                    min_dist = d;
                    closest_idx = i;
                }
            }
            scene.polygons[closest_idx].points.push_back(p);
        } else if (cmd == "d") {
            auto x = 0.0;
            auto y = 0.0;
            iss >> x >> y;
            auto p = Point{x, y};
            auto min_dist = std::numeric_limits<double>::max();
            auto poly_idx = size_t{0};
            auto point_it = scene.polygons[0].points.begin();
            auto found = false;
            for (auto i = size_t{0}; i < scene.polygons.size(); ++i) {
                for (auto it = scene.polygons[i].points.begin(); it != scene.polygons[i].points.end(); ++it) {
                    auto d = distance(p, *it);
                    if (d < min_dist) {
                        min_dist = d;
                        poly_idx = i;
                        point_it = it;
                        found = true;
                    }
                }
            }
            if (!found) {
                std::cout << "No points.\n";
                continue;
            }
            scene.polygons[poly_idx].points.erase(point_it);
            if (scene.polygons[poly_idx].points.size() < 3) {
                scene.polygons.erase(scene.polygons.begin() + static_cast<std::ptrdiff_t>(poly_idx));
            }
        } else if (cmd == "F") {
            auto x = 0.0;
            auto y = 0.0;
            iss >> x >> y;
            auto p = Point{x, y};
            if (scene.polygons.empty()) {
                std::cout << "No polygons.\n";
                continue;
            }
            auto closest_idx = size_t{0};
            auto min_dist = distance_to_polygon(p, scene.polygons[0]);
            for (auto i = size_t{1}; i < scene.polygons.size(); ++i) {
                auto d = distance_to_polygon(p, scene.polygons[i]);
                if (d < min_dist) {
                    min_dist = d;
                    closest_idx = i;
                }
            }
            std::cout << "Closest polygon: " << closest_idx << " at distance " << min_dist << "\n";
        } else if (cmd == "f") {
            auto x = 0.0;
            auto y = 0.0;
            iss >> x >> y;
            auto p = Point{x, y};
            auto min_dist = std::numeric_limits<double>::max();
            auto closest_pt = Point{0.0, 0.0};
            auto found = false;
            for (const auto& poly : scene.polygons) {
                for (const auto& pt : poly.points) {
                    auto d = distance(p, pt);
                    if (d < min_dist) {
                        min_dist = d;
                        closest_pt = pt;
                        found = true;
                    }
                }
            }
            if (!found) {
                std::cout << "No points.\n";
            } else {
                std::cout << "Closest point: (" << closest_pt.x << ", " << closest_pt.y << ") at distance " << min_dist << "\n";
            }
        } else if (cmd == "L") {
            auto arg = std::string{};
            iss >> arg;
            if (arg == "*") {
                for (auto i = size_t{0}; i < scene.polygons.size(); ++i) {
                    std::cout << "Polygon " << i << ": " << scene.polygons[i].points.size() << " vertices\n";
                }
            } else {
                auto n = std::stoi(arg);
                for (auto i = size_t{0}; i < scene.polygons.size(); ++i) {
                    if (static_cast<int>(scene.polygons[i].points.size()) == n) {
                        std::cout << "Polygon " << i << ": " << n << " vertices\n";
                    }
                }
            }
        } else if (cmd == "C") {
            auto arg = std::string{};
            iss >> arg;
            if (arg == "*") {
                for (auto i = size_t{0}; i < scene.polygons.size(); ++i) {
                    std::cout << "Polygon " << i << ":\n";
                    for (const auto& pt : scene.polygons[i].points) {
                        std::cout << "  (" << pt.x << ", " << pt.y << ")\n";
                    }
                }
            } else {
                auto n = std::stoi(arg);
                for (auto i = size_t{0}; i < scene.polygons.size(); ++i) {
                    if (static_cast<int>(scene.polygons[i].points.size()) == n) {
                        std::cout << "Polygon " << i << ":\n";
                        for (const auto& pt : scene.polygons[i].points) {
                            std::cout << "  (" << pt.x << ", " << pt.y << ")\n";
                        }
                    }
                }
            }
        } else if (cmd == "l") {
            for (auto i = size_t{0}; i < scene.polygons.size(); ++i) {
                std::cout << "Polygon " << i << ":\n";
                for (const auto& pt : scene.polygons[i].points) {
                    std::cout << "  (" << pt.x << ", " << pt.y << ")\n";
                }
            }
        } else {
            std::cout << "Invalid command. Type h for help.\n";
        }
    }
    return 0;
}