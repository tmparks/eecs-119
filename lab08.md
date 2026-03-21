# Assignment 8

The goal of this assignment is to make you familiar with the use of files, as
well as with problems involved in the design of an interactive program. As the
problem to solve we have chosen a simplified version of the program used to keep
course grades.

## General Outline of the Program

The solution to this assignment is a program to be run from a terminal. The
program will execute commands typed by the user regarding the creation,
maintenance and updating of a small database containing course grades for a
number of students.

The database will contain the following generic information:
* The number of students in the course.
* The number of assignments graded so far.
* The names of those assignments.

In addition it will contain specific information for each student. This
information will be simply
* The student name.
* The grades for the student.

The program should be able to execute the following commands:

<dl>
<dt>NEW</dt>
<dd>The user wishes to forget all about the current content of the database and
create a new one. (it may mean also that there isn't any database and she wants
to create one.) the program should repeatedly prompt the user for student names
until the word “END” is entered instead of a student name. Each name provided by
the user should be checked against all the previously entered names to insure
that it is unique. Repeated names should be rejected by the program. The number
of graded assignments should be set to zero and all previously recorded grades
discarded.</dd>

<dt>EDIT</dt>
<dd>The user wants to edit the database left by the last session. The program
should read the data from the disk (more information later) overwriting whatever
information may be currently in memory. Every session must start with a “NEW” or
an “EDIT” commands. Unless one of these two commands is issued none of the
others makes any sense.</dd>

<dt>UPDATE</dt>
<dd>The user wants to enter the grades for a new assignment. The program should
prompt the user for the name of the assignment and after obtaining the name and
checking that it is different from the names of all other assignments stored, it
should run through the list of students printing the name of each student on the
terminal and asking the user to provide the corresponding grade. If the
assignment name given by the user has already been used, a warning message
should be printed and the command execution terminated.</dd>

<dt>CHANGE</dt>
<dd>The user wants to perform some small change in data currently in memory.
The program should ask the user whether she wants to change a <i>student
name</i>, a <i>grade</i> or an <i>assignment name</i>. If the item to be changed
is a name (student or assignment) the program should ask for the currently
stored name, and if found, request the new name to be stored in its place. The
program should refuse to store new names which are identical to names that have
been stored previously. If the item to be changed is a grade, the program should
prompt the user for the name of the student and the name of the assignment. If
both pieces of data match items in the current database, the program should
print the currently stored value and prompt the user for the new score to be
stored in its place. If the data provided by the user at some point is not found
in the current database, the program should print a nasty message and terminate
execution of the command without changing anything.</dd>

<dt>SAVE</dt>
<dd>This command should cause the program to output the contents of the current
database to a disk file. If more than one "SAVE" command is issued during one
session, the output of the last one will be the only one kept. It is from a file
created by a "SAVE" command that the command "EDIT" will get its input (more
details below).</dd>

<dt>TYPE</dt>
<dd>This command should cause the program to print on the terminal all the
information currently stored in the database in readable form: a header with the
generic information like the number of students, the number of assignments and
the assignment names, followed by one line for each student containing the
student name and his or her grades.</dd>

<dt>LIST</dt>
<dd>The effect of this command is the same as that of "TYPE" except that the
information should be sent to a disk file to be printed and posted (more details
later).</dd>

<dt>HELP</dt>
<dd>This command without any argument should produce a list of the available
commands followed by a message saying "to get information about any of the
commands, type a line containing 'HELP &lt;comm&gt;' with &lt;comm&gt; replaced
by the desired command name". If a word follows 'HELP', and if the word is a
command, a _two_ line explanation of the command and how to use it should be
given. if the word following 'HELP' is not a command do the same as if no
argument had been given. To make matters easy for the user, whenever the program
is entered a message saying "type 'HELP' help for instructions" should be
printed.</dd>

<dt>QUIT</dt>
<dd>Guess what? The user is tired of playing with the machine and wants to quit.
Before terminating execution the program should ask the user whether she wants
to do "SAVE" and if the answer is affirmative the program should do so.</dd>
<dl>

## The Details

The previous section describes the program operation from the user point of
view. This section is intended to give enough details so that you do not
complicate or trivialize the problem unless you want to.

Write your program to handle a maximum of one hundred (100) students and at most
ten (10) assignments per student. During a session, you should store the entire
current version of the database in the addressable memory of your program, so
that parts of it can be changed without continually copying information from one
file to another.

The student names will be single words (i.e., no blanks) of at most thirty (30)
characters. Assignment names will be single words of at most six (6) characters.
These names cannot span more than a single input line. The names read in are
padded with blanks on the right to make them the correct length. Assignment
scores will be integers.

