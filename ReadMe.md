## Intervals
### Initialization
```
from intervals import Intervals

i = Intervals.from_pairs(((1, 3), (4, 7), (8, 9)))
j = Intervals.from_pairs(((0, 2), (3, 6), (7, 10)))
```
#### the union [1, 3) ∪ [4, 7) ∪ [8, 9)
```
>>> i
Intervals((1.0, 3.0), (4.0, 7.0), (8.0, 9.0))
```
#### the union [0, 2) ∪ [3, 6) ∪ [7, 10)
```
>>> j
Intervals((0.0, 2.0), (3.0, 6.0), (7.0, 10.0))
```
### Operations
#### complementation
```
>>> ~i
Intervals((-inf, 1.0), (3.0, 4.0), (7.0, 8.0), ...)
```
#### intersection
```
>>> i & j
Intervals((1.0, 2.0), (4.0, 6.0), (8.0, 9.0))
```
#### list of operations
```
~i     # complementation
i & j  # intersection
i | j  # union
i - j  # difference
i ^ j  # symmetric difference

i == j # equality
i <= j # inclusion
i >= j # exclusion
i < j  # strict inclusion
i > j  # strict exclusion
```
### Other Methods
#### membership
```
>>> i(2)
True
```
#### measure
```
>>> i.leb()
6.0
```
## Simple Functions
### Initialization
```
from intervals import Intervals, SimpleFunction

i = Intervals.from_pairs(((1, 3), (4, 7), (8, 9)))
x = SimpleFunction.from_intervals(i)
y = SimpleFunction.from_function(fun=lambda x: 0.1*(x-5)**2, start=0, stop=10, num_steps=20)
```
#### indicator of the union [1, 3) ∪ [4, 7) ∪ [8, 9)
```
>>> x
SimpleFunction(1.0*(1.0, 3.0) + 1.0*(4.0, 7.0) + 1.0*(8.0, 9.0))
```

![](01.png)
#### approximation of the function x ↦ 0.1(x − 5)^2
```
>>> y
SimpleFunction(2.5*(0.0, 0.5) + 2.025*(0.5, 1.0) + 1.6*(1.0, 1.5) + ...)
```
![](02.png)
### Operations
#### multiplication
```
>>> x * y
SimpleFunction(1.6*(1.0, 1.5) + 1.225*(1.5, 2.0) + 0.9*(2.0, 2.5) + ...)
```
![](03.png)
#### addition
```
>>> x + y
SimpleFunction(2.5*(0.0, 0.5) + 2.025*(0.5, 1.0) + 2.6*(1.0, 1.5) + ...)
```
![](04.png)
#### pointwise minimum
```
>>> x & y
SimpleFunction(1.0*(1.0, 2.0) + 0.9*(2.0, 2.5) + 0.625*(2.5, 3.0) + ...)
```
![](05.png)
#### list of operations
```
-x     # negation
x * y  # multiplication
x + y  # addition
x - y  # subtraction

i & j  # pointwise minimum
i | j  # pointwise maximum

i == j # equality
i <= j # pointwise order
i >= j
i < j
i > j
```
### Other Methods
#### evaluation
```
>>> x(2)
1.0
```
#### integration
```
>>> x.leb()
6.0
```
## Composite Functions
...
