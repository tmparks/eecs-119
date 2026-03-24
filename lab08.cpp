//* Write a C++ program for the instructions in the file lab08.md

//* Refactor the code in lab08.cpp to follow the guidelines in the file style-cpp.md

//* Fix missing include directives in the file lab08.cpp

//* Refactor the code in lab08.cpp to use features of C++20

//* Fix the errors in the file lab08.cpp

#include <algorithm>
#include <array>
#include <cctype>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <ranges>
#include <sstream>
#include <string>
#include <string_view>
#include <vector>

constexpr std::size_t kMaxStudents = 100;
constexpr std::size_t kMaxAssignments = 10;
constexpr std::size_t kMaxStudentName = 30;
constexpr std::size_t kMaxAssignmentName = 6;

struct Student {
    std::string name;
    std::array<int, kMaxAssignments> scores{};
};

struct Database {
    std::vector<std::string> assignment_names;
    std::vector<Student> students;
    bool started = false;
};

static std::string trim(std::string_view s) {
    auto first = s.find_first_not_of(" \t\r\n");
    if (first == std::string_view::npos) {
        return {};
    }
    auto last = s.find_last_not_of(" \t\r\n");
    return std::string{s.substr(first, last - first + 1)};
}

static std::string to_upper(std::string_view s) {
    std::string result;
    result.reserve(s.size());
    std::ranges::transform(s, std::back_inserter(result), [](unsigned char c) {
        return static_cast<char>(std::toupper(c));
    });
    return result;
}

static bool student_exists(Database const& db, std::string_view name) {
    const auto target = to_upper(name);
    return std::ranges::any_of(db.students, [&](auto const& st) {
        return to_upper(st.name) == target;
    });
}

static std::size_t find_student(Database const& db, std::string_view name) {
    const auto target = to_upper(name);
    auto it = std::ranges::find_if(db.students, [&](auto const& st) {
        return to_upper(st.name) == target;
    });
    if (it == db.students.end()) {
        return db.students.size();
    }
    return std::distance(db.students.begin(), it);
}

static bool assignment_exists(Database const& db, std::string_view name) {
    const auto target = to_upper(name);
    return std::ranges::any_of(db.assignment_names, [&](auto const& an) {
        return to_upper(an) == target;
    });
}

static std::size_t find_assignment(Database const& db, std::string_view name) {
    const auto target = to_upper(name);
    auto it = std::ranges::find_if(db.assignment_names, [&](auto const& an) {
        return to_upper(an) == target;
    });
    if (it == db.assignment_names.end()) {
        return db.assignment_names.size();
    }
    return std::distance(db.assignment_names.begin(), it);
}

static std::string prompt_name(std::string const& prompt, std::size_t limit) {
    while (true) {
        std::cout << prompt;
        std::cout.flush();

        std::string line;
        if (!std::getline(std::cin, line)) {
            return {};
        }

        std::istringstream iss(line);
        std::string token;
        if (!(iss >> token)) {
            continue;
        }

        if (token.size() > limit) {
            token.resize(limit);
        }

        return token;
    }
}

static int prompt_int(std::string const& prompt) {
    while (true) {
        std::cout << prompt;
        std::cout.flush();

        std::string line;
        if (!std::getline(std::cin, line)) {
            continue;
        }

        std::istringstream iss(line);
        int value = 0;
        if (iss >> value) {
            return value;
        }

        std::cout << "Bad integer, try again.\n";
    }
}

static void command_new(Database& db) {
    db.assignment_names.clear();
    db.students.clear();
    db.started = true;

    std::cout << "NEW: enter student names one per line, END to finish\n";
    while (db.students.size() < kMaxStudents) {
        auto name = prompt_name("Student name: ", kMaxStudentName);
        if (to_upper(name) == "END") {
            break;
        }
        if (name.empty()) {
            continue;
        }
        if (student_exists(db, name)) {
            std::cout << "Duplicate student name.\n";
            continue;
        }
        db.students.push_back(Student{std::move(name), {}});
    }

    if (db.students.size() >= kMaxStudents) {
        std::cout << "Reached maximum number of students.\n";
    }
}

