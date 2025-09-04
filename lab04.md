<style>body{text-align:justify}</style>
# Programming Assignment 4
## Text formatter

If you look at the handouts for this course carefully, you may notice certain
characteristics that suggest that they are produced with the aid of a machine.
For example, blanks are added between words so all the lines of a paragraph
(except the last one) have exactly the same length, something which is very hard
to do for a human typist.

A program that takes as input a string of text sprinkled with commands about how
to process the text and produces a document as output is called a text formatter.
In this lab you will write the core of a text formatter similar to the one used
to produce the course handouts.

### The basic formatter

Write a program that reads text from an input file and produces output which is
a copy of the input where:

1.  each line starts in the leftmost column of the output page
2.  two words in the same line are separated by exactly one blank
3.  no word is split across lines (hyphenation is too hard a probiem to tackle
    in one week)
4.  each output line contains as many words as possible without exceeding 40
    characters
5.  input lines that start with the character '.' are not printed: these lines
    will contain a formatter command (see below)

You may assume (for this part and all others) that no word will have more than
30 characters (by "word" I mean any sequence of non blank characters). For
example, if • represents a blank and the input file contains:

    This•line•contains•more•than•40•characters
    but•this••••other•••line••••••will•••••••just••fit
    .XX••garbage
    in•the•second•line.••.YY•Here
    is
    additional•••text.

then the output file should contain:

    This•line•contains•more•than•40
    characters•but•this•other•line•will•just
    fit•in•the•second•line.•.YY•Here•is
    additional•text.

### Some simple formatting commands

Interspersed with the input text, there will be instructions for the text
formatter: any input line that starts with the character '.' should be assumed
to contain one formatter command (no text). Formatter commands should never be
printed. They are only used to control the manner in which the rest of the text
is printed.

To complete this section, you have to modify the basic formatter to execute the
following commands.

<dl>
<dt>.PP</dt>
<dd>A new paragraph should be started with the first word following the command.
The paragraph should be separated from the previous one by a blank line and the
first line of the new paragraph should be indented five spaces with respect to
the other lines of the paragraph.</dd>
<dt>.LP</dt>
<dd>Same as ".PP" but the first line of the paragraph is not indented.</dd>
<dt>.W NN</dt>
<dd>Starting with the first line of the next paragraph, each line should contain
as many words as possible without exceeding "NN" characters (where "NN" will be
an integer between 30 and 99).</dd>
</dl>

Your program should assume that the input file starts with a ".W" command and a
paragraph command (".LP"' or ".PP").

For example, if the input is:

    W•33
    .PP
    Here•is•a•sample•••paragraph•which•starts•the•fle.
    This•paragraph•doesn't•••••make•much•sense.
    .LP
    Here•is
    ••••a••paragraph•which
    is•not•indented.

then the output should be:

    •••••Here•is•a•sample•paragraph
    which•starts•the•file.•This
    paragraph•doesn't•make•much
    sense.

    Here•is•a•paragraph•which•is•not
    indented.

### Some additional commands

<dl>
<dt>.SP N</dt>
<dd>Starting with the next paragraph, "N" blank lines should be printed in
between any two lines of output. That is, ".SP 1" will cause the paragraphs that
follow the command to be printed doubly spaced. The separation between two
consecutive paragraphs should always be one more than the spacing between lines
of the first paragraph of the pair. You may assume that "N" will be an integer
between 0 and 9, with 0 meaning single spaced output is desired. Single spacing
should be assumed at the beginning unless otherwise specified before the first
paragraph command in the file (remember: there will be a paragraph command
before the first word of text).</dd>
<dt>.I NN</dt>
<dd>Beginning with the next paragraph, each line should start with "NN" blanks.
These blanks should be counted as characters printed in the line, that is, if
the formatter is printing lines with at most 80 characters and we instruct it to
indent them 10 spaces, only 70 characters can be put in the remainder of the
line. The automatic indentation produced by the "PP" command should be added to
the indentation produced by this command. An indentation of 0 should be assumed
for the first paragraph unless the first line of the input specifies other
indentation.</dd>
<dt>.M NN</dt>
<dd>Beginning with the next paragraph the first character of each line of output
should be preceded by "NN" blanks. These blanks should not be counted towards
the line length established by the last ".W" command. The intention is to move
the whole output away from the left end of the line printer paper.</dd>
</dl>

### For those who like a challenge

<dl>
<dt>.JST</dt>
<dd>Starting with the next paragraph your formatter should insert blanks between
words in a line so the last character of each line (except the last line of each
paragraph) is a non blank character. The blanks should be added in an
intelligent way: if you select any two consecutive words of the output line, the
number of blanks between them should not differ by more than one from the number
of blanks between any other two consecutive words in the same line. Adding all
the needed blanks between the last two words in the line is not a satisfactory
solution to this problem.</dd>
<dt>.NJST</dt>
<dd>Cancels the effect of a previous ".JST" command starting with the next
paragraph.</dd>
</dl>

For examples of text produced with the ".JST" command, see this handout.

### For Hot Shots

<dl>
<dt>.IP NN <L></dt>
<dd>A new paragraph should be started with the first word following the command.
The new paragraph should be separated from the previous paragraph by a blank
line. All the lines of the new paragraph should be indented "NN" characters.
The "<L>" which is called the "paragraph label" and is whatever appears
immediately after "NN" enclosed in angled brackets, is to be placed in the first
line of the paragraph with its first character in the first output column. You
may assume that the number of characters inside the brackets is less than "NN".
The angle brackets are intended to delimit the label and should not be printed.
(For example, this paragraph was produced with a ".IP" command.)</dd>
<dt>.NF</dt>
<dd>Immediately after reading this command the formatter should print the input
exactly as it is read, starting in a new line and including blanks, line breaks,
etc. until the command ".FI" is found or the end of the file is reached.</dd>
<dt>.FI</dt>
<dd>Begin a new line and resume formatting the input according to the
instructions that were in effect when the preceding ".NF" command was found.</dd>
</dl>

Formatter commands found after ".NF" and before ".FI" should be ignored. This
applies to ".NF" commands as well: no nesting of ".NF" commands is possible.

### Some Details

Note that a word that starts with '.' may not be a formatter command: formatter
commands always are at the beginning of an input line.

Write a separate program for each part. The solution to one section can be
obtained by adding some code to the solution of the previous part. Do not try to
write the solution to the whole problem at once: you will be courting disaster.

Commands that your program cannot interpret should be ignored (not printed!).
