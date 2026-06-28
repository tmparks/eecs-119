# Assignment 10
## The Traveling Salesman Problem

For the last assignment we are going to work on a problem that is essentially
unsolved: the notorious traveling-salesman problem. By "essentially unsolved" we
mean there is no algorithm that is guaranteed to work on reasonably large
examples in a reasonable amount of time.

Simply stated, the problem is the following: We are given the location of n
cities, and we want to start at city 1, visit every other city exactly once (no
repeat visits), and return home. (Such a pregrination is called a _tour_.) In
what order should we visit the cities so that the total distance traveled is as
small as possible?

## Part 1: The distance matrix (4 points)

The city locations are given in terms of Longitude West and Latitude North in
the file /cc1/e119/data/coordinates (data at the fingertips of every competent
astrologer[1]). For example, the first two lines look like this:

```
                   Longitude (W) Latitude (N)
                    deg  min      deg  min
West New York, N.J.  74   01       40   47
Binghamton, N.Y.     75   55       42   06
```

A complete listing is given for reference at the end of this assignment. To
compute the great-circle distance in miles between two cities on the earth's
surface (flying as the crow flies) we're going to need a little trigonometry.
(Sailors, aviators, and crows, of course, deal with this problem every day [2].)
Consider the figure below, showing cities 1 and 2 on an idealized spherical
earth.

![lab10a](lab10a.png)

The spherical law of cosines [3] tells us that

    cos(a) = cos(b) cos(c) + sin(b) sin(c) cos(A)

where

    b = 90° - latitude of city 1
    c = 90° - latitude of city 2

and

    A = difference in longitude between city 1 and 2

If we then find the angle `a` in radians, the distance between city 1 and 2 is
`a*R` miles, where `R=3959` miles is the mean radius of the earth.

Compute the distance matrix

    var dist: array[1..n, 1..n] of integer;

by entering into `dist[i,j]` the distance between city `i` and city `j` in
miles, _rounded off to the nearest integer_, for every `i` and `j`. (Hint:
`dist[i,j] = dist[j,i]` and `dist[i,i] = 0`, so less than half of the entries
need to be computed.) As a simple check, the great-circle distance between West
New York, N.J. and Bingamton, N.Y. is 134 miles, between West New York, N.J. and
Charcoal Point Village, Alaska, 2755 miles.

So that we all agree on the next part, the official distance matrix is in the
file /cc1/e119/data/dist_mat, and your results should agree precisely.

## Part 2: 2-Opt, A Heuristic Algorithm (6 points)

As we warned you, there is no way known that can _guarantee_ the correct
solution of this size problem and execute on our machine in a reasonable amount
of time. Furthermore, there are some good reasons for believing that no such
algorithm exists at all. If you want to lear more about that, you should study
the theory of NP-complete problems [4]. We can, however, try to find _reasonably
good_ solutions to our particular problem, and we are going to use a very
effective heuristic method [5,6].

The idea is the following. Start with any tour at all. (We will use a completely
random tour; more about that later.) Try to find an improved tour by breaking
two links, and reconnecting the pieces with two other lines, as shown below:

![lab10b](lab10b.png)

If such an improvement can be found, adopt the change, and start looking for
improvements all over again, from the beginning. When, eventually, you have
looked at all possible pairs of links to break, and haven't found an
improvement, save the final tour and its cost, and stop. Such a tour is called
"locally optimal with respect to 2-changes", or simply "2-opt".

For reasonably hard problems, different random starts will produce a variety of
locally optimal solutions. The usual strategy is to produce a few and pick the
best one.

## Details, Comments, Suggestions

Use the following random number generator to produce (pseudo-) random real
numbers between 0.0 and 1.0 (greater than 0.0 and less than 1.0):

```
var seed: real:
{global real variable, to be initialized by user}

function ran: real;
(random number generator}
var i: integer;
begin
    i:= 1061 *trunc(seed*1048576.0) + 221589;
    i:= i mod 1048576;
    seed:= i/1048576.0;
    ran: = seed;
end;
```

The seed must be initialized to a value between 0.0 and 1.0. Remember your
initial seed so you can reproduce a result if you want to.

A random integer between `1` and the integer `k` is then `1 + trunc(ran * k)`.
It is your job to produce a random tour.

Programs such as these can use large amounts of computer time. We suggest
therefore that you debug your program on the traveling salesman problem defined
by the first 10 cities. Also, we suggest that you compile a working version of
your program for "production" using `pc` -- that will run a lot faster than
`pix`.