static void command_edit(Database& db) {
    std::ifstream file("recdata", std::ios::binary);
    if (!file) {
        std::cout << "EDIT: cannot open recdata\n";
        return;
    }

    int16_t n_students = 0;
    int16_t n_assignments = 0;
    file.read(reinterpret_cast<char*>(&n_students), sizeof(n_students));
    file.read(reinterpret_cast<char*>(&n_assignments), sizeof(n_assignments));

    if (!file || n_students < 0 || n_students > static_cast<int16_t>(kMaxStudents) ||
        n_assignments < 0 || n_assignments > static_cast<int16_t>(kMaxAssignments)) {
        std::cout << "EDIT: corrupted recdata\n";
        return;
    }

    db.assignment_names.clear();
    db.students.clear();

    for (int i = 0; i < n_assignments; ++i) {
        std::array<char, kMaxAssignmentName> buffer{};
        file.read(buffer.data(), buffer.size());
        std::string name{buffer.data(), buffer.size()};
        while (!name.empty() && name.back() == ' ') {
            name.pop_back();
        }
        db.assignment_names.push_back(std::move(name));
    }

    for (int i = 0; i < n_students; ++i) {
        std::array<char, kMaxStudentName> buffer{};
        file.read(buffer.data(), buffer.size());
        std::string name{buffer.data(), buffer.size()};
        while (!name.empty() && name.back() == ' ') {
            name.pop_back();
        }

        Student st;
        st.name = std::move(name);

        for (std::size_t j = 0; j < kMaxAssignments; ++j) {
            int32_t score = 0;
            file.read(reinterpret_cast<char*>(&score), sizeof(score));
            st.scores[j] = score;
        }

        db.students.push_back(std::move(st));
    }

    if (!file.good() && !file.eof()) {
        std::cout << "EDIT: read error\n";
        return;
    }

    db.started = true;
}

static void command_update(Database& db) {
    if (db.assignment_names.size() >= kMaxAssignments) {
        std::cout << "Cannot add more assignments.\n";
        return;
    }

    auto name = prompt_name("Assignment name: ", kMaxAssignmentName);
    if (name.empty()) {
        return;
    }

    if (assignment_exists(db, name)) {
        std::cout << "Duplicate assignment name. UPDATE aborted.\n";
        return;
    }

    db.assignment_names.push_back(name);
    const auto assn_idx = db.assignment_names.size() - 1;

    for (auto& student : db.students) {
        student.scores[assn_idx] = prompt_int("Score for " + student.name + ": ");
    }
}

static void command_change(Database& db) {
    auto item = prompt_name("Change (student, assignment, grade): ", 20);
    const auto item_u = to_upper(item);

    if (item_u.find("STUDENT") != std::string::npos) {
        auto old_name = prompt_name("Current student name: ", kMaxStudentName);
        const auto idx = find_student(db, old_name);
        if (idx == db.students.size()) {
            std::cout << "Student not found.\n";
            return;
        }
        auto new_name = prompt_name("New student name: ", kMaxStudentName);
        if (new_name.empty() || student_exists(db, new_name)) {
            std::cout << "Invalid new name.\n";
            return;
        }
        db.students[idx].name = std::move(new_name);

    } else if (item_u.find("ASSIGNMENT") != std::string::npos) {
        auto old_name = prompt_name("Current assignment name: ", kMaxAssignmentName);
        const auto idx = find_assignment(db, old_name);
        if (idx == db.assignment_names.size()) {
            std::cout << "Assignment not found.\n";
            return;
        }
        auto new_name = prompt_name("New assignment name: ", kMaxAssignmentName);
        if (new_name.empty() || assignment_exists(db, new_name)) {
            std::cout << "Invalid new name.\n";
            return;
        }
        db.assignment_names[idx] = std::move(new_name);

    } else if (item_u.find("GRADE") != std::string::npos) {
        auto student_name = prompt_name("Student name: ", kMaxStudentName);
        const auto sidx = find_student(db, student_name);
        if (sidx == db.students.size()) {
            std::cout << "Student not found.\n";
            return;
        }

        auto assignment_name = prompt_name("Assignment name: ", kMaxAssignmentName);
        const auto aidx = find_assignment(db, assignment_name);
        if (aidx == db.assignment_names.size()) {
            std::cout << "Assignment not found.\n";
            return;
        }

        std::cout << "Current grade: " << db.students[sidx].scores[aidx] << "\n";
        db.students[sidx].scores[aidx] = prompt_int("New grade: ");

    } else {
        std::cout << "Unknown change item.\n";
    }
}

static void command_type(Database const& db, std::ostream& out) {
    out << "Students: " << db.students.size() << "\n";
    out << "Assignments: " << db.assignment_names.size() << "\n";
    out << "Assignment names:";
    for (auto const& name : db.assignment_names) {
        out << " " << name;
    }
    out << "\n";

    for (auto const& student : db.students) {
        out << student.name;
        for (std::size_t j = 0; j < db.assignment_names.size(); ++j) {
            out << " " << student.scores[j];
        }
        out << "\n";
    }
}

