
## Intervals
### Initialization
```
from intervals import Intervals

i = Intervals.from_pairs(((1, 3), (4, 7), (8, 9))) # the union (1, 3] U (4, 7] U (8, 9]
j = Intervals.from_pairs(((0, 2), (3, 6), (7, 10))) # the union (0, 2] U (3, 6] U (7, 10]
```
```
>>> i
Intervals((1.0, 3.0), (4.0, 7.0), (8.0, 9.0))
```
```
>>> j
Intervals((0.0, 2.0), (3.0, 6.0), (7.0, 10.0))
```
### Operations
complementation
```
>>> ~i
Intervals((-inf, 1.0), (3.0, 4.0), (7.0, 8.0), (9.0, inf))
```
intersection
```
>>> i & j
Intervals((1.0, 2.0), (4.0, 6.0), (8.0, 9.0))
```
union
```
>>> i | j
Intervals((0.0, 10.0))
```
difference
```
>>> i - j
Intervals((2.0, 3.0), (6.0, 7.0))
```
symmetric difference
```
>>> i ^ j
Intervals((0.0, 1.0), (2.0, 4.0), (6.0, 8.0), (9.0, 10.0))
```
inclusion
```
>>> i & j <= i
True
```
membership
```
>>> i(2)
True
```
measure
```
>>> i.leb()
6.0
```
## Simple Functions
```
from intervals import Intervals, SimpleFunction

x = SimpleFunction.indicator(Intervals.from_pairs(((1, 3), (4, 7), (8, 9))))
y = SimpleFunction.approx(lambda x: x**2 / 16, start=0, stop=10, num_steps=5)
```
```
>>> x
SimpleFunction(1.0*(1.0, 3.0) + 1.0*(4.0, 7.0) + 1.0*(8.0, 9.0))
```
```
>>> y
SimpleFunction(0.25*(2.0, 4.0) + 1.0*(4.0, 6.0) + 2.25*(6.0, 8.0) + 4.0*(8.0, 10.0))
```
### Operations
...

