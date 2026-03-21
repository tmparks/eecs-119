//* Write a C++ program for the instructions in the file lab08.md

#include <bits/stdc++.h>
using namespace std;

const int MAX_STUDENTS = 100;
const int MAX_ASSIGNMENTS = 10;
const int MAX_STUDENT_NAME = 30;
const int MAX_ASSIGN_NAME = 6;

struct Student {
    string name;
    int scores[MAX_ASSIGNMENTS];
};

vector<string> asgn_names;
vector<Student> students;
bool session_started = false;

string trim(const string& s) {
    size_t a = s.find_first_not_of(" \t\r\n");
    if (a == string::npos) return "";
    size_t b = s.find_last_not_of(" \t\r\n");
    return s.substr(a, b - a + 1);
}

string to_upper(const string& s) {
    string out = s;
    for (char& c : out) c = toupper((unsigned char)c);
    return out;
}

bool student_exists(const string& name) {
    for (auto& st : students)
        if (to_upper(st.name) == to_upper(name))
            return true;
    return false;
}

int student_index(const string& name) {
    for (int i = 0; i < (int)students.size(); i++)
        if (to_upper(students[i].name) == to_upper(name))
            return i;
    return -1;
}

bool assignment_exists(const string& name) {
    for (auto& as : asgn_names)
        if (to_upper(as) == to_upper(name))
            return true;
    return false;
}

int assignment_index(const string& name) {
    for (int i = 0; i < (int)asgn_names.size(); i++)
        if (to_upper(asgn_names[i]) == to_upper(name))
            return i;
    return -1;
}

string name_input(const string& prompt, int limit) {
    while (true) {
        cout << prompt;
        cout.flush();
        string line;
        if (!getline(cin, line)) return "";
        istringstream iss(line);
        string w;
        if (!(iss >> w)) continue;
        if ((int)w.size() > limit)
            w = w.substr(0, limit);
        return w;
    }
}

int int_input(const string& prompt) {
    while (true) {
        cout << prompt;
        cout.flush();
        string line;
        if (!getline(cin, line)) continue;
        istringstream iss(line);
        int v;
        if (iss >> v) return v;
        cout << "Bad integer, try again.\n";
    }
}

void cmd_new() {
    students.clear();
    asgn_names.clear();
    session_started = true;
    cout << "NEW: Enter student names, one per line, 'END' to finish.\n";
    while (true) {
        if ((int)students.size() >= MAX_STUDENTS) {
            cout << "Reached maximum number of students (" << MAX_STUDENTS << ").\n";
            break;
        }
        string name = name_input("Student name: ", MAX_STUDENT_NAME);
        if (to_upper(name) == "END") break;
        if (name.empty()) continue;
        if (student_exists(name)) {
            cout << "Duplicate student name. Try again.\n";
            continue;
        }
        Student st;
        st.name = name;
        for (int i = 0; i < MAX_ASSIGNMENTS; i++) st.scores[i] = 0;
        students.push_back(st);
    }
    cout << "NEW complete. " << students.size() << " students.\n";
}

void cmd_edit() {
    ifstream f("recdata", ios::binary);
    if (!f) {
        cout << "EDIT: cannot open recdata file.\n";
        return;
    }
    int16_t nst, nasgn;
    f.read((char*)&nst, sizeof(nst));
    f.read((char*)&nasgn, sizeof(nasgn));
    if (!f || nst < 0 || nst > MAX_STUDENTS || nasgn < 0 || nasgn > MAX_ASSIGNMENTS) {
        cout << "EDIT: recdata corrupted or invalid.\n";
        return;
    }
    students.clear();
    asgn_names.clear();
    for (int i = 0; i < nasgn; i++) {
        char an[MAX_ASSIGN_NAME];
        f.read(an, MAX_ASSIGN_NAME);
        string s(an, MAX_ASSIGN_NAME);
        while (!s.empty() && s.back() == ' ') s.pop_back();
        asgn_names.push_back(s);
    }
    for (int i = 0; i < nst; i++) {
        char nm[MAX_STUDENT_NAME];
        f.read(nm, MAX_STUDENT_NAME);
        Student st;
        st.name = string(nm, MAX_STUDENT_NAME);
        while (!st.name.empty() && st.name.back() == ' ') st.name.pop_back();
        for (int j = 0; j < MAX_ASSIGNMENTS; j++) {
            int32_t sc;
            f.read((char*)&sc, sizeof(sc));
            st.scores[j] = sc;
        }
        students.push_back(st);
    }
    if (!f.good() && !f.eof()) {
        cout << "EDIT: error reading recdata.\n";
        return;
    }
    session_started = true;
    cout << "EDIT complete. " << students.size() << " students, "
         << asgn_names.size() << " assignments.\n";
}

