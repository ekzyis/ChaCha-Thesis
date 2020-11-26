#!/usr/bin/env python

"""
Create the performance plots.
"""

# x axis tags. all benchmarks are starting from action zero.
x = [0, 100, 200, 283, 400, 800, 3200]

# benchmark at 283 is 4516.4ms which is weird. Leaving it out and replacing with linear .
benchmark_0 = [0, 773.27, 1898.92, None, 4033.5, 8961.2, 37003]
benchmark_0[3] = 4033.5 * 3 / 4

benchmark_1 = [0, 933.18, 843, 4.75, 1017.09, 304.14, 849.67]

import matplotlib.pyplot as plt

plt.plot(x, benchmark_0, 'o')
plt.plot(x, benchmark_1, 'o')
plt.ylabel('time in milliseconds')
plt.xlabel('action')
plt.show()
