# Programming Assignment 6
## Problem 1

A professor in a certain EECS course at a college in New Jersey wished to teach
his class how to use recursion for sorting a file. After explaining the logic
behind the Quicksort algorithm, he explained its implementation with the
following PASCAL program (which is also availaable as /cc1/e119/ps6/quicksort.p).
A smart student pointed out that while the program worked on some examples, it
did not work on others. Find the bugs and fix it.

```
program quicksort(input, output);
const
    size = 15; { maximum problem size }
type
    item = integer;
    arrayindex = 1..size;
    indexvar = 0..size;
var
    k: arrayindex;
    n: array [arrayindex] of item;
    arraysize: arrayindex;

    procedure swap(var left, right: indexvar);
    { swap two elements and move the left and right indices }
    var
        temp: item;
    begin
        temp := n[left];
        n[left] := n[right];
        n[right] := temp;
        left := left + 1;
        right := right - 1;
    end; { swap }

    procedure quicksort(i, j: indexvar);
    var
        left, right: indexvar;
        pick: item;
    begin
        left := i + 1;
        right := j;
        pick := n[i];
        repeat
            while n[left] < pick do
                { go left until an element is out of place }
                left := left + 1;
            while n[right] > pick do
                { go right until an element is out of place }
                right := right - 1;
            if left <= right then
                { interchange elements }
                swap(left, right)
        until left > right;
        if right > i then { recurse on smaller problems }
            quicksort(i, right);
        if left < j then
            quicksort(left, j)
    end; { quicksort }

begin
    write('I can sort arrays of size up to ');
    writeln(size);
    writeln('how large an array would you like me to sort? ');
    read(arraysize);
    writeln('now enter the elements of your array, all on one line ');
    for k := 1 to arraysize do
        read(n[k]);
    quicksort(1, arraysize);
    writeln('sorted numbers are ');
    for k := 1 to arraysize do
        write(n[k])
end.
```