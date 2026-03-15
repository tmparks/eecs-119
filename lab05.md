# Programming Assignment 5

## A simple graphics language

The purpose of this lab is to give you an idea of how to control some devices
that produce graphical output. You will write a program to interpret a very
simple lanugage to make the line printer behave like a (lousy) plotter.

The lanugage that you will interpret will describe how to draw straight lines of
different lengths at different angles in different places on a page (56 lines of
130 characters each) of printer output. The drawing will be performed by
assigning characters to a page image array; the characters will be placed in the
array by an imaginary "pen" which can move around the page controlled by the
commands of the language. For example, the program given below left would draw
the triangle shown below right with its lower left vertex in the 40th column of
the 10th (from bottom) line:

    MOVE  10 40               *
    VCHANGE   0              * *
    HCHANGE   2             *   *
    STEP     10            *     *
    VCHANGE   1           *       *
    HCHANGE  -1          *         *
    STEP     10         *           *
    VCHANGE  -1        *             *
    STEP     10       *               *
    PRINT            *                 *
    ERASE           * * * * * * * * * * *

What follows is a quick description of the commands of the language. Refer to
the above example for details.

<dl>
<dt>MOVE n m</dt>
<dd>causes the imaginary pen to be positioned at the row n and the column m of
the page image. No asterisk is written. (When the page image is printed, row 1
should be at the bottom and row 56 the top, column 1 at the left end of a line
and column 130 at the right.)</dd>
<dt>STEP n</dt>
<dd>will cause the imaginary pen to move n times and an asterisk to be assigned
_after_ each move to the page image character that corresponds to the location
of the pen. The position of the pen after each move is determined by its
previous position and the values of the variables VCHANGE and HCHANGE in the
obvious way: the new row is obtained by adding VCHANGE to the old row and the
new column by adding HCHANGE to the old column.</dd>
<dt>VCHANGE n</dt>
<dd>causes the value of VCHANGE to become n, so the next STEP command will place
asterisks in the page image n lines apart.</dd>
<dt>HCHANGE n</dt>
<dd>causes the value of HCHANGE to become n, so the next STEP command will place
asterisks in the page image n columns apart.</dd>
<dt>PRINT</dt>
<dd>causes the current contents of the page image to be printed on the line
printer as described before: line 1 at the bottom of the printed page and column
1 at the left of each line. (The printer writes 56 lines on each page, so you do
not need to do anything special to pass on to the next page of paper.)</dd>
<dt>ERASE</dt>
<dd>causes the page image to be filled with blanks so a fresh drawing can be
produced.</dd>
</dl>

Your program should read a program written in this language from the input file
and execute it according to the descriptions given above, putting its output on
the output file. The output file can then be printed using the UNIX print
command.

Do not assume that each command is in a separate line. Clear the page image
initially so that programs in the graphics language do not have to start with an
ERASE command. Keep the coordinates of the pen in variables of type real and
assume that the values of VCHANGE and HCHANGE are real also. To place the
asterisks in the page image use the rounded values of the pen position. This is
needed in order to be able to produce lines like this:

    **********
              **********
                        **********

which in spite of its appearance is a straight line (or as close as the line
printer will ever get to one of approximately that slope).

## Turning in your assignment

Leave your program in a file called lab5.p. Run your program on the input file
/cc1/e119/data/lab5. Turn in the printed output as well as a listing. (There is
a shorter test file /cc1/e119/data/lab5.short that may be useful for debugging.)

## Comments

Notice that no two commands in our graphics language begin with the same
character. You may take advantage of this fact to recognize the commands.
(Assume that if new commands are added later, it will always be the case that
the first character determines the command uniquely.) However, your program
should accommodate both upper- and lower-case letters.

The imaginary "pen" may move off the page. Your program should handle this
gracefully, keeping track of where the pen is at all times, even if it is
off-page, and "drawing" only on-page points. As an extra feature, you may want
to tell the user how many off-page points there were, after each PRINT command.
