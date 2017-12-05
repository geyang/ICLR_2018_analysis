import matplotlib.pyplot as plt
import matplotlib.dates as mdate

import numpy as np

# Generate some random data.
N = 40
now = 17478639984.2 / 1000
raw = np.array([now + i * 1000 for i in range(N)])
vals = np.sin(np.linspace(0, 10, N))

# Convert to the correct format for matplotlib.
# mdate.epoch2num converts epoch timestamps to the right format for matplotlib
print(raw[0])
secs = mdate.epoch2num(raw)

fig, ax = plt.subplots()

# Plot the date using plot_date rather than plot
ax.plot_date(secs, vals)

# Choose your xtick format string
date_fmt = '%y-%m-%d %H:%M:%S'

# Use a DateFormatter to set the data to the correct format.
date_formatter = mdate.DateFormatter(date_fmt)
ax.xaxis.set_major_formatter(date_formatter)

# Sets the tick labels diagonal so they fit easier.
fig.autofmt_xdate()

plt.show()