The program should manipulate exactly four (4) files called "input", "output",
"recdata" and "chardata". The files "input" and "output" should be directed to
the terminal to communicate with the user. The file "chardata" is the text file
whither the "LIST" command output is put. The file "recdata" is a file _of any
type other than_ TEXT whence the command "EDIT" reads its data and whither the
command "SAVE" writes the database content.

You may use any technique for detecting duplicate names. We suggest you use the
simplest possible technique, even if it is not the most efficient. You may also
use the first character to recognize commands, but you should accommodate upper-
or lower-case characters. (In a "NEW" command you should look for the entire
word "end" or "END".)

## The Program Should Be Friendly and Robust

Make your program _friendly_ and _robust_. Have it write frequent (short)
messages telling the user what is happening and requesting input when it is
waiting for it. That is what we mean by friendly. By robust we mean that it
should not fail because of small errors on the part of the user. Although making
a program "idiot proof" is practically impossible, it is worth trying. To be
more specific, here is a list of the errors your program should handle:

1.  Blanks precede a command. Solution: Skip over blanks until the first word is
    found.
2.  Illegal command found. Solution: Write a warning message, ignore command,
    and skip to the next line.
3.  Characters follow a valid command on a line. Solution: Skip and ignore all
    characters which follow a command on a line.
4.  A session does not start with a NEW or EDIT command. Solution: Write a
    warning message, and ignore commands (except for the HELP command) until
    NEW or EDIT is found.
5.  Student (or assignment) name entered is longer than the limit. Solution:
    Ignore the extra characters.
6.  In a CHANGE command, the given student name or assignment name does not
    exist. Solution: Write a message and terminate execution of command.
7.  In NEW, UPDATE and CHANGE commands, a duplicate student or assignment name
    is detected. Solution: Write a message, and prompt the user for another
    name.
8.  The word following a HELP command is not a command. Solution: Do the same as
    if no argument had been given.
9.  More than 100 students or 10 assignments are entered. Solution: Write a
    message and disable additions to the database.

You do _not_ have to check for any other types of errors.

## What to turn in.

Leave your program in a file called lab8.p. In addition to turning in a listing
of the program, turn in a sample session that illustrates all of the features of
your program.

To get a copy of a session, use the UNIX "script" facility. Remember to insert a
"flush(output)" command before reading from the terminal. (This forces any
output to appear on the screen.) To start recording, type "script junk". (Ignore
the warning message which appears.) Then run your program. When you are done,
type "control-d". A copy of the session will be in file "junk", which you can
then print.

The test run you turn in (produced with the commands just described) should show
the following (in the given order):

1.  Basic system operation. Enter the grading system, create a new database with
    3 student names. Use the UPDATE command to enter 2 assignments. TYPE the
    database. Use the CHANGE command to change a student name, an assignment
    name, and one grade. TYPE the database again. LIST the database. SAVE the
    database. QUIT. In UNIX, type out the chardata file (using the "x" command).
    Next, reenter your grading program. Issue the EDIT command, and then issue a
    TYPE command to verify that the data was recovered properly. Finally, using
    the HELP command, show the available help messages. QUIT. (In this section,
    do not illustrate any error handling, of course, unless you unintentionally
    make some mistakes.)
2.  Error handling. Again enter your system. With examples of your choice,
    illustrate the errors your program can handle (i.e., errors 1 through 8
    given above). Do _not_ illustrate error 9 since this would be time
    consuming. Please illustrate the errors in the order we have discussed them
    here.
3.  Optional. Illustrate any other features your system may have.

## For the Hot Shot

Add commands to sort the data by student name or by total number of points in
the assignments. Add a maximum score and a weight for each assignment and
commands to compute normalized weighted scores and sort the database by scores.
Print a score distribution histogram. Add an "alias" feature, wherein students
can choose (presumably secret) aliases. Relax. Go to a movie. Enjoy spring.

## Hints

The most convenient way we know of storing the database in a file which is not
of type TEXT, is to store it in a file whose records are of the type shown
below. The first record of the file should contain the generic information and
the remaining records of the file (one per student) should contain the specific
information.

```
shortword = packed array [1..6] of char;
word = packed array [1..30] of char;
kind = (generic, specific);
item = record
    case flag : kind of
      generic :
        ( nostuds : 0..100;
          noasgn : 0..10;
          asgnnm : array [1..10] of shortword );
      specific :
        ( name : word;
          scores: array [1..10] of integer)
    end;
```

We urge you to write the program in several well-planned sessions. Build it
piece by piece, top-down, and maintain a working (incomplete) version of it at
all times. You will get much more credit for a working program that is
functional, readable, but incomplete (in the sense that some features are
missing), than for a (complete) mess.
 