void cmd_update() {
    if ((int)asgn_names.size() >= MAX_ASSIGNMENTS) {
        cout << "Maximum assignments reached.\n";
        return;
    }
    string name = name_input("Assignment name: ", MAX_ASSIGN_NAME);
    if (name.empty()) { cout << "No assignment name provided.\n"; return; }
    if (assignment_exists(name)) {
        cout << "Duplicate assignment name; update aborted.\n";
        return;
    }
    asgn_names.push_back(name);
    int idx = asgn_names.size() - 1;
    for (auto& st : students) {
        int grade = int_input("Enter grade for " + st.name + ": ");
        st.scores[idx] = grade;
    }
    cout << "UPDATE complete.\n";
}

void cmd_change() {
    string item = name_input("Change student name, grade, or assignment? ", 20);
    string upitem = to_upper(item);
    if (upitem == "STUDENT" || upitem == "STUDENT NAME") {
        string oldn = name_input("Current student name: ", MAX_STUDENT_NAME);
        int idx = student_index(oldn);
        if (idx < 0) { cout << "Student not found. CHANGE aborted.\n"; return; }
        string newn = name_input("New student name: ", MAX_STUDENT_NAME);
        if (newn.empty()) { cout << "No new name. CHANGE aborted.\n"; return; }
        if (student_exists(newn)) { cout << "Duplicate name. CHANGE aborted.\n"; return; }
        students[idx].name = newn;
        cout << "Student name changed.\n";
    } else if (upitem == "ASSIGNMENT" || upitem == "ASSIGNMENT NAME") {
        string oldn = name_input("Current assignment name: ", MAX_ASSIGN_NAME);
        int idx = assignment_index(oldn);
        if (idx < 0) { cout << "Assignment not found. CHANGE aborted.\n"; return; }
        string newn = name_input("New assignment name: ", MAX_ASSIGN_NAME);
        if (newn.empty()) { cout << "No new name. CHANGE aborted.\n"; return; }
        if (assignment_exists(newn)) { cout << "Duplicate assignment name. CHANGE aborted.\n"; return; }
        asgn_names[idx] = newn;
        cout << "Assignment name changed.\n";
    } else if (upitem == "GRADE") {
        string stn = name_input("Student name: ", MAX_STUDENT_NAME);
        int si = student_index(stn);
        if (si < 0) { cout << "Student not found. CHANGE aborted.\n"; return; }
        string an = name_input("Assignment name: ", MAX_ASSIGN_NAME);
        int ai = assignment_index(an);
        if (ai < 0) { cout << "Assignment not found. CHANGE aborted.\n"; return; }
        cout << "Current grade: " << students[si].scores[ai] << "\n";
        int ng = int_input("New grade: ");
        students[si].scores[ai] = ng;
        cout << "Grade changed.\n";
    } else {
        cout << "Unknown CHANGE item. Aborted.\n";
    }
}

void cmd_type(ostream& out) {
    out << "Number of students: " << students.size() << "\n";
    out << "Number of assignments: " << asgn_names.size() << "\n";
    out << "Assignments:";
    for (auto& a: asgn_names) out << " " << a;
    out << "\n";
    out << "----------------------------------------\n";
    for (auto& st : students) {
        out << st.name;
        for (int j = 0; j < (int)asgn_names.size(); j++) {
            out << " " << st.scores[j];
        }
        out << "\n";
    }
}

void cmd_list() {
    ofstream out("chardata");
    if (!out) {
        cout << "Could not open chardata for LIST.\n";
        return;
    }
    cmd_type(out);
    cout << "LIST output written to chardata.\n";
}

