# Programming Assignment 2
## Part Two

For this part you have to compute the value of the following mathematical
quantity:

                 x
    (1)  I(x) =  ∫ exp(-t^2) dt
                 0

where `x` is between 0 and 1. If you do not understand this expression, don't
panic! You do not really have to understand what it is in order to do this
assignment. The important thing to notice is that `I(x)` cannot be computed
directly ("in closed form" as mathematicians would say). Instead, `I(x)` can be
computed in a numerical fashion, as indicated by the expression:

                ∞
    (2)  I(x) = Σ (-1)^n * x^(2 * n + 1) / (n! * (2 * n + 1))
               n=0

Equation (2) says that `I(x)` can be computed as a sum of terms. The first term
`(n=0)` is `x`; the second term `(n=1)` is

    -x^3 / 3

The third term `(n=2)` is

    x^4 / 10

The fourth term `(n=3)` is

    -x^7 / 42

and so on. It is easy to show that if only terms for `n=0` through `n=j` are
computed and added, the magnitude error in computing `I(x)` will be less than
the value of the `j`th term. In other words, we do not have to compute "all"
terms in equation (2), but can stop when we have a "small enough" term in the
series (and thus a "small enough" error in the computation).

Your job is to write a program that reads in `x`, computes `I(x)` using equation
(2), and writes the result. Your program should do the following:

1.  Check that `x > 0` and that `x <= 1`. (If it's not, your friendly user
    interface should remind the user of the proper use of this program.)
2.  Stop the computation of `I(x)` when term number `n` is between -1E-6 and
    1E-6, or after 15 iterations, whichever comes first. When it stops, the
    program should print a message including the reason for stopping, the
    computed value of `I(x)`, and the error (i.e., the value of the last term
    computed).
3.  For term `n` in the series, you will need `n!` and `x^(2 * n + 1)`. To
    compute these values, be sure to use the values you obtained in the previous
    step. That is, `n!` can be computed as `n * (n-1)!`, and `x^(2 * n + 1)` can
    be computed as `x * x * x^(2 * (n - 1) + 1)`.