## For the Hot Shot

The method can be generalized in a natural way to the algorithm where you try
removing all combinations of k links at a time. Locally optimal tours are then
called k-opt. An important contribution of Lin [6] was to find that 3-opt tours
are much better than 2-opt tours for the size problem considered here. (On the
other hand, 4-opt tours are not that much better than 3-opt tours.) Implement a
program that finds 3-opt tours.

Investigate the question of whether "good" starting points will produce better
local optima than random starting points. Try to reduce the effective size of
the problem by "freezing" links that occur in many local optima (called
"reduction" in [6]). Write a program that plots tours. Invent your own
heuristic. Relax. Slow down. Take it easy. Enjoy spring.

**Request:** Indefinite amounts of computer time can be spent on these problems.
If you have finished the graded part (which requires only a moderate amount of
cpu time), please be considerate of those who haven't. Don't run 3-opt when the
load factor is significant. Better yet, if you can, use another computer.

## What to Hand in

Leave your program in lab10.p, then run it with 3 different starting seeds for
both the 10-city sub-problem and the complete problem. Submit a listing of your
program, and your best tour and cost for each problem.

## References

1.  E. Derney, _Longitudes and Latitudes in the United States_, American
    Federation of Astrologers, Washington, D.C., 1945.
2.  C.H. Cotter, _The Astronomical and Mathematical Foundations of Geography_,
    American Elsevier, N.Y., 1966.
3.  C.D. Hodgman (ed.), _Mathematical Tables from Handbook of Chemistry and
    Physics_, (11th edition), Chemical Rubber, Cleveland, Ohio, 1959.
4.  M.R. Garey and D.S. Johnson, _Computers and Intractability: A Guide to the
    Theory of NP-Completeness_, W.H. Freeman, San Francisco, 1979.
5.  G.A. Croes, "A Method for Solving Traveling-Salesman Problems," _Operations
    Research_, vol. 6, no. 6, pp. 791-812, 1958.
6.  S. Lin, "Computer Solutions of the Traveling Salesman Problem," _Bell System
    Technical Journal_, vol. 44, no. 10, pp. 2245-69, 1965.

## Appendix: The Cities and Their Coordinates

```
Longitude (W)	Latitude (N)	City
Deg	Min	Deg	Min
74	01	40	47	West New York, NJ
75	55	42	06	Binghamton, NY
80	00	40	27	Pittsburgh, PA
75	15	41	34	Honesdale, PA
82	33	35	36	Asheville, NC
74	39	40	21	Princeton, NJ
122	54	47	02	Olympia, WA
81	31	41	05	Akron, OH
122	10	37	26	Palo Alto, CA
78	38	35	47	Raleigh, NC
75	32	39	09	Dover, DE
73	56	42	49	Schenectady, NY
111	56	33	26	Tempe, AZ
131	42	55	22	Charcoal Point Village, AK
86	18	32	21	Montgomery, AL
83	19	36	51	Harlan, KY
77	06	38	53	Arlington, VA
98	29	29	25	San Antonio, TX
104	59	39	45	Denver, CO
121	30	38	35	Sacramento, CA
71	23	41	53	Pawtucket, RI
80	09	26	00	Hollywood, FL
84	23	33	46	Atlanta, GA
76	18	36	51	Norfolk, VA
94	23	40	24	Keokuk, IA
91	22	39	42	Hannibal, MO
83	03	42	20	Detroit, MI
88	26	42	35	Lake Geneva, WI
92	17	30	00	Kaplan, LA
73	52	41	09	Ossining, NY
78	14	39	37	Berkeley Springs, WV
93	58	44	19	Saint Peter, MN
95	23	29	45	Houston, TX
111	37	42	39	Soda Springs, ID
74	45	41	48	Liberty, NY
89	39	39	49	Springfield, IL
155	05	19	44	Hilo, HI
86	23	35	51	Murfreesboro, TN
111	40	40	14	Provo, UT
68	00	46	52	Caribou, ME
106	13	41	54	Medicine Bow, WY
96	55	35	20	Shawnee, OK
67	06	18	23	Moca, PR
110	28	40	11	Lovelock, NV
100	04	45	44	Mound City, SD
98	52	48	07	Devils Lake, ND
91	51	33	56	Star City, AR
80	50	32	41	Yamasee, SC
77	09	39	05	Rockville, MD
120	12	45	00	Fossil, OR
```