void cmd_save() {
    ofstream f("recdata", ios::binary | ios::trunc);
    if (!f) { cout << "Could not open recdata for SAVE.\n"; return; }
    int16_t nst = (int16_t)students.size();
    int16_t nasgn = (int16_t)asgn_names.size();
    f.write((char*)&nst, sizeof(nst));
    f.write((char*)&nasgn, sizeof(nasgn));
    for (int i = 0; i < nasgn; i++) {
        char an[MAX_ASSIGN_NAME];
        memset(an, ' ', sizeof(an));
        string s = asgn_names[i];
        memcpy(an, s.c_str(), min((size_t)MAX_ASSIGN_NAME, s.size()));
        f.write(an, sizeof(an));
    }
    for (int i = 0; i < nst; i++) {
        char nm[MAX_STUDENT_NAME];
        memset(nm, ' ', sizeof(nm));
        string s = students[i].name;
        memcpy(nm, s.c_str(), min((size_t)MAX_STUDENT_NAME, s.size()));
        f.write(nm, sizeof(nm));
        for (int j = 0; j < MAX_ASSIGNMENTS; j++) {
            int32_t sc = students[i].scores[j];
            f.write((char*)&sc, sizeof(sc));
        }
    }
    if (!f.good()) {
        cout << "Error writing recdata.\n";
        return;
    }
    cout << "SAVE complete.\n";
}

void cmd_help(const string& arg) {
    map<string, string> helpText {
        {"NEW", "NEW: create new database (students)."},
        {"EDIT", "EDIT: load database from recdata file."},
        {"UPDATE", "UPDATE: new assignment + grades for each student."},
        {"CHANGE", "CHANGE: modify student name, assignment name, or grade."},
        {"SAVE", "SAVE: write database to recdata file."},
        {"TYPE", "TYPE: show current database to screen."},
        {"LIST", "LIST: write current database to chardata file."},
        {"HELP", "HELP: show commands help."},
        {"QUIT", "QUIT: exit, ask to SAVE first."}
    };
    if (arg.empty()) {
        cout << "Available commands: NEW EDIT UPDATE CHANGE SAVE TYPE LIST HELP QUIT\n";
        cout << "Type 'HELP <command>' for a two-line explanation.\n";
        return;
    }
    string uarg = to_upper(arg);
    if (helpText.count(uarg) == 0) {
        cout << "Available commands: NEW EDIT UPDATE CHANGE SAVE TYPE LIST HELP QUIT\n";
        cout << "Type 'HELP <command>' for a two-line explanation.\n";
        return;
    }
    cout << helpText[uarg] << "\n";
    cout << "Usage: " << uarg << " ... (see assignment spec) \n";
}

int main() {
    cout << "type 'HELP' help for instructions\n";
    string line;
    while (true) {
        cout << "\nCommand: ";
        cout.flush();
        if (!getline(cin, line)) break;
        line = trim(line);
        if (line.empty()) continue;
        istringstream iss(line);
        string cmd;
        iss >> cmd;
        if (cmd.empty()) continue;
        string arg;
        iss >> arg;
        string ucmd = to_upper(cmd);

        if (!session_started && ucmd != "NEW" && ucmd != "EDIT" && ucmd != "HELP") {
            cout << "Session not started. Use NEW or EDIT first.\n";
            continue;
        }

        if (ucmd == "NEW") {
            cmd_new();
        } else if (ucmd == "EDIT") {
            cmd_edit();
        } else if (ucmd == "UPDATE") {
            cmd_update();
        } else if (ucmd == "CHANGE") {
            cmd_change();
        } else if (ucmd == "SAVE") {
            cmd_save();
        } else if (ucmd == "TYPE") {
            cmd_type(cout);
        } else if (ucmd == "LIST") {
            cmd_list();
        } else if (ucmd == "HELP") {
            cmd_help(arg);
        } else if (ucmd == "QUIT") {
            string ans = name_input("Do you want to SAVE before quitting? (yes/no): ", 10);
            string uans = to_upper(ans);
            if (uans == "Y" || uans == "YES") cmd_save();
            cout << "Goodbye.\n";
            break;
        } else {
            cout << "Illegal command: " << cmd << ".\n";
        }
    }
    return 0;
}