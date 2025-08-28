# Programming Assignment 1
## Part Three

Write a program that reads a sequence of words from a file and prints them (on
the terminal or another file) as they are read except that:

1.  line breaks in the input are ignored
2.  only one blank is printed between two words in the same line
3.  a new output line is started after any word that starts with r, s or t.

The program should terminate when the character '%' is encountered. For the
purpose of this assignment a word is any sequence of non blank characters except
'%'.

To illustrate, let us represent a blank character by •. (Of course, your
program will read and write real blanks.) If the input is:

    this•is•••the•time•for•all•good•persons•to•come••
    running••to•the•aid•of•Inspector••••••Clouzot%

the output should be

    this
    is•the
    time
    for•all•good•persons•to
    come•running
    to
    the
    aid•of•Inspector•Clouzot
