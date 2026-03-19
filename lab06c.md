# Programming Assignment 6
## Problem 3

What does the following recursive PASCAL program do?

```
program strange (input, output);
var
    arg: integer;

    function f(x: integer): integer;

        function g(x: integer): integer;
        begin
            if x > 100 then g := x - 10
            else g := f(g(x + 11));
        end;

    begin
        if x > 100 then f := x - 10
        else f := g(f(x + 11));
    end;

begin
    writeln('on what input would you like me to run the function ');
    read(arg);
    writeln('f(', arg, ') = ', f(arg))
end.
```

That is, can you characterize the function which it computes?

Hint 1: It is not the constant function

Hint 2: It's a hard recursion to simulate by hand.
