//* Write a C++ program for the instructions in the file lab04.md

#include <bits/stdc++.h>
using namespace std;

struct ParagraphState {
    int width = 40;
    int spacing = 0;
    int indent = 0;
    int margin = 0;
    bool justify = false;
};

struct ParaConfig {
    bool start = false;
    bool pp = false;
    bool lp = false;
    bool ip = false;
    int ip_indent = 0;
    string ip_label;
};

static string trim(const string &s) {
    size_t i = 0, j = s.size();
    while (i < j && isspace((unsigned char)s[i])) i++;
    while (j > i && isspace((unsigned char)s[j-1])) j--;
    return s.substr(i, j - i);
}

int toInt(const string &s) {
    try { return stoi(s); } catch (...) { return -1; }
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(NULL);

    ParagraphState state;
    ParaConfig nextPara;
    bool inParagraph = false;
    bool inNF = false;
    bool firstOutput = true;
    int prevParaSpacing = 0;

    vector<string> curWords;
    bool firstLineInPara = false;
    int curLineIndent = 0;
    int paraIndentBase = 0;
    int paraFirstLineExtra = 0;
    bool paraHasLabel = false;
    string paraLabel;
    int paraLabelIndent = 0;

    auto flushLine = [&](bool isLastLine) {
        if (curWords.empty()) return;
        int indent = curLineIndent;
        int width = state.width;
        string out;
        // build prefix: margin, then indentation (including label if first line)
        out.append(state.margin, ' ');
        if (paraHasLabel && firstLineInPara) {
            // label at col 0 (after margin)
            out += paraLabel;
            int afterLabel = paraLabelIndent - (int)paraLabel.size();
            if (afterLabel < 0) afterLabel = 0;
            out.append(afterLabel, ' ');
            // still count full indent for width calc
        } else {
            out.append(indent, ' ');
        }
        int totalWordsLen = 0;
        for (auto &w : curWords) totalWordsLen += w.size();
        int gaps = max(0, (int)curWords.size() - 1);
        int used = indent + totalWordsLen + gaps;
        if (paraHasLabel && firstLineInPara) {
            // indent already includes label indent; no change
        }
        if (state.justify && !isLastLine && gaps > 0) {
            int spaceNeeded = width - indent - totalWordsLen;
            if (spaceNeeded < gaps) spaceNeeded = gaps;
            int base = spaceNeeded / gaps;
            int extra = spaceNeeded % gaps;
            for (int i = 0; i < (int)curWords.size(); i++) {
                out += curWords[i];
                if (i + 1 < (int)curWords.size()) {
                    int sp = base + (extra > 0 ? 1 : 0);
                    extra -= (extra > 0 ? 1 : 0);
                    out.append(sp, ' ');
                }
            }
        } else {
            for (int i = 0; i < (int)curWords.size(); i++) {
                out += curWords[i];
                if (i + 1 < (int)curWords.size()) out.push_back(' ');
            }
        }
        cout << out << "\n";
        firstOutput = false;
        if (!isLastLine && state.spacing > 0) {
            for (int i = 0; i < state.spacing; i++) cout << "\n";
        }
        curWords.clear();
    };

    auto startParagraph = [&](const ParaConfig &cfg) {
        if (inParagraph) {
            // end previous paragraph
            flushLine(true);
            if (prevParaSpacing >= 0) {
                int blank = prevParaSpacing + 1;
                for (int i = 0; i < blank; i++) cout << "\n";
            }
            prevParaSpacing = state.spacing;
        }
        inParagraph = true;
        firstLineInPara = true;
        paraIndentBase = state.indent;
        paraFirstLineExtra = 0;
        paraHasLabel = false;
        paraLabel.clear();
        paraLabelIndent = 0;
        if (cfg.pp) paraFirstLineExtra = 5;
        if (cfg.lp) paraFirstLineExtra = 0;
        if (cfg.ip) {
            paraHasLabel = true;
            paraLabel = cfg.ip_label;
            paraLabelIndent = cfg.ip_indent;
            paraIndentBase = cfg.ip_indent;
            paraFirstLineExtra = 0;
        }
    };

    auto setLineIndent = [&](bool firstLine) {
        curLineIndent = paraIndentBase + (firstLine ? paraFirstLineExtra : 0);
        if (paraHasLabel && firstLine) {
            curLineIndent = paraLabelIndent;
        }
    };

    string line;
    while (true) {
        if (!std::getline(cin, line)) break;
        if (inNF) {
            if (line.rfind(".FI", 0) == 0) {
                inNF = false;
                // resume formatting on new line
                curWords.clear();
            } else {
                cout << line << "\n";
            }
            continue;
        }
        if (!line.empty() && line[0] == '.') {
            string t = line.substr(1);
            string cmd;
            string rest;
            {
                istringstream iss(t);
                iss >> cmd;
                getline(iss, rest);
                rest = trim(rest);
            }
            if (cmd == "W") {
                int v = toInt(rest);
                if (v >= 30 && v <= 99) state.width = v;
            } else if (cmd == "PP") {
                if (!inParagraph) {
                    nextPara = {};
                    nextPara.start = true;
                    nextPara.pp = true;
                } else {
                    ParaConfig cfg; cfg.start = true; cfg.pp = true;
                    startParagraph(cfg);
                }
            } else if (cmd == "LP") {
                if (!inParagraph) {
                    nextPara = {};
                    nextPara.start = true;
                    nextPara.lp = true;
                } else {
                    ParaConfig cfg; cfg.start = true; cfg.lp = true;
                    startParagraph(cfg);
                }
            } else if (cmd == "SP") {
                int v = toInt(rest);
                if (v >= 0 && v <= 9) state.spacing = v;
            } else if (cmd == "I") {
                int v = toInt(rest);
                if (v >= 0) state.indent = v;
            } else if (cmd == "M") {
                int v = toInt(rest);
                if (v >= 0) state.margin = v;
            } else if (cmd == "JST") {
                state.justify = true;
            } else if (cmd == "NJST") {
                state.justify = false;
            } else if (cmd == "IP") {
                // format: NN <L>
                int nn = -1;
                string label;
                {
                    istringstream iss(rest);
                    iss >> nn;
                    string tmp;
                    getline(iss, tmp);
                    tmp = trim(tmp);
                    if (!tmp.empty() && tmp.front() == '<' && tmp.back() == '>') {
                        label = tmp.substr(1, tmp.size()-2);
                    }
                }
                if (nn >= 0 && !label.empty()) {
                    if (!inParagraph) {
                        nextPara = {};
                        nextPara.start = true;
                        nextPara.ip = true;
                        nextPara.ip_indent = nn;
                        nextPara.ip_label = label;
                    } else {
                        ParaConfig cfg; cfg.start = true; cfg.ip = true;
                        cfg.ip_indent = nn;
                        cfg.ip_label = label;
                        startParagraph(cfg);
                    }
                }
            } else if (cmd == "NF") {
                // begin no-format mode
                if (inParagraph) {
                    flushLine(true);
                }
                inNF = true;
            } else if (cmd == "FI") {
                // ignore if not in NF
            } else {
                // unknown command: ignore
            }
            continue;
        }
        // normal text line
        // start paragraph if needed
        if (!inParagraph) {
            if (nextPara.start) {
                startParagraph(nextPara);
                nextPara = {};
            } else {
                // no paragraph command yet; treat as default LP
                ParaConfig cfg; cfg.start = true; cfg.lp = true;
                startParagraph(cfg);
            }
        }
        if (curWords.empty()) {
            setLineIndent(firstLineInPara);
        }
        // split into words
        istringstream iss(line);
        string w;
        while (iss >> w) {
            int wordlen = w.size();
            int currentLen = curLineIndent;
            if (!curWords.empty()) currentLen += (int)curWords.size() - 1; // spaces
            for (auto &cw : curWords) currentLen += cw.size();
            int would = currentLen;
            if (!curWords.empty()) would += 1;
            would += wordlen;
            if (would > state.width) {
                flushLine(false);
                firstLineInPara = false;
                setLineIndent(false);
            }
            if (curWords.empty() && firstLineInPara) {
                setLineIndent(true);
            }
            curWords.push_back(w);
        }
    }
    if (!inNF) {
        if (!curWords.empty()) flushLine(true);
    }
    return 0;
}
