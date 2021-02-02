```python
from intervals import Intervals

i = Intervals.from_pairs(((1, 3), (4, 7), (8, 9))) # the union (1, 3] U (4, 7] U (8, 9]
j = Intervals.from_pairs(((0, 2), (3, 6), (7, 10))) # the union (0, 2] U (3, 6] U (7, 10]

i.compl() # complementation
i & j # intersection
i | j # union
i <= j # inclusion
i < j # strict inclusion
```