static void command_list(Database const& db) {
    std::ofstream out("chardata");
    if (!out) {
        std::cout << "LIST: cannot open chardata\n";
        return;
    }
    command_type(db, out);
    std::cout << "LIST written to chardata\n";
}

static void command_save(Database const& db) {
    std::ofstream file("recdata", std::ios::binary | std::ios::trunc);
    if (!file) {
        std::cout << "SAVE: cannot open recdata\n";
        return;
    }

    const int16_t n_students = static_cast<int16_t>(db.students.size());
    const int16_t n_assignments = static_cast<int16_t>(db.assignment_names.size());

    file.write(reinterpret_cast<const char*>(&n_students), sizeof(n_students));
    file.write(reinterpret_cast<const char*>(&n_assignments), sizeof(n_assignments));

    for (auto const& asgn : db.assignment_names) {
        std::array<char, kMaxAssignmentName> buffer;
        buffer.fill(' ');
        std::copy_n(asgn.data(), std::min(asgn.size(), kMaxAssignmentName), buffer.data());
        file.write(buffer.data(), buffer.size());
    }

    for (auto const& student : db.students) {
        std::array<char, kMaxStudentName> buffer;
        buffer.fill(' ');
        std::copy_n(student.name.data(), std::min(student.name.size(), kMaxStudentName), buffer.data());
        file.write(buffer.data(), buffer.size());

        for (auto score : student.scores) {
            const int32_t sc32 = static_cast<int32_t>(score);
            file.write(reinterpret_cast<const char*>(&sc32), sizeof(sc32));
        }
    }

    if (!file.good()) {
        std::cout << "SAVE: write failed\n";
    }
}

static void command_help(std::string_view arg) {
    static const std::map<std::string, std::string> help_text = {
        {"NEW", "NEW - build a new database."},
        {"EDIT", "EDIT - load database from recdata."},
        {"UPDATE", "UPDATE - add assignment and grades."},
        {"CHANGE", "CHANGE - modify student/assignment/grade."},
        {"SAVE", "SAVE - persist database to recdata."},
        {"TYPE", "TYPE - display database on screen."},
        {"LIST", "LIST - write database to chardata."},
        {"HELP", "HELP - show this message."},
        {"QUIT", "QUIT - exit program."},
    };

    if (arg.empty()) {
        std::cout << "Commands: NEW EDIT UPDATE CHANGE SAVE TYPE LIST HELP QUIT\n";
        std::cout << "Use HELP <command> for details.\n";
        return;
    }

    const auto key = to_upper(arg);
    if (auto it = help_text.find(key); it != help_text.end()) {
        std::cout << it->second << "\n";
        std::cout << "Usage: " << key << " ...\n";
        return;
    }

    std::cout << "Commands: NEW EDIT UPDATE CHANGE SAVE TYPE LIST HELP QUIT\n";
    std::cout << "Use HELP <command> for details.\n";
}

int main() {
    Database db;
    std::cout << "type 'HELP' help for instructions\n";

    for (std::string line; std::cout << "\nCommand: ", std::getline(std::cin, line);) {
        const auto trimmed = trim(line);
        if (trimmed.empty()) {
            continue;
        }

        std::istringstream iss(trimmed);
        std::string command;
        iss >> command;
        if (command.empty()) {
            continue;
        }
        std::string arg;
        iss >> arg;

        const auto ucmd = to_upper(command);
        if (!db.started && ucmd != "NEW" && ucmd != "EDIT" && ucmd != "HELP") {
            std::cout << "Session not started. Use NEW or EDIT first.\n";
            continue;
        }

        if (ucmd == "NEW") {
            command_new(db);
        } else if (ucmd == "EDIT") {
            command_edit(db);
        } else if (ucmd == "UPDATE") {
            command_update(db);
        } else if (ucmd == "CHANGE") {
            command_change(db);
        } else if (ucmd == "SAVE") {
            command_save(db);
        } else if (ucmd == "TYPE") {
            command_type(db, std::cout);
        } else if (ucmd == "LIST") {
            command_list(db);
        } else if (ucmd == "HELP") {
            command_help(arg);
        } else if (ucmd == "QUIT") {
            const auto answer = prompt_name("Save before quitting? (yes/no): ", 4);
            const auto ans_u = to_upper(answer);
            if (ans_u == "YES" || ans_u == "Y") {
                command_save(db);
            }
            break;
        } else {
            std::cout << "Illegal command.\n";
        }
    }

    return 0;
}