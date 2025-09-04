# Programming Assignment 3
## Part One: A simulation of a predator prey system

Once upon a time there was a nice little island where no mammals lived. Then a
family of settlers moved to the island with their sheep, cows, goats and
rabbits, and the trouble started. Somehow, a few (ten) of the settlers' rabbits
escaped from their pen and formed a wild colony, which (lacking any natural
enemies on the island) grew very quickly.

The growth of the rabbit colony can be estimated as follows. The rabbits had a
birth rate of approximately 0.2 per month; that is, if `r` rabbits were alive on
a given month, `0.2 * r` rabbits would be born that month. Being the only wild
mammal on the island, all the rabbit deaths were due to starvation. The island
could produce only a certain amount of vegetation so the starvation rate of
rabbits had to increase as the number of rabbits increased. Given the dimensions
of the island this rate could be approximated by `0.00002 * r`, which means that
in a month in which `r` rabbits were alive, `0.00002 * r * r` rabbits would die
of starvation. With these birth and death rates, the rabbit population would
have become stable at ten thousand, since:

    0.2 * r = 0.00002 * r * r    (births = deaths)

exactly when `r = 10000`.

However, well before reaching these levels, the rabbits became a real problem
for the settlers, since they were turning the once-green island into a patch of
dirt where the sheep and cows could no longer graze. Forced into action and
after much thought, they decided to solve the problem the natural way: by
introducing a predator to the island. And that is how one good day, fifty months
after the first rabbits escaped, ten coyotes were released on the island.

Coyotes had a birth rate of 0.08 per month. They ate rabbits, and the more
rabbits there were, the more they ate (they were easier to catch). If ten
thousand rabbits lived on the island, each coyote would eat about forty five
rabbits per month, and each coyote would eat proportionately less as the number
of rabbits decreased. A good estimate is that each coyote would eat
`r * 45/10000` rabbits during a month in which there were `r` rabbits alive.

Coyotes died of starvation: they would get too old to compete effectively with
younger coyotes for the rabbits that were available. The starvation rate of
coyotes would clearly depend on the number of rabbits alive: the more rabbits
the smaller the rate. A good approximation to the real rate is given by the
expression `250/r`, that is, during a month in which `c` coyotes and `r` rabbits
are alive, approximately `c * 250/r` coyotes would starve to death.

Your assignment is to write a program that simulates the situation just
described and predicts the evolution of the two populations. The results
generated could then be used to predict whether the rabbit population would be
reduced to tolerable levels by the coyotes, and how long the settlers would have
to wait for those levels to be reached.

The program should assume that all the births and deaths occur at the end of the
month, using the populations of one month and the given estimates of the birth
and starvation rates to compute the expected populations the following month.
Use variables of type real to store the numbers of coyotes and rabbits alive on
a given month: 0.03 rabbits may not have any meaning, but we are dealing with
approximations and if integer variables are used to keep these values, errors
accumulate very quickly and the results obtained are meaningless.

The program should display the results graphically by printing a line of the
form:

    m |        r        c

after each three month period of the simulated time interval. In such a line `m`
stands for the month number, the number of blanks between the '|' and the 'r' is
the closest integer to one one-hundredth of the number of rabbits alive at the
end of the period, and the number of blanks between the '|' and the 'c' is the
closest integer to the number of coyotes alive at the end of the three month
interval multiplied by two. (To obtain the closest integer to a real number see
the function `round` in the textbook.) At the end of the simulation, print out
the number of rabbits and coyotes left on the island.

Summary of the parameters of the simulation:

|         | Births     | Starvation Deaths | Other Deaths       |
| ------- | ---------- | ----------------- | ------------------ |
| Coyotes | `0.08 * c` | `c * (250/r)`     |                    |
| Rabbits | `0.2 * r`  | `0.00002 * r * r` | `c * r * 45/10000` |

The simulation should start at the month in which the ten (10) rabbits escape
(month 0) and proceed month by month until three hundred months have elapsed or
until the populations change less than 1% in a month, whichever comes first.
(To test this last condition for rabbits, say, for a month in which `r` rabbits
are alive and the change in rabbits is `rchange`, simply test whether
`abs(rchange)/r` is less than 0.01). The number of coyotes is zero until the 
beginning of the fiftieth month when ten coyotes are introduced.

I recommend that you use three functions with the following signatures:

    newrabbits(oldrabbits: float, oldcoyotes: float) -> float
    newcoyotes(oldrabbits: float, oldcoyotes: float) -> float
    printline(month: int, rabbits: float, coyotes: float) -> None

The first function will compute the number of rabbits alive during a month when
given the number of rabbits and coyotes alive during the previous month. The
second will do the same for the number of coyotes. The third will print a line
like the one described earlier when given the month number and the number of
rabbits and coyotes alive that month.
