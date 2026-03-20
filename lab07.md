# Assignment 7

## Another exercise in recursion

A common application of computers is picture processing: the analysis of visual
scenes. This assignment uses a simple picture processing task as an excuse to
get you to write a recursive function.

To perform scene analysis, we must put pictures into a form recognizable by a
computer. This is done normally by _digitizing_ the picture, that is, by
dividing the whole scene into a large number of small areas of the same size and
shape (normally square), called _pixels_, and giving the light intensity falling
on each of the pixels. Thus a picture is represented by a large number of
integers representing light intensities at different point in the original
scene.

For our exercise we will use this idea, but the light intensities in the
digitized picture will have only two possible values: light or dark. The images
to be analyzed by our program will be represented as shown below:

```
15
30
-------------------***---***--
----********------***-----**--
---***----**--**---***----***-
--***--**-***--**---********--
--**--***-***--***----****----
--**---*--***-----------------
--****---***----------***-----
----******-------------***----
---------------------**-------
--*--**----***---***--***-----
-**-*****--****--*-**-****----
-********--***------****------
-***----****------------------
--***--**---------------------
---*****----------------------
```

The first number given represents the number of lines into which the picture has
been divided (i.e., the number of pixels in the vertical direction). The second
number represents the number of pixels in each line. The picture is then
represented by the specified number of lines, each line containing the specified
number of characters, and each character being either a `-` (representing light)
or a `*` (representing shadow).

If you think of the scene represented above as a picture taken through a
microscope, you can imagine that it may be useful to have an automatic way of
counting how many distinct dark regions appear in the picture, how many of them
are of a certain size, how many have a certain shape, etc.

## Part One (6 pts)

Write a program that reads a picture represented in the manner described above,
prints the picture and tells how many distinct dark regions appear in it. For
the purposes of counting connected regions consider each pixel adjacent _only_
to the four pixels immediately above, below, to its left and to its right. That
is, a pixel is _not adjacent_ to the four pixels that touch it diagonally. Using
this criterion the sample picture given above contains seven distinct areas,
whereas considering the set of adjacent pixels to include the diagonal neighbors
as well, would have given a count of six.

You may assume for all parts of this problem that each line of the input file
contains a line of the picture to be processed and that the picture elements
will be the first characters of each of those input lines. You can assume also
that the picture has been divided in no more than 100 lines each containing no
more than 100 pixels.

## Part Two (3 pts)

Expand your program to shat it also prints the number of distinct dark regions
that touch the edge of the picture. For example, in the sample picture given
only two regions touch the edge even though one of them touches it in two
different places.

## Part Three (1 pt)

Have your program also print a series of pictures of the same size and shape as
the input, each picture containing exclusively dark areas of roughly the same
size. To be more precise, print a picture displaying only the dark areas that
cover between one and twenty pixels, another picture showing only the dark areas
that cover between twenty one and forty pixels, another with the areas that
cover between forty one and eighty pixels and another with the areas that cover
more than eighty pixels.

## Part Four (for the hot shots, no credit)

Print a picture that shows only those dark regions that are totally surrounded
by another dark region.

## Hints

Represent your pictures internally as a two-dimensional array of integer. This
representation is much more flexible than using an array of characters or a
boolean array.

Write the program for Part 1 before attempting Part 2, and complete the program
for Part 2 before starting on Part 3.

## Turning in your assignment

Leave your program (which performs all parts) in file lab7.p. Run this program
on input file /cc1/e119/data/lab7. Turn in a copy of the output and a listing.
